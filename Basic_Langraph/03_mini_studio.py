"""
Mini Studio : Build your own Graph!!

Build both graphs from scratch. Only the imports are given.
Each node should print its own name. Verify with draw_ascii() (uv add grandalf).

--- Problem 1 ---

                 node2 -> node4
               /                \
    START -> node1                node6 -> END
               \                /
                 node3 -> node5

    START -> node1
    node1 -> node2      node1 -> node3
    node2 -> node4      node3 -> node5
    node4 -> node6      node5 -> node6
    node6 -> END

--- Problem 2 ---

                              node5
                            /       \
    START -> node1 -> node2 -> node4   node7 -> END
                   \        /      \  /   ^
                     node3 -       node6  |
                          \_______________|

    START -> node1
    node1 -> node2      node1 -> node3
    node2 -> node4      node3 -> node4
    node3 -> node7
    node4 -> node5      node4 -> node6
    node5 -> node7      node6 -> node7
    node7 -> END

Predict the output order and how many times each node runs before running it.
Problem 2 has a surprise -- count the runs of node7 carefully.
"""

from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


# --- Problem 1 ---


# --- Problem 2 ---
