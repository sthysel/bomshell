# bomshell development tasks

# List available recipes
default:
    @just --list

# Install dependencies
install:
    uv sync --all-extras

# Run tests
test *args:
    uv run pytest {{ args }}

# Run tests with coverage
test-cov:
    uv run pytest --cov --cov-report=term-missing

# Lint code
lint:
    uv run ruff check src tests

# Format code
fmt:
    uv run ruff format src tests

# Fix linting issues
fix:
    uv run ruff check --fix src tests

# Type check
typecheck:
    uv run mypy src

# Run all pre-commit hooks on all files
pre-commit:
    uv run pre-commit run --all-files

# Install pre-commit hooks
pre-commit-install:
    uv run pre-commit install

# Run QA checks (lint + typecheck + test)
qa: lint typecheck test

# Bump patch version (0.0.X)
bump-patch:
    uv run bump-my-version bump patch

# Bump minor version (0.X.0)
bump-minor:
    uv run bump-my-version bump minor

# Bump major version (X.0.0)
bump-major:
    uv run bump-my-version bump major

# Show current version
version:
    uv run bump-my-version show current_version

# Show what would change for a version bump (dry run)
bump-dry part="patch":
    uv run bump-my-version bump --dry-run --verbose {{ part }}

# Build package
build:
    uv build

# Clean build artifacts
clean:
    rm -rf dist/ build/ *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov/
