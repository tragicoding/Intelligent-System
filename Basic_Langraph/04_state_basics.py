"""
Practice 4 : State

A single-node graph that reads a question from the State and writes an answer.

    START -> answering_agent -> END

Expected output:
    State In Node: {'user_question': 'how are you?'}
    final output: {'user_question': 'how are you?', 'ai_answer': "I'm an AI Agent for you!!"}

Run: uv run python 04_state_basics.py
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class State(TypedDict):
    # TODO: declare `user_question` and `ai_answer` as str
    pass


def answering_agent(state: State):
    print(f"State In Node: {state}")
    # TODO: return the ai_answer update instead of an empty dict
    return {}


builder = StateGraph(State)
builder.add_node("answering_agent", answering_agent)

builder.add_edge(START, "answering_agent")
builder.add_edge("answering_agent", END)

graph = builder.compile()

if __name__ == "__main__":
    outcome = graph.invoke({"user_question": "how are you?"})
    print(f"final output: {outcome}")


# Challenge
# 1. Return {} and compare the final output. Which keys survive?
# 2. Invoke without `user_question`. Does it fail?
# 3. Add a second node that rewrites `ai_answer`. Which value wins?
