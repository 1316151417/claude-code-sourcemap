import os
import tempfile
from python_tools.utils.file_ops import (
    read_file_range,
    write_text,
    get_file_encoding,
    get_line_endings,
)


def test_read_file_range_full():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("line1\nline2\nline3\n")
        f.flush()
        path = f.name

    try:
        result = read_file_range(path)
        assert result.content == "line1\nline2\nline3\n"
        assert result.total_lines == 3
    finally:
        os.unlink(path)


def test_read_file_range_with_offset_and_limit():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("line1\nline2\nline3\nline4\nline5\n")
        f.flush()
        path = f.name

    try:
        result = read_file_range(path, offset=2, limit=2)
        assert result.content == "line2\nline3\n"
        assert result.start_line == 2
        assert result.num_lines == 2
        assert result.total_lines == 5
    finally:
        os.unlink(path)


def test_write_text_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.txt")
        write_text(path, "hello world")
        with open(path) as f:
            assert f.read() == "hello world"


def test_write_text_preserves_content():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "test.txt")
        write_text(path, "hello world")
        info = get_file_encoding(path)
        assert info.encoding == "utf-8"
