from abc import ABC, abstractmethod
from Dto import *
from typing import List

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

    def get_books_by_id(self, ids: List[int]) -> BookSearchResultDto:
        books = []
        for id in ids:
            books.append(self.client.get_by_id(id))
            if book is not None:
                books.append(book)
            raise BooksNotFoundError()
        return BookSearchResultDto(count=len(books), next=None, prev=None, results=books)
    
    

