from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.auth.schemas import RegisterIn, LoginIn, TokenOut
from app.modules.auth.service import register_user, authenticate, issue_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload.email, payload.password, payload.full_name)
    except ValueError as e:
        if str(e) == "EMAIL_EXISTS":
            raise HTTPException(status_code=409, detail="Email already registered")
        raise

    token, expires_in = issue_token(user)
    return TokenOut(access_token=token, expires_in=expires_in)

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = authenticate(db, payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token, expires_in = issue_token(user)
    return TokenOut(access_token=token, expires_in=expires_in)
