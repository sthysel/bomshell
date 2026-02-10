# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bomshell is a Python CLI tool for retrieving weather data from the Australian Bureau of Meteorology (BOM). It fetches spatial data from BOM's public FTP server and builds a local SQLite database for weather information queries.

## Build and Test Commands

Use `just` to run common development tasks:

```bash
just              # List all available recipes
just install      # Install dependencies
just test         # Run tests
just test-cov     # Run tests with coverage
just lint         # Lint code
just fmt          # Format code
just fix          # Auto-fix linting issues
just typecheck    # Run ty
just pre-commit   # Run all pre-commit hooks
just qa           # Run lint + typecheck + test
just build        # Build package
just clean        # Clean build artifacts
```

Version management with bump-my-version:

```bash
just version      # Show current version
just bump-patch   # Bump patch version (0.0.X)
just bump-minor   # Bump minor version (0.X.0)
just bump-major   # Bump major version (X.0.0)
just bump-dry     # Dry run to preview changes
```

## Architecture

### Entry Point
- **CLI**: `src/bomshell/cli.py` - Click-based CLI with commands:
  - `bomshell knobs` - Print configuration settings
  - `bomshell spatial fetch/sync/build/csvdump/tabledump` - Spatial data management

### Core Modules
- `settings.py` - Configuration management with dotenv support, XDG base directories
- `knobs.py` - Configuration registry (environment variables: `BOM_CACHE`, `BOM_FTP_TIMEOUT`, etc.)
- `fetch_gis.py` - Spatial data fetching from BOM FTP, SQLite database creation
- `fetch.py` - FTP file downloading utilities
- `dump_gis.py` - Data export to CSV and formatted tables
- `bom_paths.py` - BOM FTP server paths and data source documentation

### Data Flow
1. Fetch DBF spatial files from BOM FTP (`ftp.bom.gov.au`)
2. Store in cache directory (`~/.cache/bomshell/spatial_cache/`)
3. Build SQLite database (`~/.cache/bomshell/spatial.sqlite`)
4. Query/export data via CLI

### Configuration
- Config file: `~/.bomshell` (dotenv format)
- Generate defaults: `bomshell knobs > ~/.bomshell`

## Code Style
- Max line length: 140 characters
- Python 3.10+ required
- Uses ruff for linting and formatting
- Pre-commit hooks enforce QA checks
