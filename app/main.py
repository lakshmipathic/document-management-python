from fastapi import FastAPI
from app.routers import ingestion, qa, selection
from app.db import init_db

app = FastAPI()
import asyncio


app.include_router(ingestion.router, prefix="/api/ingestion", tags=["Ingestion"])
app.include_router(qa.router, prefix="/api/qa", tags=["Q&A"])
app.include_router(selection.router, prefix="/api/selection", tags=["Selection"])
async def main():
    await init_db()

if __name__ == "__main__":
    # For Uvicorn, it will run the event loop for you.
    # Just call the initialization function within the event loop.
    asyncio.create_task(main())