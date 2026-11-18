from abc import ABC, abstractmethod
from Dto import *
from typing import List


class ReviewService(ABC):
    @abstractmethod
    def publish_review(self, comment: str, rating: int) -> ReviewDto:
        pass

    @abstractmethod
    def get_review_by_id(self, review_id: int) -> ReviewDto:
        pass 

    @abstractmethod
    def update_review(self, review_id: int, new_comment: str, new_rating: int, review_date: date) -> ReviewDto:
        pass

    @abstractmethod 
    def delete_review(self, review_id: int) -> None:
        pass


class ReviewServiceV1(ReviewService):
    def __init__(self, client: BookClient, repository: ReviewRepository, queue: ReviewQueue) -> None:
        self.client = client
        self.repository = repository
        self.queue = queue 


    def publish_review(self, dto: CreateReviewDto, reviewer_id: int) -> ReviewDto:
        if not( 1 <= dt.rating <= 5):
            raise InvalidRatingError()
        if self.client.get_by_id(dto.book_id) is None:
            raise BookNotFoundError()

        review_id = self.repository.save_pending(dto)
        self.queue.publish_for_enrichment(review_id)
        return review_id

    



