"""
Practice 7 : Dict reducer + NotRequired

    START -> answering_agent -> translating_agent -> END

Each agent marks itself "done" in `agent_status`. Without a reducer the second
write replaces the whole dict, so only the last mark survives. `operator.or_`
merges the two dicts instead.

Expected output after the fix:
    agent_status = {'answering_agent': 'done', 'translating_agent': 'done'}

draw_ascii() requires grandalf: uv add grandalf
Run: uv run python 07_dict_reducer.py
"""
from operator import or_
from typing import Annotated, Literal
from typing_extensions import NotRequired, TypedDict  # NotRequired: py3.11+ in typing
from langgraph.graph import StateGraph, START, END


class AgentStatus(TypedDict):
    answering_agent: NotRequired[Literal["done"]]
    translating_agent: NotRequired[Literal["done"]]

class State(TypedDict):
    user_question: str
    last_agent: str
    ai_answer: str
    ai_answer_kor: str
    agent_status: AgentStatus
    # TODO: attach an or_ reducer to `agent_status` using Annotated


def answering_agent(state: State):
    return {
        "ai_answer": "I'm an AI Agent for you!!",
        "last_agent": "answering_agent",
        "agent_status": {"answering_agent": "done"},
    }


def translating_agent(state: State):
    return {
        "ai_answer_kor": "저는 당신을 위한 인공지능 에이전트입니다",
        "last_agent": "translating_agent",
        "agent_status": {"translating_agent": "done"},
    }


builder = StateGraph(State)
builder.add_node("answering_agent", answering_agent)
builder.add_node("translating_agent", translating_agent)

builder.add_edge(START, "answering_agent")
builder.add_edge("answering_agent", "translating_agent")
builder.add_edge("translating_agent", END)

graph = builder.compile()

if __name__ == "__main__":
    print(graph.get_graph().draw_ascii())

    outcome = graph.invoke({"user_question": "how are you?"})
    print(outcome)


# Challenge
# 1. Run it before and after the reducer. Compare `agent_status`.
# 2. `last_agent` has no reducer. Why is that fine here?
# 3. Drop NotRequired from AgentStatus. What breaks, and when?
