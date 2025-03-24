from models import chat_history_models as models
from schemas import chat_history_schemas as schemas
from sqlalchemy.orm import Session


# Get chat history by ID
def get_chat_history(db: Session, id: int):
    return db.query(models.ChatHistory).filter_by(id=id).first()


# Get all chat history entries, with pagination
def get_chat_histories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ChatHistory).offset(skip).limit(limit).all()


# Create a new chat history entry
def create_chat_history(db: Session, chat_history: schemas.ChatHistoryCreate):
    db_chat_history = models.ChatHistory(
        **chat_history.dict()
    )  # Use .dict() to convert Pydantic model to dict
    db.add(db_chat_history)
    db.commit()
    db.refresh(db_chat_history)
    return db_chat_history


# Get chat history by session_id
def get_chat_history_by_session_id(
    db: Session, session_id: str, skip: int = 0, limit: int = 100
):
    return (
        db.query(models.ChatHistory)
        .filter(models.ChatHistory.session_id == session_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
