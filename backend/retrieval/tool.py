"""Function Calling 工具定义与执行（负责人：组员 D）

TOOLS 是传给大模型的工具列表（OpenAI 格式）；execute_tool 根据模型给出的
工具名和参数执行对应函数。新增工具时两处一起加。
"""
from typing import Any

from backend.retrieval.search import search_knowledge_base

TOOLS: list[dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            # TODO 组员 D：打磨描述，描述写得好坏直接影响模型是否会调用工具
            "description": "在企业知识库中检索与问题相关的文档片段。回答任何与知识库内容有关的问题前都应先调用此工具。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "检索用的问题或关键词"},
                    "top_k": {"type": "integer", "description": "返回片段数量，默认 5", "default": 5},
                },
                "required": ["query"],
            },
        },
    }
]

_REGISTRY = {"search_knowledge_base": search_knowledge_base}


def execute_tool(name: str, args: dict[str, Any]) -> Any:
    """执行工具。未知工具名抛出 ValueError。"""
    if name not in _REGISTRY:
        raise ValueError(f"未知工具：{name}")
    return _REGISTRY[name](**args)
