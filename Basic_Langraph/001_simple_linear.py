from langgraph.graph import StateGraph , START, END
from typing_extensions import TypedDict

#all node must have this class's rule and date, structure
class State(TypedDict):
    number : int

def node_1(state : State):
    print(f"node_1이 받은 값 : {state["number"]}")
    return {"number" : state["number"] + 5 }

def node_2(state : State):
    print(f"node_2가 받은 값 : {state["number"]}")
    return {"number": state["number"] + 5}

def node_3(state : State):
    print(f"node_3이 받은 값 : {state["number"]}")
    return {"number" : state["number"]}

#create StateGraph Object
builder = StateGraph(State)

#create node
builder.add_node("node_1" , node_1)
builder.add_node("node_2" , node_2)
builder.add_node("node_3" , node_3)

#create edge
builder.add_edge(START , "node_1")
builder.add_edge("node_1" , "node_2")
builder.add_edge("node_2" , "node_3")
builder.add_edge("node_3" , END)

#take the graph , and execute the function 
m_graph = builder.compile()
m_graph.invoke( {"number" : 5} )

#Draw the graph as with ascii
print(m_graph.get_graph().draw_ascii())
