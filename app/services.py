import numpy as np
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Document
import openai
from sqlalchemy import text

openai.api_key = "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"

async def generate_embeddings(text: str):
    response =  openai.Embedding.create(input=text, model="text-embedding-ada-002")
    embeddings = response.data[0].embedding
    return embeddings
async def retrieve_relevant_embeddings(query: str, session: AsyncSession):
    query_embedding = await generate_embeddings(query)
    query = text("SELECT * FROM documents")
    result = await session.execute(query)
    documents = result.fetchall()
    
    similarities = [
        (doc, np.dot(query_embedding, doc.embeddings) / 
         (np.linalg.norm(query_embedding) * np.linalg.norm(doc.embeddings)))
        for doc in documents
    ]
    top_docs = sorted(similarities, key=lambda x: x[1], reverse=True)[:5]
    return [doc[0] for doc in top_docs]

async def generate_answer(question: str, documents: list):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # You can also use "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    # Extract and return the answer from the response
    answer = response.choices[0].message.content
    return answer
