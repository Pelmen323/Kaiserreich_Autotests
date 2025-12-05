<!-- Copilot / AI agent instructions for Kaiserreich_Tests -->
# Copilot Instructions — Kaiserreich Pytests

Purpose: fast orientation for an AI coding agent to be immediately productive in this repository.

- **Big picture:** This repo contains static-analysis pytest suites that parse Hearts of Iron IV mod files (Kaiserreich). Tests operate by parsing the mod files and analysing token/flag/loc/event/OOB usage — they do NOT run the game. Tests live under `tests/` and rely on parsing helpers in `data/` and several root scripts. Use `core/runner.py` to resolve the target mod path; CI workflows should provide `--repo_path` where appropriate (see CI specifics below).

- **How tests run (essential commands):**
  - Local: `pytest -v -s --tb=short "--username=YOUR_USER" "--mod_name=MOD_FOLDER" -n 6`
  - Deprecated: invoking a direct CI run with a hard-coded `--repo_path=...` is deprecated for this repository; automated CI runs are managed by private GitHub Actions that supply repository paths and secrets.
  - The project requires `pytest` and `pytest-xdist` (see `requirements.txt` / `Pipfile`). `pytest.ini` enables CLI logging and defines markers like `smoke`, `kr_specific`, `flaky`.

- **Key files to reference:**
  - `core/runner.py` — constructs `full_path_to_mod` and ensures cross-platform normalization and trailing slash behaviour.
  - `pytest.ini` — runtime flags, logging and markers.
  - `README.md` — overall project intent and usage examples (local runs and CI notes).
  - `requirements.txt` / `Pipfile` — pinned dependencies used in CI and locally.
  - `data/` and many root scripts (e.g., `generate_*`, helpers at repo root) — primary parsing utilities; tests call these directly.

- **Repository conventions & patterns (explicit):**
  - Tests parse Paradox scripting files using custom parsing utilities and token-stream helpers; treat inputs as token lists / AST-like structures rather than running an interpreter.
  - Tests are named `test_*.py` and grouped in subfolders (e.g., `tests/variables/`) by domain (flags, events, localisation, ideas, etc.).
  - CLI test runner parameters are passed as quoted string options (e.g., `"--username=..."`) — these are required for local runs unless CI provides `--repo_path`.
  - Parallelization: tests are designed to run under `pytest-xdist -n <cores>`. Avoid introducing global mutable state in helpers; prefer passing contexts or using thread-safe constructs.

- **When editing or adding tests:**
  - Prefer small, focused tests that operate on parsed file data rather than touching the filesystem or external services.
  - Reuse parsing utilities under `data/` or root helper scripts to keep behavior consistent.
  - Apply existing pytest markers for categorization (`smoke`, `kr_specific`, `flaky`). Add new markers to `pytest.ini` if necessary.

- **CI specifics (GitHub Actions):**
  - CI for this repository is implemented with private GitHub Actions. Actions supply environment variables and may pass `--repo_path` to tests; avoid hard-coded per-user paths in workflows.
  - To produce XML test artifacts in Actions, include `--junitxml TestResults.xml` on the pytest command line.

- **Skip / Do not touch:**
  - `misc_scripts_and_outdated_files/` is legacy/outdated; skip this folder entirely — do not add new dependencies on its contents.

- **Examples to cite when changing behavior:**
  - Path handling: maintain `core/runner.py` behavior — it uses `os.name`, `os.path.normpath`, and `ensure_trailing_slash()` to normalize mod paths.
  - Logging: tests run with `log_cli=true` and `DEBUG` level via `pytest.ini`; keep logs informative but avoid noisy prints.

- **Do NOT assume:**
  - Tests do not execute the HOI4 binary — any change that attempts to run the game is out of scope.
  - The mod path is always local to the machine user — prefer CI-provided `--repo_path` in automation.

