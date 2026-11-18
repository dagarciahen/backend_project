from abc import ABC, abstractmethod
from book_client import *
from exceptions import *
from Dto import *
from typing import List


class ReviewService(ABC):
    @abstractmethod
    def publish_review(self, dto: CreateReviewDto, reviewer_id: int) -> ReviewDto:
        pass

    @abstractmethod
    def get_review(self, review_id: int) -> ReviewDto:
        pass 

    @abstractmethod
    def update_review(self, review_id: int, comment: str, rating: int, review_date: date) -> ReviewDto:
        pass

    @abstractmethod 
    def delete_review(self, review_id: int, reviewer_id: int) -> None:
        pass


class ReviewServiceV1(ReviewService):
    def __init__(self, client: BookClient, repository: ReviewRepository, queue: ReviewQueue) -> None:
        self.client = client
        self.repository = repository
        self.queue = queue 


    def publish_review(self, dto: CreateReviewDto, reviewer_id: int) -> ReviewDto:
        """
        when an user post a review (sync) the review will be saved on db with status pending returns 202
        """
        if not( 1 <= dto.rating <= 5):
            raise InvalidRatingError()
        if self.client.get_by_id(dto.book_id) is None:
            raise BookNotFoundError()
        if len(dto.comment) == 0:
            raise InvalidCommentError()


        review= self.repository.save(dto, reviewer_id, status=ReviewStatus.PENDING)
        self.queue.publish_review_created(review.review_id)
        return review


    def get_review(self, review_id: int) -> ReviewDto:
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundError
        return review
    
    def update_review(self, review_id: int, comment: str, rating: int, reviewer_id: int) -> ReviewDto:
        if not(1 <= rating <= 5):
            raise InvalidRatingError()
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundError()
        if review.reviewer_id != reviewer_id:
            raise ReviewerNotFoundError()
        if len(comment) == 0:
            raise InvalidCommentError()
        updated = self.repository.update(review_id, comment, rating, status=ReviewStatus.PENDING)
        self.queue.publish_review_created(review.review_id)
        return updated


    def delete_review(self, review_id: int, reviewer_id: int) -> None:
        review = self.repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundError
        if review.reviewer_id != reviewer_id:
            raise ReviewerNotFoundError()
        self.repository.delete(review_id)



