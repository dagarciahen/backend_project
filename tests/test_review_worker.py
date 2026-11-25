from unittest.mock import Mock

from app.client.book_client import BookClient
from app.config.rabbitmq import RabbitMQ
from app.exceptions import ExternalApiError
from app.messaging.review_worker import RabbitMQWorker
from app.models.dto import BookDto, PersonDto
from app.models.models import Review, ReviewCreated
from app.repository.repository import ReviewRepository


def build_worker():
    rabbitmq = Mock(spec=RabbitMQ)
    repository = Mock(spec=ReviewRepository)
    client = Mock(spec=BookClient)
    return RabbitMQWorker(rabbitmq, repository, client), rabbitmq, repository, client


def build_review():
    return Review(reviewer_id=1, book_id=10, comment="good", rating=5, review_id=5)


def build_book():
    return BookDto(
        id=10,
        title="Frankenstein",
        subjects=[],
        authors=[
            PersonDto(1797, 1851, "Shelley, Mary"),
            PersonDto(None, None, "Other, Author"),
        ],
        summaries=[],
        translators=[],
        bookshelves=[],
        languages=["en"],
        copyright=False,
        media_type="Text",
        formats={"image/jpeg": "https://cover.jpg"},
        download_count=1,
    )


def test_consumes_from_exchanges():
    worker, rabbitmq, _, _ = build_worker()
    connection = rabbitmq.get_connection.return_value
    channel = connection.channel.return_value

    worker.consume()
    channel.basic_consume.assert_called_once_with(
        queue="review.processing", on_message_callback=worker.parser
    )
    channel.start_consuming.assert_called_once()
    connection.close.assert_called_once()


def test_process_ok():
    worker, _, repository, client = build_worker()
    repository.get_by_id.return_value = build_review()
    client.get_by_id.return_value = build_book()

    worker.process(ReviewCreated(review_id=5))

    client.get_by_id.assert_called_once_with(10)
    repository.save_enrichment.assert_called_once_with(
        5, "Frankenstein", "Shelley, Mary, Other, Author", "https://cover.jpg"
    )


def test_process_book_not_found_marks_processed_without_data():
    worker, _, repository, client = build_worker()
    repository.get_by_id.return_value = build_review()
    client.get_by_id.return_value = None

    worker.process(ReviewCreated(review_id=5))

    repository.save_enrichment.assert_called_once_with(5, None, None, None)


def test_process_review_deleted_does_nothing():
    worker, _, repository, client = build_worker()
    repository.get_by_id.return_value = None

    worker.process(ReviewCreated(review_id=5))

    client.get_by_id.assert_not_called()
    repository.save_enrichment.assert_not_called()


def test_parser_ok():
    worker, _, repository, client = build_worker()
    channel = Mock()
    method = Mock()
    method.delivery_tag = 1
    repository.get_by_id.return_value = build_review()
    client.get_by_id.return_value = build_book()

    worker.parser(channel, method, None, b'{"review_id" : 5}')

    repository.save_enrichment.assert_called_once()
    channel.basic_nack.assert_not_called()
    channel.basic_ack.assert_called_once_with(delivery_tag=1)


def test_parser_invalid_body_nack_without_requeue():
    worker, _, repository, _ = build_worker()
    channel = Mock()
    method = Mock()
    method.delivery_tag = 1

    worker.parser(channel, method, None, b"not json")

    channel.basic_nack.assert_called_once_with(delivery_tag=1, requeue=False)
    channel.basic_ack.assert_not_called()
    repository.save_enrichment.assert_not_called()


def test_parser_external_api_error_nack_with_requeue():
    worker, _, repository, client = build_worker()
    channel = Mock()
    method = Mock()
    method.delivery_tag = 1
    repository.get_by_id.return_value = build_review()
    client.get_by_id.side_effect = ExternalApiError()

    worker.parser(channel, method, None, b'{"review_id" : 5}')

    channel.basic_nack.assert_called_once_with(delivery_tag=1, requeue=True)
    channel.basic_ack.assert_not_called()
