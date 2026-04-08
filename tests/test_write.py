import os
import tempfile
from python_tools.tools.write import FileWriteTool
from python_tools.types import WriteInput


def test_write_creates_new_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "new_file.txt")
        tool = FileWriteTool()
        result = tool.call(WriteInput(file_path=path, content="hello world"))

        assert result.success is True
        assert result.data.type == "create"
        assert result.data.original_file is None

        with open(path) as f:
            assert f.read() == "hello world"


def test_write_updates_existing_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("original content")
        f.flush()
        path = f.name

    try:
        tool = FileWriteTool()
        result = tool.call(WriteInput(file_path=path, content="updated content"))

        assert result.success is True
        assert result.data.type == "update"
        assert result.data.original_file == "original content"

        with open(path) as f:
            assert f.read() == "updated content"
    finally:
        os.unlink(path)
