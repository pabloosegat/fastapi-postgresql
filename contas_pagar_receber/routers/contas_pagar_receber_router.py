from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix='/contas-pagar-receber')

class ContaPagarReceberResponse(BaseModel):
    id: int
    desc: str
    valor: float
    tipo: str

class ContaPagarReceberRequest(BaseModel):
    desc: str
    valor: float
    tipo: str


@router.get('', response_model=List[ContaPagarReceberResponse])
def listar_contas():
    return [
        ContaPagarReceberResponse(id=1, desc='Conta de Luz', valor=100.00, tipo='Pagar'),
        ContaPagarReceberResponse(id=2, desc='Conta de Agua', valor=50.00, tipo='Pagar'),
        ContaPagarReceberResponse(id=3, desc='Conta de Internet', valor=200.00, tipo='Pagar'),
        ContaPagarReceberResponse(id=4, desc='Conta de Telefone', valor=150.00, tipo='Pagar'),
        ContaPagarReceberResponse(id=5, desc='Conta de Salario', valor=5000.00, tipo='Receber'),
        ContaPagarReceberResponse(id=6, desc='Conta de Aluguel' , valor=5000.00, tipo='Pagar')
    ]

@router.post('', response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta: ContaPagarReceberRequest): 
    return ContaPagarReceberResponse(
        id=7,
        desc=conta.desc,
        valor=conta.valor,
        tipo=conta.tipo
    )