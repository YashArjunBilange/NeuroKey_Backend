from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class ConversationMemory(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String) # 'user' or 'system' or 'friend'
    message = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
