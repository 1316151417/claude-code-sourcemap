import os
import tempfile
import pytest
from python_tools.utils.subprocess import run_ripgrep, _check_ripgrep_available


def test_run_ripgrep_files_with_matches():
    if not _check_ripgrep_available():
        pytest.skip("ripgrep (rg) is not installed")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("hello world\n")
        with open(os.path.join(tmpdir, "file2.txt"), "w") as f:
            f.write("foo bar\n")

        result = run_ripgrep(
            pattern="hello",
            path=tmpdir,
            output_mode="files_with_matches",
        )
        assert "file1.txt" in result.filenames
        assert "file2.txt" not in result.filenames


def test_run_ripgrep_content():
    if not _check_ripgrep_available():
        pytest.skip("ripgrep (rg) is not installed")

    with tempfile.TemporaryDirectory() as tmpdir:
        with open(os.path.join(tmpdir, "test.txt"), "w") as f:
            f.write("line1: hello\nline2: world\n")

        result = run_ripgrep(
            pattern="hello",
            path=tmpdir,
            output_mode="content",
        )
        assert "line1: hello" in result.content