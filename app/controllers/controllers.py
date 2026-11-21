from abc import ABC, abstractmethod

from fastapi import HTTPException

from app.exceptions import *
from app.models.dto import *
from app.services.book_service import BookService
from app.services.review_service import ReviewService
# ruff: noqa


#interfaces
class BookController(ABC):
    @abstractmethod
    def search_book_by_id(self, book_id: int) -> BookDto:
        pass

    @abstractmethod
    def search_books_by_id(self, ids: list[int]) -> BookSearchResultDto:
        pass

    @abstractmethod
    def search_books_by_keyword(self, keywords: str) -> BookSearchResultDto:
        pass

class ReviewController(ABC):
    @abstractmethod
    def publish_review(self, dto: CreateReviewDto, reviewer_id: int)-> ReviewDto:
        pass

    @abstractmethod
    def get_review(self, review_id: int) -> ReviewDto:
        pass

    @abstractmethod
    def update_review(self, review_id: int, comment: str, rating: int, reviewer_id: int ) -> ReviewDto:
        pass

    @abstractmethod
    def delete_review(self, review_id: int, reviewer_id: int) -> None:
        pass

class BookControllerV1(BookController):
    GENERAL_ERROR_MESSAGE = "Something went wrong"

    def __init__(self, service: BookService) -> None:
        super().__init__()
        self.service = service

    def search_book_by_id(self, book_id: int) -> BookDto:
        try:
            return self.service.get_book_by_id(book_id)
        except BookNotFoundError:
            raise HTTPException(status_code=404, detail= "book not found")
        except ExternalApiError:
            raise HTTPException(status_code=503, detail= "Books provider not found")
        except Exception:
            raise HTTPException(status_code=500, detail=self.GENERAL_ERROR_MESSAGE)

    def search_books_by_keyword(self, keywords) -> Optional[BookSearchResultDto]:
        try:
            return self.service.get_books_by_keywords(keywords)
        except BookNotFoundError:
            raise HTTPException(status_code = 503, detail = "Book not found")
        except ExternalApiError:
            raise HTTPException(status_code = 503, detail = "Books provider not found")
        except Exception:                                                             
            raise HTTPException(status_code =500, detail = self.GENERAL_ERROR_MESSAGE)

class ReviewControllerV1(ReviewController):
    GENERAL_ERROR_MESSAGE = "something went wrong"

    def __init__(self, service: ReviewService) -> None:
        super().__init__()
        self.service = service

    def publish_review(self, dto: CreateReviewDto, reviewer_id: int)-> ReviewDto:
        try:
            return self.service.publish_review(dto, reviewer_id)
        except BookNotFoundError:
            raise HTTPException(status_code=404, detail="book not found")
        except InvalidRatingError:
            raise HTTPException(status_code = 422, detail="invalid rating error")
        except InvalidCommentError:
            raise HTTPException(status_code= 422, detail="Invalid comment")
        except ExternalApiError:
            raise HTTPException(status_code = 503, detail= "Books provider failed")
        except Exception:
            raise HTTPException(status_code = 500, detail=self.GENERAL_ERROR_MESSAGE)

    def get_review(self, review_id: int) -> ReviewDto:
        try:
            return self.service.get_review(review_id)
        except ReviewNotFoundError:
            raise HTTPException(status_code=404, detail="Review id not found")
        except Exception:
            raise HTTPException(status_code=500, detail= self.GENERAL_ERROR_MESSAGE)

    def update_review(self, review_id: int, comment: str, rating: int, reviewer_id: int ) -> ReviewDto:
        try:
            return self.service.update_review(review_id, comment, rating, reviewer_id)
        except ReviewNotFoundError:
            raise HTTPException(status_code=404, detail= "review id not found")
        except ReviewerNotFoundError:
            raise HTTPException(status_code=404, detail="Reviewer id not found")
        except InvalidRatingError:
            raise HTTPException(status_code = 422, detail="invalid rating error")
        except InvalidCommentError:
            raise HTTPException(status_code= 422, detail="Invalid comment")
        except ExternalApiError:
            raise HTTPException(status_code = 503, detail= "Books provider failed")
        except Exception:
            raise HTTPException(status_code=500, detail= self.GENERAL_ERROR_MESSAGE)


    def delete_review(self, review_id: int, reviewer_id: int) -> None:
        try:
            return self.service.delete_review(review_id, reviewer_id)
        except ReviewNotFoundError:
            raise HTTPException(status_code=404, detail = "review id not found")
        except ReviewerNotFoundError:
            raise HTTPException(status_code=404, detail = "reviewer id not found")
        except Exception:
            raise HTTPException(status_code=500, detail=self.GENERAL_ERROR_MESSAGE)

