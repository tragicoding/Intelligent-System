r"""
Homework : Travel Planner Graph

Read README.md first. Scoring is step by step: 3 -> 5 -> 8 -> 10 pts.

    START -> intake --(Command)--> planner (subgraph) --> budget_check
    budget_check --(conditional edge)--> finalize    -> END
                                    \--> over_budget -> END

    [planner subgraph]
    START -> plan_start -> book_transport -+
                        -> book_hotel     -+-> summarize -> END
                        -> find_food      -+

Grading checks results only; node names and graph shape are up to you.
Do NOT rename these, the grader uses them:
    graph, merge_ledger, the State keys, the staff_status keys,
    PRICES, DOMESTIC_CITIES, BOOKING_FEE, LEDGER_LABELS, format_itinerary

Run: uv run python hw_travel_planner.py
Test: uv run python test_public.py

Suggested order -- run the tests after each step. The TODOs below say "step N".
    1. intake returns trip_type, connect START -> intake -> END          (3 pts)
    2. planner subgraph nodes, then run planner_graph on its own
    3. reducers in TravelState and PlannerState
    4. add the planner node, connect intake -> planner                   (5 pts)
    5. intake returns a Command that moves to planner
    6. budget_check, conditional edge, finalize / over_budget            (8 pts)
    7. ledger items and merge_ledger                                     (10 pts)
"""

import operator
from operator import or_
from typing import Literal

from typing_extensions import Annotated, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


# --- Given: price table and helpers (do not change) -------------------------

DOMESTIC_CITIES = ["Jeju", "Busan", "Gangneung"]

PRICES = {
    "domestic": {"transport": 120_000, "hotel_per_night": 80_000, "food_per_day": 30_000},
    "overseas": {"transport": 450_000, "hotel_per_night": 150_000, "food_per_day": 60_000},
}

BOOKING_FEE = 3_000

# ledger item id -> label (10 pts). The amounts come from PRICES / BOOKING_FEE.
LEDGER_LABELS = {
    "fee": "booking fee",
    "transport": "transport",
    "hotel": "hotel",
    "food": "food",
}


def format_itinerary(state, within_budget: bool) -> str:
    if within_budget:
        status = "within budget"
    else:
        status = f"over budget by {state['total_cost'] - state['budget']:,} won"
    return (
        f"{state['customer']} / {state['destination']} {state['days']} days"
        f" / {state['total_cost']:,} won ({status})"
    )


# --- 10 pts: custom reducer --------------------------------------------------


class LedgerItem(TypedDict):
    id: str
    label: NotRequired[str]
    amount: NotRequired[int]
    remove: NotRequired[bool]


def merge_ledger(left: list[LedgerItem] | None, right) -> list[LedgerItem]:
    # LangGraph calls this every time a node returns {"ledger": ...}.
    #   left   = the ledger list currently in the state
    #   right  = what the node returned for "ledger": one item (dict) or a list of items,
    #            e.g. [{"id": "hotel", "label": "hotel", "amount": 0}]
    #            or a delete request from summarize: [{"id": "hotel", "remove": True}]
    #   return = the new ledger list that is stored in the state
    # TODO (step 7, 10 pts): This placeholder only concatenates, like operator.add.
    #   Rewrite it with the rules in README.md, section 3 (merge by `id`).
    return left + right


# --- State -------------------------------------------------------------------


class TravelState(TypedDict):
    customer: str
    destination: str
    days: int
    budget: int
    trip_type: Literal["domestic", "overseas"]
    bookings: list[str]          # TODO (step 3): attach a reducer
    total_cost: int              # TODO (step 3): attach a reducer
    staff_status: dict[str, str]  # TODO (step 3): attach a reducer
    ledger: Annotated[list[LedgerItem], merge_ledger]
    budget_status: Literal["within", "over"]
    itinerary: str


class PlannerState(TypedDict):
    trip_type: Literal["domestic", "overseas"]
    days: int
    nights: int
    bookings: list[str]          # TODO (step 3): same reducer as TravelState
    total_cost: int              # TODO (step 3): same reducer as TravelState
    staff_status: dict[str, str]  # TODO (step 3): same reducer as TravelState
    ledger: Annotated[list[LedgerItem], merge_ledger]


# --- Planner subgraph (step 2) -----------------------------------------------


def plan_start(state: PlannerState):
    # TODO (step 2): nights = days - 1
    ...


