from fastapi import APIRouter, UploadFile, File, HTTPException
import csv
from io import StringIO
import uuid
from database.database import SessionLocal
from database.models import Request, Product

router = APIRouter()

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are accepted.")

    content = await file.read()
    decoded = content.decode('utf-8')
    reader = csv.reader(StringIO(decoded))
    next(reader)  

    request_id = str(uuid.uuid4())
    db = SessionLocal()

    try:
        request = Request(id=request_id)
        db.add(request)
        db.commit()
        db.refresh(request)

        for row in reader:
            if len(row) < 3:
                raise HTTPException(status_code=400, detail="Invalid CSV format.")
            serial_number, product_name, input_image_urls = row[0], row[1], row[2]
            product = Product(
                request_id=request.id,
                serial_number=int(serial_number),
                product_name=product_name,
                input_image_urls=input_image_urls
            )
            db.add(product)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return {"request_id": request_id}
