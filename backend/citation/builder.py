"""引用处理（负责人：项目经理）

职责：
1. 给检索到的文本块编号 [1][2]…，拼成交给模型的上下文
2. 产出发给前端的 citations 事件数据
3. （TODO）从最终答案中解析实际用到的编号，只保留被引用的来源

当前状态：基础版可用，第 3 项待实现。
"""
from typing import Any


def build_context(chunks: list[dict[str, Any]]) -> tuple[str, list[dict[str, Any]]]:
    """把文本块编号并拼成上下文。

    返回：(给模型看的上下文文本, citations 列表)
    citations 每项为 {"id": int, "doc_name": str, "page": int, "content": str}
    """
    citations = []
    parts = []
    for i, c in enumerate(chunks, start=1):
        citations.append(
            {"id": i, "doc_name": c["doc_name"], "page": c["page"], "content": c["content"]}
        )
        parts.append(f"[{i}] 《{c['doc_name']}》第 {c['page']} 页：{c['content']}")
    return "\n\n".join(parts), citations


def filter_used(answer: str, citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """只保留答案中实际出现过的引用编号。TODO 项目经理：实现。"""
    return citations
