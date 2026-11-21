from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.controllers.controllers import ReviewControllerV1
from app.exceptions import *
from app.models.dto import *
from app.services.review_service import ReviewService


def test_publish_review_ok():
    service = Mock(spec=ReviewService)
    review_dto = Mock(spec=ReviewDto)
    create_review_dto = Mock(spec=CreateReviewDto)
    service.publish_review.return_value = review_dto
    controller = ReviewControllerV1(service)

    result = controller.publish_review(create_review_dto, 1)
    assert result is review_dto
    service.publish_review.assert_called_once_with(create_review_dto, 1)




def test_update_review_ok():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    review_dto = Mock(spec=ReviewDto)
    service.update_review.return_value = review_dto

    result = controller.update_review(5, "new", 4, 7)

    assert result is review_dto 
    service.update_review.assert_called_once_with(5, "new", 4, 7)

def test_publish_review_invalid_rating():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    create_review_dto = Mock(spec=CreateReviewDto)
    service.publish_review.side_effect = InvalidRatingError()

    with pytest.raises(HTTPException) as exc:
        controller.publish_review(create_review_dto, reviewer_id=7)
    assert exc.value.status_code == 422

def test_publish_review_invalid_comment():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    create_review_dto = Mock(spec=CreateReviewDto)
    service.publish_review.side_effect = InvalidCommentError()

    with pytest.raises(HTTPException) as exc:
        controller.publish_review(create_review_dto, reviewer_id=7)

    assert exc.value.status_code == 422


def test_publish_review_book_not_found():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    create_review_dto = Mock(spec=CreateReviewDto)
    service.publish_review.side_effect = BookNotFoundError()

    with pytest.raises(HTTPException) as exc:
        controller.publish_review(create_review_dto, reviewer_id=7)

    assert exc.value.status_code == 404


def test_publish_review_external_api_error():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    create_review_dto = Mock(spec=CreateReviewDto)
    service.publish_review.side_effect = ExternalApiError()

    with pytest.raises(HTTPException) as exc:
        controller.publish_review(create_review_dto, reviewer_id=7)

    assert exc.value.status_code == 503


def test_publish_review_unexpected_error():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    create_review_dto = Mock(spec=CreateReviewDto)
    service.publish_review.side_effect = RuntimeError("boom")

    with pytest.raises(HTTPException) as exc:
        controller.publish_review(create_review_dto, reviewer_id=7)

    assert exc.value.status_code == 500


def test_get_review_not_found():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    service.get_review.side_effect = ReviewNotFoundError()

    with pytest.raises(HTTPException) as exc:
        controller.get_review(5)

    assert exc.value.status_code == 404



def test_update_review_not_found():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    service.update_review.side_effect = ReviewNotFoundError()

    with pytest.raises(HTTPException) as exc:
        controller.update_review(5, "new", 4, reviewer_id=7)

    assert exc.value.status_code == 404


def test_update_review_reviewer_not_found():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    service.update_review.side_effect = ReviewerNotFoundError()

    with pytest.raises(HTTPException) as exc:
        controller.update_review(5, "new", 4, reviewer_id=7)

    assert exc.value.status_code == 404


def test_update_review_invalid_rating():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    service.update_review.side_effect = InvalidRatingError()

    with pytest.raises(HTTPException) as exc:
        controller.update_review(5, "new", 4, reviewer_id=7)

    assert exc.value.status_code == 422


def test_delete_review_reviewer_not_found():
    service = Mock(spec=ReviewService)
    controller = ReviewControllerV1(service)
    service.delete_review.side_effect = ReviewerNotFoundError()

    with pytest.raises(HTTPException) as exc:
        controller.delete_review(5, reviewer_id=7)

    assert exc.value.status_code == 404