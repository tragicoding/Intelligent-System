from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

class State(TypedDict):
    user_question : str
    ai_answer :  str
    ai_translation : str

def AI_ANSWER(state : State):
    print(f"initial state : {state}")
    print("----------------------------")
    return {"ai_answer" : "I'm AI"}

def AI_TRANSLATION(state : State):
    print(f"previous node state :{state} ")
    print("----------------------------")
    return {"ai_translation" : "나는 인공지능 입니다."}

builder = StateGraph(State)
builder.add_node("AI_ANSWER" , AI_ANSWER)
builder.add_node("AI_TRANSLATION" , AI_TRANSLATION)
builder.add_edge(START , "AI_ANSWER")
builder.add_edge("AI_ANSWER" , "AI_TRANSLATION")
builder.add_edge("AI_TRANSLATION" , END)

print("------------invoke()-------------")
graph = builder.compile()
output = graph.invoke({"user_question" : "Who are you?"})
print(output)
print(graph.get_graph().draw_ascii())
"""
Guess the output
{"user_question : Who are you?"}
------------------------------
{"user_question" : "Who are you?, "ai_answer" : "I'm AI"}
------------------------------
{"user_question" : "Who are you?, "ai_answer" : "I'm AI"}
{"user_question" : "Who are you?, "ai_answer" : "I'm AI" , "ai_translation" : "나는 인공지능입니다."}

"""