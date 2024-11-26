from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Document
from app.db import db_session
from app.services import generate_embeddings
from pydantic import BaseModel

router = APIRouter()
class IngestDocumentRequest(BaseModel):
    title: str
    content: str

@router.post("/")
async def ingest_document(request: IngestDocumentRequest, session: AsyncSession = Depends(db_session)):
    try:
        embeddings = await generate_embeddings(request.content)
        document = Document(title=request.title, content=request.content, embeddings=embeddings)
        session.add(document)
        await session.commit()
        return {"message": "Document ingested successfully"}
    except Exception as e:
        print("e")
        raise HTTPException(status_code=500, detail=str(e))
