"""
Practice 6 : Reducer (parallel writes to one key)

                 node2
               /       \
    START -> node1       node4 -> END
               \       /
                 node3

node2 and node3 run in parallel and both write to `messages`.
As given, this raises InvalidUpdateError. Run it first, read the error,
then add the reducer so the lists get concatenated instead.

Expected output after the fix:
    {'messages': ["hello I'm node 1", ..., "hello I'm node 4"]}

draw_ascii() requires grandalf: uv add grandalf
Run: uv run python 06_reducer.py
"""

import operator

from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    messages: list[str]
    # TODO: attach an operator.add reducer to `messages` using Annotated


def node1(state: State):
    return {"messages": ["hello I'm node 1"]}


def node2(state: State):
    return {"messages": ["hello I'm node 2"]}


def node3(state: State):
    return {"messages": ["hello I'm node 3"]}


def node4(state: State):
    return {"messages": ["hello I'm node 4"]}


builder = StateGraph(State)
builder.add_node("node1", node1)
builder.add_node("node2", node2)
builder.add_node("node3", node3)
builder.add_node("node4", node4)

builder.add_edge(START, "node1")
builder.add_edge("node1", "node2")
builder.add_edge("node1", "node3")
builder.add_edge("node2", "node4")
builder.add_edge("node3", "node4")
builder.add_edge("node4", END)

graph = builder.compile()

if __name__ == "__main__":
    print(graph.get_graph().draw_ascii())

    outcome = graph.invoke({})
    print(outcome)


# Challenge
# 1. Switch to the commented-out `messages: list[str]` and read the error.
# 2. Invoke with {"messages": ["seed"]}. Where does it end up?
# 3. Replace operator.add with your own reducer that drops duplicates.
