# SuperPersonalAgent（博查 + LangGraph Agent）

基于 **LangGraph** 的简单对话 Agent：调用 **阿里云 DashScope 兼容接口**（默认 `qwen-plus`）进行推理，并通过 **博查（Bocha）Web Search API** 检索网络信息。

## 功能概览

- 使用 LangGraph 编排 **LLM 节点**与**工具执行节点**（带条件边：有 `tool_calls` 则执行工具，否则结束）。
- 自定义消息归约 `reduce_messages`：同 `id` 替换，否则追加（见 `bocha_agent/state.py`）。
- 密钥与端点通过环境变量 / 项目根目录 `.env` 配置，避免写入代码仓库。

## 技术栈

| 类别 | 依赖 |
|------|------|
| 编排 | LangGraph、LangChain Core |
| 模型 | LangChain OpenAI（兼容 DashScope OpenAI 接口） |
| 工具 | 博查 HTTP API、`requests` |
| 配置 | `python-dotenv` |

完整列表见 [`requirements.txt`](requirements.txt)。

## 目录结构

```text
.
├── main.py                 # 推荐入口
├── BoCha.py                # 兼容入口，同上
├── bocha_agent/
│   ├── config.py           # 环境变量与默认值
│   ├── schemas.py          # Pydantic 工具入参
│   ├── state.py            # AgentState、reduce_messages
│   ├── agent.py            # LangGraph Agent
│   ├── factory.py          # create_default_agent()
│   ├── entrypoint.py       # 演示：打印图 + invoke
│   └── tools/
│       └── bocha_search.py # 博查搜索 Tool
├── scripts/
│   └── run_with_langgraph.ps1  # Windows：conda run langgraph 环境执行 main
├── .env.example            # 环境变量模板（复制为 .env）
└── requirements.txt
```

## 环境要求

- Python 3.10+（建议与本地 LangGraph 开发环境一致）
- 博查 API Key、[DashScope](https://help.aliyun.com/zh/model-studio/) API Key（或兼容的 OpenAI 风格 Key，视 `OPENAI_API_KEY` 用途而定）

## 快速开始

### 1. 克隆与依赖

```bash
cd SuperPersonalAgent
pip install -r requirements.txt
```

使用 Conda 时（示例环境名 `langgraph`）：

```bash
conda activate langgraph
pip install -r requirements.txt
```

### 2. 配置密钥

复制模板并编辑：

```bash
copy .env.example .env
```

在 `.env` 中填写（**勿将真实 `.env` 提交到 Git**）：

| 变量 | 说明 |
|------|------|
| `BOCHA_API_KEY` | 博查 API |
| `DASHSCOPE_API_KEY` | 通义 / DashScope（与代码中默认 `openai_api_base` 一致） |

也可使用 `OPENAI_API_KEY` 代替 `DASHSCOPE_API_KEY`（二选一，见 `config.py`）。

### 3. 运行

在项目根目录执行任一方式：

```bash
python main.py
```

```bash
python BoCha.py
```

```bash
python -m bocha_agent
```

Windows 下若已安装 Conda 环境 `langgraph`：

```powershell
.\scripts\run_with_langgraph.ps1
```

默认会打印 LangGraph ASCII 示意图，并执行 `entrypoint.py` 中的示例用户问题，最后输出模型最后一条回复。

## 可选环境变量

可在 `.env` 中覆盖（详见 `.env.example`）：

- `DASHSCOPE_BASE_URL`：默认 `https://dashscope.aliyuncs.com/compatible-mode/v1`
- `LLM_MODEL`：默认 `qwen-plus`
- `BOCHA_SEARCH_COUNT`：博查返回条数相关默认
- `BOCHA_WEB_SEARCH_URL`：博查接口 URL（一般无需改）

## 安全说明

- 仓库中仅保留 **`.env.example`**，不要提交包含真实密钥的 **`.env`**。
- 若密钥曾误提交，请在服务商侧**轮换密钥**，并清理 Git 历史（必要时使用 `git filter-repo` 等工具）。


