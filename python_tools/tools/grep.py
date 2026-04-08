"""GrepTool - Search file contents with regex."""

import os
import time
from typing import Optional

from python_tools.base import Tool, ToolResult
from python_tools.types import GrepInput, GrepOutput
from python_tools.utils.path import expand_path
from python_tools.utils.subprocess import run_ripgrep


class GrepTool(Tool[GrepInput, GrepOutput]):
    """Tool for searching file contents with regex.

    Supports:
    - files_with_matches (default)
    - content (with line numbers)
    - count (matches per file)
    - Case insensitive, multiline, context
    """

    name = "Grep"
    description = "Search file contents using regular expressions."

    def call(self, input_data: GrepInput) -> ToolResult[GrepOutput]:
        """Search for a pattern in files.

        Args:
            input_data: GrepInput with pattern, path, options

        Returns:
            ToolResult with search results
        """
        start_time = time.time()

        search_path = expand_path(input_data.path) if input_data.path else os.getcwd()

        try:
            result = run_ripgrep(
                pattern=input_data.pattern,
                path=str(search_path),
                output_mode=input_data.output_mode,
                glob=input_data.glob,
                case_insensitive=input_data.case_insensitive,
                show_line_numbers=input_data.show_line_numbers,
                context=input_data.context,
                head_limit=input_data.head_limit,
                multiline=input_data.multiline,
            )

            return ToolResult(
                success=True,
                data=GrepOutput(
                    mode=result.mode,
                    num_files=result.num_files,
                    filenames=result.filenames,
                    content=result.content,
                    num_matches=result.num_matches,
                    num_lines=len(result.content.split("\n")) if result.content else 0,
                ),
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=str(e),
                data=GrepOutput(
                    mode=input_data.output_mode,
                    num_files=0,
                    filenames=[],
                ),
            )