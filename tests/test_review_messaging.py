import json
from unittest.mock import Mock

import pytest

from app.exceptions import PublishError
from app.messaging.review_queue import RabbitMQReviewQueue
from app.models.models import ReviewCreated


def test_publish_uses_exchange_and_routing_key():
    rabbitmq = Mock()
    connection = rabbitmq.get_connection.return_value
    channel = connection.channel.return_value
    queue = RabbitMQReviewQueue(rabbitmq)

    queue.publish_review_created(ReviewCreated(review_id=5))

    kwargs = channel.basic_publish.call_args.kwargs
    assert kwargs["exchange"] == "review"
    assert kwargs["routing_key"] == "review.created"


def test_content_body_ok():
    rabbitmq = Mock()
    connection = rabbitmq.get_connection.return_value
    channel = connection.channel.return_value
    queue = RabbitMQReviewQueue(rabbitmq)

    queue.publish_review_created(ReviewCreated(review_id=5))

    kwargs = channel.basic_publish.call_args.kwargs
    assert json.loads(kwargs["body"]) == {"review_id": 5}


def test_message_is_persistent():
    rabbitmq = Mock()
    connection = rabbitmq.get_connection.return_value
    channel = connection.channel.return_value
    queue = RabbitMQReviewQueue(rabbitmq)

    queue.publish_review_created(ReviewCreated(review_id=5))

    kwargs = channel.basic_publish.call_args.kwargs
    assert kwargs["properties"].delivery_mode == 2


def test_connection_closes_after_error():
    rabbitmq = Mock()
    connection = rabbitmq.get_connection.return_value
    channel = connection.channel.return_value
    queue = RabbitMQReviewQueue(rabbitmq)
    channel.basic_publish.side_effect = Exception("rabbit down")
    with pytest.raises(PublishError):
        queue.publish_review_created(ReviewCreated(review_id=5))
    connection.close.assert_called_once()
