from unittest.mock import Mock

import pytest

from app.client.book_client import BookClient
from app.exceptions import BookNotFoundError, InvalidCommentError, InvalidRatingError
from app.models.dto import CreateReviewDto
from app.services.review_validator import MAX_COMMENT_LENGTH, ReviewValidator


@pytest.fixture
def client():
    return Mock(spec=BookClient)


@pytest.fixture
def validator(client):
    return ReviewValidator(client)


def test_validate_create_ok(validator, client):
    client.get_by_id.return_value = Mock()
    validator.validate_create(CreateReviewDto(1, 5, "good book"))


def test_validate_create_comment_at_limit_ok(validator, client):
    client.get_by_id.return_value = Mock()
    validator.validate_create(CreateReviewDto(1, 5, "a" * MAX_COMMENT_LENGTH))


def test_validate_create_comment_too_long(validator, client):
    with pytest.raises(InvalidCommentError):
        validator.validate_create(CreateReviewDto(1, 5, "a" * (MAX_COMMENT_LENGTH + 1)))
    client.get_by_id.assert_not_called()


@pytest.mark.parametrize("comment", ["", "   "])
def test_validate_create_blank_comment(validator, comment):
    with pytest.raises(InvalidCommentError):
        validator.validate_create(CreateReviewDto(1, 5, comment))


@pytest.mark.parametrize("rating", [0, 6])
def test_validate_create_invalid_rating(validator, rating):
    with pytest.raises(InvalidRatingError):
        validator.validate_create(CreateReviewDto(1, rating, "good book"))


def test_validate_create_book_not_found(validator, client):
    client.get_by_id.return_value = None
    with pytest.raises(BookNotFoundError):
        validator.validate_create(CreateReviewDto(999, 5, "good book"))


def test_validate_update_comment_too_long(validator):
    with pytest.raises(InvalidCommentError):
        validator.validate_update(4, "a" * (MAX_COMMENT_LENGTH + 1))


def test_validate_update_invalid_rating(validator):
    with pytest.raises(InvalidRatingError):
        validator.validate_update(6, "good book")
