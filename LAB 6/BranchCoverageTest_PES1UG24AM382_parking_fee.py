"""
Lab 6 - Branch coverage tests for parking_fee.py
Name: Pandu C V    SRN: PES1UG24AM382

Goal: make every decision (if / elif / else) evaluate to BOTH True and False,
and exercise the boundary values around each condition.
Run:
    coverage run --branch -m pytest BranchCoverageTest_PES1UG24AM382_parking_fee.py
    coverage report -m
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass, HOURLY_RATE


# =====================================================================
# parking_fee(vehicle, minutes, is_ev, lost_ticket)
# Decisions:
#   D1 vehicle not in HOURLY_RATE      D2 minutes < 0
#   D3 minutes <= 30                   D4 minutes % 60 != 0
#   D5 is_ev and vehicle != "truck"    D6 lost_ticket
# =====================================================================

# ---- D1: unknown vehicle (True) / known vehicle (False) ----
@pytest.mark.parametrize("vehicle", ["plane", "", "Car", None])
def test_unknown_vehicle_raises(vehicle):
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee(vehicle, 60, False, False)


@pytest.mark.parametrize("vehicle, rate", [("bike", 10), ("car", 30), ("truck", 60)])
def test_every_known_vehicle_one_hour(vehicle, rate):
    assert parking_fee(vehicle, 60, False, False) == rate


# ---- D2: negative duration (True) / zero is valid (False) ----
def test_negative_duration_raises():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_zero_minutes_is_free():
    assert parking_fee("car", 0, False, False) == 0


# ---- D3: boundary of the free 30-minute window ----
def test_exactly_30_minutes_is_free():
    assert parking_fee("truck", 30, False, False) == 0


def test_31_minutes_is_charged_one_hour():
    assert parking_fee("car", 31, False, False) == 30


# ---- D4: exact hours (False) vs. partial hour rounded up (True) ----
def test_exact_hours_not_rounded():
    assert parking_fee("car", 120, False, False) == 60      # 2 h


def test_partial_hour_rounded_up():
    assert parking_fee("car", 121, False, False) == 90      # 2 h 1 min -> 3 h


def test_59_minutes_rounds_to_one_hour():
    assert parking_fee("bike", 59, False, False) == 10


# ---- D5: EV discount (compound condition) ----
def test_ev_car_gets_half_price():
    assert parking_fee("car", 120, True, False) == 30       # 60 -> 30


def test_ev_bike_half_price_floor_division():
    assert parking_fee("bike", 60, True, False) == 5        # 10 // 2


def test_ev_truck_gets_no_discount():
    # is_ev True but vehicle == "truck" -> condition False
    assert parking_fee("truck", 60, True, False) == 60


def test_non_ev_car_no_discount():
    # is_ev False -> condition False (short-circuit)
    assert parking_fee("car", 60, False, False) == 30


# ---- D6: lost ticket penalty ----
def test_lost_ticket_adds_200():
    assert parking_fee("car", 60, False, True) == 230


def test_lost_ticket_on_free_stay_still_charged():
    assert parking_fee("car", 10, False, True) == 200


def test_ev_discount_applied_before_lost_ticket_fee():
    # penalty itself is NOT halved: 60 // 2 + 200
    assert parking_fee("car", 120, True, True) == 230


def test_ev_truck_lost_ticket():
    assert parking_fee("truck", 90, True, True) == 120 + 200


# =====================================================================
# find_slot(vehicle, free_slots, is_disabled)
# Decisions: free_slots <= 0 | is_disabled | vehicle == "truck"
# =====================================================================

@pytest.mark.parametrize("free_slots", [0, -3])
def test_no_free_slots_returns_full(free_slots):
    assert find_slot("car", free_slots, False) == "full"


def test_full_takes_priority_over_disabled():
    assert find_slot("truck", 0, True) == "full"


def test_one_free_slot_is_not_full():
    assert find_slot("car", 1, False) == "any floor"


def test_disabled_driver_ground_floor():
    assert find_slot("car", 5, True) == "ground floor"


def test_disabled_truck_driver_ground_floor():
    # is_disabled is checked before vehicle type
    assert find_slot("truck", 5, True) == "ground floor"


def test_truck_goes_to_basement():
    assert find_slot("truck", 5, False) == "basement"


@pytest.mark.parametrize("vehicle", ["car", "bike"])
def test_non_truck_any_floor(vehicle):
    assert find_slot(vehicle, 5, False) == "any floor"


# =====================================================================
# monthly_pass(vehicle, is_resident)
# Decisions: vehicle == "bike" | elif vehicle == "car" | else | is_resident
# =====================================================================

@pytest.mark.parametrize("vehicle, resident, expected", [
    ("bike", False, 500),
    ("bike", True, 400),     # 500 - 500 // 5
    ("car", False, 1500),
    ("car", True, 1200),     # 1500 - 1500 // 5
])
def test_monthly_pass_prices(vehicle, resident, expected):
    assert monthly_pass(vehicle, resident) == expected


@pytest.mark.parametrize("vehicle", ["truck", "plane"])
def test_no_pass_for_other_vehicles(vehicle):
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass(vehicle, True)


def test_rate_table_unchanged():
    assert HOURLY_RATE == {"bike": 10, "car": 30, "truck": 60}
