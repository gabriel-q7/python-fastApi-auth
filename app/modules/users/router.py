from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token
from app.modules.users.schemas import UserOut, UpdateMeIn
from app.modules.users.service import get_user_by_id, update_me

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/users", tags=["users"])

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return user

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user

@router.patch("/me", response_model=UserOut)
def patch_me(payload: UpdateMeIn, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_me(db, user, payload.full_name)
