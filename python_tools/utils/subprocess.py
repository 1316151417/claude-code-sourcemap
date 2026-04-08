"""Subprocess utility functions for Claude Code Tools."""

import subprocess
from typing import Optional, List


def run_ripgrep(
    pattern: str,
    path: Optional[str] = None,
    glob: Optional[str] = None,
    context: Optional[int] = None,
    multiline: bool = False,
    case_insensitive: bool = False,
    show_line_numbers: bool = True,
    head_limit: Optional[int] = None,
    output_mode: str = "files_with_matches"
) -> subprocess.CompletedProcess:
    """Run ripgrep with the given arguments."""
    cmd: List[str] = ["rg"]
    if case_insensitive:
        cmd.append("-i")
    if multiline:
        cmd.append("-U")
    if show_line_numbers:
        cmd.append("-n")
    if context is not None:
        cmd.extend(["-C", str(context)])
    if head_limit is not None:
        cmd.extend(["--limit", str(head_limit)])
    if output_mode == "count":
        cmd.append("-c")
    elif output_mode == "files_with_matches":
        cmd.append("-l")
    if glob is not None:
        cmd.extend(["-g", glob])
    cmd.append(pattern)
    if path is not None:
        cmd.append(path)
    return subprocess.run(cmd, capture_output=True, text=True)
