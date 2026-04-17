"""Agent 图状态：messages 使用 reduce_messages，同 id 则替换否则追加。"""

from __future__ import annotations

from typing import Annotated
from typing import TypedDict
from uuid import uuid4

from langchain_core.messages import AnyMessage


def reduce_messages(
    left: list[AnyMessage], right: list[AnyMessage]
) -> list[AnyMessage]:
    for message in right:
        if not message.id:
            message.id = str(uuid4())

    merged = list(left)
    for message in right:
        replaced = False
        for i, existing in enumerate(merged):
            if existing.id == message.id:
                merged[i] = message
                replaced = True
                break
        if not replaced:
            merged.append(message)
    return merged


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], reduce_messages]
