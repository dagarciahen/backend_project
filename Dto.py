from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
from datetime import date

@dataclass
class PersonDto:
    birth_year: Optional[int]
    death_year: Optional[int]
    name : str

@dataclass
class BookDto:
    id: int
    title: str
    subjects : List[str]
    authors: List[PersonDto]
    summaries: List[str]
    translators: List[PersonDto]
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
class BookItemResultDto:
    id: int
    status: int
    book: Optional[BookDto] = None
    error : Optional[str] = None
    



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
class UpdateReviewDto:
    comment: str
    rating: int


@dataclass
class ReviewsSearchsDto:
    results: List[ReviewDto]

class ReviewStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"

    