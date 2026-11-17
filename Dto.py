from dataclasses import dataclass
from typing import List, dict, Optional
from datetime import date

@dataclass
class BookDto:
    id: int
    title: str
    subjects : List[str]
    authors: List[str]
    summaries: List[str]
    translators: List[str]
    bookshelves: List[str]
    languages: List[str]
    copyright: Optional[bool]
    media_type: str
    formats: dict[str, str]
    download_count: int

@dataclass
class BookSearchResultDto:
    count: Optional[int]
    next: Optional[str]
    prev: Optional[str]
    results: List[BookDto]
    
@dataclass
class PersonDto:
    birth_year: Optional[int]
    death_year: Optional[int]
    name : str


@dataclass
class CreateReviewDto:
    book_id: int
    rating: int
    comment: str

@dataclass
class ReviewerDto:
    reviewer_id: str
    username: str
    joined_at: date 
    review_count: int

@dataclass
class ReviewDto:
    review_id: int
    book_id: int
    reviewer_id: int
    rating: int
    comment: str
    review_date: date


@dataclass
class ReviewsSearchsDto:
    results: List[ReviewDto]
