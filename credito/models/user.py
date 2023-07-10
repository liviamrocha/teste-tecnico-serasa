from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel, EmailStr
from credito.security import HashedPassword


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    password: HashedPassword

class UserResponse(BaseModel):
    email: EmailStr

class UserRequest(BaseModel):
    email: str
    password: str
   