def book_transport(state: PlannerState):
    # TODO (step 2): cost = PRICES[trip_type]["transport"]
    #   bookings     -> [f"transport: round trip {cost:,} won"]
    #   total_cost   -> cost
    #   staff_status -> {"book_transport": "done"}
    #   (step 7) ledger -> [{"id": "transport", "label": LEDGER_LABELS["transport"], "amount": cost}]
    ...


def book_hotel(state: PlannerState):
    # TODO (step 2): cost = hotel_per_night * nights
    #   bookings     -> [f"hotel: {nights} nights {cost:,} won"]
    #   total_cost / staff_status like book_transport
    #   (step 7) ledger -> [{"id": "hotel", "label": LEDGER_LABELS["hotel"], "amount": cost}]
    ...


def find_food(state: PlannerState):
    # TODO (step 2): cost = food_per_day * days
    #   bookings     -> [f"food: {days} days {cost:,} won"]
    #   total_cost / staff_status like book_transport
    #   (step 7) ledger -> [{"id": "food", "label": LEDGER_LABELS["food"], "amount": cost}]
    ...


def summarize(state: PlannerState):
    # TODO (step 7): remove every ledger item whose amount is 0
    #   by returning {"id": ..., "remove": True} items.
    return {}


# TODO (step 2): build the planner subgraph and compile it as `planner_graph`
#   START -> plan_start -> (book_transport, book_hotel, find_food) -> summarize -> END
#   Try it on its own first, then delete the test line:
#       print(planner_graph.invoke({"trip_type": "domestic", "days": 3}))
#   Before step 3 this raises InvalidUpdateError -- that is expected, step 3 fixes it.
#   While this line is in the file, test_public.py cannot load the file (0 pts).


# --- Main graph --------------------------------------------------------------


def intake(state: TravelState):
    # TODO (step 1): return {"trip_type": "domestic"} when destination is exactly one of
    #   DOMESTIC_CITIES, otherwise {"trip_type": "overseas"}.
    # TODO (step 5): return a Command instead of a dict
    #   - update: trip_type and staff_status {"intake": "done"}
    #   - goto:   "planner" (one planner handles both trip types)
    # TODO (step 7): also put the booking fee into `ledger` in the update:
    #   ledger -> [{"id": "fee", "label": LEDGER_LABELS["fee"], "amount": BOOKING_FEE}]
    # WARNING: do not write `bookings` or `total_cost` here (see README).
    ...


def budget_check(state: TravelState):
    # TODO (step 6): decide the budget result and store it in the state
    #   budget_status -> "within" if total_cost <= budget, otherwise "over"
    #   staff_status  -> {"budget_check": "done"}
    ...


def route_budget(state: TravelState) -> Literal["finalize", "over_budget"]:
    # TODO (step 6): return the name of the next node, chosen only from budget_status
    #   (budget_check already wrote it). Do not compare total_cost and budget again here.
    #   "within" -> "finalize",  "over" -> "over_budget"
    ...


def finalize(state: TravelState):
    # TODO (step 6): itinerary = format_itinerary(state, within_budget=True)
    ...


def over_budget(state: TravelState):
    # TODO (step 6): itinerary = format_itinerary(state, within_budget=False)
    ...


builder = StateGraph(TravelState)

# TODO: register the nodes and connect them, one step at a time.
#   step 1: START -> intake -> END
#   step 4: add the node "planner" (the node is planner_graph itself),
#           change intake -> END into intake -> planner -> END
#   step 5: register intake with destinations=("planner",)
#           and delete the plain edge intake -> planner (the Command moves now)
#   step 6: planner -> budget_check (instead of END),
#           budget_check -> finalize / over_budget with a conditional edge (route_budget),
#           finalize / over_budget -> END

graph = builder.compile()


if __name__ == "__main__":
    print(graph.get_graph(xray=True).draw_ascii())
    outcome = graph.invoke({"customer": "Kim", "destination": "Jeju", "days": 3, "budget": 500_000})
    print(outcome)


# Think about it (not graded)
# 1. Remove the reducer from `bookings`. Which error do you get, and why?
# 2. Keep merge_ledger as plain concatenation and finish the 10 pts nodes.
#    How many "fee" items end up in the final ledger? Why?
# 3. intake uses a Command, budget_check uses a conditional edge. Swap them in your head.
#    Which one reads better for each place?
