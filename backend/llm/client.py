"""大模型调用层（负责人：组员 B）

对外只暴露 stream_chat()，组员 E 的 Agent 循环会调用它。
函数签名和产出的事件格式不要改；只替换内部实现。

当前状态：USE_MOCK_LLM=true 时返回假数据；真实调用部分已给出骨架，待组员 B 完善。
"""
import asyncio
import json
from typing import Any, AsyncIterator

from backend import config


async def stream_chat(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
) -> AsyncIterator[dict[str, Any]]:
    """流式调用大模型。

    参数：
        messages: OpenAI 格式的消息列表
        tools:    OpenAI 格式的工具定义列表（可为 None）

    逐个产出以下两种字典之一：
        {"type": "token", "delta": "文字片段"}
        {"type": "tool_call", "id": "调用ID", "name": "工具名", "args": {...}}
    """
    if config.USE_MOCK_LLM:
        async for item in _mock_stream(messages, tools):
            yield item
        return

    # ---------- 真实调用（TODO 组员 B：完善、加超时与重试） ----------
    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=config.LLM_API_KEY, base_url=config.LLM_BASE_URL)
    stream = await client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=messages,
        tools=tools or None,
        stream=True,
    )

    # 流式返回时，工具调用的参数是分片到达的，需要按 index 拼接
    pending: dict[int, dict[str, Any]] = {}
    async for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        if delta.content:
            yield {"type": "token", "delta": delta.content}
        for tc in delta.tool_calls or []:
            slot = pending.setdefault(tc.index, {"id": "", "name": "", "args": ""})
            if tc.id:
                slot["id"] = tc.id
            if tc.function and tc.function.name:
                slot["name"] = tc.function.name
            if tc.function and tc.function.arguments:
                slot["args"] += tc.function.arguments

    for slot in pending.values():
        yield {
            "type": "tool_call",
            "id": slot["id"],
            "name": slot["name"],
            "args": json.loads(slot["args"] or "{}"),
        }


async def _mock_stream(messages, tools):
    """假数据：第一轮请求检索工具，拿到工具结果后逐字输出一段带引用的答案。"""
    has_tool_result = any(m.get("role") == "tool" for m in messages)
    if tools and not has_tool_result:
        question = next(m["content"] for m in reversed(messages) if m["role"] == "user")
        yield {
            "type": "tool_call",
            "id": "mock_call_1",
            "name": "search_knowledge_base",
            "args": {"query": question, "top_k": 3},
        }
        return

    answer = "这是一段假答案，用于联调。根据知识库，示例制度规定了请假流程[1]，并说明了审批时限[2]。"
    for ch in answer:
        await asyncio.sleep(0.02)
        yield {"type": "token", "delta": ch}
