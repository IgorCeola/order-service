import pika
import json
import uuid
import os

class RabbitMQClient:
    def __init__(self):
        self.url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.corr_id = None

    def _connect(self):
        if self.connection and self.connection.is_open:
            return

        params = pika.URLParameters(self.url)
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def validate_book(self, book_id: str):

        self._connect()
        self.channel.queue_declare(queue="validate_book_queue")

        self.response = None
        self.corr_id = str(uuid.uuid4())

        message = {"book_id": book_id}

        self.channel.basic_publish(
            exchange='',
            routing_key='validate_book_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=json.dumps(message)
        )

        while self.response is None:
            self.connection.process_data_events()

        print("Enviado:", message, "correlation:", self.corr_id)

        return json.loads(self.response)
