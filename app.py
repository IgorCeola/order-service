from fastapi import FastAPI
from controllers.order_controller import router

app = FastAPI(title="Order Service")

app.include_router(router)

@app.get("/")
def root():
    return {"mensagem": "Order Service ativo, Capitão!"}
