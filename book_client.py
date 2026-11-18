import requests
from typing import List, Optional
from pydantic import TypeAdapter, ValidationError
from abc import ABC, abstractmethod
from exceptions import *
from Dto import *
from dotenv import load_dotenv
import os

load_dotenv()


_book = TypeAdapter(BookDto)
_result = TypeAdapter(BookSearchResultDto)

class BookClient(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BookDto]:
        pass

    @abstractmethod
    def get_by_ids(self, ids: List[int]) -> BookSearchResultDto:
        pass

    @abstractmethod
    def search(self, query: str) -> BookSearchResultDto:
        pass

class GutendexClient(BookClient):
    API_URL = os.getenv("URL")

    def get_by_id(self, id: int) -> Optional[BookDto]:
        resp = self._get(f"{self.API_URL}/{id}")
        if resp.status_code == 404:
            return None
        return self._parse(_book, resp)
    
    def get_by_ids(self, ids: List[int]) -> BookSearchResultDto:
        resp = self._get(self.API_URL, params ={"ids": ",".join(map(str, ids))})
        return self._parse(_result, resp)

    def search(self, query: str) -> BookSearchResultDto:
        resp = self._get(self.API_URL, params ={"search": query})
        return self._parse(_result, resp)


    def _get(self, url: str, params: dict = None) -> requests.Response:
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code != 404:
                resp.raise_for_status()
            return resp
        except requests.RequestException:
            raise ExternalApiError()

    def _parse(self, adapter: TypeAdapter, resp: requests.Response):
        try:
            return adapter.validate_python(resp.json())
        except (ValueError, ValidationError):
            raise ExternalApiError()

"""
    def _to_result_dto(self, data: dict) -> BookSearchResultDto:
        return BookSearchResultDto(
            count=data["count"],
            next=data["next"],
            prev=data["previous"],
            results=[self._to_book_dto(b) for b in data["results"]],
        )
"""