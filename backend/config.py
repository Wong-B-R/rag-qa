"""全局配置（负责人：项目经理）

从项目根目录的 .env 读取配置。.env 不进仓库，每人复制 .env.example 后自行填写。
"""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

# 大模型（兼容 OpenAI 格式的接口，如 DeepSeek、通义千问）
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# 为 true 时整条链路使用假数据，不调用真实模型（未填 Key 时也能开发调试）
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "true").lower() == "true"

# 知识库文本块文件（组员 C 产出）
CHUNKS_PATH = ROOT_DIR / os.getenv("CHUNKS_PATH", "data/chunks.json")

# 前端开发服务器地址，用于 CORS
FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS", "http://localhost:5173,http://localhost:3000"
).split(",")

# Agent 最多调用工具的轮数，防止死循环
MAX_TOOL_ROUNDS = int(os.getenv("MAX_TOOL_ROUNDS", "3"))
