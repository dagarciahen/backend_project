from Dto import *
from models import *
from abc import ABC, abstractmethod


class ReviewRepository(ABC):
    @abstractmethod
    def save(self, review: Review, status: ReviewStatus) -> Review: 
        pass

    @abstractmethod
    def update(self, review_id: int, comment: str, rating: int, status : ReviewStatus) -> Review:
        pass

    @abstractmethod
    def delete(self, review_id: int, reviewer_id: int) -> None:
        pass 

    @abstractmethod
    def get_by_id(self, review_id: int, reviewer_id : int) -> Optional[Review]:
        pass


