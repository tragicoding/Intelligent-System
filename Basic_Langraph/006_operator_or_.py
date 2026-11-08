from operator import or_
from typing import Annotated
from typing import NotRequired
from langgraph.graph import StateGraph,START,END
from typing_extensions import TypedDict
from typing import Literal

class AgentStatus(TypedDict):
    answering_agent : NotRequired[Literal["done"]]
    translating_agent : NotRequired[Literal["done"]]

class State(TypedDict):
    user_question : str
    last_agent    : str
    ai_answer     : str
    ai_answer_kor : str
    #or_ == | operator : merge
    agent_status  : Annotated[AgentStatus,or_]

def answering_agent(state : State):
    return {
        "ai_answer_kor" : "I'm an AI Agent.",
        "last_agent" : "answering_agent",
        "agent_status" : {"answering_agent" : "done"}
    }

def translating_agent(state : State):
    return {
        "ai_answer_kor" : "저는 인공지능입니다.",
        "last_agent" : "translating_agent",
        "agent_status" : {"translating_agent" : "done"}
    }

builder = StateGraph(State)
builder.add_node("answering_agent" , answering_agent)
builder.add_node("translating_agent" , translating_agent)
builder.add_edge(START , "answering_agent")
builder.add_edge("answering_agent" , "translating_agent")
builder.add_edge("translating_agent" , END)

graph = builder.compile()
print(graph.get_graph().draw_ascii())

outcome = graph.invoke({})
print(outcome)