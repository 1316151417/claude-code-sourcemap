import os
import tempfile
from python_tools.tools.edit import FileEditTool
from python_tools.types import EditInput


def test_edit_simple_replacement():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("hello world")
        f.flush()
        path = f.name

    try:
        tool = FileEditTool()
        result = tool.call(EditInput(
            file_path=path,
            old_string="world",
            new_string="python",
        ))

        assert result.success is True
        assert result.data.old_string == "world"
        assert result.data.new_string == "python"

        # Verify file was modified
        with open(path) as f:
            assert f.read() == "hello python"
    finally:
        os.unlink(path)


def test_edit_replace_all():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
        f.write("foo bar foo baz foo")
        f.flush()
        path = f.name

    try:
        tool = FileEditTool()
        result = tool.call(EditInput(
            file_path=path,
            old_string="foo",
            new_string="XXX",
            replace_all=True,
        ))

        assert result.success is True
        assert result.data.replace_all is True

        with open(path) as f:
            assert f.read() == "XXX bar XXX baz XXX"
    finally:
        os.unlink(path)


def test_edit_file_not_found():
    tool = FileEditTool()
    result = tool.call(EditInput(
        file_path="/nonexistent/file.txt",
        old_string="test",
        new_string="replacement",
    ))

    assert result.success is False
    assert "not found" in result.error.lower()