"""
Practice 9 : Conditional edge (routing)

                      -> image_generation_agent -> END
    START -> router_agent
                      -> question_answering_agent -> END

router_agent does nothing but pass the state through. A routing function
looks at `state["mode"]` and returns a label; the label -> node mapping
decides which branch runs. Only one branch runs per invoke.

draw_ascii() requires grandalf: uv add grandalf
Run: uv run python 09_conditional_edge.py
"""

from typing import Literal

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    mode: Literal["image_generation", "question"]
    user_question: str
    ai_answer: str


def router_agent(state: State):
    print(f"router_agent: mode={state['mode']}")
    return None


def image_generation_agent(state: State):
    print("image_generation_agent")
    return {"ai_answer": f"[image] {state['user_question']}"}


def question_answering_agent(state: State):
    print("question_answering_agent")
    return {"ai_answer": f"[answer] {state['user_question']}"}


builder = StateGraph(State)
builder.add_node("router_agent", router_agent)
builder.add_node("image_generation_agent", image_generation_agent)
builder.add_node("question_answering_agent", question_answering_agent)

builder.add_edge(START, "router_agent")


def routing_function(state: State) -> Literal["image_generation", "question"]:
    # TODO: return the label to route on, based on the state
    ...


# TODO: add conditional edges from "router_agent" using routing_function,
#       mapping "image_generation" and "question" to their agent nodes

# TODO: connect both agent nodes to END

graph = builder.compile()

if __name__ == "__main__":
    print(graph.get_graph().draw_ascii())

    outcome = graph.invoke(
        {
            "mode": "question",
            "user_question": "What is the capital of South Korea",
        }
        # {
        #     "mode": "image_generation",
        #     "user_question": "Draw a coffee bean swimming in a cup of coffee",
        # }
    )
    print(outcome)


# Challenge
# 1. Switch to the commented-out input. Which node runs now?
# 2. Return a label that is not in the mapping. Read the error.
# 3. Drop the mapping dict and return node names directly from the function.
