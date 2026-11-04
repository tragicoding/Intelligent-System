"""
Practice 8 : Input / Output schema

    START -> answering_agent -> translating_agent -> END

Same graph as Practice 7, but StateGraph gets an input_schema and an
output_schema. Internally the full State still flows; only the entry and
exit surfaces are narrowed.

Expected output:
    {'ai_answer_kor': '저는 당신을 위한 인공지능 에이전트입니다'}

Run: uv run python 08_io_schema.py
"""

from operator import or_
from typing import Annotated, Literal

from typing_extensions import NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END


class InputState(TypedDict):
    user_question: str


class OutputState(TypedDict):
    ai_answer_kor: str


class AgentStatus(TypedDict):
    answering_agent: NotRequired[Literal["done"]]
    translating_agent: NotRequired[Literal["done"]]


class State(TypedDict):
    user_question: str
    last_agent: str
    ai_answer: str
    ai_answer_kor: str
    agent_status: Annotated[AgentStatus, or_]


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


builder = StateGraph(State, input_schema=InputState, output_schema=OutputState)

builder.add_node("answering_agent", answering_agent)
builder.add_node("translating_agent", translating_agent)

builder.add_edge(START, "answering_agent")
builder.add_edge("answering_agent", "translating_agent")
builder.add_edge("translating_agent", END)

graph = builder.compile()

if __name__ == "__main__":
    outcome = graph.invoke({"user_question": "how are you?"})
    print(outcome)


# Challenge
# 1. Pass an extra key not in InputState. Does it reach the nodes?
# 2. Print the state inside each node. Is the full State still there?
# 3. Drop output_schema. How does the result change?
