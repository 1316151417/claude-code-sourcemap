"""FileReadTool - Read files with offset/limit support."""

import base64
import json
import os
from pathlib import Path
from typing import Optional

from python_tools.base import Tool, ToolResult
from python_tools.types import ReadInput, ReadOutput
from python_tools.utils.file_ops import read_file_range
from python_tools.utils.path import expand_path


class FileReadTool(Tool[ReadInput, ReadOutput]):
    """Tool for reading files.

    Supports:
    - Full file reading
    - Offset/limit for partial reads
    - Text, image (base64), notebook, PDF detection
    """

    name = "Read"
    description = "Read the contents of a file from the filesystem."

    def call(self, input_data: ReadInput) -> ToolResult[ReadOutput]:
        """Read a file.

        Args:
            input_data: ReadInput with file_path, offset, limit, pages

        Returns:
            ToolResult with file content and metadata
        """
        try:
            file_path = expand_path(input_data.file_path)

            # Check file exists
            if not os.path.exists(file_path):
                return ToolResult(
                    success=False,
                    error=f"File not found: {file_path}",
                    data=ReadOutput(
                        type="file_unchanged",
                        file_path=str(file_path),
                    )
                )

            # Determine file type
            ext = os.path.splitext(file_path)[1].lower()

            # Handle images
            if ext in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
                return ToolResult(
                    success=True,
                    data=self._read_image(file_path)
                )

            # Handle PDF
            if ext == ".pdf":
                return ToolResult(
                    success=True,
                    data=self._read_pdf(file_path, input_data.pages)
                )

            # Handle notebooks
            if ext == ".ipynb":
                return ToolResult(
                    success=True,
                    data=self._read_notebook(file_path)
                )

            # Handle text files
            return ToolResult(
                success=True,
                data=self._read_text(file_path, input_data.offset, input_data.limit)
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                data=ReadOutput(
                    type="file_unchanged",
                    file_path=str(input_data.file_path),
                )
            )

    def _read_text(
        self,
        file_path: Path,
        offset: Optional[int] = 1,
        limit: Optional[int] = None,
    ) -> ReadOutput:
        """Read a text file."""
        result = read_file_range(str(file_path), offset=offset, limit=limit)

        return ReadOutput(
            type="text",
            file_path=str(file_path),
            content=result.content,
            num_lines=result.num_lines,
            start_line=result.start_line,
            total_lines=result.total_lines,
        )

    def _read_image(self, file_path: Path) -> ReadOutput:
        """Read an image file as base64."""
        with open(file_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")

        return ReadOutput(
            type="image",
            file_path=str(file_path),
            base64=data,
        )

    def _read_pdf(self, file_path: Path, pages: Optional[str] = None) -> ReadOutput:
        """Read a PDF file (basic support)."""
        return ReadOutput(
            type="pdf",
            file_path=str(file_path),
            content=f"PDF file (pages: {pages or 'all'})",
        )

    def _read_notebook(self, file_path: Path) -> ReadOutput:
        """Read a Jupyter notebook."""
        with open(file_path, "r", encoding="utf-8") as f:
            notebook = json.load(f)

        return ReadOutput(
            type="notebook",
            file_path=str(file_path),
            content=json.dumps(notebook, indent=2),
        )