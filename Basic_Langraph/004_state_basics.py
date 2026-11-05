from langgraph.graph import StateGraph , START , END
from typing_extensions import TypedDict

class State(TypedDict):
    user_question : str
    answer : str

def ai_answer(state : State):
    print(f"user_question : {state["user_question"]}")
    return {"user_question" : "Are you AI???"}

builder = StateGraph(State)
builder.add_node("ai_answer" , ai_answer)
builder.add_edge(START , "ai_answer")
builder.add_edge("ai_answer" , END)

graph = builder.compile()
outcome = graph.invoke(
    {
        "user_question" : "Who are you?"
    }
)
print(f"final state of this graph:{outcome}")
print(graph.get_graph().draw_ascii())