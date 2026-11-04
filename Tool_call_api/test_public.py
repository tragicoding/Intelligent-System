"""
Public tests for hw_travel_planner.py -- run them as often as you like:

    uv run python test_public.py

Stages count step by step (3 -> 5 -> 8 -> 10), like the real grading.
Only results are checked: node names and graph shape are up to you.
The real grading uses many more hidden tests, so passing these is not a guarantee.
Do not change the expected values here; change your code instead.
"""

import traceback

PLANNER_NODES = ["book_transport", "book_hotel", "find_food"]

# (input, expected result) -- the same trips as the table in README section 1
TRIPS = [
    ({"customer": "Kim", "destination": "Jeju", "days": 3, "budget": 500_000}, {
        "trip_type": "domestic",
        "total_cost": 370_000,
        "bookings": ["transport: round trip 120,000 won", "hotel: 2 nights 160,000 won", "food: 3 days 90,000 won"],
        "budget_status": "within",
        "itinerary": "Kim / Jeju 3 days / 370,000 won (within budget)",
        "ledger": {"fee": 3_000, "transport": 120_000, "hotel": 160_000, "food": 90_000},
    }),
    ({"customer": "Park", "destination": "Busan", "days": 2, "budget": 260_000}, {
        "trip_type": "domestic",
        "total_cost": 260_000,
        "bookings": ["transport: round trip 120,000 won", "hotel: 1 nights 80,000 won", "food: 2 days 60,000 won"],
        "budget_status": "within",
        "itinerary": "Park / Busan 2 days / 260,000 won (within budget)",
        "ledger": {"fee": 3_000, "transport": 120_000, "hotel": 80_000, "food": 60_000},
    }),
    ({"customer": "Baek", "destination": "Gangneung", "days": 5, "budget": 600_000}, {
        "trip_type": "domestic",
        "total_cost": 590_000,
        "bookings": ["transport: round trip 120,000 won", "hotel: 4 nights 320,000 won", "food: 5 days 150,000 won"],
        "budget_status": "within",
        "itinerary": "Baek / Gangneung 5 days / 590,000 won (within budget)",
        "ledger": {"fee": 3_000, "transport": 120_000, "hotel": 320_000, "food": 150_000},
    }),
    ({"customer": "Lee", "destination": "Paris", "days": 5, "budget": 1_000_000}, {
        "trip_type": "overseas",
        "total_cost": 1_350_000,
        "bookings": ["transport: round trip 450,000 won", "hotel: 4 nights 600,000 won", "food: 5 days 300,000 won"],
        "budget_status": "over",
        "itinerary": "Lee / Paris 5 days / 1,350,000 won (over budget by 350,000 won)",
        "ledger": {"fee": 3_000, "transport": 450_000, "hotel": 600_000, "food": 300_000},
    }),
    ({"customer": "Moon", "destination": "Bangkok", "days": 4, "budget": 1_000_000}, {
        "trip_type": "overseas",
        "total_cost": 1_140_000,
        "bookings": ["transport: round trip 450,000 won", "hotel: 3 nights 450,000 won", "food: 4 days 240,000 won"],
        "budget_status": "over",
        "itinerary": "Moon / Bangkok 4 days / 1,140,000 won (over budget by 140,000 won)",
        "ledger": {"fee": 3_000, "transport": 450_000, "hotel": 450_000, "food": 240_000},
    }),
]


def expect(actual, expected, what):
    if actual != expected:
        raise AssertionError(f"{what}: expected {expected!r}, got {actual!r}")


