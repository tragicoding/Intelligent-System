from langgraph.graph import StateGraph, START , END
from typing_extensions import TypedDict

class State(TypedDict):
    messages : list[str]

def node1(state : State):
    return {"messages" : ["I'm node1"]}
def node2(state : State):
    return {"messages" : state.get("messages").append("I'm node2")}
def node3(state : State):
    return {"messages" : state.get("messages").append("I'm node2")}
def node4(state : State):
    return {"messages" : state.get("messages").append("I'm node3")}
