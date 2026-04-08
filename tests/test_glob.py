import os
import tempfile
from python_tools.tools.glob import GlobTool
from python_tools.types import GlobInput


def test_glob_simple_pattern():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        for name in ["file1.txt", "file2.txt", "file3.js"]:
            with open(os.path.join(tmpdir, name), "w") as f:
                f.write("content")

        tool = GlobTool()
        result = tool.call(GlobInput(pattern="*.txt", path=tmpdir))

        assert result.success is True
        assert result.data.num_files == 2
        assert "file1.txt" in result.data.filenames
        assert "file3.js" not in result.data.filenames


def test_glob_nested_pattern():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create nested structure
        os.makedirs(os.path.join(tmpdir, "subdir"))
        with open(os.path.join(tmpdir, "subdir", "nested.txt"), "w") as f:
            f.write("content")

        tool = GlobTool()
        result = tool.call(GlobInput(pattern="**/*.txt", path=tmpdir))

        assert result.success is True
        assert result.data.num_files >= 1