"""Git diff utility functions for Claude Code Tools."""

import difflib
from typing import Optional


def generate_patch(
    file_path: str,
    old_content: str,
    new_content: str
) -> dict:
    """Generate a unified diff patch between two strings.

    Returns a dict with:
        - original: the original content
        - updated: the new content
        - patch: the unified diff patch string
    """
    original_lines = old_content.splitlines(keepends=True)
    new_lines = new_content.splitlines(keepends=True)
    diff = difflib.unified_diff(
        original_lines,
        new_lines,
        fromfile=file_path,
        tofile=file_path,
        lineterm=""
    )
    return {
        "original": old_content,
        "updated": new_content,
        "patch": "".join(diff)
    }


def find_actual_string(content: str, search_string: str) -> Optional[str]:
    """Find the search_string in content.

    Returns the matched string if found, None otherwise.
    """
    if search_string in content:
        return search_string
    return None
