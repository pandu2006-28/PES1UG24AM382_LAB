"""
Lab 7 - Fuzz testing parking_fee.py with Hypothesis
Name: Pandu C V    SRN: PES1UG24AM382

Run:  pytest test_parking_fee.py      (or: python -m pytest test_parking_fee.py)

Expected behaviour of the hardened functions:
  * They must NEVER raise an exception, whatever the input.
  * For invalid input they return None.
  * For valid input they return the correct value.
"""
import string

from hypothesis import given, settings, strategies as st
from parking_fee import minutes_parked, hourly_rate, format_plate, RATES

# Any kind of input: random text, None, numbers, lists, bytes ...
any_input = st.one_of(st.text(), st.none(), st.integers(), st.floats(),
                      st.booleans(), st.lists(st.text()), st.binary())

# Text built only from characters the functions care about, so Hypothesis
# hits "almost valid" inputs (e.g. "9:-:", "25:00-26:99", "10:00-09:00") far more often
time_chars = st.text(alphabet="0123456789:- ", max_size=15)
plate_chars = st.text(alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 -", max_size=14)


# =====================================================================
# 1. minutes_parked("HH:MM-HH:MM")
# =====================================================================

@given(st.text() | st.none())
def test_minutes_parked_no_crash(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed with: {e!r}"


@given(any_input | time_chars)
def test_minutes_parked_no_crash_any_type(s):
    try:
        minutes_parked(s)
    except Exception as e:
        assert False, f"minutes_parked crashed on {s!r} with: {e!r}"


@given(time_chars)
def test_minutes_parked_never_negative(s):
    # A duration can never be negative (exit before entry must be rejected)
    try:
        result = minutes_parked(s)
    except Exception:
        return  # crashes are reported by the no-crash tests
    assert result is None or (isinstance(result, int) and result >= 0), \
        f"minutes_parked({s!r}) returned invalid duration {result!r}"


@given(st.integers(0, 23), st.integers(0, 59), st.integers(0, 23), st.integers(0, 59))
def test_minutes_parked_valid_times(h1, m1, h2, m2):
    s = f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}"
    expected = (h2 * 60 + m2) - (h1 * 60 + m1)
    result = minutes_parked(s)
    if expected >= 0:
        assert result == expected
    else:
        assert result is None


# =====================================================================
# 2. hourly_rate(vehicle)
# =====================================================================

@given(st.text() | st.none())
def test_hourly_rate_no_crash(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed with: {e!r}"


@given(any_input)
def test_hourly_rate_no_crash_any_type(s):
    try:
        hourly_rate(s)
    except Exception as e:
        assert False, f"hourly_rate crashed on {s!r} with: {e!r}"


@given(st.sampled_from(sorted(RATES)), st.text(alphabet=" \t", max_size=3),
       st.text(alphabet=" \t", max_size=3), st.booleans())
def test_hourly_rate_valid_vehicle(vehicle, left_pad, right_pad, upper):
    # Valid vehicle names in any case and with surrounding spaces still work
    name = vehicle.upper() if upper else vehicle
    assert hourly_rate(left_pad + name + right_pad) == RATES[vehicle]


@given(st.text())
def test_hourly_rate_only_known_values(s):
    try:
        result = hourly_rate(s)
    except Exception:
        return
    assert result is None or result in RATES.values()


# =====================================================================
# 3. format_plate("ka01ab1234") -> "KA 01 AB 1234"
# =====================================================================

@given(st.text() | st.none())
def test_format_plate_no_crash(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed with: {e!r}"


@given(any_input | plate_chars)
def test_format_plate_no_crash_any_type(s):
    try:
        format_plate(s)
    except Exception as e:
        assert False, f"format_plate crashed on {s!r} with: {e!r}"


@given(plate_chars)
def test_format_plate_output_shape(s):
    # Output must be None or exactly "AA 00 AA 0000"
    try:
        result = format_plate(s)
    except Exception:
        return
    if result is not None:
        parts = result.split(" ")
        assert len(result) == 13 and [len(p) for p in parts] == [2, 2, 2, 4], \
            f"format_plate({s!r}) returned badly formatted {result!r}"
        assert parts[0].isalpha() and parts[2].isalpha()
        assert parts[1].isdigit() and parts[3].isdigit()


letters = st.text(alphabet=string.ascii_letters, min_size=2, max_size=2)
digits = lambda n: st.text(alphabet=string.digits, min_size=n, max_size=n)


@given(letters, digits(2), letters, digits(4))
def test_format_plate_valid(state, rto, series, number):
    plate = state + rto + series + number
    assert format_plate(plate) == f"{state.upper()} {rto} {series.upper()} {number}"
