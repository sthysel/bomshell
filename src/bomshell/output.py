"""Centralized output module for bomshell CLI.

All user-facing output goes through these helpers. When ``--json`` mode
is active, informational messages are suppressed and structured data is
emitted as JSON to stdout.
"""

import json
from typing import Any

from rich.console import Console

_console = Console()
_err_console = Console(stderr=True)

_json_mode: bool = False


def set_json_mode(enabled: bool) -> None:
    global _json_mode
    _json_mode = enabled


def is_json_mode() -> bool:
    return _json_mode


def emit_json(data: Any) -> None:
    """Print *data* as JSON to stdout (always, regardless of mode)."""
    print(json.dumps(data, default=str, ensure_ascii=False, indent=2))


def print_info(msg: str) -> None:
    if not _json_mode:
        _console.print(msg)


def print_success(msg: str) -> None:
    if not _json_mode:
        _console.print(msg, style="green")


def print_warning(msg: str) -> None:
    if not _json_mode:
        _console.print(msg, style="yellow")


def print_error(msg: str) -> None:
    _err_console.print(msg, style="red")


def print_cyan(msg: str) -> None:
    if not _json_mode:
        _console.print(msg, style="cyan")
