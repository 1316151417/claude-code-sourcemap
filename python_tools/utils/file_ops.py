"""File operation utility functions for Claude Code Tools."""

import os
import tempfile
from typing import Optional, Tuple


def read_file_range(file_path: str, start: int, end: Optional[int] = None) -> str:
    """Read a range of lines from a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        if start > 1:
            for _ in range(start - 1):
                f.readline()
        if end is None:
            return f.read()
        lines = []
        for _ in range(end - start + 1):
            line = f.readline()
            if not line:
                break
            lines.append(line)
        return "".join(lines)


def write_text(file_path: str, content: str) -> None:
    """Write text content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
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


def get_file_encoding(file_path: str) -> str:
    """Detect the encoding of a file."""
    try:
        with open(file_path, "rb") as f:
            f.read(1024)
        return "utf-8"
    except UnicodeDecodeError:
        return "latin-1"


def get_line_endings(file_path: str) -> str:
    """Detect the line ending style of a file."""
    with open(file_path, "rb") as f:
        data = f.read(1024)
    if b"\r\n" in data:
        return "crlf"
    elif b"\r" in data:
        return "cr"
    return "lf"
