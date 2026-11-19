from abc import ABC, abstractmethod
from models import Review
from Dto import ReviewDto, CreateReviewDto
class ReviewMapper:
    def to_entity(self, dto: CreateReviewDto, reviewer_id: int) -> Review:
        return Review(reviewer_id = reviewer_id, book_id = dto.book_id, comment=dto.comment, rating=dto.rating)

    def to_dto(self, review: Review) -> ReviewDto:
        return ReviewDto(review_id = review.review_id, book_id = review.book_id, reviewer_id = review.reviewer_id, rating = review.rating, comment = review.comment, review_date = review.review_date)
    
    