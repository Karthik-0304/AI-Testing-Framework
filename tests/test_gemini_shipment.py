from http import client
from unittest import result

from fastapi.testclient import TestClient
from app.main import app
from app.gemini_client import ask_gemini
from app.ai_evaluator import evaluate_shipment_response

client = TestClient(app)


def test_gemini_gives_correct_shipment_infromation():

    api_response = client.get("/shipments/SH1001")

    assert api_response.status_code == 200

    trusted_shipment = api_response.json()

    prompt = (
        "You are a shipment support assistant. "
        "Answer the customer using only the following trusted data. "
        "Do not add any other shipment facts. "
        f"Shipment ID: {trusted_shipment['shipment_id']}. "
        f"Status: {trusted_shipment['status']}. "
        f"Destination: {trusted_shipment['destination']}. "
        "Explain the current status and destination in one sentence."
    )

    ai_response = ask_gemini(prompt)

    print("\nGemini response:", ai_response)

    result = evaluate_shipment_response(ai_response, trusted_shipment)

    assert result["status_correct"] is True, (
        f"Incorrect shipment status in Gemini response: {ai_response}"
    )

    assert result["destination_correct"] is True, (
        f"Incorrect destination in Gemini response: {ai_response}"
    )

    assert result["passed"] is True
