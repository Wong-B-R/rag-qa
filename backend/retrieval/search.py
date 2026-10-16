"""知识库检索（负责人：组员 D）

本阶段为朴素检索（关键词匹配或 BM25）。下一阶段会换成向量检索，
届时只替换函数内部实现，search_knowledge_base 的签名和返回格式保持不变。

当前状态：占位实现——简单关键词计数打分，能跑但效果很差，待组员 D 替换。
"""
import json
from functools import lru_cache
from typing import Any

from backend import config


@lru_cache(maxsize=1)
def load_chunks() -> list[dict[str, Any]]:
    """读取组员 C 产出的文本块文件。"""
    with open(config.CHUNKS_PATH, encoding="utf-8") as f:
        return json.load(f)


def search_knowledge_base(query: str, top_k: int = 5) -> list[dict[str, Any]]:
    """检索与问题最相关的文本块。

    返回：按 score 从高到低排序的列表，每项为
        {"chunk_id": str, "doc_name": str, "page": int, "content": str, "score": float}
    """
    # TODO 组员 D：换成 BM25（推荐 rank_bm25 + jieba 分词）
    chunks = load_chunks()
    scored = []
    for c in chunks:
        score = float(sum(1 for ch in set(query) if ch in c["content"]))
        scored.append({**c, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
