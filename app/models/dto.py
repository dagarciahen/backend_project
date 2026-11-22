from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass
class PersonDto:
    birth_year: int | None
    death_year: int | None
    name: str


class ReviewStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    PROCESSING = "processing"


@dataclass
class ReviewDto:
    review_id: int
    book_id: int
    reviewer_id: int
    rating: int
    comment: str
    review_date: datetime
    status: ReviewStatus


@dataclass
class BookDto:
    id: int
    title: str
    subjects: list[str]
    authors: list[PersonDto]
    summaries: list[str]
    translators: list[PersonDto]
    bookshelves: list[str]
    languages: list[str]
    copyright: bool | None
    media_type: str
    formats: dict[str, str]
    download_count: int


@dataclass
class BookSearchResultDto:
    count: int | None
    next: str | None
    previous: str | None
    results: list[BookDto]


@dataclass
class BookItemResultDto:
    id: int
    status: int
    book: BookDto | None = None
    error: str | None = None


@dataclass
class ReviewerDto:
    reviewer_id: int
    username: str
    joined_at: datetime
    review_count: int


@dataclass
class ReviewsSearchsDto:
    results: list[ReviewDto]


@dataclass
class CreateReviewDto:
    book_id: int
    rating: int
    comment: str


@dataclass
class UpdateReviewDto:
    comment: str
    rating: int
