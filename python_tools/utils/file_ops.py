"""File operation utility functions for Claude Code Tools."""

import os
import tempfile
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class FileReadResult:
    """Result of reading a file range."""
    content: str
    total_lines: int
    start_line: int
    num_lines: int


@dataclass
class FileEncodingInfo:
    """Information about file encoding."""
    encoding: str
    line_endings: str


def read_file_range(file_path: str, offset: int = 1, limit: Optional[int] = None) -> FileReadResult:
    """Read a range of lines from a file.

    Args:
        file_path: Path to the file to read
        offset: Starting line number (1-indexed)
        limit: Maximum number of lines to read, or None for all remaining

    Returns:
        FileReadResult with content, total_lines, start_line, and num_lines
    """
    with open(file_path, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    total_lines = len(all_lines)

    # Adjust offset to 0-based indexing
    start_idx = offset - 1

    if limit is None:
        end_idx = total_lines
    else:
        end_idx = start_idx + limit

    # Clamp to valid range
    start_idx = max(0, min(start_idx, total_lines))
    end_idx = max(start_idx, min(end_idx, total_lines))

    selected_lines = all_lines[start_idx:end_idx]
    content = "".join(selected_lines)
    num_lines = len(selected_lines)

    return FileReadResult(
        content=content,
        total_lines=total_lines,
        start_line=offset,
        num_lines=num_lines
    )


def write_text(file_path: str, content: str, encoding: str = 'utf-8', line_endings: str = 'LF') -> None:
    """Write text content to a file.

    Args:
        file_path: Path to the file to write
        content: Text content to write
        encoding: Character encoding to use (default: utf-8)
        line_endings: Line ending style - 'LF' or 'CRLF' (default: 'LF')
    """
    if line_endings == 'CRLF':
        content = content.replace('\n', '\r\n')

    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)


def atomic_write(file_path: str, content: str) -> None:
    """Write content to a file atomically."""
    dir_path = os.path.dirname(file_path)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=dir_path,
        delete=False
    ) as f:
        f.write(content)
        temp_path = f.name
    os.replace(temp_path, file_path)


def get_file_encoding(file_path: str) -> FileEncodingInfo:
    """Detect the encoding and line endings of a file.

    Returns:
        FileEncodingInfo with encoding and line_endings fields
    """
    try:
        with open(file_path, "rb") as f:
            f.read(1024)
        encoding = "utf-8"
    except UnicodeDecodeError:
        encoding = "latin-1"

    line_endings = get_line_endings(file_path)

    return FileEncodingInfo(encoding=encoding, line_endings=line_endings)


def get_line_endings(file_path: str) -> Literal["LF", "CRLF", "unknown"]:
    """Detect the line ending style of a file.

    Returns:
        One of "LF", "CRLF", or "unknown"
    """
    with open(file_path, "rb") as f:
        data = f.read(1024)

    if b"\r\n" in data:
        return "CRLF"
    elif b"\r" in data:
        return "CRLF"  # treating CR as part of CRLF for simplicity
    elif b"\n" in data:
        return "LF"
    return "unknown"
