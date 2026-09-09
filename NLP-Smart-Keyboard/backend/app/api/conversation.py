from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.conversation import memory

router = APIRouter()

class MessageRequest(BaseModel):
    session_id: str
    role: str
    message: str

class SessionRequest(BaseModel):
    session_id: str

@router.post("/message")
async def add_message(req: MessageRequest, db: Session = Depends(get_db)):
    msg = memory.add_message(db, req.session_id, req.role, req.message)
    return {"status": "success", "id": msg.id if msg else None}

@router.get("/{session_id}")
async def get_history(session_id: str, limit: int = 10, db: Session = Depends(get_db)):
    messages = memory.get_recent_context(db, session_id, limit)
    return {"session_id": session_id, "messages": [{"role": m.role, "message": m.message, "timestamp": m.timestamp} for m in messages]}

@router.post("/clear")
async def clear_history(req: SessionRequest, db: Session = Depends(get_db)):
    return memory.clear_memory(db, req.session_id)
