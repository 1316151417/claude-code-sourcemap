"""Base classes for Claude Code Tools."""

from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


class ToolInput(BaseModel, Generic[InputT]):
    """Base class for tool inputs."""

    pass


class ToolResult(BaseModel, Generic[OutputT]):
    """Base class for tool results."""

    success: bool = True
    error: Optional[str] = None
    data: Optional[OutputT] = None


class Tool(ABC, Generic[InputT, OutputT]):
    """Abstract base class for all tools."""

    name: str
    description: str = ""

    @abstractmethod
    async def call(self, input_data: InputT) -> ToolResult[OutputT]:
        """Execute the tool with the given input."""
        pass

    def input_schema(self) -> type[BaseModel]:
        """Return the input schema for this tool."""
        return self.__class__.__orig_bases__[0].__args__[0]  # type: ignore

    def output_schema(self) -> type[BaseModel]:
        """Return the output schema for this tool."""
        return self.__class__.__orig_bases__[0].__args__[1]  # type: ignore
