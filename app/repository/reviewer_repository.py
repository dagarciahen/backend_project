from abc import ABC, abstractmethod
from typing import Optional
from app.models.models import Reviewer

class ReviewerRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Reviewer]:
        pass

    