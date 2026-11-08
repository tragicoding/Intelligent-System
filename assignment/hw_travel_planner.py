"""
여행 요청을 받아 예약 내역과 예산 확인 결과를 반환한다.
교통과 숙박과 식비를 병렬로 계산하고 장부는 식별자를 기준으로 합친다.
"""

import operator
from operator import or_
from typing import Literal

from typing_extensions import Annotated, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command


# 목록에 있는 도시와 정확히 일치하는 경우에만 국내 여행으로 처리한다.
DOMESTIC_CITIES = ["Jeju", "Busan", "Gangneung"]

# 여행 구분에 따라 교통비와 숙박비와 식비의 기준 금액을 선택한다.
PRICES = {
    "domestic": {"transport": 120_000, "hotel_per_night": 80_000, "food_per_day": 30_000},
    "overseas": {"transport": 450_000, "hotel_per_night": 150_000, "food_per_day": 60_000},
}

# 예약 수수료는 장부에만 기록하고 예산 비교에 쓰는 여행 경비에는 더하지 않는다.
BOOKING_FEE = 3_000

# 장부에 기록할 항목 이름은 주어진 값을 그대로 사용한다.
LEDGER_LABELS = {
    "fee": "booking fee",
    "transport": "transport",
    "hotel": "hotel",
    "food": "food",
}


# 예산 확인 결과에 맞춰 주어진 형식의 여행 안내 문장을 만든다.
def format_itinerary(state, within_budget: bool) -> str:
    if within_budget:
        status = "within budget"
    else:
        status = f"over budget by {state['total_cost'] - state['budget']:,} won"
    return (
        f"{state['customer']} / {state['destination']} {state['days']} days"
        f" / {state['total_cost']:,} won ({status})"
    )


# 장부 항목은 식별자를 기준으로 구분하고 삭제 요청도 같은 형태로 전달
class LedgerItem(TypedDict):
    id     : str
    label  : NotRequired[str]
    amount : NotRequired[int]
    remove : NotRequired[bool]


# 기존 장부를 복사한 뒤 새 항목과 삭제 요청을 전달된 순서대로 반영한
def merge_ledger(left : list[LedgerItem] | None, right) -> list[LedgerItem]:
    # 사전의 입력 순서를 이용해 같은 항목을 교체해도 위치가 유지되게 한다.
    items_by_id = {}

    for item in left or []:
        if "id" not in item:
            raise ValueError("장부 항목에는 식별자가 필요하다.")
        items_by_id[item["id"]] = item.copy()

    # 새 값이 없거나 단일 항목인 경우에도 목록으로 처리
    if right is None:
        updates = []
    elif isinstance(right, dict):
        updates = [right]
    else:
        updates = right

    for item in updates:
        if "id" not in item:
            raise ValueError("장부 항목에는 식별자가 필요하다.")

        item_id = item["id"]

        # 삭제 여부가 참인 경우에만 삭제하고 나머지는 항목 전체를 저장.
        if item.get("remove") is True:
            items_by_id.pop(item_id, None)
        else:
            items_by_id[item_id] = item.copy()

    return list(items_by_id.values())


# 메인 그래프는 여행 요청과 예약 결과와 예산 확인 결과를 관리한다.
class TravelState(TypedDict):
    customer      : str
    destination   : str
    days          : int
    budget        : int
    trip_type     : Literal["domestic", "overseas"]

    # 병렬 노드가 반환한 예약 목록은 이어 붙이고 경비는 합산한다.
    bookings      : Annotated[list[str], operator.add]
    total_cost    : Annotated[int, operator.add]

    # 담당 노드마다 남기는 완료 기록은 사전으로 합친다.
    staff_status  : Annotated[dict[str, str], or_]
    ledger        : Annotated[list[LedgerItem], merge_ledger]
    budget_status : Literal["within", "over"]
    itinerary     : str


# 서브그래프의 공유 항목에는 메인 그래프와 같은 병합 규칙을 적용
class PlannerState(TypedDict):
    trip_type    : Literal["domestic", "overseas"]
    days         : int
    # 숙박 일수는 서브그래프 내부에서만 사용한다.
    nights       : int
    bookings     : Annotated[list[str], operator.add]
    total_cost   : Annotated[int, operator.add]
    staff_status : Annotated[dict[str, str], or_]
    ledger       : Annotated[list[LedgerItem], merge_ledger]


# 여행 일수에서 하루를 빼서 실제 숙박 일수를 구한다.
def plan_start(state : PlannerState):
    return {"nights" : state["days"] - 1}


# 여행 구분에 맞는 왕복 교통비를 예약 내역과 장부에 기록
def book_transport(state : PlannerState):
    cost = PRICES[state["trip_type"]]["transport"]

    return {
        "bookings"     : [f"transport: round trip {cost:,} won"],
        "total_cost"   : cost,
        "staff_status" : {"book_transport" : "done"},
        "ledger"       : [
            {"id" : "transport", "label" : LEDGER_LABELS["transport"], "amount" : cost}
        ],
    }


