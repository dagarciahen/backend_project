import requests
from typing import List, Optional
from abc import ABC, abstractmethod
from exceptions import *
from Dto import *

class BookClient(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[BookDto]:
        pass

    @abstractmethod
    def get_by_ids(self, ids: List[int]) -> BookSearchResultDto:
        pass

    @abstractmethod
    def searc(self, query: str) -> BookSearchResultDto:
        pass

class GutendexClient(BookClient):
    BASE_URL = "url"

    def get_by_id(self, id: int) -> Optional[BookDto]:
        resp = self._get(f"{self.BASE_URL}/{id}")
        if resp.status_code == 404:
            return None
        return self._to_book_dto(resp.json())
    
    def get_by_ids(self, ids: List[int]) -> BookSearchResultDto:
        resp = self._get(self.BASE_URL, params ={"ids": ",".join(map(str, ids))})
        return self._to_result_dto(resp.json())

    def search(self, query: str) -> BookSearchResultDto:
        resp = self._get(self.BASE_URL, params ={"search": query})
        return self._to_result_dto(resp.json())


    def _get(self, url: str, params: dict = None) -> request.Response:
        try:
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code != 404:
                resp.raise_for_status()
            return resp
        except requests.RequestException:
            raise ExternalApiError()

    def _to_book_dto(self, data: dict) -> BookDto:
        return BookDto(
            id=data["id"],
            title=data["title"],
            subjects=data["subjects"],
            authors=[a["name"] for a in data["authors"]],
            summaries=data["summaries"],
            translators=[t["name"] for t in data["translators"]],
            bookshelves=data["bookshelves"],
            languages=data["languages"],
            copyright=data["copyright"],
            media_type=data["media_type"],
            formats=data["formats"],
            download_count=data["download_count"],
        )
    
    def _to_result_dto(self, data: dict) -> BookSearchResultDto:
        return BookSearchResultDto(
            count=data["count"],
            next=data["next"],
            prev=data["previous"],
            results=[self._to_book_dto(b) for b in data["results"]],
        )