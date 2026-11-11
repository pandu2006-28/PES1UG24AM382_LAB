"""
Lab 6 - Code (line/statement) coverage tests for parking_fee.py
Name: Pandu C V    SRN: PES1UG24AM382

Goal: execute every line of parking_fee.py at least once.
Run:
    coverage run -m pytest CodeCoverageTest_PES1UG24AM382_parking_fee.py
    coverage report -m
"""
import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------------- parking_fee() ----------------

def test_free_short_stay():
    # minutes <= 30 -> free (line 10)
    assert parking_fee("car", 20, False, False) == 0


def test_unknown_vehicle_raises():
    # line 6
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("plane", 60, False, False)


def test_negative_duration_raises():
    # line 8
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -5, False, False)


def test_partial_hour_rounded_up():
    # 90 min -> 1 full hour + partial hour rounded up = 2 hours (lines 12-15)
    assert parking_fee("car", 90, False, False) == 60


def test_ev_car_half_price():
    # EV discount for non-truck (line 17): 2 hours * 30 = 60 -> 30
    assert parking_fee("car", 90, True, False) == 30


def test_lost_ticket_penalty():
    # lost ticket adds 200 (line 19): 2 hours * 10 = 20 + 200
    assert parking_fee("bike", 120, False, True) == 220


# ---------------- find_slot() ----------------

def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_disabled_gets_ground_floor():
    assert find_slot("car", 5, True) == "ground floor"


def test_truck_goes_to_basement():
    assert find_slot("truck", 5, False) == "basement"


# ---------------- monthly_pass() ----------------

def test_bike_pass_non_resident():
    assert monthly_pass("bike", False) == 500


def test_car_pass_resident_discount():
    # 20% resident discount: 1500 - 300
    assert monthly_pass("car", True) == 1200


def test_no_pass_for_truck():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
