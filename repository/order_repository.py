from bson import ObjectId
from domain.order import Order
from database import orders_collection

class OrderRepository:
    def listar(self):
        orders = list(orders_collection.find())
        for order in orders:
            order["id"] = str(order["_id"])
            del order["_id"]
        return orders

    def buscar_por_id(self, id: str):
        try:
            obj_id = ObjectId(id)
        except:
            return None

        order = orders_collection.find_one({"_id": obj_id})
        if order:
            order["id"] = str(order["_id"])
            del order["_id"]
        return order

    def adicionar(self, order: Order):
        data = order.dict(exclude_unset=True)
        result = orders_collection.insert_one(data)
        order.id = str(result.inserted_id)
        return order

    def atualizar(self, id: str, dados: dict):
        try:
            obj_id = ObjectId(id)
        except:
            return None

        result = orders_collection.update_one({"_id": obj_id}, {"$set": dados})
        if result.modified_count == 0:
            return None
        return self.buscar_por_id(id)

    def remover(self, id: str):
        try:
            obj_id = ObjectId(id)
        except:
            return None

        result = orders_collection.delete_one({"_id": obj_id})
        return result.deleted_count > 0
