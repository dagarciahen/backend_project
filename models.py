from dataclasses import dataclass
from typing import List, dict, Optional
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
    review_id: int
    joined_at: date   
    reviewer_id: int
    book_id: int
    comment: str
    rating: int
    review_date: date
