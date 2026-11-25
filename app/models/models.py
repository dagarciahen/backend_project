from dataclasses import dataclass
from datetime import date

from app.models.dto import ReviewStatus


@dataclass
class Book:
    id: int
    title: str
    subjects: list[str]
    authors: list[str]
    summaries: list[str]
    languages: list[str]


@dataclass
class Person:
    birth_year: int | None
    death_year: int | None
    name: str


@dataclass
class Reviewer:
    reviewer_id: int
    username: str
    email: str
    password_hash: str
    joined_at: date


@dataclass
class Review:
    reviewer_id: int
    book_id: int
    comment: str
    rating: int
    status: ReviewStatus = ReviewStatus.PENDING
    review_id: int | None = None
    review_date: date | None = None
    book_title: str | None = None
    book_authors: str | None = None
    cover_url: str | None = None


@dataclass
class ReviewCreated:
    review_id: int
