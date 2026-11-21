from abc import ABC, abstractmethod

from app.config.database_settings import Database
from app.models.dto import *
from app.models.models import *


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
    @abstractmethod
    def update_status(self, review_id: int, status: ReviewStatus) -> None:
        pass 

class MariaDbReviewRepository(ReviewRepository):
    def __init__(self, database: Database) -> None:
        self.database = database 

    def get_by_id(self, review_id: int) -> Review:
        conn = self.database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SElect review_id, reviewer_id, book_id, comment, rating, status, review_date "
                "FROM reviews WHERE review_id = ?",
                (review_id,)
            )
            row = cursor.fetchone()
            if row is None:
                return None
            return Review(
                review_id=row[0],
                reviewer_id = row[1],
                book_id=row[2],
                comment =row[3],
                rating = row[4],
                status = ReviewStatus(row[5]),
                review_date = row[6],
            )
        finally:
            conn.close()



    def save(self, review: Review, status: ReviewStatus) -> Review:
        conn = self.database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reviews (reviewer_id, book_id, comment, rating, status) "
                "VALUES (?,?,?,?,?)",
                (review.reviewer_id, review.book_id, review.comment, review.rating, status.value)
            )
            conn.commit()
            review.review_id = cursor.lastrowid
            review.status = status
            return review
        finally:
            conn.close()

    def update(self, review_id: int, comment: str, rating: int, status: ReviewStatus):
        conn = self.database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reviews SET comment = ?, rating = ?, status = ? "
                "WHERE review_id = ?",
                (comment, rating, status.value, review_id)
            )
            conn.commit()
        finally:
            conn.close()
        return self.get_by_id(review_id)

    def delete(self, review_id: int, reviewer_id : int):
        conn = self.database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM reviews WHERE review_id = ? AND reviewer_id = ? ",
                (review_id, reviewer_id)
            )
            conn.commit()
        finally:
            conn.close()
        

    def update_status(self, review_id: int, status: ReviewStatus) -> None:
        conn = self.database.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reviews SET status = ? WHERE review_id = ?",
                (status.value, review_id)
            )
            conn.commit()
        finally:
            conn.close()





