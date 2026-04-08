import os
import tempfile
from python_tools.tools.read import FileReadTool
from python_tools.types import ReadInput


def test_read_simple_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("line1\nline2\nline3\n")
        f.flush()
        path = f.name

    try:
        tool = FileReadTool()
        result = tool.call(ReadInput(file_path=path))

        assert result.success is True
        assert result.data.type == "text"
        assert result.data.content == "line1\nline2\nline3\n"
        assert result.data.total_lines == 3
    finally:
        os.unlink(path)


def test_read_with_offset_and_limit():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("line1\nline2\nline3\nline4\nline5\n")
        f.flush()
        path = f.name

    try:
        tool = FileReadTool()
        result = tool.call(ReadInput(file_path=path, offset=2, limit=2))

        assert result.success is True
        assert result.data.content == "line2\nline3\n"
        assert result.data.start_line == 2
        assert result.data.num_lines == 2
    finally:
        os.unlink(path)


def test_read_nonexistent_file():
    tool = FileReadTool()
    result = tool.call(ReadInput(file_path="/nonexistent/file.txt"))

    assert result.success is False
    assert result.error is not None
    assert "not found" in result.error.lower()