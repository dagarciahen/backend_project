from unittest.mock import Mock 
from app.models.models import Review, ReviewCreated
from datetime import date 
from app.messaging.review_queue import ReviewQueue
from app.models.dto import CreateReviewDto, ReviewDto, ReviewStatus, BookDto
from app.client.book_client import BookClient
from app.services.review_service import ReviewServiceV1
from app.repository.repository import ReviewRepository

def test_publish_review_ok():
    client= Mock(spec=BookClient)
    repository = Mock(spec=ReviewRepository)
    queue = Mock(spec=ReviewQueue)
    service = ReviewServiceV1(client, repository, queue)
    service.validator = Mock()
    service.mapper = Mock()

    dto = CreateReviewDto(1, 3, "Excelent Book")
    review = Mock(spec=Review)
    saved = Mock(spec=Review)
    saved.review_id = 2
    service.mapper.to_entity.return_value = review
    repository.save.return_value = saved

    expected_dto = Mock(spec=ReviewDto)
    service.mapper.to_dto.return_value = expected_dto
    result = service.publish_review(dto, 8)
    assert result is expected_dto

    repository.save.assert_called_once_with(review, status=ReviewStatus.PENDING)
    service.mapper.to_dto.assert_called_once_with(saved)
    queue.publish_review_created.assert_called_once_with(ReviewCreated(review_id=2))
    
    
    

def test_update_review_ok():
    client = Mock(spec=BookClient)
    repository = Mock(spec=ReviewRepository)
    queue = Mock(spec=ReviewQueue)

    service = ReviewServiceV1(client, repository, queue)
    service.validator = Mock()
    service.mapper = Mock()

    old_review = Mock(spec=Review)
    old_review.review_id = 5
    old_review.reviewer_id = 8
    repository.get_by_id.return_value = old_review

    updated = Mock(spec=Review)
    updated.review_id = 5
    repository.update.return_value = updated

    expected_dto = Mock(spec=ReviewDto)
    service.mapper.to_dto.return_value = expected_dto

    result = service.update_review(5, "Excellent", 4, reviewer_id=8)

    assert result is expected_dto
    service.validator.validate_update.assert_called_once_with(4, "Excellent")
    repository.update.assert_called_once_with(5, "Excellent", 4, status=ReviewStatus.PENDING)
    queue.publish_review_created.assert_called_once_with(ReviewCreated(review_id=5))
    service.mapper.to_dto.assert_called_once_with(updated)
    

def test_get_review_ok():
    client= Mock(spec=BookClient)
    repository = Mock(spec=ReviewRepository)
    queue = Mock(spec=ReviewQueue)
    service = ReviewServiceV1(client, repository, queue)
    service.mapper = Mock()
    expected_dto = Mock(spec=ReviewDto)
    service.mapper.to_dto.return_value = expected_dto

    repository.get_by_id.return_value = expected_dto
    result = service.get_review(1)
    assert result is expected_dto
    repository.get_by_id.assert_called_once_with(1)

def test_delete_review_ok():
    client= Mock(spec=BookClient)
    repository = Mock(spec=ReviewRepository)
    queue = Mock(spec=ReviewQueue)
    review = Mock(spec=ReviewDto)
    review.review_id = 1
    review.reviewer_id = 2
    repository.get_by_id.return_value= review

    service = ReviewServiceV1(client, repository, queue)

    repository.delete.return_value = review
    service.delete_review(1,2)
    repository.delete.assert_called_once_with(1,2)
    


    
