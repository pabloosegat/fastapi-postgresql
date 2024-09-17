from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from models.fornecedor_cliente_model import FornecedorCliente
from shared.dependencies import get_db
from shared.exceptions import NotFound


router = APIRouter(prefix='/fornecedor-cliente')

class FornecedorClienteResponse(BaseModel):
    id: int
    nome: str
    
    class Config:
        orm_mode = True

class FornecedorClienteRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=255)

# CRUD

# Create
@router.post('', response_model=FornecedorClienteResponse)
def criar_fornecedor_cliente(fornecedor_cliente: FornecedorClienteRequest,
                            db: Session=Depends(get_db)) -> FornecedorClienteResponse:
    
    for_cli = FornecedorCliente(**fornecedor_cliente.dict())
    
    db.add(for_cli)
    db.commit()
    db.refresh(for_cli)
    
    return for_cli

# Read
@router.get('', response_model=List[FornecedorClienteResponse])
def listar_fornecedor_cliente(db: Session=Depends(get_db)) -> List[FornecedorClienteResponse]:
    return db.query(FornecedorCliente).all()

@router.get('/{id_fornecedor_cliente}', response_model=FornecedorClienteResponse)
def listar_um_fornecedor_cliente(id_fornecedor_cliente: int,
                                db: Session=Depends(get_db)) -> FornecedorClienteResponse:

    return consultar_fornecedor_cliente_por_id(id_fornecedor_cliente, db)

# Update
@router.put('/{id_fornecedor_cliente}', status_code=200)
def atualizar_fornecedor_cliente(id_fornecedor_cliente: int,
                                fornecedor_cliente_request: FornecedorClienteRequest,
                                db: Session=Depends(get_db)) -> FornecedorClienteResponse:
    
    for_cli = consultar_fornecedor_cliente_por_id(id_fornecedor_cliente, db)
    
    for_cli.nome = fornecedor_cliente_request.nome
    
    db.add(for_cli)
    db.commit()
    db.refresh(for_cli)
    
    return for_cli

# Delete
@router.delete('/{id_fornecedor_cliente}', status_code = 204)
def deletar_fornecedor_cliente(id_fornecedor_cliente: int,
                            db: Session=Depends(get_db)):

    for_cli = consultar_fornecedor_cliente_por_id(id_fornecedor_cliente, db)
    
    db.delete(for_cli)
    db.commit()

def consultar_fornecedor_cliente_por_id(id_fornecedor_cliente: int,
                        db: Session=Depends(get_db)) -> FornecedorCliente:
    fornecedor_cliente: FornecedorCliente = db.get(FornecedorCliente, id_fornecedor_cliente)
    
    if fornecedor_cliente is None:
        raise NotFound('Fornecedor/Cliente')
    
    return fornecedor_cliente