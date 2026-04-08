import os
import tempfile
import pytest
import shutil
from python_tools.tools.grep import GrepTool
from python_tools.types import GrepInput


def _ripgrep_available():
    """Check if ripgrep is available."""
    return shutil.which("rg") is not None


pytestmark = pytest.mark.skipif(
    not _ripgrep_available(),
    reason="ripgrep (rg) is not installed"
)


def test_grep_files_with_matches():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "match.txt"), "w") as f:
            f.write("hello world\n")
        with open(os.path.join(tmpdir, "nomatch.txt"), "w") as f:
            f.write("foo bar\n")

        tool = GrepTool()
        result = tool.call(GrepInput(pattern="hello", path=tmpdir))

        assert result.success is True
        assert result.data.mode == "files_with_matches"
        assert "match.txt" in result.data.filenames
        assert "nomatch.txt" not in result.data.filenames


def test_grep_content_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test.txt"), "w") as f:
            f.write("line1: hello\nline2: world\nline3: hello again\n")

        tool = GrepTool()
        result = tool.call(GrepInput(
            pattern="hello",
            path=tmpdir,
            output_mode="content",
        ))

        assert result.success is True
        assert result.data.mode == "content"
        assert result.data.content is not None
        assert "line1" in result.data.content


def test_grep_no_matches():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test.txt"), "w") as f:
            f.write("foo bar\n")

        tool = GrepTool()
        result = tool.call(GrepInput(pattern="nonexistent", path=tmpdir))

        assert result.success is True
        assert result.data.num_files == 0
        assert len(result.data.filenames) == 0


def test_grep_case_insensitive():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test.txt"), "w") as f:
            f.write("Hello World\nhello world\n")

        tool = GrepTool()
        result = tool.call(GrepInput(
            pattern="hello",
            path=tmpdir,
            case_insensitive=True,
        ))

        assert result.success is True
        assert result.data.num_files == 1


def test_grep_count_mode():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test.txt"), "w") as f:
            f.write("hello\nhello\nhello\n")

        tool = GrepTool()
        result = tool.call(GrepInput(
            pattern="hello",
            path=tmpdir,
            output_mode="count",
        ))

        assert result.success is True
        assert result.data.mode == "count"
        assert result.data.num_matches >= 3