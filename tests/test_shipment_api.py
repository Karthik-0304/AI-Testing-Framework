from http import client

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_existing_shipment():
    response = client.get("/shipments/SH1001")

    assert response.status_code == 200

    data = response.json()

    assert data["shipment_id"] == "SH1001"
    assert data["status"] == "In Transit"
    assert data["destination"] == "Chennai"

def test_get_another_existing_shipment():
    response = client.get("/shipments/SH1002")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "Delivered"


def test_get_unknown_shipment():
    response = client.get("/shipments/UNKNOWN999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"

def test_shipment_id_case_insensitive():
    response = client.get("/shipments/sh1001")  # Lowercase shipment ID

    assert response.status_code == 200
    assert response.json()["shipment_id"] == "SH1001"  # Should still return the correct shipment

def test_response_has_required_fields():
    response = client.get("/shipments/SH1001")

    assert response.status_code == 200

    data = response.json()

    # Check that all required fields are present
    assert "shipment_id" in data
    assert "status" in data
    assert "destination" in data


def test_empty_shipment_id_returns_not_found():
    response = client.get("/shipments/")

    # The route requires a shipment ID, so this URL
    # should not match the shipment endpoint.
    assert response.status_code == 404