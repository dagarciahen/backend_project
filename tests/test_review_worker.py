from unittest.mock import Mock
import pytest
from app.repository.repository import ReviewRepository 
from app.models.dto import ReviewStatus
from app.messaging.review_worker import RabbitMQWorker
from app.config.rabbitmq import RabbitMQ
from app.models.models import ReviewCreated


def test_consumes_from_exchanges():
    rabbitmq = Mock(spec=RabbitMQ)
    repository = Mock(spec=ReviewRepository)
    worker = RabbitMQWorker(rabbitmq, repository)
    connection = rabbitmq.get_connection.return_value
    channel = connection.channel.return_value

    worker.consume()
    channel.basic_consume.assert_called_once_with(queue="review.processing", on_message_callback=worker.parser)
    channel.start_consuming.assert_called_once()
    connection.close.assert_called_once()

def test_process_ok():
    rabbitmq = Mock(spec=RabbitMQ)
    repository = Mock(spec=ReviewRepository)
    worker = RabbitMQWorker(rabbitmq, repository)

    worker.process(ReviewCreated(review_id=5))

    repository.update_status.assert_called_once_with(5, ReviewStatus.PROCESSED)
def test_parser_ok():
    rabbitmq = Mock(spec=RabbitMQ)
    repository = Mock(spec=ReviewRepository)
    channel = Mock()
    method = Mock()
    method.delivery_tag = 1 
    worker = RabbitMQWorker(rabbitmq, repository)
    body = b'{"review_id" : 5}'
    worker.parser(channel, method, None, body)

    repository.update_status.assert_called_once_with(5, ReviewStatus.PROCESSED)
    channel.basic_nack.assert_not_called()
    channel.basic_ack.assert_called_once_with(delivery_tag=1)


