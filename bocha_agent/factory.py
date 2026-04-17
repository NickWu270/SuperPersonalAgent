from langchain_openai import ChatOpenAI

from bocha_agent.agent import Agent
from bocha_agent.config import (
    DEFAULT_SYSTEM_PROMPT,
    get_bocha_api_key,
    get_dashscope_base_url,
    get_llm_api_key,
    get_llm_model,
    DEFAULT_BOCHA_COUNT,
)
from bocha_agent.tools.bocha_search import BoChaSearchResult


def create_default_agent(system: str | None = None) -> Agent:
    """使用环境变量中的密钥与默认工具构造 Agent。"""
    model = ChatOpenAI(
        model=get_llm_model(),
        openai_api_key=get_llm_api_key(),
        openai_api_base=get_dashscope_base_url(),
    )
    tool = BoChaSearchResult(
        api_key=get_bocha_api_key(),
        count=DEFAULT_BOCHA_COUNT,
    )
    prompt = system if system is not None else DEFAULT_SYSTEM_PROMPT
    return Agent(model, [tool], system=prompt)
