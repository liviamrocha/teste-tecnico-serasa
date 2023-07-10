from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from credito.routes import main_router

app = FastAPI(
    title="Serasa Crédito",
    version="0.1.0",
    description="Busca por melhores ofertas de empréstimos entre os parceiros do Serasa Crédito",
)

app.include_router(main_router)
