from pydantic import BaseModel, Field, constr

class EmprestimoResponseSchema(BaseModel):
    identificador: str = Field(
        description="Identificador da oferta"
    )
    parceiro: str = Field(
        description="Nome do parceiro"
    )
    parcelas: int = Field(
        description="Quantidade de parcelas"
    )
    valor: float = Field(
        description="Valor total"
    )

class CPFModel(BaseModel):
    cpf: constr(regex=r'^\d{11}$')
