"""Tool registry for Claude Code Tools."""

from typing import Optional
from python_tools.base import Tool
from python_tools.tools import (
    FileReadTool,
    FileEditTool,
    FileWriteTool,
    GlobTool,
    GrepTool,
)


class ToolRegistry:
    """Registry of available tools."""

    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register the default set of tools."""
        self.register(FileReadTool())
        self.register(FileEditTool())
        self.register(FileWriteTool())
        self.register(GlobTool())
        self.register(GrepTool())

    def register(self, tool: Tool) -> None:
        """Register a tool.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        """List all registered tool names.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def get_all(self) -> dict[str, Tool]:
        """Get all registered tools.

        Returns:
            Dictionary of tool name to tool instance
        """
        return self._tools.copy()


# Global registry instance
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Get the global tool registry.

    Returns:
        Global ToolRegistry instance
    """
    return _registry