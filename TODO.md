# TODO

## Merge `refactor` into `main`
- Local `main` holds an unpushed merge of `refactor` (`49d2a74`), but it is behind `origin/main` by one commit:
  `263e39b` "Remove the Hugging Face and Gradio voices" (it edits the old copied library that `refactor` deletes).
- Steps: `git fetch`, `git checkout main`, `git merge refactor` (if not already in), then `git merge origin/main`.
- Expected conflicts. Keep the `refactor` side for all of them:
  - `README.md`, `uv.lock`: `git checkout --ours README.md uv.lock`
  - `waxal_agent/engines.py`, `scripts/check_api.py`, `tests/test_pipeline.py` (deleted on `refactor`): `git rm` them
- Check: `uv run pytest` (5 tests), no `waxal_agent/` folder left, then `git push origin main`.
- Afterwards, delete the `refactor` branch (local and on GitHub).

## Content
- `data/skills/register-on-partner-website/SKILL.md` is a stub: write the registration steps on renassur.sn.
- `docs/skills/` has no copy of the older `answer-from-the-code` and `declare-a-claim` skills (deleted): bring them back or drop them.

## Settings
- Consider `AGENT_MEMORY_MODEL=claude-haiku-5-5` in `.env`: the notes saved after each answer would cost far less.
- `.env` still has an unused `HF_TOKEN=` line (the Hugging Face voice was removed).
- `token.txt` is in the folder (git-ignored): keep it out of any commit.

## DeepSeek (when the key is available)
- Run the two-question cache test on `deepseek-flash` (`DEEPSEEK_API_KEY`) and compare the cost and the answers with Claude.
- With DeepSeek the agent has no `web_search` and reads PDFs in text mode only.
