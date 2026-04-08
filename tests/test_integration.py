"""Integration tests for the complete tool system."""

import os
import tempfile
from python_tools.tools.read import FileReadTool
from python_tools.tools.edit import FileEditTool
from python_tools.tools.write import FileWriteTool
from python_tools.tools.glob import GlobTool
from python_tools.types import ReadInput, EditInput, WriteInput, GlobInput


def test_end_to_end_file_workflow():
    """Test complete workflow: write -> read -> edit -> read."""
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, "test.txt")

        # Write
        write_tool = FileWriteTool()
        write_result = write_tool.call(WriteInput(file_path=file_path, content="hello world"))
        assert write_result.success is True
        assert write_result.data.type == "create"

        # Read
        read_tool = FileReadTool()
        read_result = read_tool.call(ReadInput(file_path=file_path))
        assert read_result.success is True
        assert "hello world" in read_result.data.content

        # Edit
        edit_tool = FileEditTool()
        edit_result = edit_tool.call(EditInput(
            file_path=file_path,
            old_string="world",
            new_string="python",
        ))
        assert edit_result.success is True
        assert edit_result.data.user_modified is True

        # Read again
        read_result2 = read_tool.call(ReadInput(file_path=file_path))
        assert "hello python" in read_result2.data.content


def test_glob_and_grep_workflow():
    """Test glob -> grep workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create files
        for name in ["file1.txt", "file2.txt", "file3.js"]:
            with open(os.path.join(tmpdir, name), "w") as f:
                if name.endswith(".txt"):
                    f.write("hello\n")
                else:
                    f.write("world\n")

        # Glob
        glob_tool = GlobTool()
        glob_result = glob_tool.call(GlobInput(pattern="*.txt", path=tmpdir))
        assert glob_result.success is True
        assert glob_result.data.num_files == 2


def test_registry_integration():
    """Test tool registry."""
    from python_tools.registry import get_registry

    registry = get_registry()
    tools = registry.list_tools()

    assert "Read" in tools
    assert "Edit" in tools
    assert "Write" in tools
    assert "Glob" in tools
    assert "Grep" in tools

    read_tool = registry.get("Read")
    assert read_tool is not None
    assert isinstance(read_tool, FileReadTool)