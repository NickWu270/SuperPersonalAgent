from typing import Type

import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, PrivateAttr

from bocha_agent.config import BOCHA_WEB_SEARCH_URL
from bocha_agent.schemas import BoChaSearchInput


class BoChaSearchResult(BaseTool):
    name: str = "bocha_web_search"
    description: str = "使用博查API进行网络搜索，可以用来查找实时信息或新闻"
    args_schema: Type[BaseModel] = BoChaSearchInput

    _api_key: str = PrivateAttr()
    _count: int = PrivateAttr()
    _summary: bool = PrivateAttr()
    _freshness: str = PrivateAttr()

    def __init__(
        self,
        api_key: str,
        count: int = 5,
        summary: bool = True,
        freshness: str = "noLimit",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._api_key = api_key
        self._count = count
        self._summary = summary
        self._freshness = freshness

    def _run(self, query: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "summary": self._summary,
            "freshness": self._freshness,
            "count": self._count,
        }
        try:
            response = requests.post(
                BOCHA_WEB_SEARCH_URL,
                headers=headers,
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("data", {}).get("webPages", {}).get("value", [])
            if not results:
                return f"未找到相关内容。\n[DEBUG] 返回数据：{data}"

            output = ""
            for i, item in enumerate(results[: self._count]):
                title = item.get("name", "无标题")
                snippet = item.get("snippet", "无摘要")
                page_url = item.get("url", "")
                output += f"{i + 1}. {title}\n{snippet}\n链接：{page_url}\n\n"

            return output.strip()
        except Exception as e:
            return f"搜索失败：{e}"
