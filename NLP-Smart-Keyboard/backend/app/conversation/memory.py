from sqlalchemy.orm import Session
from app.models.schema import ConversationMemory

def add_message(db: Session, session_id: str, role: str, message: str):
    if not message.strip():
        return None
        
    db_msg = ConversationMemory(session_id=session_id, role=role, message=message)
    db.add(db_msg)
    db.commit()
    db.refresh(db_msg)
    return db_msg

def get_recent_context(db: Session, session_id: str, limit: int = 10):
    messages = db.query(ConversationMemory)\
                 .filter(ConversationMemory.session_id == session_id)\
                 .order_by(ConversationMemory.timestamp.desc())\
                 .limit(limit)\
                 .all()
                 
    # Return in chronological order
    return list(reversed(messages))

def clear_memory(db: Session, session_id: str):
    db.query(ConversationMemory).filter(ConversationMemory.session_id == session_id).delete()
    db.commit()
    return {"status": "cleared", "session_id": session_id}
