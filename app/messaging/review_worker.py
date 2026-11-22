import json
from abc import ABC, abstractmethod

from app.config.database_settings import Database
from app.config.rabbitmq import RabbitMQ
from app.models.dto import ReviewStatus
from app.models.models import ReviewCreated
from app.repository.repository import MariaDbReviewRepository

##publisherr


class ReviewWorker(ABC):
    @abstractmethod
    def process(self, event: ReviewCreated) -> None:
        pass

    @abstractmethod
    def parser(self, channel, method, properties, body):
        pass

    @abstractmethod
    def consume(self):
        pass


class RabbitMQWorker(ReviewWorker):
    EXCHANGE = "review"
    QUEUE = "review.processing"
    ROUTING_KEY = "review.created"

    def __init__(self, rabbitmq: RabbitMQ, repository: MariaDbReviewRepository):
        self.rabbitmq = rabbitmq
        self.repository = repository

    def process(self, event: ReviewCreated) -> None:
        self.repository.update_status(event.review_id, ReviewStatus.PROCESSED)

    def parser(self, channel, method, properties, body) -> None:
        # try to parser body could fail nack if fail ack if ok
        try:
            event = ReviewCreated(**json.loads(body))
            self.process(event)
        except json.JSONDecodeError:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            return
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self) -> None:
        connection = self.rabbitmq.get_connection()
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.EXCHANGE, exchange_type="direct", durable=True
            )
            channel.queue_declare(queue=self.QUEUE, durable=True)
            channel.queue_bind(
                queue=self.QUEUE, exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY
            )
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self.QUEUE, on_message_callback=self.parser)
            channel.start_consuming()
        finally:
            connection.close()


if __name__ == "__main__":
    worker = RabbitMQWorker(RabbitMQ(), MariaDbReviewRepository(Database()))
    worker.consume()
