from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
from app.db.models.user import User

def register_user(db: Session, email: str, password: str, full_name: str | None) -> User:
    existing = db.scalar(select(User).where(User.email == email))
    if existing:
        raise ValueError("EMAIL_EXISTS")

    user = User(email=email, password_hash=hash_password(password), full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate(db: Session, email: str, password: str) -> User | None:
    user = db.scalar(select(User).where(User.email == email))
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def issue_token(user: User) -> tuple[str, int]:
    token = create_access_token(subject=str(user.id))
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return token, expires_in
