import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routers import contas_pagar_receber_router
from shared.exceptions import NotFound


app = FastAPI()
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)

@app.get('/')
def hello_world() -> dict:
    return {'message': 'Hello, World!'}

app.include_router(contas_pagar_receber_router.router)

@app.exception_handler(NotFound)
async def not_found_excepion_handler(request: Request, exc: NotFound):
    return JSONResponse(
        status_code=404,
        content={'message': f'Oops! {exc.name} não encontrada!'}
    )

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8001, reload=True)