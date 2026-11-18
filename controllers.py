from abc import ABC, abstractmethod
from Dto import *
from review_service import ReviewService
from book_service import BookService
from fastapi import APIRouter, Depends HTTPException

from exceptions import *

#interfaces
class BookController(ABC):
    @abstractmethod
    def search_books_by_id(self, id: int) -> BookSearchResultDto:
        pass

    @abstractmethod
    def search_books_by_keyword(self, keywords: str):
        pass

class ReviewController(ABC):
    @abstractmethod
    def publish_review(self, dto: CreateReviewDto, reviewer_id: int)-> ReviewDto:
        pass

    @abstractmethod
    def get_review(self, id: int) -> ReviewDto:
        pass

    @abstractmethod
    def update_review(self, id: int, comment: str, rating: int ) -> ReviewDto:
        pass

    @abstractmethod
    def delete_review(self, id: int) -> None:
        pass



class ReviewControllerV1(ReviewController):

    router = APIRouter()
    def __init__(self, service: ReviewService) -> None:
        super().__init__()
        self.service = service

    def publish_review(self, dto: CreateReviewDto, reviewer_id: int) -> ReviewDto:



class BookControllerV1(BookController):
    GENERAL_ERROR_MESSAGE = "Something went wrong"

    def __init__(self, service: BookService) -> None:
        super().__init__()
        self.service = service

    def fetch_books(self, skip= 0, limit: int = 10):
        return self.service.get_books_by_id(skip, limit)

    




class ReviewControllerV1()