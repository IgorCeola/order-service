from domain.order import Order
from messaging.rabbitmq_client import RabbitMQClient

class OrderUseCase:
    def __init__(self, repository):
        self.repository = repository
        self.rabbit = RabbitMQClient()

    def listar_orders(self):
        return self.repository.listar()

    def buscar_order(self, id: str):
        return self.repository.buscar_por_id(id)    

    def validar_book(self, book_id: str):
        resp = self.rabbit.validate_book(book_id)
        return resp["valid"]

    def adicionar_order(self, dados: dict):
        if not self.validar_book(dados["book_id"]):
            raise ValueError("Livro não existe!")
        novo = Order(**dados)
        return self.repository.adicionar(novo)

    def atualizar_order(self, id: str, dados: dict):
        if "book_id" in dados:
            if not self.validar_book(dados["book_id"]):
                raise ValueError("Livro não existe!")
        return self.repository.atualizar(id, dados)
