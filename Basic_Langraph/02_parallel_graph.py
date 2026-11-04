"""
Practice 2 : Parallel Graph (fan-out / fan-in)

Target:
                 node_2
               /        \
    START -> node_1       node_4 -> END
               \        /
                 node_3

Edges:
    START  -> node_1
    node_1 -> node_2      node_1 -> node_3
    node_2 -> node_4      node_3 -> node_4
    node_4 -> END

Expected output:
    I'm node 1!!
    I'm node 2!!
    I'm node 3!!
    I'm node 4!!        (only once)
    None

draw_ascii() requires grandalf: uv add grandalf
Run: uv run python 02_parallel_graph.py
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


def node_4(state):
    # TODO: print and return None
    ...


builder = StateGraph(State)

builder.add_node("node_1", node_1)
# TODO: register node_2, node_3, node_4

builder.add_edge(START, "node_1")
# TODO: fan-out from node_1 to node_2 and node_3
# TODO: fan-in from node_2 and node_3 to node_4
# TODO: connect node_4 -> END

graph = builder.compile()

if __name__ == "__main__":
    # TODO: invoke with {} and print the result
    ...
    # TODO: print graph.get_graph().draw_ascii() and compare with the target


# Challenge
# 1. Why does node_4 run only once?
# 2. Make node_2 and node_3 both write to a `logs` key. It raises
#    InvalidUpdateError -- fix it with Annotated[list[str], operator.add].
# 3. Add node_1 -> node_4. When does node_4 run now?
