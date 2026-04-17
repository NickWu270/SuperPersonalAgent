from langchain_core.messages import HumanMessage

from bocha_agent.factory import create_default_agent


def main() -> None:
    abot = create_default_agent()
    ascii_diagram = abot.graph.get_graph().draw_ascii()
    print(ascii_diagram)

    messages = [
        HumanMessage(
            content=(
                "利用现有工具访问见微数据网站，查询一下里面有什么内容，"
                "查询该网站招股说明书"
            )
        )
    ]
    result = abot.graph.invoke({"messages": messages})
    print(result["messages"][-1].content)
