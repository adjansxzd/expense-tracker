# AGENTS.md — instructions for AI coding agents

These rules apply to any AI assistant (Claude, Copilot, Codex, Cursor, etc.) working in this
repository. If your tool does not load this file automatically, the human operator must paste
the relevant sections into the prompt and say so in the AI-use record.

## 1. Purpose
`expense-tracker` is a small, single-user command-line tool that records personal expenses in a
local JSON file and prints listings and per-category reports (text / CSV / JSON). It has no
network access, no server, and no database. Treat all data as personal financial data.

## 2. Architecture (src layout)
| Path | Responsibility |
|---|---|
| `src/expense_tracker/models.py` | `Expense` dataclass, dict (de)serialisation, money (`Decimal`) |
| `src/expense_tracker/storage.py` | Load/save the JSON data file, ID allocation |
| `src/expense_tracker/reports.py` | Pure aggregation functions (totals, month filter) |
| `src/expense_tracker/formatters.py` | Output-format strategies (text / csv / json) |
| `src/expense_tracker/cli.py` | argparse wiring only; no business logic |
| `tests/` | pytest suite; `tests/test_cli.py` holds end-to-end characterization tests |

Data flow: `cli` → `storage` / `reports` → `formatters` → stdout.
Business rules belong in `models` or `reports`, not in `cli`.

## 3. Setup
```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .
```
Python >= 3.10 is required.

## 4. Safe commands (may be run without asking)
| Purpose | Command |
|---|---|
| Tests | `python -m pytest -q` |
| Lint | `ruff check src tests` |
| Types | `mypy src` |
| Build | `python -m build --wheel --outdir dist/` |
| Run the CLI | `python -m expense_tracker --file /tmp/<scratch>.json <command>` |
| Read-only git | `git status`, `git diff`, `git log` |

Always pass `--file` pointing to a scratch file under `/tmp` when running the CLI, so that the
user's real `expenses.json` is never read or modified.

## 5. Coding conventions
- Python 3.10+, type hints on all new or changed functions; `mypy src` must stay clean.
- Money is `decimal.Decimal`, never `float`. Round only when formatting (2 decimal places).
- Keep `cli.py` thin: parse arguments, call validation/domain code, pick a formatter.
- New output formats are added by registering a formatter in `formatters.py`,
  not by adding `if/elif` branches in `cli.py`.
- Errors shown to the user go to stderr with exit code 2; no raw tracebacks for bad input.
- Style is enforced by `ruff` (config in `pyproject.toml`); do not reformat unrelated code.

## 6. Test expectations
- Every behaviour change or bug fix comes with a test that fails before and passes after.
- Do not delete, skip, or weaken existing tests to make a change pass.
- Before proposing a change as done, run tests + lint + mypy and paste the actual output.
  Never report results you did not execute.
- The acceptance criteria in `ACCEPTANCE.md` must keep passing.

## 7. Forbidden actions
- No secrets: never add API keys, tokens, passwords, or real personal/financial data to the
  repo, test fixtures, logs, or prompts. Use obviously fake sample data.
- No deployments or publishing (`twine upload`, pushing tags, creating releases).
- No destructive commands: `rm -rf`, `git push --force`, `git reset --hard`, history rewrites,
  deleting or overwriting `expenses.json` or any file outside the repo / `/tmp`.
- No dependency changes without human review: do not add, remove, or upgrade packages in
  `pyproject.toml` or `requirements-dev.txt`; propose the change and stop.
- No network calls from code or tests.
- Do not modify `AGENTS.md`, `ACCEPTANCE.md`, or CI configuration without explicit approval.

## 8. Review gates
- Work happens on a feature branch (`agent/<topic>`); never commit directly to `main`.
- A human reviews every diff and the test log before merge.
- Changes touching `storage.py` (data persistence) or money handling need an extra manual
  check with a copy of a real-shaped data file.
- If you are unsure, or a step requires a forbidden action, stop and ask.
