"""
Practice 1 : Sequential Graph

Target: START -> node_1 -> node_2 -> node_3 -> END

Expected output:
    I'm node 1!!
    I'm node 2!!
    I'm node 3!!
    None

Run: uv run python 01_sequential_graph.py
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class State(TypedDict):
    pass


def node_1(state):
    print("I'm node 1!!")
    return None


def node_2(state):
    # TODO: print and return None
    ...


def node_3(state):
    # TODO: print and return None
    ...


builder = StateGraph(State)

builder.add_node("node_1", node_1)
# TODO: register node_2 and node_3

builder.add_edge(START, "node_1")
# TODO: connect node_1 -> node_2 -> node_3 -> END

graph = builder.compile()

if __name__ == "__main__":
    # TODO: invoke with {} and print the result
    ...


# Challenge
# 1. Add `count: int` to State and increment it in every node.
# 2. Swap the node_2 / node_3 edges. What changes?
# 3. Remove the edge to END and compile. Read the error.
