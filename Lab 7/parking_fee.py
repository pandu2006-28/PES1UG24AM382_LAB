import re

RATES = {"bike": 10, "car": 30, "truck": 60}

# "HH:MM" with 1-2 digit hour and exactly 2 digit minutes (ASCII digits only)
TIME_RE = re.compile(r"(\d{1,2}):(\d{2})", re.ASCII)
# Indian number plate: 2 letters, 2 digits, 2 letters, 4 digits  (e.g. KA01AB1234)
PLATE_RE = re.compile(r"[A-Z]{2}\d{2}[A-Z]{2}\d{4}", re.ASCII)


def _parse_time(t):
    """Return minutes since midnight for 'HH:MM', or None if invalid."""
    match = TIME_RE.fullmatch(t.strip())
    if match is None:
        return None
    hours, mins = int(match.group(1)), int(match.group(2))
    if not (0 <= hours <= 23 and 0 <= mins <= 59):
        return None
    return hours * 60 + mins


def minutes_parked(times):
    """'HH:MM-HH:MM' -> minutes parked (int >= 0), or None for invalid input."""
    if not isinstance(times, str):
        return None
    parts = times.split('-')
    if len(parts) != 2:
        return None
    entry = _parse_time(parts[0])
    exit_time = _parse_time(parts[1])
    if entry is None or exit_time is None:
        return None
    if exit_time < entry:          # exit before entry is not a valid duration
        return None
    return exit_time - entry


def hourly_rate(vehicle):
    """Vehicle type (any case / surrounding spaces) -> hourly rate, or None if unknown."""
    if not isinstance(vehicle, str):
        return None
    return RATES.get(vehicle.strip().lower())


def format_plate(plate):
    """'ka01ab1234' -> 'KA 01 AB 1234', or None if the plate is invalid."""
    if not isinstance(plate, str) or not plate.isascii():
        return None
    p = plate.replace(" ", "").replace("-", "").upper()
    if not PLATE_RE.fullmatch(p):
        return None
    return p[0:2] + " " + p[2:4] + " " + p[4:6] + " " + p[6:10]


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    if result is None:
        print("Invalid time range. Use HH:MM-HH:MM with exit after entry.")
    else:
        print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    if result is None:
        print("Invalid vehicle type. Choose bike, car or truck.")
    else:
        print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    if result is None:
        print("Invalid number plate. Expected format like KA01AB1234.")
    else:
        print("Formatted Plate:", result)


if __name__ == "__main__":
    main()
