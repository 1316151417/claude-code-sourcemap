"""Path utility functions for Claude Code Tools."""

from pathlib import Path
from typing import Optional


def expand_path(path: str) -> Path:
    """Expand a path string, handling ~ and environment variables."""
    return Path(path).expanduser().resolve()


def normalize_path(path: str) -> str:
    """Normalize a path string to a canonical form."""
    return str(expand_path(path))
