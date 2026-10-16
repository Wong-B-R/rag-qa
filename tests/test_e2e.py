"""端到端测试（负责人：项目经理）

先启动后端，再在项目根目录执行：
    python tests/test_e2e.py

对每个测试问题调用问答接口，检查：
1. 是否触发了检索工具（tool_call 事件）
2. 是否返回了引用（citations 事件且非空）
3. 是否有答案输出且以 done 正常结束、没有 error

当前状态：基础版可用；TODO 项目经理：改为读取 data/test_questions.json，输出汇总统计。
"""
import json
import sys

import httpx

BASE_URL = "http://localhost:8000"

QUESTIONS = ["三天以上的请假由谁审批？"]


def parse_sse(lines):
    """把 SSE 文本行解析成 (event, data) 序列。"""
    event, data = None, None
    for line in lines:
        if line.startswith("event:"):
            event = line[6:].strip()
        elif line.startswith("data:"):
            data = json.loads(line[5:].strip())
        elif line == "" and event:
            yield event, data
            event, data = None, None


def run_one(question: str) -> dict:
    result = {"tool_call": False, "citations": 0, "answer": "", "done": False, "error": None}
    with httpx.stream("POST", f"{BASE_URL}/api/chat/stream",
                      json={"question": question, "history": []}, timeout=60) as r:
        for event, data in parse_sse(r.iter_lines()):
            if event == "tool_call":
                result["tool_call"] = True
            elif event == "citations":
                result["citations"] = len(data)
            elif event == "token":
                result["answer"] += data["delta"]
            elif event == "error":
                result["error"] = data["message"]
            elif event == "done":
                result["done"] = True
    return result


def main():
    passed = 0
    for q in QUESTIONS:
        r = run_one(q)
        ok = r["tool_call"] and r["citations"] > 0 and r["answer"] and r["done"] and not r["error"]
        passed += ok
        print(f"[{'通过' if ok else '失败'}] {q}")
        print(f"  检索：{r['tool_call']}  引用数：{r['citations']}  错误：{r['error']}")
        print(f"  答案：{r['answer'][:80]}")
    print(f"\n共 {len(QUESTIONS)} 题，通过 {passed} 题")
    sys.exit(0 if passed == len(QUESTIONS) else 1)


if __name__ == "__main__":
    main()
