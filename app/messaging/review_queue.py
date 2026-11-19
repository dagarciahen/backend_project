from abc import abstractmethod, ABC
from app.models.models import ReviewCreated
from app.config.rabbitmq import RabbitMQ
import pika
import json


##publisherr
##direct  change method 
class ReviewQueue(ABC):
    @abstractmethod
    def publish_review_created(self, event: ReviewCreated) -> None:
        pass

class RabbitMQReviewQueue(ReviewQueue):
    """
    declare queue and exchanges before publish if they does not exists thwy will be created 
    """
    EXCHANGE = "review"
    QUEUE = "review.processing"
    ROUTING_KEY = "review.created"

    def __init__(self, rabbitmq: RabbitMQ):
        self.rabbitmq = rabbitmq

    def publish_review_created(self, event: ReviewCreated) -> None:
        connection = self.rabbitmq.get_connection()
        try:
            channel = connection.channel()
            channel.exchange_declare(exchange= self.EXCHANGE, exchange_type="direct", durable=True)
            channel.queue_declare(queue=self.QUEUE, durable = True)
            channel.queue.bind(queue=self.QUEUE, exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY)
            channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY, body=json.dumps({"review_id": event.review_id}), properties=pika.BasicProperties(delivery_mode=2))
        finally:
            connection.close()



    