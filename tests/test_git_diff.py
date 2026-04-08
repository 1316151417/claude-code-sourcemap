from python_tools.utils.git_diff import generate_patch, find_actual_string


def test_generate_patch_simple():
    result = generate_patch(
        file_path="/test.txt",
        old_content="hello world",
        new_content="hello python",
    )
    assert result["original"] == "hello world"
    assert result["updated"] == "hello python"


def test_find_actual_string_found():
    content = 'foo("hello")\nbar("world")\n'
    result = find_actual_string(content, '"hello"')
    assert result == '"hello"'


def test_find_actual_string_not_found():
    content = "hello world"
    result = find_actual_string(content, "not exist")
    assert result is None