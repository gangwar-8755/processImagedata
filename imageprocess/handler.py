from fastapi import APIRouter, HTTPException
import requests
from database.database import SessionLocal
from database.models import Request

router = APIRouter()

@router.post("/webhook/{request_id}")
async def webhook_handler(request_id: str):
    db = SessionLocal()
    try:
        request = db.query(Request).filter(Request.id == request_id).first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found.")
        if request.status != "completed":
            raise HTTPException(status_code=400, detail="Request not yet completed.")
        webhook_url = "https://your_webhook_endpoint"
        response = requests.post(webhook_url, json={"request_id": request_id, "status": request.status})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to trigger webhook.")
        return {"message": "Webhook triggered successfully."}
    finally:
        db.close()
