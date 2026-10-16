@echo off
chcp 65001 >nul
cd /d %~dp0
if not exist .env (
    copy .env.example .env >nul
    echo 已从 .env.example 生成 .env，需要真实模型时请编辑其中的 LLM_API_KEY
)
python -m uvicorn backend.main:app --reload --port 8000
