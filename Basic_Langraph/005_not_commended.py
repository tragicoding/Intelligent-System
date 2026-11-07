from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict

class State(TypedDict):
    messages : list[str]

def node1( state : State):
    return {"messages" : ["hello I'm node1"]}

def node2( state : State):
    print(state)
    return {"messages" : state.get("messages").append("hellod I'm node2")}

def node3( state : State):
    print(state)
    return {"messages" : state.get("messages").append("hello I'm node3")}

builder = StateGraph(State)
builder.add_node("node1" , node1)
builder.add_node("node2" , node2)
builder.add_node("node3" , node3)
builder.add_edge(START , "node1")
builder.add_edge("node1" , "node2")
builder.add_edge("node2" , "node3")
builder.add_edge("node3" , END)

graph = builder.compile()
print(graph.invoke({}))

