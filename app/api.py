from fastapi import APIRouter, HTTPException
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from app.agent import agent
from app.models import ChatRequest, ChatResponse, ToolCallRecord

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await agent.ainvoke({"messages": [HumanMessage(content=request.question)]})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    messages = result.get("messages", [])
    tool_calls_used = []
    evidence = []

    for msg in messages:
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                record = ToolCallRecord(
                    tool_name=tc["name"],
                    arguments=tc["args"],
                    raw_output=None,
                )
                tool_calls_used.append(record)
        elif isinstance(msg, ToolMessage):
            for tc in tool_calls_used:
                if tc.raw_output is None:
                    tc.raw_output = msg.content
                    break
            evidence.append(
                ToolCallRecord(
                    tool_name=msg.name or "",
                    arguments={},
                    raw_output=msg.content,
                )
            )

    last_message = messages[-1] if messages else None
    answer = last_message.content if last_message and hasattr(last_message, "content") else ""

    return ChatResponse(
        answer=answer,
        tool_calls_used=tool_calls_used,
        evidence=evidence,
    )
