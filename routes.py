
## https://stackoverflow.com/questions/27933802/difference-between-controller-and-router

from fastapi import FastAPI, APIRouter, Depends, Query
from controllers import BookController, BookControllerV1, ReviewController, ReviewControllerV1
from book_client import GutendexClient
from book_service import BookService 
from review_service import ReviewService

app = FastAPi()
router = APIRouter()
MAX_BOOK_ID = 2_147_483_647


## helper methods for dependency injectipon
def get_book_controller() -> BookController:
    return BookControllerV1(BookService(GutendexClient()))

def get_review_controller() -> ReviewController:
    service = ReviewControllerV1(GutendexClient(), MariaDbReviewRepository(), RabbitMqReviewQueue())
    return ReviewControllerV1(service)


#https://fastapi.tiangolo.com/tutorial/query-params-str-validations/#query-parameter-list-multiple-values-with-defaults
@router.get("/book/search")
def search_books(q: Annotated[str, Query(min_length=1, max_length=100)], controller: BookController = Depends(get_book_controller())) ->  BookSearchResultDto:
    return controller.search_books_by_keyword(q)

@router.get("/book{book_id}", status_code = 202)
def get_book(book_id: int, controller: BookController = Depends(get_book_controller)) -> BookDto:
    if book_id <= 0 or book_id > MAX_BOOK_ID:
        raise HTTPException(status_code=422, detail="book_id out of range")
    return controller.search_books_by_id(book_id)
    

@router.get("/book")
def get_books(ids: Annotated[List[int], Query(min_length= 1, max_length=32)], controller: BookController = Depends(get_book_controller)) -> BookSearchResultDto:
    if any(i <=0 for i in ids):
        raise HttpException(status_code=422, detail="ids must be positive")
    return controller.search_books_by_ids(ids)



