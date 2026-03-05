# EarningsCall Python SDK

## Project Context

- Open-source Python client library for the EarningsCall API
- Published to PyPI as `earningscall`
- Tests: `pytest tests/` (uses `responses` for HTTP mocking)
- Lint: `ruff check .` and `black --check --diff .`
- Coverage: `python -m coverage run -m pytest tests/ && python -m coverage combine && python -m coverage report --show-missing`
- CI checks coveralls — do not let coverage decrease

## Python Clean Code Rules

### Architecture

- Keep functions small (<40 lines). Avoid deep nesting (max 2 levels).
- Prefer composition over inheritance.

### Exception Handling

- Catch the most specific exception possible.
- Never catch `Exception` unless top-level handler.
- Never swallow exceptions (`except Exception: pass` is forbidden).
- Never use `raise e` — use bare `raise`.
- Let programmer errors (KeyError, AttributeError, etc.) fail fast — don't catch them.

### Data Handling

- Use `dict["key"]` for required fields — let KeyError bubble up if missing.
- Use `.get()` only for genuinely optional fields with sensible defaults.
- Do not use `getattr()` as a substitute for proper type checking or configuration. If a module attribute is typed, trust the type.
- Fail fast over defensive guessing.

### Imports

- All imports at module level. No lazy imports.
- Order: stdlib, third-party, local.

### Logging

- Never use `print()`. Use the project logger: `log = logging.getLogger(__file__)`.
- Use f-strings for log messages.
- No sensitive data in logs (credentials, API keys, PII).

### Testing

- Business logic must be unit-testable. Mock external services.
- Test error paths.
- Use `responses` library for HTTP mocking, not `unittest.mock.patch` on requests.

### Forbidden Patterns

- `except Exception: pass`
- Catching generic `Exception` without reason
- Hardcoded credentials or environment-specific resource names
- Mutable default arguments
- Silent fallback behavior
- `print()` instead of logger
- `raise e` instead of bare `raise`
