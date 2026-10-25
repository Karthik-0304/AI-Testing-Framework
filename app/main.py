import re

from fastapi import FastAPI, HTTPException

app = FastAPI(title="AI Shipment Testing API", description="API for testing AI shipment functionality", version="1.0.0")

SHIPMENTS = {
    "SH1001":{
        "shipment_id": "SH1001",
        "status": "In Transit",
        "destination": "Chennai",
    },
    "SH1002":{
        "shipment_id": "SH1002",
        "status": "Delivered",
        "destination": "Bangalore",
    },
    "SH1003":{
        "shipment_id": "SH1003",
        "status":"Delayed",
        "destination": "Hyderabad",
    }
}


@app.get("/")
def health_check():
    return {"message": "AI Shipment Testing API is running."}


@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    shipment = SHIPMENTS.get(shipment_id.upper())
    
    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Shipment not found",
        )

    return shipment