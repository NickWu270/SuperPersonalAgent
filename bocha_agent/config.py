"""从环境变量读取运行配置。请在运行前设置 BOCHA_API_KEY 与 DASHSCOPE_API_KEY（或 OPENAI_API_KEY）。"""

from __future__ import annotations

import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv

    load_dotenv(_ROOT / ".env")
    load_dotenv()
except ImportError:
    pass


def _require(key: str, env_name: str) -> str:
    if not key:
        raise ValueError(
            f"Missing env var {env_name}. "
            "Set it in the system environment or project-root .env (see .env.example)."
        )
    return key


def get_bocha_api_key() -> str:
    return _require(os.environ.get("BOCHA_API_KEY", "").strip(), "BOCHA_API_KEY")


def get_llm_api_key() -> str:
    key = (
        os.environ.get("DASHSCOPE_API_KEY", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
    )
    return _require(key, "DASHSCOPE_API_KEY 或 OPENAI_API_KEY")


def get_dashscope_base_url() -> str:
    return os.environ.get(
        "DASHSCOPE_BASE_URL",
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
    ).rstrip("/")


def get_llm_model() -> str:
    return os.environ.get("LLM_MODEL", "qwen-plus")


BOCHA_WEB_SEARCH_URL = os.environ.get(
    "BOCHA_WEB_SEARCH_URL",
    "https://api.bochaai.com/v1/web-search",
)

DEFAULT_BOCHA_COUNT = int(os.environ.get("BOCHA_SEARCH_COUNT", "2"))

DEFAULT_SYSTEM_PROMPT = """你是一位聪明的助理,懂得使用tools来查阅网站最新消息"""
