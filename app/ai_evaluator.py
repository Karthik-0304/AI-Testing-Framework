import re

def evaluate_shipment_response(
    ai_response: str,
    trusted_shipment: dict,
) -> dict:
    """
    Compare an AI response with trusted shipment data.
    This is a basic keyword-based evaluator.
    """

    expected_status = trusted_shipment["status"].lower()
    expected_destination = trusted_shipment["destination"].lower()

    actual_response = ai_response.lower()

    status_correct = expected_status in actual_response
    destination_correct = expected_destination in actual_response

    passed = status_correct and destination_correct

    return {
        "passed": passed,
        "status_correct": status_correct,
        "destination_correct": destination_correct,
    }

def _contains_negated_phrase(text: str, phrase: str) -> bool:
    """
    Check whether a phrase is preceded by a negation.
    Example: 'not in transit' is a negated phrase.
    """

    escaped_phrase = re.escape(phrase)

    pattern = (
        rf"\b(?:not|never|isn't|isnt|wasn't|wasnt|"
        rf"no longer)\s+(?:currently\s+)?{escaped_phrase}\b"
    )

    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def evaluate_shipment_response(
    ai_response: str,
    trusted_shipment: dict,
) -> dict:
    """
    Compare an AI response with trusted shipment data.
    This evaluator checks for expected keywords and
    basic negation of the expected status.
    """

    expected_status = trusted_shipment["status"].lower()
    expected_destination = trusted_shipment["destination"].lower()

    actual_response = ai_response.lower()

    status_correct = (
        expected_status in actual_response
        and not _contains_negated_phrase(
            actual_response,
            expected_status,
        )
    )

    destination_correct = expected_destination in actual_response

    passed = status_correct and destination_correct

    return {
        "passed": passed,
        "status_correct": status_correct,
        "destination_correct": destination_correct,
    }


KNOWN_STATUSES = [
    "In Transit",
    "Delivered",
    "Delayed",
]


def _contains_negated_phrase(text: str, phrase: str) -> bool:
    """Check whether a status is preceded by a negation."""

    escaped_phrase = re.escape(phrase)

    pattern = (
        rf"\b(?:not|never|isn't|isnt|wasn't|wasnt|"
        rf"no longer)\s+(?:currently\s+)?{escaped_phrase}\b"
    )

    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def evaluate_shipment_response(
    ai_response: str,
    trusted_shipment: dict,
) -> dict:
    """
    Compare an AI response with trusted shipment data.
    Checks expected values, basic negation, and conflicting statuses.
    """

    expected_status = trusted_shipment["status"].lower()
    expected_destination = trusted_shipment["destination"].lower()
    actual_response = ai_response.lower()

    expected_status_present = expected_status in actual_response

    expected_status_negated = _contains_negated_phrase(
        actual_response,
        expected_status,
    )

    conflicting_status_present = any(
        status.lower() in actual_response
        for status in KNOWN_STATUSES
        if status.lower() != expected_status
    )

    status_correct = (
        expected_status_present
        and not expected_status_negated
        and not conflicting_status_present
    )

    destination_correct = expected_destination in actual_response

    passed = status_correct and destination_correct

    return {
        "passed": passed,
        "status_correct": status_correct,
        "destination_correct": destination_correct,
    }
