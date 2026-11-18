import pytest
from unittest.mock import Mock
from fastapi import HTTPException

from Dto import *
from exceptions import *
from review_service import ReviewService
from controllers import ReviewControllerV1

class FakeReviewRepository(ReviewRepository):
    def __init__(self):
        self.reviews = {}
        self.next_id = 1

    def save(self, dto, reviewer_

















#for tda



@pytest.fixture
def service():
    return Mock(spec=ReviewService)


@pytest.fixture
def controller(service):
    return ReviewControllerV1(service)


def test_publish_review_ok(service, controller):
    expected = Mock(spec=ReviewDto)
    service.publish_review.return_value = expected
    
    service.publish_review.return_value = expected

    result = controller.publish_review(DTO, reviewer_id=7)

    assert result is expected
    service.publish_review.assert_called_once_with(DTO, 7)

def test_update_review_ok(service, controller):
    expected = Mock(spec=ReviewDto)
    service.publish_review.return_value =expected
    result = controller.update_review(5, "not so great", 4, reviewer_id=7)
    assert result is expected
    service.update_review.assert_called_once_with(5, "not so great", 4, 7)
    

@pytest.mark.parametrize("error, status", [
    (InvalidRatingError(), 400),
    (InvalidCommentError(), 400),
    (BookNotFoundError(), 404),
    (ExternalApiError(), 503),
    (RuntimeError("boom"), 500),
])
def test_publish_review_errors(controller, service, error, status):
    service.publish_review.side_effect = error

    with pytest.raises(HTTPException) as exc:
        controller.publish_review(DTO, reviewer_id=7)

    assert exc.value.status_code == status


def test_get_review_not_found(controller, service):
    service.get_review_by_id.side_effect = ReviewNotFoundError()

    with pytest.raises(HTTPException) as exc:
        controller.get_review(5)

    assert exc.value.status_code == 404


@pytest.mark.parametrize("error, status", [
    (ReviewNotFoundError(), 404),
    (NotReviewOwnerError(), 403),
    (InvalidRatingError(), 400),
])
def test_update_review_maps_errors(controller, service, error, status):
    service.update_review.side_effect = error

    with pytest.raises(HTTPException) as exc:
        controller.update_review(5, "new", 4, reviewer_id=7)

    assert exc.value.status_code == status


def test_delete_review_not_owner(controller, service):
    service.delete_review.side_effect = NotReviewOwnerError()

    with pytest.raises(HTTPException) as exc:
        controller.delete_review(5, reviewer_id=7)

    assert exc.value.status_code == 403