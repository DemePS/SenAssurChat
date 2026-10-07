"""SenAssurChat is the library plus a page and some content: these tests check that the pieces fit. The library has its own tests (WaxalAgent/tests)."""

import re
from pathlib import Path

import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from waxal_agent.mt.fake import FakeTranslator
from waxal_agent.pipeline import Pipeline
from waxal_agent.stt.fake import FakeListener
from waxal_agent.tts.fake import FakeSpeaker
from waxal_server.app import create_app

import senassurchat.cli as app_cli

ROOT = Path(__file__).parent.parent
PAGE = ROOT / "senassurchat" / "static" / "index.html"


class Agent:
    def run(self, user_id, english):
        return "ok"


def make_client():
    pipeline = Pipeline(FakeListener(), FakeTranslator(), FakeSpeaker(), Agent())
    return TestClient(create_app(pipeline, static_dir=app_cli.STATIC, title="SenAssurChat"))


def test_the_server_shows_the_apps_own_page():
    r = make_client().get("/")
    assert r.status_code == 200 and "SenAssurChat" in r.text and r.text == PAGE.read_text(encoding="utf-8")


def test_every_endpoint_the_page_calls_exists_in_the_library_server():
    called = set(re.findall(r"""['"`](/api/[a-z/]+)""", PAGE.read_text(encoding="utf-8")))
    assert called
    client = make_client()
    for path in sorted(called):
        # not 404/405: the route exists (a GET on a POST route answers 405, a bad body 4xx)
        assert client.request("POST" if path != "/api/health" else "GET", path).status_code != 404, path


def test_the_command_starts_the_library_server_with_the_apps_page(monkeypatch):
    seen = {}
    monkeypatch.setattr(app_cli, "serve", lambda **kw: seen.update(kw))
    app_cli.main()
    assert seen == {"prog": "senassurchat", "static_dir": app_cli.STATIC, "title": "SenAssurChat"}


def test_the_app_ships_its_content():
    assert (ROOT / "data").is_dir() and (ROOT / "library").is_dir()


def test_the_skills_are_where_the_library_looks_for_them():
    skills = sorted(p.parent.name for p in (ROOT / "data" / "skills").glob("*/SKILL.md"))
    assert skills == ["explain-my-contract", "recommend-partner-insurance", "register-on-partner-website"]
    assert (ROOT / "data" / "instructions" / "INSTRUCTIONS.md").is_file()
