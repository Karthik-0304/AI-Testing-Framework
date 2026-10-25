
from app.ai_evaluator import evaluate_shipment_response


TRUSTED_SHIPMENT = {
    "shipment_id": "SH1001",
    "status": "In Transit",
    "destination": "Chennai",
}


def test_correct_ai_response_passes():
    ai_response = (
        "Shipment SH1001 is In Transit "
        "and its destination is Chennai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is True
    assert result["status_correct"] is True
    assert result["destination_correct"] is True


def test_wrong_status_fails():
    ai_response = (
        "Shipment SH1001 is Delivered "
        "and its destination is Chennai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is False
    assert result["destination_correct"] is True


def test_wrong_destination_fails():
    ai_response = (
        "Shipment SH1001 is In Transit "
        "and its destination is Mumbai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is True
    assert result["destination_correct"] is False

def test_wrong_status_and_destination_fail():
    ai_response = (
        "Shipment SH1001 is Delivered "
        "and its destination is Mumbai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is False
    assert result["destination_correct"] is False


def test_unrelated_response_fails():
    ai_response = "Your food order will arrive tomorrow."

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is False
    assert result["destination_correct"] is False


def test_negated_status_fails():
    ai_response = (
        "Shipment SH1001 is not In Transit "
        "and its destination is Chennai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is False
    assert result["destination_correct"] is True


def test_negated_status_with_currently_fails():
    ai_response = (
        "Shipment SH1001 is not currently In Transit "
        "and its destination is Chennai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is False
    assert result["destination_correct"] is True



def test_conflicting_status_fails():
    ai_response = (
        "Shipment SH1001 is In Transit, "
        "but the latest status says Delivered. "
        "Its destination is Chennai."
    )

    result = evaluate_shipment_response(
        ai_response,
        TRUSTED_SHIPMENT,
    )

    assert result["passed"] is False
    assert result["status_correct"] is False
    assert result["destination_correct"] is True
