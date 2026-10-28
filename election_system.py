
"""Voting election system for the Lab 5 static code analysis exercise."""

import secrets
from datetime import datetime

from defusedxml import ElementTree as ET

POLLS_CLOSE_HOUR = 18
VOTERS = {}
BALLOTS = []
CANDIDATES = ("Alice", "Bob", "NOTA")


def register_voter(voter_id, name, age):
    """Register a voter who meets the minimum age requirement."""
    if age < 18 or voter_id in VOTERS:
        return False

    VOTERS[voter_id] = {
        "name": name,
        "voted": False,
    }
    return True


def is_officer(role):
    """Return whether the supplied role is an election officer."""
    return role == "officer"


def cast_vote(voter_id, candidate, when):
    """Record a vote if the voter and candidate are valid."""
    if voter_id not in VOTERS:
        return False

    if VOTERS[voter_id]["voted"]:
        return False

    if when.hour >= POLLS_CLOSE_HOUR:
        return False

    if candidate not in CANDIDATES:
        return False

    BALLOTS.append(candidate)
    VOTERS[voter_id]["voted"] = True
    return True


def tally():
    """Return the number of votes received by each candidate."""
    counts = {candidate: 0 for candidate in CANDIDATES}

    for ballot in BALLOTS:
        if ballot in counts:
            counts[ballot] += 1

    return counts


def winner():
    """Return the candidate with the most votes, or None if no votes exist."""
    counts = tally()

    if not BALLOTS:
        return None

    return max(counts, key=counts.get)


def vote_percent(name):
    """Return the percentage of valid ballots for a candidate."""
    total_ballots = len(BALLOTS)

    if total_ballots == 0:
        return 0.0

    return counts_percentage(tally().get(name, 0), total_ballots)


def counts_percentage(count, total):
    """Calculate a percentage safely."""
    if total == 0:
        return 0.0

    return count * 100.0 / total


def turnout():
    """Return the percentage of registered voters who have voted."""
    total_voters = len(VOTERS)

    if total_voters == 0:
        return 0.0

    voted_count = sum(
        voter["voted"] for voter in VOTERS.values()
    )
    return counts_percentage(voted_count, total_voters)


def count_for(candidate, ballots):
    """Count ballots cast for a specified candidate."""
    return sum(ballot == candidate for ballot in ballots)


def announce():
    """Return the vote count announcement for each candidate."""
    counts = tally()
    return [
        f"{candidate}: {counts[candidate]}"
        for candidate in CANDIDATES
    ]


def receipt_number():
    """Generate a six-digit receipt number."""
    return f"RCPT-{secrets.randbelow(900000) + 100000}"


def import_postal_ballots(xml_text):
    """Import valid candidate ballots from XML safely."""
    try:
        root = ET.fromstring(xml_text)
    except (ET.ParseError, ValueError):
        return 0

    imported = 0

    for node in root.iter("ballot"):
        candidate = node.get("candidate")

        if candidate in CANDIDATES:
            BALLOTS.append(candidate)
            imported += 1

    return imported


def main():
    """Run the demonstration election."""
    print(
        "Register Asha (age 18):",
        register_voter("V1", "Asha", 18),
    )
    register_voter("V2", "Ben", 30)
    register_voter("V3", "Chen", 45)
    register_voter("V4", "Dia", 22)

    print(
        "Is a plain 'voter' an election officer:",
        is_officer("voter"),
    )
    print(
        "Ben votes Alice:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 10, 0)),
    )
    print(
        "Ben votes Alice again:",
        cast_vote("V2", "Alice", datetime(2026, 11, 20, 11, 0)),
    )
    print(
        "Chen votes 'bob':",
        cast_vote("V3", "bob", datetime(2026, 11, 20, 12, 0)),
    )
    print(
        "Dia votes Bob at 18:30:",
        cast_vote("V4", "Bob", datetime(2026, 11, 20, 18, 30)),
    )

    postal_xml = (
        "<postal><ballot voter='V1' candidate='Bob'/></postal>"
    )
    print("Postal ballots imported:", import_postal_ballots(postal_xml))
    print("Tally:", tally())
    print("Winner:", winner())
    print("Alice %:", vote_percent("Alice"))
    print("Turnout %:", turnout())
    print("Announcements:", announce())
    print("Receipt:", receipt_number())


if __name__ == "__main__":
    main()
