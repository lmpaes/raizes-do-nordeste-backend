from fastapi import FastAPI
from app.api.routes.usuario_routes import router as usuario_router
from app.api.routes.auth_routes import router as auth_router

app = FastAPI(title="Raízes do Nordeste API")

# Registrar rotas
app.include_router(usuario_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API funcionando corretamente"}