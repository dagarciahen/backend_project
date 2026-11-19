from abc import ABC, abstractmethod
from Dto import *
from exceptions import *
from typing import List
from book_client import BookClient

class BookService(ABC):
    @abstractmethod
    def get_book_by_id(self, id: int) -> BookSearchResultDto:
        pass

    @abstractmethod
    def get_books_by_id(self, ids: List[int]) -> BookSearchResultDto:
        pass

    @abstractmethod
    def get_books_by_keywords(self, query: str) -> BookSearchResultDto:
        pass


class BookServiceV1(BookService):
    def __init__(self, client: BookClient) -> None:
        self.client = client 

    def get_book_by_id(self, id: int) -> BookDto:
        book = self.client.get_by_id(id)
        if book is None:
            raise BookNotFoundError()
        return book
