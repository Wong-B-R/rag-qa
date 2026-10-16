#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ ! -f .env ]; then
  cp .env.example .env
  echo "已从 .env.example 生成 .env，需要真实模型时请编辑其中的 LLM_API_KEY"
fi
python3 -m uvicorn backend.main:app --reload --port 8000
