"""FileEditTool - Edit files with old_string -> new_string replacement."""

import os
from pathlib import Path
from typing import Optional

from python_tools.base import Tool, ToolResult
from python_tools.types import EditInput, EditOutput
from python_tools.utils.file_ops import write_text, get_line_endings
from python_tools.utils.git_diff import find_actual_string, generate_patch
from python_tools.utils.path import expand_path


class FileEditTool(Tool[EditInput, EditOutput]):
    """Tool for editing files.

    Replaces old_string with new_string in the specified file.
    Supports replace_all for multiple replacements.
    """

    name = "Edit"
    description = "Edit a file by replacing old_string with new_string."

    def call(self, input_data: EditInput) -> ToolResult[EditOutput]:
        """Edit a file.

        Args:
            input_data: EditInput with file_path, old_string, new_string, replace_all

        Returns:
            ToolResult with edit details
        """
        file_path = expand_path(input_data.file_path)

        # Check file exists
        if not os.path.exists(file_path):
            return ToolResult(
                success=False,
                error=f"File not found: {file_path}",
                data=EditOutput(
                    file_path=str(file_path),
                    old_string=input_data.old_string,
                    new_string=input_data.new_string,
                    original_file=None,
                    user_modified=False,
                    replace_all=input_data.replace_all,
                )
            )

        try:
            # Read current content
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                original_content = f.read()

            original_file = original_content

            # Find actual string (handle quote normalization)
            actual_old_string = find_actual_string(original_content, input_data.old_string)

            if actual_old_string is None:
                # String not found
                return ToolResult(
                    success=False,
                    error=f"String not found: {input_data.old_string}",
                    data=EditOutput(
                        file_path=str(file_path),
                        old_string=input_data.old_string,
                        new_string=input_data.new_string,
                        original_file=original_content,
                        user_modified=False,
                        replace_all=input_data.replace_all,
                    )
                )

            # Perform replacement
            if input_data.replace_all:
                new_content = original_content.replace(
                    actual_old_string,
                    input_data.new_string,
                )
            else:
                new_content = original_content.replace(
                    actual_old_string,
                    input_data.new_string,
                    1,
                )

            # Get line endings to preserve
            line_endings = get_line_endings(file_path)

            # Write back
            write_text(file_path, new_content, line_endings=line_endings)

            return ToolResult(
                success=True,
                data=EditOutput(
                    file_path=str(file_path),
                    old_string=actual_old_string,
                    new_string=input_data.new_string,
                    original_file=original_file,
                    user_modified=True,
                    replace_all=input_data.replace_all,
                )
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                data=EditOutput(
                    file_path=str(file_path),
                    old_string=input_data.old_string,
                    new_string=input_data.new_string,
                    original_file=None,
                    user_modified=False,
                    replace_all=input_data.replace_all,
                )
            )