from typing import List

from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from credito.db import ActiveSession
from credito.models.user import User, UserRequest, UserResponse

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O usuário já existe.")
    
    db_user = User.from_orm(user)  
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user