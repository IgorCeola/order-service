from fastapi import APIRouter, HTTPException
from usecases.order_usecase import OrderUseCase
from repository.order_repository import OrderRepository

router = APIRouter()
repo = OrderRepository()
usecase = OrderUseCase(repo)

@router.get("/pedidos")
def listar_orders():
    return usecase.listar_orders()

@router.get("/pedidos/{id}")
def buscar_order(id: str):
    order = usecase.buscar_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return order

# @router.post("/pedidos")
# def adicionar_order(dados: dict):
#     return usecase.adicionar_order(dados)

@router.put("/pedidos/{id}")
def atualizar_order(id: str, dados: dict):
    atualizado = usecase.atualizar_order(id, dados)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return atualizado

@router.delete("/pedidos/{id}")
def remover_order(id: str):
    removido = usecase.remover_order(id)
    if not removido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado.")
    return {"mensagem": "Order removida com sucesso"}

@router.post("/pedidos")
def adicionar_order(dados: dict):
    try:
        return usecase.adicionar_order(dados)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

