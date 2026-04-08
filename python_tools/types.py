"""Type definitions for Claude Code Tools."""

from typing import Any, Literal, Optional
from pydantic import BaseModel, Field


class ReadInput(BaseModel):
    """Input schema for FileReadTool."""

    file_path: str = Field(description="The absolute path to the file to read")
    offset: Optional[int] = Field(default=1, description="Line number to start reading from (1-indexed)")
    limit: Optional[int] = Field(default=None, description="Number of lines to read")
    pages: Optional[str] = Field(default=None, description="Page range for PDF files (e.g., '1-5')")


class ReadOutput(BaseModel):
    """Output schema for FileReadTool."""

    type: Literal["text", "image", "notebook", "pdf", "file_unchanged"]
    file_path: str
    content: Optional[str] = None
    num_lines: Optional[int] = None
    start_line: Optional[int] = None
    total_lines: Optional[int] = None
    base64: Optional[str] = None


class EditInput(BaseModel):
    """Input schema for FileEditTool."""

    file_path: str = Field(description="The absolute path to the file to edit")
    old_string: str = Field(description="The exact string to find and replace")
    new_string: str = Field(description="The replacement string")
    replace_all: bool = Field(default=False, description="Replace all occurrences")


class EditOutput(BaseModel):
    """Output schema for FileEditTool."""

    file_path: str
    old_string: str
    new_string: str
    original_file: Optional[str] = None
    user_modified: bool = False
    replace_all: bool = False


class WriteInput(BaseModel):
    """Input schema for FileWriteTool."""

    file_path: str = Field(description="The absolute path to the file to write")
    content: str = Field(description="The content to write to the file")


class WriteOutput(BaseModel):
    """Output schema for FileWriteTool."""

    type: Literal["create", "update"]
    file_path: str
    content: str
    original_file: Optional[str] = None


class GlobInput(BaseModel):
    """Input schema for GlobTool."""

    pattern: str = Field(description="The glob pattern to match files against")
    path: Optional[str] = Field(default=None, description="The directory to search in")


class GlobOutput(BaseModel):
    """Output schema for GlobTool."""

    duration_ms: float
    num_files: int
    filenames: list[str]
    truncated: bool = False


class GrepInput(BaseModel):
    """Input schema for GrepTool."""

    pattern: str = Field(description="The regular expression pattern to search for")
    path: Optional[str] = Field(default=None, description="File or directory to search in")
    glob: Optional[str] = Field(default=None, description="Glob pattern to filter files (e.g., '*.js')")
    output_mode: Literal["content", "files_with_matches", "count"] = Field(default="files_with_matches")
    context: Optional[int] = Field(default=None, description="Lines of context around match")
    multiline: bool = Field(default=False, description="Enable multiline mode")
    case_insensitive: bool = Field(default=False, description="Case insensitive search")
    show_line_numbers: bool = Field(default=True, description="Show line numbers")
    head_limit: Optional[int] = Field(default=None, description="Maximum number of results")


class GrepOutput(BaseModel):
    """Output schema for GrepTool."""

    mode: Literal["content", "files_with_matches", "count"]
    num_files: Optional[int] = None
    filenames: Optional[list[str]] = None
    content: Optional[str] = None
    num_lines: Optional[int] = None
    num_matches: Optional[int] = None
