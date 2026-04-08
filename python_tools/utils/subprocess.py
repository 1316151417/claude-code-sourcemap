"""Subprocess utility functions for Claude Code Tools."""

import subprocess
import shutil
from typing import Optional, List
from python_tools.types import RipgrepResult


def _check_ripgrep_available() -> bool:
    """Check if ripgrep is available in PATH."""
    return shutil.which("rg") is not None


def run_ripgrep(
    pattern: str,
    path: str,
    output_mode: str = "files_with_matches",
    glob: Optional[str] = None,
    case_insensitive: bool = False,
    show_line_numbers: bool = True,
    context: Optional[int] = None,
    head_limit: Optional[int] = None,
    multiline: bool = False,
) -> RipgrepResult:
    """Run ripgrep with the given arguments.

    Returns RipgrepResult with fields:
    - mode: the output mode used
    - filenames: list of matching filenames (for files_with_matches mode)
    - content: matched content lines (for content mode)
    - num_matches: number of matches found
    - num_files: number of files with matches
    - truncated: whether results were truncated
    """
    if not _check_ripgrep_available():
        raise RuntimeError(
            "ripgrep (rg) is not installed. "
            "Please install it with: brew install ripgrep (macOS) or apt install ripgrep (Linux)"
        )

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
    # For content mode, no special flag needed - rg outputs content by default
    if glob is not None:
        cmd.extend(["-g", glob])
    cmd.append(pattern)
    if path is not None:
        cmd.append(path)

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Parse output based on mode
    filenames: list[str] = []
    content: str = ""
    num_matches: int = 0
    num_files: int = 0
    truncated: bool = False

    if result.returncode != 0 and result.returncode != 1:
        # Returncode 0 means matches found, 1 means no matches (which is OK)
        raise RuntimeError(f"ripgrep failed: {result.stderr}")

    if output_mode == "files_with_matches":
        filenames = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        num_files = len(filenames)
        # Check if results were truncated
        if head_limit is not None and num_files >= head_limit:
            truncated = True
    elif output_mode == "content":
        content = result.stdout
        # Count matches (lines with content)
        num_matches = len([line for line in result.stdout.strip().split("\n") if line.strip()])
        # For content mode, we need to count unique files
        # This is tricky since content mode doesn't show filenames by default
        # Run again to get file count
        if num_matches > 0:
            count_cmd = cmd.copy()
            # Remove -n (line numbers) for counting
            if "-n" in count_cmd:
                count_cmd.remove("-n")
            # Change to files_with_matches to get unique files
            count_cmd[count_cmd.index("rg")] = "rg"
            count_cmd = ["rg", "-l"] + cmd[1:]
            files_result = subprocess.run(
                ["rg", "-l"] + cmd[1:],
                capture_output=True,
                text=True,
            )
            filenames = [line.strip() for line in files_result.stdout.strip().split("\n") if line.strip()]
            num_files = len(filenames)
    elif output_mode == "count":
        # Count mode outputs in format "file:count"
        for line in result.stdout.strip().split("\n"):
            if ":" in line:
                _, count = line.rsplit(":", 1)
                try:
                    num_matches += int(count.strip())
                except ValueError:
                    pass
        # For count mode, filenames are all files searched
        # We don't have this info easily, so leave it empty

    return RipgrepResult(
        mode=output_mode,
        filenames=filenames,
        content=content,
        num_matches=num_matches,
        num_files=num_files,
        truncated=truncated,
    )