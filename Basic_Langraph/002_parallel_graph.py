from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

class State(TypedDict):
    pass

def node_1_1(state : State):
    return None
def node_2_1(state : State):
    return None
def node_1_2(state : State):
    return None
def node_2_2(state : State):
    return None

def node_3(state : State):
    return None

builder = StateGraph(State)

builder.add_node("node_1_1" , node_1_1)
builder.add_node("node_1_2" , node_1_2)
builder.add_node("node_2_1" , node_2_1)
builder.add_node("node_2_2" , node_2_2)
builder.add_node("node_3" , node_3)

builder.add_edge(START , "node_1_1")
builder.add_edge(START , "node_2_1")
builder.add_edge("node_1_1" , "node_1_2")
builder.add_edge("node_2_1" , "node_2_2")
builder.add_edge("node_1_2" , "node_3")
builder.add_edge("node_2_2" , "node_3")
builder.add_edge("node_3" , END)

m_graph = builder.compile()
m_graph.invoke({})
print(m_graph.get_graph().draw_ascii())