def build_tests(hw):
    cache = {}

    def run(trip):
        key = (trip["destination"], trip["days"])
        if key not in cache:
            cache[key] = hw.graph.invoke(dict(trip))
        return cache[key]

    def label(trip):
        return f"{trip['destination']} {trip['days']} days"

    first = TRIPS[0][0]
    tests = [(3, f"graph.invoke runs without error ({label(first)})", lambda: run(first))]

    # --- 5 pts: domestic trips ---
    def domestic(trip, exp):
        def fn():
            out = run(trip)
            expect(out.get("total_cost"), exp["total_cost"], "total_cost")
            expect(sorted(out.get("bookings", [])), sorted(exp["bookings"]), "bookings")
            for node in PLANNER_NODES:
                expect(out.get("staff_status", {}).get(node), "done", f"staff_status[{node!r}]")
        return fn

    for trip, exp in TRIPS:
        if exp["trip_type"] == "domestic":
            tests.append((5, f"domestic {label(trip)}", domestic(trip, exp)))

    # --- 8 pts: every trip, domestic and overseas, within and over budget ---
    def full(trip, exp):
        def fn():
            out = run(trip)
            for key in ("trip_type", "total_cost", "budget_status", "itinerary"):
                expect(out.get(key), exp[key], key)
            expect(sorted(out.get("bookings", [])), sorted(exp["bookings"]), "bookings")
            for node in ["intake", *PLANNER_NODES, "budget_check"]:
                expect(out.get("staff_status", {}).get(node), "done", f"staff_status[{node!r}]")
        return fn

    for trip, exp in TRIPS:
        tests.append((8, f"full flow {label(trip)}", full(trip, exp)))

    # --- 10 pts: merge_ledger (README section 3) ---
    a1, b2 = {"id": "a", "amount": 1}, {"id": "b", "amount": 2}

    def unit(name, fn):
        tests.append((10, f"merge_ledger: {name}", fn))

    unit("None -> []", lambda: expect(hw.merge_ledger(None, None), [], "merge_ledger(None, None)"))
    unit("replace keeps position (README example)", lambda: expect(
        hw.merge_ledger([a1, b2], {"id": "a", "amount": 9}), [{"id": "a", "amount": 9}, b2], "replace"))
    unit("remove (README example)", lambda: expect(
        hw.merge_ledger([a1, b2], {"id": "a", "remove": True}), [b2], "remove"))
    unit("new id is appended", lambda: expect(hw.merge_ledger([a1], [b2]), [a1, b2], "append"))

    def ledger(trip, exp):
        def fn():
            items = run(trip).get("ledger") or []
            ids = [item["id"] for item in items]
            if len(ids) != len(set(ids)):
                raise AssertionError(f"duplicated ids in ledger: {ids}")
            expect({item["id"]: item.get("amount") for item in items}, exp["ledger"], "ledger")
        return fn

    for trip, exp in TRIPS:
        tests.append((10, f"graph ledger {label(trip)}", ledger(trip, exp)))
    return tests


def main():
    try:
        import hw_travel_planner as hw
    except Exception as e:  # noqa: BLE001
        print("hw_travel_planner.py could not be loaded (0 pts)")
        for frame in traceback.extract_tb(e.__traceback__):
            if frame.filename.endswith("hw_travel_planner.py"):
                where = f"line {frame.lineno}: {frame.line}"
        print(f"  {where}" if "where" in locals() else "")
        print(f"  {type(e).__name__}: {e}")
        return

    results = []
    for stage, name, fn in build_tests(hw):
        try:
            fn()
            results.append((stage, name, None))
        except Exception as e:  # noqa: BLE001
            results.append((stage, name, f"{type(e).__name__}: {e}"))

    for stage in (3, 5, 8, 10):
        print(f"\n[{stage} pts]")
        for s, name, error in results:
            if s == stage:
                print(f"  {'PASS' if error is None else 'FAIL'}  {name}")
                if error:
                    print(f"        {error[:300]}")

    reached = 0
    for stage in (3, 5, 8, 10):
        if all(error is None for s, _, error in results if s == stage):
            reached = stage
        else:
            break
    print(f"\nPublic tests reached: {reached} pts (hidden tests are added in the real grading)")


if __name__ == "__main__":
    main()
