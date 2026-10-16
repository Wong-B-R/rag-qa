"""后端主程序（负责人：项目经理）

启动：在项目根目录执行
    uvicorn backend.main:app --reload --port 8000

各组员的模块都挂在这里，除项目经理外请勿修改本文件；需要新路由请在群里提。
"""
import json
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend import config
from backend.agent.loop import run_agent

app = FastAPI(title="RAG 知识库问答平台", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.FRONTEND_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str
    history: list[dict[str, Any]] = []


def to_sse(event: str, data: Any) -> str:
    """把一个事件编码成 SSE 文本格式。"""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/api/health")
def health():
    return {"status": "ok", "mock_llm": config.USE_MOCK_LLM}


@app.post("/api/chat/stream")
async def chat_stream(req: ChatRequest):
    """流式问答接口，事件格式见 docs/接口约定.md。"""

    async def event_generator():
        try:
            async for ev in run_agent(req.question, req.history):
                yield to_sse(ev["event"], ev["data"])
        except Exception as e:  # 任何异常都转成 error 事件，前端不会卡住
            yield to_sse("error", {"message": str(e)})
        yield to_sse("done", {})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
