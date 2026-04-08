"""GlobTool - Find files by glob pattern."""

import fnmatch
import os
import time
from pathlib import Path
from typing import Optional

from python_tools.base import Tool, ToolResult
from python_tools.types import GlobInput, GlobOutput
from python_tools.utils.path import expand_path


VCS_DIRECTORIES_TO_EXCLUDE = [".git", ".svn", ".hg", "node_modules", "__pycache__"]


class GlobTool(Tool[GlobInput, GlobOutput]):
    """Tool for finding files by glob pattern.

    Supports recursive patterns (**) and path filtering.
    """

    name = "Glob"
    description = "Find files matching a glob pattern."

    def call(self, input_data: GlobInput) -> ToolResult[GlobOutput]:
        """Search for files matching a glob pattern.

        Args:
            input_data: GlobInput with pattern and optional path

        Returns:
            ToolResult with matching filenames
        """
        start_time = time.time()

        search_path = expand_path(input_data.path) if input_data.path else os.getcwd()

        if not os.path.isdir(search_path):
            return ToolResult(
                success=False,
                error=f"Directory not found: {search_path}",
                data=GlobOutput(
                    duration_ms=0,
                    num_files=0,
                    filenames=[],
                    truncated=False,
                )
            )

        matches = list(self._glob_search(search_path, input_data.pattern))

        # Sort by modification time (newest first)
        matches.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)

        truncated = len(matches) > 100
        if truncated:
            matches = matches[:100]

        # Convert to relative paths
        filenames = [os.path.relpath(p, search_path) for p in matches]

        return ToolResult(
            success=True,
            data=GlobOutput(
                duration_ms=(time.time() - start_time) * 1000,
                num_files=len(filenames),
                filenames=filenames,
                truncated=truncated,
            )
        )

    def _glob_search(self, base_path: str, pattern: str) -> list[str]:
        """Perform glob search, excluding VCS directories.

        Args:
            base_path: Base directory to search
            pattern: Glob pattern

        Yields:
            Matching file paths
        """
        import glob

        # Normalize pattern
        if pattern.startswith("/"):
            pattern = pattern[1:]

        full_pattern = os.path.join(base_path, pattern)

        for match in glob.glob(full_pattern, recursive=True):
            # Check if any VCS directory is in the path
            path_parts = match.split(os.sep)
            if any(vcs in path_parts for vcs in VCS_DIRECTORIES_TO_EXCLUDE):
                continue

            if os.path.isfile(match):
                yield match