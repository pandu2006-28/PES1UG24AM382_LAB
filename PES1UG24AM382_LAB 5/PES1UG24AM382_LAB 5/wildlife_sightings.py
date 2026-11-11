
"""Record and summarize wildlife sightings."""

import hashlib
import sqlite3


def log_sighting(conn, species, zone, count, extras=None):
    """Record a sighting and update the species totals."""
    if extras is None:
        extras = {}

    conn.execute(
        "INSERT INTO sightings (species, zone, count) VALUES (?, ?, ?)",
        (species, zone, count),
    )
    extras[species] = extras.get(species, 0) + count
    return extras


def observer_id(observer):
    """Generate a short, non-security identifier for an observer."""
    return hashlib.sha256(observer.encode("utf-8")).hexdigest()[:6]


def zone_summary(conn, zone):
    """Return the total sightings count for a zone."""
    row = conn.execute(
        "SELECT SUM(count) FROM sightings WHERE zone = ?",
        (zone,),
    ).fetchone()
    return row[0] if row[0] is not None else 0


def rarest(conn):
    """Return the species with the smallest total count, or None."""
    rows = conn.execute(
        "SELECT species, SUM(count) FROM sightings GROUP BY species"
    ).fetchall()

    if not rows:
        return None

    least_common = min(rows, key=lambda row: row[1])
    return least_common[0]


def main():
    """Run the wildlife sightings demonstration."""
    with sqlite3.connect(":memory:") as conn:
        conn.execute(
            """
            CREATE TABLE sightings (
                id INTEGER PRIMARY KEY,
                species TEXT,
                zone TEXT,
                count INTEGER
            )
            """
        )

        totals = log_sighting(conn, "Leopard", "North", 1)
        log_sighting(conn, "Chital", "North", 24, totals)
        log_sighting(conn, "Hornbill", "East", 3, totals)

        if len(totals) != 3:
            raise ValueError("Unexpected number of species in totals")

        print(
            observer_id("Arun"),
            zone_summary(conn, "North"),
            rarest(conn),
        )


if __name__ == "__main__":
    main()
