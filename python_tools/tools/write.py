"""FileWriteTool - Write files with full content replacement."""

import os
from pathlib import Path

from python_tools.base import Tool, ToolResult
from python_tools.types import WriteInput, WriteOutput
from python_tools.utils.file_ops import write_text
from python_tools.utils.path import expand_path


class FileWriteTool(Tool[WriteInput, WriteOutput]):
    """Tool for writing files.

    Creates new files or overwrites existing files with full content replacement.
    """

    name = "Write"
    description = "Write content to a file (creates new or overwrites existing)."

    def call(self, input_data: WriteInput) -> ToolResult[WriteOutput]:
        """Write to a file.

        Args:
            input_data: WriteInput with file_path and content

        Returns:
            ToolResult with write details
        """
        file_path = expand_path(input_data.file_path)

        # Check if file exists
        original_file = None
        file_existed = os.path.exists(file_path)

        if file_existed:
            # Read original content for patch
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    original_file = f.read()
            except Exception:
                original_file = None

        # Ensure parent directory exists
        parent = os.path.dirname(file_path)
        if parent:
            os.makedirs(parent, exist_ok=True)

        # Write content
        write_text(file_path, input_data.content)

        return ToolResult(
            success=True,
            data=WriteOutput(
                type="create" if not file_existed else "update",
                file_path=str(file_path),
                content=input_data.content,
                original_file=original_file,
            )
        )
