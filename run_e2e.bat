@echo off
chcp 65001 >nul
cd /d %~dp0
echo [1/3] 检查依赖...
python -m pip install -q -r requirements.txt
if not exist .env copy .env.example .env >nul
echo [2/3] 在新窗口启动后端...
start "RAG 后端" cmd /k python -m uvicorn backend.main:app --port 8000
timeout /t 6 /nobreak >nul
echo [3/3] 运行端到端测试...
echo.
python tests/test_e2e.py
echo.
echo 测试结束。后端窗口可直接关闭。
pause
