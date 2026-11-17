from abc import ABC, abstractmethod
from Dto import BookSearchResultDto
from fastapi import HTTPException

from exceptions import *

#interfaces
class BookController(ABC):
    @abstractmethod
    def search_books_by_id(self, id: int) -> BookSearchResultDto:
        pass

    @abstractmethod
    def search_books_by_keyword(self, keywords: str):
        pass


class BookControllerV1(BookController):
    GENERAL_ERROR_MESSAGE = "Something went wrong"

    def __init__(self, service: BookService) -> None:
        super().__init__()
        self.service = service

    def fetch_books(self, skip= 0, limit: int = 10):
        return self.service.get_books_by_id(skip, limit)

    




class Re