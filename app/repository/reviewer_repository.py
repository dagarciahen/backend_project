from abc import ABC, abstractmethod
from typing import Optional
from app.models.models import Reviewer

class ReviewerRepository(ABC):
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Reviewer]:
        pass

class MariaDBReviewerRepository(ReviewerRepository):
    def __init__(self):
        self.database = database 

    def get_by_username(self, username: str) -> Optional[Reviewer]:
        conn = self.database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT reviewer_id, username, email, password_hash, joined_at "
                "FROM reviewers WHERE username = ?",
                (username,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Reviewer(reviewer_id=row[0], username=row[1], email=row[2], password_hash=row[3], joined_at=row[4])
        finally:
            conn.close()


    