from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.user import User

def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))

def update_me(db: Session, user: User, full_name: str | None) -> User:
    user.full_name = full_name
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
