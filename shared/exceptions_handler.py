from fastapi import Request
from fastapi.responses import JSONResponse

from shared.exceptions import ContaNotFound, FornecedorNotFound


async def conta_not_found_handler(request: Request, exc: ContaNotFound):
    return JSONResponse(
        status_code=404,
        content={'message': f'Oops! Esta conta não foi encontrada!'}
    )

async def fornecedor_not_found_handler(request: Request, exc: FornecedorNotFound):
    return JSONResponse(
        status_code=404,
        content={'message': f'Oops! Fornecedor não encontrado na base de dados!'}
    )