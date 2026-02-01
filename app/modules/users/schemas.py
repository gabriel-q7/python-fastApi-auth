from pydantic import BaseModel, EmailStr, Field
import uuid
from datetime import datetime

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str | None
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

class UpdateMeIn(BaseModel):
    full_name: str | None = Field(default=None, max_length=200)
