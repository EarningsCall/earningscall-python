# CLAUDE.md

## What this repo is

The public Python client library for the EarningsCall developer API, published
to PyPI as [`earningscall`](https://pypi.org/project/earningscall/). It is a
thin `requests`-based SDK: all calls hit `https://v2.api.earningscall.biz` (domain
overridable via `EARNINGSCALL_DOMAIN`), plus `https://earningscall.biz/exchanges.json`
for the exchange list. Auth is an `apikey` query param resolved from
`earningscall.api_key`, then the `ECALL_API_KEY` / `EARNINGSCALL_API_KEY` env
vars, defaulting to `"demo"` (AAPL-only sample access; other symbols raise
`InsufficientApiAccessError`). Public surface (see `earningscall/__init__.py`):
`get_company`, `get_all_companies`, `get_sp500_companies`, `get_calendar`,
`Symbols`, `load_symbols`, `exchanges`, and module-level config
(`api_key`, `enable_requests_cache`, `retry_strategy`).

## Key files

- `earningscall/api.py` — HTTP layer. Endpoint wrappers (`events`,
  `transcript`, `audio`, `slides`, `calendar`, `symbols-v2.txt`,
  `symbols/sp500.txt`), retry with backoff on 429/5xx, 401 →
  `InvalidApiKeyError`, optional `requests-cache` sqlite cache
  (`.earningscall_cache` in the temp dir, on by default).
- `earningscall/exports.py` — the top-level functions re-exported by
  `__init__.py`.
- `earningscall/company.py` — `Company`: `events()`, `get_transcript()`
  (levels 1–4), `download_audio_file()`, `download_slide_deck()`. Maps 404 →
  `None`/`[]` and 403 → `InsufficientApiAccessError`.
- `earningscall/symbols.py` — `CompanyInfo`/`Symbols`; parses the
  tab-separated `symbols-v2.txt` index; cached in a module-level singleton.
- `earningscall/exchanges.py`, `sectors.py` — index↔name tables; exchanges
  load dynamically from `exchanges.json` with a hardcoded fallback list.
- `earningscall/transcript.py`, `event.py`, `calendar.py` — `dataclasses_json`
  response models. `errors.py` — exception types.
- `tests/` — pytest + `responses`; recorded YAML fixtures in `tests/data`, no
  live network. `scripts/` — runnable examples (`python -m scripts.<name>`).

## How changes ship

- Build/test/lint via Hatch (hatchling backend) — commands in
  [DEVELOPMENT.md](DEVELOPMENT.md). CI (`.github/workflows/test.yml`) runs
  `hatch run lint:all` (ruff, black, mypy), `hatch run cov` (Coveralls), and a
  containerized matrix `hatch run all:test` on Python 3.10–3.14.
- Releases: bump the static `version` in `pyproject.toml` `[project]`, add a
  `## Release \`X.Y.Z\` - YYYY-MM-DD` entry to `CHANGELOG.md`, then push a
  `vX.Y.Z` tag. `.github/workflows/release.yml` builds and publishes to PyPI
  via trusted publishing (OIDC, `pypi` environment), signs with Sigstore, and
  creates the GitHub Release. Merges to `master` build but do not publish.

## Gotchas

- `[tool.hatch.version]` in pyproject points at `hatch_init/__about__.py`,
  which does not exist — dead template config (version is not in `dynamic`).
  The real version is `[project] version`. The `--cov=hatch_init` script there
  is equally dead; `hatch.toml` `[envs.default]` overrides it. Don't "fix"
  either by creating `hatch_init/`.
- Module-level singletons (`symbols._symbols`, `exchanges._exchanges_in_order`)
  and the on-disk requests cache persist stale data across calls; use
  `clear_symbols()` / `api.purge_cache()` in tests (see the autouse fixture in
  `tests/test_helper.py`).
