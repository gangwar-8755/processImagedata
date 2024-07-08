import requests
from PIL import Image
from io import BytesIO
from sqlalchemy.orm import sessionmaker
from database.database import engine
from database.models import Request, Product
import os

SessionLocal = sessionmaker(bind=engine)

def compress_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    buffer = BytesIO()
    img.save(buffer, "JPEG", quality=50)
    buffer.seek(0)
    return buffer

def process_images():
    db = SessionLocal()
    try:
        pending_requests = db.query(Request).filter(Request.status == "pending").all()
        for request in pending_requests:
            for product in request.products:
                input_urls = product.input_image_urls.split(',')
                output_urls = []
                for url in input_urls:
                    compressed_image = compress_image(url)
                    output_url = f"https://your_storage_service/{os.path.basename(url)}"
                    output_urls.append(output_url)
                product.output_image_urls = ','.join(output_urls)
            request.status = "completed"
            db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    process_images()
