from database import Base

from sqlalchemy import Column, Integer, String



class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    message = Column(String)