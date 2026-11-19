import json
from unittest.mock import Mock
import pytest

from app.models.models import ReviewCreated
from app.messaging.review_queue import RabbitMQReviewQueue


def test_publish_uses_exchange_and_routing_key():
    rabbitmq = Mock()
    channel = rabbitmq.get_connection.return_value.channel.return_value
    queue = RabbitMQReviewQueue(rabbitmq)

    queue.publish_review_created(ReviewCreated(review_id=5))

    kwargs = channel.basic_publish.call_args.kwargs
    assert kwargs["exchange"] == "review"
    assert kwargs["routing_key"] == "review.created"