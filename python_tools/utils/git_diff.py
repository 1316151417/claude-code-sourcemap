"""Git diff utility functions for Claude Code Tools."""

from typing import Optional


def generate_patch(
    original_content: str,
    new_content: str,
    file_path: Optional[str] = None
) -> str:
    """Generate a unified diff patch between two strings."""
    import difflib
    original_lines = original_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    diff = difflib.unified_diff(
        original_lines,
        new_lines,
        fromfile=file_path or "original",
        tofile=file_path or "modified",
        lineterm=""
    )
    return "".join(diff)
