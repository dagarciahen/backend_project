from dataclasses import dataclass
from typing import List, Dict, Optional
from app.models.dto import ReviewStatus
from datetime import date

@dataclass
class Book:
    id: int
    title: str
    subjects: List[str]
    authors: List[str]
    summaries: List[str]
    languages: List[str]

@dataclass
class Person:
    birth_year : Optional[int]
    death_year : Optional[int]
    name : str


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
    review_id : Optional[int] = None 
    review_date : Optional[date] = None

@dataclass
class ReviewCreated:
    review_id : int 
