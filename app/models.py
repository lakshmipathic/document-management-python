from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, JSON

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    embeddings = Column(JSON, nullable=False)
