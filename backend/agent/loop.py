"""Agent 循环（负责人：组员 E）

流程：模型判断是否调用工具 → 执行工具 → 结果回填 → 模型生成答案（可多轮）。
对外只暴露 run_agent()，main.py 会把它产出的事件转成 SSE 推给前端。

产出的事件（与 docs/接口约定.md 一致；done 由 main.py 统一发送）：
    {"event": "tool_call", "data": {"name": ..., "args": {...}}}
    {"event": "citations", "data": [{"id", "doc_name", "page", "content"}, ...]}
    {"event": "token",     "data": {"delta": "..."}}

当前状态：基础单/多轮循环已能跑通（配合假数据），待组员 E 打磨提示词与异常处理。
"""
import json
from typing import Any, AsyncIterator

from backend import config
from backend.citation.builder import build_context
from backend.llm.client import stream_chat
from backend.retrieval.tool import TOOLS, execute_tool

# TODO 组员 E：打磨系统提示词
SYSTEM_PROMPT = (
    "你是企业知识库问答助手。回答问题前先调用 search_knowledge_base 检索资料，"
    "只依据检索到的片段作答，并在相应句子后用 [编号] 标注来源，如 [1]、[2]。"
    "如果资料中没有答案，请直接说明“知识库中未找到相关内容”，不要编造。"
)


async def run_agent(question: str, history: list[dict[str, Any]]) -> AsyncIterator[dict[str, Any]]:
    messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history
    messages.append({"role": "user", "content": question})

    for _ in range(config.MAX_TOOL_ROUNDS + 1):
        tool_calls = []
        async for item in stream_chat(messages, tools=TOOLS):
            if item["type"] == "token":
                yield {"event": "token", "data": {"delta": item["delta"]}}
            elif item["type"] == "tool_call":
                tool_calls.append(item)

        if not tool_calls:  # 模型没有再调用工具，说明答案已输出完毕
            return

        # 把模型的工具调用请求记入对话
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {"id": tc["id"], "type": "function",
                 "function": {"name": tc["name"], "arguments": json.dumps(tc["args"], ensure_ascii=False)}}
                for tc in tool_calls
            ],
        })

        for tc in tool_calls:
            yield {"event": "tool_call", "data": {"name": tc["name"], "args": tc["args"]}}
            chunks = execute_tool(tc["name"], tc["args"])
            context, citations = build_context(chunks)
            yield {"event": "citations", "data": citations}
            messages.append({"role": "tool", "tool_call_id": tc["id"], "content": context})

    yield {"event": "token", "data": {"delta": "（已达到最大工具调用轮数）"}}
