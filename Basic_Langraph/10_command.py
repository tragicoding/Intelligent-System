"""
Practice 10 : Command (update + goto) and subgraphs

Two small agent graphs are built first, then plugged into a supervisor graph
as nodes. The supervisor node returns a Command instead of a dict:
`update` writes to the state, `goto` picks the next node -- no conditional
edge needed.

                      -> account_agent (subgraph) -> END
    START -> supervisor
                      -> order_agent   (subgraph) -> END

The two subgraphs are already built. Your job is the supervisor: make its
node return a Command, then wire up the supervisor graph.

Expected final outputs:
    {'request': '...password', 'selected_agent': 'Account Agent', 'result': "The Account Agent processed the 'Change password' request."}
    {'request': '...delivery', 'selected_agent': 'Order Agent',   'result': "The Order Agent processed the 'Track delivery' request."}

Run: uv run python 10_command.py
"""

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


# --- Account agent (subgraph) ---


class AccountState(TypedDict):
    request: str
    account_task: str
    result: str


def account_agent_node(state: AccountState):
    if "password" in state["request"].lower():
        task = "Change password"
    else:
        task = "Change email"

    return {
        "account_task": task,
        "result": f"The Account Agent processed the '{task}' request.",
    }


account_builder = StateGraph(AccountState)
account_builder.add_node("account_agent_node", account_agent_node)
account_builder.add_edge(START, "account_agent_node")
account_builder.add_edge("account_agent_node", END)

account_agent_graph = account_builder.compile()


# --- Order agent (subgraph) ---


class OrderState(TypedDict):
    request: str
    order_task: str
    result: str


def order_agent_node(state: OrderState):
    if "delivery" in state["request"].lower():
        task = "Track delivery"
    else:
        task = "Request a return"

    return {
        "order_task": task,
        "result": f"The Order Agent processed the '{task}' request.",
    }


order_builder = StateGraph(OrderState)
order_builder.add_node("order_agent_node", order_agent_node)
order_builder.add_edge(START, "order_agent_node")
order_builder.add_edge("order_agent_node", END)

order_agent_graph = order_builder.compile()


# --- Run each subgraph on its own first ---

result = account_agent_graph.invoke({"request": "I want to change my password"})
print(result)

result = order_agent_graph.invoke({"request": "I want to track my delivery"})
print(result)

exit()


# --- Supervisor graph ---


class SupervisorState(TypedDict):
    request: str
    selected_agent: str
    result: str


def supervisor_agent_node(state: SupervisorState):
    request = state["request"]

    if "password" in request.lower() or "email" in request.lower():
        # TODO: return a Command that updates selected_agent / result
        #       and goes to "account_agent"
        return {}

    # TODO: same for the Order Agent, going to "order_agent"
    return {}


# TODO: build the supervisor graph
#       - add supervisor_agent_node with destinations=("account_agent", "order_agent")
#       - add the two compiled subgraphs as the nodes "account_agent" / "order_agent"
#       - START -> supervisor_agent_node, and both agents -> END
#       - compile it as `supervisor_graph`


# TODO: invoke the supervisor graph twice with the two requests above and print


# Challenge
# 1. Remove `destinations=`. Does it still run? What changes in draw_ascii()?
# 2. `account_task` is not in SupervisorState. Where does it go?
# 3. Replace the Command with a conditional edge. Which reads better here?
