from fastapi import APIRouter, HTTPException
from database.database import SessionLocal
from database.models import Request

router = APIRouter()

@router.get("/status/{request_id}")
async def check_status(request_id: str):
    db = SessionLocal()
    try:
        request = db.query(Request).filter(Request.id == request_id).first()
        if not request:
            raise HTTPException(status_code=404, detail="Request not found.")
        return {"request_id": request_id, "status": request.status}
    finally:
        db.close()
