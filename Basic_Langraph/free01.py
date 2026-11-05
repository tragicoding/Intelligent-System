from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict

class State(TypedDict):
    number : int

def node_1(state : State):
    print(state["number"])
    return {"number" : state["number"] + 5}

def node_2(state : State):
    print(state["number"])
    return {"number" : state["number"] + 5}

def node_3(state : State):
    print(state["number"] + 5)
    return {"number" : state["number"] + 5}

builder = StateGraph(State)

builder.add_node("node_1" , node_1)
builder.add_node("node_2" , node_2)
builder.add_node("node_3" , node_3)

builder.add_edge(START , "node_1")
builder.add_edge("node_1" , "node_2")
builder.add_edge("node_2" , "node_3")
builder.add_edge("node_3" , END)

m_graph = builder.compile()
m_graph.invoke({"number" : 5})
print(m_graph.get_graph().draw_ascii())