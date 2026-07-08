from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ToolCallRecord(BaseModel):
    tool_name: str
    arguments: dict
    raw_output: object


class ChatResponse(BaseModel):
    answer: str
    tool_calls_used: list[ToolCallRecord]
