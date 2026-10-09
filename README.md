# SenAssurChat

An insurance assistant in Wolof (and French) for Senegal. A person sends a voice note in Wolof, and the answer comes back as a Wolof voice
note and as text. It answers from the CIMA insurance code and its interpretations, and sends the person to the partner insurer, Renassur.

SenAssurChat is a thin layer over the **WaxalAgent library** (`../WaxalAgent`: the core `waxal_agent` and the web layer `waxal_server`). All
the code is there: the pipeline (speech recognition, translation, agent, voice), the per-person agent, S3 sync, the test page's server, the
WhatsApp webhook, links and browsing. **The library's README is the reference** for how all of that works and for every setting. This
folder only holds what makes the app its own:

| Path | What it is |
|---|---|
| `senassurchat/` | the `senassurchat` command (the library's server with this app's name) and the app's page, `static/index.html` |
| `data/instructions/INSTRUCTIONS.md` | the agent's general instructions: the two documents, and the link to the partner |
| `data/skills/` | the skills: `explain-my-contract`, `recommend-partner-insurance`, `register-on-partner-website` |
| `library/` | the documents the agent answers from: `CODE-CIMA-2019.pdf`, `Interpretations-CMA.pdf` (git-ignored) |
| `example.env` | the settings, with this app's values (`WAXAL_LINK_DOMAINS=renassur.sn=Renassur`) |
| `docs/` | `INSTRUCTIONS.example.md` and `skills/`: the committed copies of the instructions and skills (`data/` is git-ignored), `SANDBOX.md` |
| `tests/test_app.py` | checks that the page, the command and the content fit the library |

`pyproject.toml` reads the library from the folder next to this one (`[tool.uv.sources]`, editable: a change in `../WaxalAgent` is seen at
once). For a release or Docker, pin a git commit
(`waxal-agent @ git+https://github.com/DemePS/WaxalAgent.git@<commit>`; the Dockerfile already installs the library from git).

## Try it

```bash
uv sync
cp example.env .env                       # every setting, with DEVELOPER_MODE=1; fill in the keys
set -a; source .env; set +a               # the server reads the environment, not the file
uv run senassurchat serve                 # http://127.0.0.1:8000/?token=<WAXAL_TOKEN>
```

Needs `ANTHROPIC_API_KEY` and `ELEVENLABS_API_KEY`, and ffmpeg. `DEVELOPER_MODE=1` keeps S3 and WhatsApp off, so only the test page is served.
Optional extra: `uv sync --extra browser` (the agent browses the allowed sites; then `playwright install chromium`). `WHATSAPP.md` has the commands to test on WhatsApp, `docs/SANDBOX.md` the Docker sandbox.

## What is specific to this app

- **Documents.** The two PDFs in `library/` are long. The library's base prompt makes the agent find the pages with `search_pdf` and open only
  those pages; the instructions tell it to use the interpretations for the articles they cover. The people's own documents (their contract) go in
  `data/users/<number>/documents/`, or in S3 under `users/<number>/documents/`.
- **Links.** `WAXAL_LINK_DOMAINS=renassur.sn=Renassur`: the agent may share a link to Renassur only, shown under the answer and never spoken.
- **Skills.** The three skills are loaded on demand. `register-on-partner-website` is a stub: its steps are to be written by the owner.
- **Page.** `senassurchat/static/index.html` is the library's test page with this app's name; it calls the library's `/api/...` routes, which the
  tests check.

To change the agent's behaviour, edit the instructions or a skill (no code). To change anything else (the pipeline, WhatsApp, S3, browsing),
change `../WaxalAgent`, not this folder.

## Tests

```bash
uv run pytest        # this app's tests; the library's own tests are in ../WaxalAgent
```
