"""
Practice 5 : State flowing through two nodes

    START -> answering_agent -> translating_agent -> END

Each node returns only the key it owns, and the updates accumulate.
Watch how `previous state is` grows between the two nodes.

Run: uv run python 05_state_flow.py
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class State(TypedDict):
    user_question: str
    ai_answer: str
    ai_answer_kor: str


def answering_agent(state: State):
    print("***********answering_agent***************")
    print("previous state is", state)
    print("*****************************************")
    return {"ai_answer": "I'm an AI Agent for you!!"}


def translating_agent(state: State):
    print("**********translating_agent**************")
    print("previous state is", state)
    print("*****************************************")
    return {"ai_answer_kor": "저는 당신을 위한 인공지능 에이전트입니다"}


builder = StateGraph(State)
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
# 1. Swap the two nodes. What is missing inside translating_agent?
# 2. Make translating_agent read state["ai_answer"] instead of a fixed string.
# 3. Run the two nodes in parallel instead. What happens?