# 일박 요금에 숙박 일수를 곱해 숙박비를 구한다.
def book_hotel(state : PlannerState):
    nights = state["nights"]
    cost   = PRICES[state["trip_type"]]["hotel_per_night"] * nights

    return {
        "bookings"     : [f"hotel: {nights} nights {cost:,} won"],
        "total_cost"   : cost,
        "staff_status" : {"book_hotel" : "done"},
        "ledger"       : [
            {"id" : "hotel", "label" : LEDGER_LABELS["hotel"], "amount" : cost}
        ],
    }


# 하루 식비에 여행 일수를 곱해 전체 식비를 구한다.
def find_food(state : PlannerState):
    days = state["days"]
    cost = PRICES[state["trip_type"]]["food_per_day"] * days

    return {
        "bookings"     : [f"food: {days} days {cost:,} won"],
        "total_cost"   : cost,
        "staff_status" : {"find_food" : "done"},
        "ledger"       : [
            {"id" : "food", "label" : LEDGER_LABELS["food"], "amount" : cost}
        ],
    }


# 금액이 영인 항목은 장부에서 삭제하도록 요청.
def summarize(state : PlannerState):
    # 삭제한 목록을 반환하는 대신 삭제할 항목의 식별자를 전달한다.
    removals = [
        {"id" : item["id"], "remove" : True}
        for item in state["ledger"]
        if item.get("amount") == 0
    ]
    return {"ledger" : removals}


# 세 예약 노드를 병렬로 실행하는 서브그래프를 만든다
planner_builder = StateGraph(PlannerState)

planner_builder.add_node("plan_start",     plan_start)
planner_builder.add_node("book_transport", book_transport)
planner_builder.add_node("book_hotel",     book_hotel)
planner_builder.add_node("find_food",      find_food)
planner_builder.add_node("summarize",      summarize)

planner_builder.add_edge(START, "plan_start")
planner_builder.add_edge("plan_start", "book_transport")
planner_builder.add_edge("plan_start", "book_hotel")
planner_builder.add_edge("plan_start", "find_food")

# 세예약 작업이 모두 끝난 뒤 장부를 정리한다
planner_builder.add_edge(["book_transport", "book_hotel", "find_food"], "summarize")
planner_builder.add_edge("summarize", END)

# 완성된 서브그래프는 메인 그래프의 노드로 등록한다.
planner_graph = planner_builder.compile()


# 여행 구분과 수수료를 기록하고 같은 명령에서 예약 단계로 이동한다.
def intake(state : TravelState) -> Command[Literal["planner"]]:
    trip_type = "domestic" if state["destination"] in DOMESTIC_CITIES else "overseas"

    # 예약 내역과 여행 경비는 세예약 노드에서만 갱신한다.
    return Command(
        update = {
            "trip_type"    : trip_type,
            "staff_status" : {"intake" : "done"},
            "ledger"       : [
                {"id" : "fee", "label" : LEDGER_LABELS["fee"], "amount" : BOOKING_FEE}
            ],
        },
        goto = "planner",
    )


# 여행 경비가 예산과 같거나 적으면 예산 이내로 판단한다.
def budget_check(state : TravelState):
    budget_status = "within" if state["total_cost"] <= state["budget"] else "over"

    return {
        "budget_status" : budget_status,
        "staff_status"  : {"budget_check" : "done"},
    }


# 이미 저장된 예산 확인 결과만 읽어 다음 노드를 선택한다.
def route_budget(state : TravelState) -> Literal["finalize", "over_budget"]:
    if state["budget_status"] == "within":
        return "finalize"
    return "over_budget"


# 예산 이내인 여행의 최종 안내 문장을 반환한다.
def finalize(state : TravelState):
    return {"itinerary" : format_itinerary(state, within_budget=True)}


# 예산을 초과한 여행의 최종 안내 문장을 반환한다.
def over_budget(state : TravelState):
    return {"itinerary" : format_itinerary(state, within_budget=False)}


# 메인그래프에서 요청접수와 예약과 예산확인을 순서대로 연결
builder = StateGraph(TravelState)

builder.add_node("intake",       intake, destinations=("planner",))
builder.add_node("planner",      planner_graph)
builder.add_node("budget_check", budget_check)
builder.add_node("finalize",     finalize)
builder.add_node("over_budget",  over_budget)

builder.add_edge(START, "intake")
builder.add_edge("planner", "budget_check")
builder.add_conditional_edges("budget_check", route_budget)
builder.add_edge("finalize", END)
builder.add_edge("over_budget", END)

graph = builder.compile()


if __name__ == "__main__":
    print(graph.get_graph(xray=True).draw_ascii())
    outcome = graph.invoke({"customer": "Kim", "destination": "Jeju", "days": 3, "budget": 500_000})
    print(outcome)
