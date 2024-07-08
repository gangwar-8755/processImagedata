from fastapi import FastAPI
from API.upload import router as upload_router
from API.status import router as status_router
from database.database import init_db

app = FastAPI()

app.include_router(upload_router, prefix="/api")
app.include_router(status_router, prefix="/api")

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
