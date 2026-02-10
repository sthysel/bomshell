# bomshell development tasks

[doc("List available recipes")]
default:
    @just --list

# ── Setup ──────────────────────────────────────────────

[group("setup")]
[doc("Install dependencies")]
install:
    uv sync --all-extras

[group("setup")]
[doc("Install pre-commit hooks")]
pre-commit-install:
    uv run pre-commit install

# ── Quality ────────────────────────────────────────────

[group("quality")]
[doc("Run tests")]
test *args:
    uv run pytest {{ args }}

[group("quality")]
[doc("Run tests with coverage")]
test-cov:
    uv run pytest --cov --cov-report=term-missing

[group("quality")]
[doc("Lint code")]
lint:
    uv run ruff check src tests

[group("quality")]
[doc("Format code")]
fmt:
    uv run ruff format src tests

[group("quality")]
[doc("Fix linting issues")]
fix:
    uv run ruff check --fix src tests

[group("quality")]
[doc("Type check")]
typecheck:
    uv run ty check .

[group("quality")]
[doc("Run all pre-commit hooks on all files")]
pre-commit:
    uv run pre-commit run --all-files

[group("quality")]
[doc("Run QA checks (lint + typecheck + test)")]
qa: lint typecheck test

# ── Version ────────────────────────────────────────────

[group("version")]
[doc("Show current version")]
version:
    uv run bump-my-version show current_version

[group("version")]
[doc("Bump patch version (0.0.X)")]
bump-patch:
    uv run bump-my-version bump patch

[group("version")]
[doc("Bump minor version (0.X.0)")]
bump-minor:
    uv run bump-my-version bump minor

[group("version")]
[doc("Bump major version (X.0.0)")]
bump-major:
    uv run bump-my-version bump major

[group("version")]
[doc("Show what would change for a version bump (dry run)")]
bump-dry part="patch":
    uv run bump-my-version bump --dry-run --verbose {{ part }}

# ── Build ──────────────────────────────────────────────

[group("build")]
[doc("Build package")]
build:
    uv build

[group("build")]
[doc("Clean build artifacts")]
clean:
    rm -rf dist/ build/ *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/
