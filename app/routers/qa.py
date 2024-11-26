from fastapi import APIRouter, HTTPException,Depends
from app.services import retrieve_relevant_embeddings, generate_answer
from app.db import db_session
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

router = APIRouter()
class QARequest(BaseModel):
    question: str

@router.post("/")
async def answer_question(questionRequest: QARequest, session: AsyncSession = Depends(db_session)):
    try:
        relevant_docs = await retrieve_relevant_embeddings(questionRequest.question, session)
        answer = await generate_answer(questionRequest.question, relevant_docs)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
