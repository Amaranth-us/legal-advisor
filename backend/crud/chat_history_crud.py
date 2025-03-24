from models import chat_history_models as models
from schemas import chat_history_schemas as schemas
from sqlalchemy import func
from sqlalchemy.orm import Session


# Get chat history by ID
def get_chat_history(db: Session, id: int):
    return db.query(models.ChatHistory).filter_by(id=id).first()


# Get all chat history entries
def get_chat_histories(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.ChatHistory).offset(skip).limit(limit).all()


# Create a new chat history entry
def create_chat_history(db: Session, chat_history: schemas.ChatHistoryCreate):
    db_chat_history = models.ChatHistory(**chat_history.dict())
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


# List all unique chat history session_ids
def get_all_sessions(db: Session):
    return db.query(models.ChatHistory.session_id).distinct().all()


# Get oldest oldest timestamp with the same session_id (beginning of the session)
def get_oldest_timestamp_by_session_id(db: Session, session_id: str):
    return (
        db.query(func.min(models.ChatHistory.timestamp))
        .filter(models.ChatHistory.session_id == session_id)
        .scalar()
    )


# Get all chat history entries of one session
def get_sessions_with_oldest_timestamps(db: Session):
    sessions = db.query(models.ChatHistory.session_id).distinct().all()

    session_with_oldest_timestamp = []
    for session in sessions:
        session_id = session[0]
        oldest_timestamp = (
            db.query(func.min(models.ChatHistory.timestamp))
            .filter(models.ChatHistory.session_id == session_id)
            .scalar()
        )
        formatted_timestamp = oldest_timestamp.strftime("%Y %m %d at %H:%M:%S")

        session_with_oldest_timestamp.append(
            {"session_id": session_id, "oldest_timestamp": formatted_timestamp}
        )

    return session_with_oldest_timestamp
