from fastapi import Depends

from sqlmodel import create_engine
from sqlmodel import Session, create_engine

from .config import env

engine = create_engine(
    env.DB_URI,
    echo=env.DB_ECHO,
    connect_args=env.DB_CONNECT_ARGS
)

def get_session():
    with Session(engine) as session:
        yield session

ActiveSession = Depends(get_session)


