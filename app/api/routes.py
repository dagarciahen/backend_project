from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import RedirectResponse

from app.client.book_client import GutendexClient
from app.config.database_settings import Database
from app.config.rabbitmq import RabbitMQ
from app.controllers.controllers import (
    BookController,
    BookControllerV1,
    ReviewController,
    ReviewControllerV1,
)
from app.messaging.review_queue import RabbitMQReviewQueue
from app.models.dto import *
from app.repository.repository import MariaDbReviewRepository
from app.services.authentication import get_current_reviewer_id
from app.services.book_service import BookServiceV1
from app.services.review_service import ReviewServiceV1

router = APIRouter()
MAX_BOOK_ID = MAX_ID = 2_147_483_647
database = Database()


## helper methods for dependency injectipon
def get_book_controller() -> BookController:
    return BookControllerV1(BookServiceV1(GutendexClient()))


def get_review_controller() -> ReviewController:
    service = ReviewServiceV1(
        GutendexClient(),
        MariaDbReviewRepository(database),
        RabbitMQReviewQueue(RabbitMQ()),
    )
    return ReviewControllerV1(service)


##books


# https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values-with-defaults
@router.get("/books/search")
def search_books(
    q: Annotated[str, Query(min_length=1, max_length=100)],
    controller: Annotated[BookController, Depends(get_book_controller)],
) -> BookSearchResultDto:
    return controller.search_books_by_keyword(q)


@router.get("/books/{book_id}", status_code=200)
def get_book(
    book_id: int, controller: Annotated[BookController, Depends(get_book_controller)]
) -> BookDto:
    if book_id <= 0 or book_id > MAX_BOOK_ID:
        raise HTTPException(status_code=422, detail="book_id out of range")
    return controller.search_book_by_id(book_id)


@router.get("/book/{book_id}", include_in_schema=False)
def legacy_book(book_id: int):
    return RedirectResponse(url=f"/books/{book_id}", status_code=307)


##reviews


@router.post("/review", status_code=202)
def post_review(
    dto: CreateReviewDto,
    reviewer_id: Annotated[int, Depends(get_current_reviewer_id)],
    controller: Annotated[ReviewController, Depends(get_review_controller)],
) -> ReviewDto:
    return controller.publish_review(dto, reviewer_id)


@router.get("/review/{review_id}")
def get_review(
    review_id: int,
    response: Response,
    controller: Annotated[ReviewController, Depends(get_review_controller)],
) -> ReviewDto:
    review = controller.get_review(review_id)
    if review.status == "processing":
        response.status_code = 202
    return review


@router.put("/review/{review_id}", status_code=202)
def put_review(
    review_id: int,
    dto: UpdateReviewDto,
    reviewer_id: Annotated[int, Depends(get_current_reviewer_id)],
    controller: Annotated[ReviewController, Depends(get_review_controller)],
) -> ReviewDto:
    if review_id <= 0 or review_id > MAX_ID:
        raise HTTPException(status_code=422, detail="review_id out of range")
    return controller.update_review(review_id, dto.comment, dto.rating, reviewer_id)


@router.delete("/review/{review_id}")
def delete_review(
    review_id: int,
    reviewer_id: Annotated[int, Depends(get_current_reviewer_id)],
    controller: Annotated[ReviewController, Depends(get_review_controller)],
):
    controller.delete_review(review_id, reviewer_id)
    return {"detail": "reviewer deleted"}
