"""Tool implementations for Claude Code Tools."""

from python_tools.base import Tool


class FileReadTool(Tool):
    """Tool for reading files."""
    name = "Read"
    description = "Read the contents of a file"


class FileEditTool(Tool):
    """Tool for editing files."""
    name = "Edit"
    description = "Edit the contents of a file"


class FileWriteTool(Tool):
    """Tool for writing files."""
    name = "Write"
    description = "Write content to a file"


class GlobTool(Tool):
    """Tool for glob pattern matching."""
    name = "Glob"
    description = "Find files matching a glob pattern"


class GrepTool(Tool):
    """Tool for searching file contents."""
    name = "Grep"
    description = "Search for patterns in files"
