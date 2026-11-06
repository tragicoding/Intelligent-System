from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict

class State(TypedDict):
    messages = list[str]

def node1( state : State):
    return {"messages" : ["hello I'm node1"]}

def node2( state : State):
    return {"messages" : state.get("messages").append("hellod I'm node2")}

builder = StateGraph(State)
builder.add_node("node1" , node1)
builder.add_node("node2" , node2)
builder.add_edge(START , "node1")
builder.add_edge("node1" , "node2")
builder.add_edge("node2" , END)

graph = builder.compile()
output = graph.invoke({})
print(output)