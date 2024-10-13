from sqlalchemy import Column, Integer, String
from database import Base

class Document(Base):
    __tablename__ = "douments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, unique=True, index=True)
