from fastapi.testclient import TestClient
from app.main import app
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

client = TestClient(app)

def test_ingest_document():
    logger.info('started') 
    response = client.post("/api/ingestion", json={"title": "Test", "content": "Sample"})
    assert response.status_code == 200

def test_answer_question():
    response = client.post("/api/qa", json={"question": "What is this about?"})
    assert response.status_code == 200
    assert "answer" in response.json()
