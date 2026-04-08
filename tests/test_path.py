import os
import tempfile
from python_tools.utils.path import expand_path, normalize_path


def test_expand_path_expands_user_home():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        result = expand_path("~/test.txt")
        assert str(result).endswith("test.txt")


def test_expand_path_absolute():
    result = expand_path("/absolute/path.txt")
    assert str(result) == "/absolute/path.txt"


def test_expand_path_relative():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        result = expand_path("relative/path.txt")
        assert "relative/path.txt" in str(result)


def test_normalize_path():
    result = normalize_path("/foo/bar/../baz")
    assert str(result) == "/foo/baz"