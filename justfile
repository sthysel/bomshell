# bomshell development tasks

[doc("List available recipes")]
default:
    @just --list

[doc("Install dependencies")]
install:
    uv sync --all-extras

[doc("Run tests")]
test *args:
    uv run pytest {{ args }}

[doc("Run tests with coverage")]
test-cov:
    uv run pytest --cov --cov-report=term-missing

[doc("Lint code")]
lint:
    uv run ruff check src tests

[doc("Format code")]
fmt:
    uv run ruff format src tests

[doc("Fix linting issues")]
fix:
    uv run ruff check --fix src tests

[doc("Type check")]
typecheck:
    uv run mypy src

[doc("Run all pre-commit hooks on all files")]
pre-commit:
    uv run pre-commit run --all-files

[doc("Install pre-commit hooks")]
pre-commit-install:
    uv run pre-commit install

[doc("Run QA checks (lint + typecheck + test)")]
qa: lint typecheck test

[doc("Bump patch version (0.0.X)")]
bump-patch:
    uv run bump-my-version bump patch

[doc("Bump minor version (0.X.0)")]
bump-minor:
    uv run bump-my-version bump minor

[doc("Bump major version (X.0.0)")]
bump-major:
    uv run bump-my-version bump major

[doc("Show current version")]
version:
    uv run bump-my-version show current_version

[doc("Show what would change for a version bump (dry run)")]
bump-dry part="patch":
    uv run bump-my-version bump --dry-run --verbose {{ part }}

[doc("Build package")]
build:
    uv build

[doc("Clean build artifacts")]
clean:
    rm -rf dist/ build/ *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/
