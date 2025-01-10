from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel


class CompletionUsage(BaseModel):
    """Usage statistics for the completion request."""
    completion_tokens: int
    """Number of tokens in the generated completion."""

    prompt_tokens: int
    """Number of tokens in the prompt."""

    total_tokens: int
    """Total number of tokens used in the request (prompt + completion)."""


class ToolCallFunction(BaseModel):
    arguments: Optional[str] = None
    """
    The arguments to call the function with, as generated by the model in JSON
    format. Note that the model does not always generate valid JSON, and may
    hallucinate parameters not defined by your function schema. Validate the
    arguments in your code before calling your function.
    """

    name: Optional[str] = None
    """The name of the function to call."""


class ToolCall(BaseModel):
    index: int

    id: Optional[str] = None
    """The ID of the tool call."""

    function: Optional[ToolCallFunction] = None

    type: Optional[Literal["function"]] = None
    """The type of the tool. Currently, only `function` is supported."""


class Completion(BaseModel):
    """Completion response from an LLM"""
    id: str
    """A unique identifier for the completion."""

    created: int
    """The Unix timestamp (in seconds) of when the completion was created."""

    model: str
    """The model used for completion."""

    usage: Optional[CompletionUsage] = None
    """Usage statistics for the completion request."""

    finish_reason: Optional[Literal["stop", "length", "tool_calls", "content_filter"]] = None
    """The reason the model stopped generating tokens.

    This will be `stop` if the model hit a natural stop point or a provided stop
    sequence, `length` if the maximum number of tokens specified in the request was
    reached, `content_filter` if content was omitted due to a flag from our content
    filters, `tool_calls` if the model called a tool.
    """

    content: Optional[str] = None
    """The generated text."""

    role: Optional[Literal["system", "user", "assistant", "tool"]] = None
    """The role of the author of this message."""

    tool_calls: Optional[List[ToolCall]] = None
    """The tool calls made by the model."""

    raw_response: Optional[Dict[str, Any]] = None
    """The raw response from the model."""