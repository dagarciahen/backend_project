from abc import ABC, abstractmethod
from book_client import *
from exceptions import *
from repository import ReviewRepository
from review_queue import ReviewQueue
from Dto import *
from typing import List
from review_validator import ReviewValidator
from review_mapper import ReviewMapper

#interface

class ReviewService(ABC):
    @abstractmethod
    def publish_review(self, dto: CreateReviewDto, reviewer_id: int) -> ReviewDto:
        pass

    @abstractmethod
    def get_review(self, review_id: int) -> ReviewDto:
        pass 

    @abstractmethod
    def update_review(self, review_id: int, comment: str, rating: int, reviewer_id: int) -> ReviewDto:
        pass

    @abstractmethod 
    def delete_review(self, review_id: int, reviewer_id: int) -> None:
        pass


class ReviewServiceV1(ReviewService):
    def __init__(self, client: BookClient, repository: ReviewRepository, queue: ReviewQueue) -> None:
        self.client = client
        self.repository = repository
        self.queue = queue 
        self.validator = ReviewValidator(client)
        self.mapper = ReviewMapper()
        self.queue = queue


    def publish_review(self, dto: CreateReviewDto, reviewer_id: int) -> ReviewDto:
        """
        when an user post a review (sync) the review will be saved on db with status pending returns 202
        """
        self.validator.validate_create(dto)
        review = self.mapper.to_entity(dto, reviewer_id)
        saved = self.repository.save(review, status=ReviewStatus.PENDING)
        self.queue.publish_review_created(saved.review_id)
        return self.mapper.to_dto(saved)

    def get_review(self, review_id: int) -> ReviewDto:
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundError
        return review
    
    def update_review(self, review_id: int, comment: str, rating: int, reviewer_id: int) -> ReviewDto:
        self.validator.validate_update(rating, comment)
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ReviewerNotFoundError
        if review.reviewer_id != reviewer_id:
            raise ReviewerNotFoundError()
        
        updated = self.repository.update(review_id, comment, rating, status=ReviewStatus.PENDING)
        self.queue.publish_review_created(updated.review_id)
        return self.mapper.to_dto(updated)


    def delete_review(self, review_id: int, reviewer_id: int) -> None:
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundError
        if review.reviewer_id != reviewer_id:
            raise ReviewerNotFoundError()
        self.repository.delete(review_id)



