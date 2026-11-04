from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

class State(TypedDict):
    number : int

def node_1_1(state : State):
    print(f"node_1_1이 받은 값 = {state["number"]}")
    return {"number" : state["number"] + 5}
def node_2_1(state : State):
    print(f"node_2_1이 받은 값 = {state["nubmer"]}")
    return {"number" : state["number"] + 5}
def node_1_2(state : State):
    print(f"node_1_2이 받은 값 = {state["number"]}")
    return {"number" : state["number"] + 5}
def node_2_2(state : State):
    print(f"node_2_2이 받은 값 = {state["number"]}")
    return {"number" : state["number"] + 5}

def node_3(state1 : State , state2 : State):
    print(f"node_3이 받은 값 = 1경로:{state1["number"]} \
          / 2경로:{state2["number"]}")

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
m_graph.invoke({"number" : 5})
print(m_graph.get_graph().draw_ascii())