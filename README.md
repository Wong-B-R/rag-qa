# RAG 知识库问答平台

岗位实践课程小组项目。第一阶段目标：跑通“提问 → 检索（朴素） → 生成”的最小问答闭环。

## 一、快速开始

需要 Python 3.9 及以上。

```bash
git clone <仓库地址>
cd rag-qa
pip install -r requirements.txt
```

一键测试：Windows 双击 `run_e2e.bat`（自动启动后端并跑测试）。

只启动后端：Windows 双击 `start.bat`，macOS / Linux 执行 `./start.sh`。

首次启动会自动生成 `.env`，默认是**假数据模式**（`USE_MOCK_LLM=true`），不需要 API Key 也能跑通全流程。

验证是否跑通（另开一个终端）：

```bash
python tests/test_e2e.py
```

看到“通过 1 题”即说明链路正常。也可以浏览器打开 http://localhost:8000/docs 查看接口。

接入真实模型：编辑 `.env`，填写 `LLM_API_KEY`，把 `USE_MOCK_LLM` 改为 `false`，重启后端。

## 二、目录与分工

```
rag-qa/
├── frontend/            组员 A   问答页（VibeCoding 生成）
├── backend/
│   ├── main.py          项目经理 主程序、路由
│   ├── config.py        项目经理 配置
│   ├── llm/             组员 B   大模型调用、流式输出
│   ├── retrieval/       组员 D   检索函数、Function Calling 工具定义
│   ├── agent/           组员 E   Agent 循环、系统提示词
│   └── citation/        项目经理 引用处理
├── data/                组员 C   原始文档、切块脚本、chunks.json、测试问题集
├── tests/               项目经理 端到端测试
└── docs/接口约定.md      项目经理 接口约定（所有人必读）
```

每个模块都已放好**占位实现**：签名按接口约定写好，内部先用假数据或简单逻辑，整条链路现在就能跑。各人只需把自己负责的文件里标了 `TODO` 的部分替换成真实实现，**不要改函数签名和返回格式**。

## 三、协作规则

1. **只改自己目录下的文件。** 要改别人的代码，先在群里说。
2. `main.py`、`config.py`、`requirements.txt`、`docs/接口约定.md` 是公共文件，只由项目经理修改。需要新依赖，在 PR 里写明，由项目经理加入。
3. **API Key 不进仓库。** 只写在自己本地的 `.env` 里。
4. 接口约定有疑问或需要修改，先在群里提，不要自己改。

## 四、Git 工作流

`main` 分支只放能跑通的代码，**任何人不得直接推送**，一律通过 Pull Request 合并。

| 负责人 | 分支名 |
|---|---|
| 组员 A | `feat/frontend` |
| 组员 B | `feat/llm` |
| 组员 C | `feat/data` |
| 组员 D | `feat/retrieval` |
| 组员 E | `feat/agent` |
| 项目经理 | `feat/core` |

**第一次：**

```bash
git clone <仓库地址>
cd rag-qa
git checkout -b feat/llm        # 换成自己的分支名
```

**每次开工前，先同步 main：**

```bash
git checkout feat/llm
git pull origin main
```

**做完一部分就提交：**

```bash
git add .
git commit -m "llm: 实现真实模型流式调用"
git push origin feat/llm
```

然后在仓库网页上发起 Pull Request，目标分支选 `main`，等项目经理审核合并。

**提交信息格式：** `模块: 做了什么`，如 `retrieval: 改用 BM25`、`frontend: 增加引用卡片`。

**提交 PR 前自查：** 本地启动后端，运行 `python tests/test_e2e.py` 通过。

不熟悉命令行的同学，可以用 VS Code 左侧的“源代码管理”面板完成提交和推送。
