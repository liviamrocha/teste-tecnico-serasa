from fastapi import APIRouter
from .emprestimos import router as emprestimos_router
from .user import router as user_router
from .auth import router as auth_router

main_router = APIRouter()

main_router.include_router(auth_router, tags=["auth"])
main_router.include_router(user_router, prefix="/user", tags=["user"])
main_router.include_router(emprestimos_router, prefix="/emprestimos", tags=["emprestimos"])
