import json
import redis 
from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException
from credito.config import env
from credito.redis import init_redis_client

from credito.models.emprestimos import CPFModel, EmprestimoResponseSchema
from credito.models.user import User
from credito.auth import AuthenticatedUser
from parceiros.api import ParceirosAPI


APLICATION_NAME = env.APP_NAME
CACHE_EXPIRATION_SECONDS = env.CACHE_EXPIRATION_SECONDS
redis_client = init_redis_client()

router = APIRouter()

@router.get(
    '/',
    summary="Retorna oferta de empréstimo",
    description="Retorna oferta de empréstimo correspondente à simulação de crédito",
    status_code=status.HTTP_200_OK,
    response_model=EmprestimoResponseSchema
)
async def get_ofertas(cpf: str, parcelas: int, valor: float, user: User = AuthenticatedUser) -> EmprestimoResponseSchema:
    if not validar_cpf(cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF inválido")

    chave_redis = f"{APLICATION_NAME}:{'emprestimo'}:{cpf}:{parcelas}:{valor}"
    oferta_cacheada = obter_oferta_cacheada(chave_redis)

    if oferta_cacheada:
        return EmprestimoResponseSchema(**oferta_cacheada)

    ofertas = ParceirosAPI().obter_ofertas(parcelas, valor)
    oferta_filtrada = filtrar_ofertas(ofertas, parcelas, valor)

    if oferta_filtrada:
        redis_client.setex(chave_redis, CACHE_EXPIRATION_SECONDS, json.dumps(oferta_filtrada))
        return EmprestimoResponseSchema(**oferta_filtrada)
    else:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Não foram encontradas ofertas de créditos correspondentes aos valores de simulação repassados")
    

def obter_oferta_cacheada(chave_redis) -> Optional[EmprestimoResponseSchema]:
    oferta_cache = redis_client.get(chave_redis)

    if oferta_cache:
        redis_client.expire(chave_redis, CACHE_EXPIRATION_SECONDS)
        oferta_filtrada = json.loads(oferta_cache)
        return oferta_filtrada
    return None


def filtrar_ofertas(ofertas: list, parcelas: int, valor: float) -> Optional[EmprestimoResponseSchema]:
    oferta_filtrada = None

    for oferta in ofertas:
        if oferta["value"] <= valor and oferta["installments"] <= parcelas:
            if oferta_filtrada is None or oferta["value"] < oferta_filtrada["value"]:
                oferta_filtrada = oferta

    if oferta_filtrada:
        return {
            "identificador": oferta_filtrada['id'],
            "parceiro": oferta_filtrada['partner'],
            "parcelas": int(oferta_filtrada['installments']),
            "valor": oferta_filtrada['value']
        }
    return None

def validar_cpf(cpf: str) -> bool:
    cpf_data = {"cpf": cpf}
    try:
        CPFModel(**cpf_data)
        return True
    except ValueError:
        return False