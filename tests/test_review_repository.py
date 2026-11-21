from datetime import date
from unittest.mock import Mock

from app.models.dto import ReviewStatus
from app.models.models import Review
from app.repository.repository import MariaDbReviewRepository


def test_save_inserts_and_sets_review_id():
    database = Mock()
    conn = database.get_connection.return_value
    cursor = conn.cursor.return_value
    cursor.lastrowid = 7
    repository = MariaDbReviewRepository(database)
    review = Review(reviewer_id=1, book_id=10, comment="good book", rating=5)

    saved = repository.save(review, ReviewStatus.PENDING)

    sql, params = cursor.execute.call_args[0]
    assert "INSERT INTO reviews" in sql
    assert params == (1, 10, "good book", 5, ReviewStatus.PENDING.value)
    conn.commit.assert_called_once()
    conn.close.assert_called_once()
    assert saved.review_id == 7


def test_get_by_id_returns_review():
    database = Mock()
    conn = database.get_connection.return_value
    cursor = conn.cursor.return_value
    cursor.fetchone.return_value = (
        3, 1, 10, "good book", 5, ReviewStatus.PENDING.value, date(2026, 11, 19)
    )
    repository = MariaDbReviewRepository(database)

    review = repository.get_by_id(3)

    assert review.review_id == 3
    assert review.reviewer_id == 1
    assert review.book_id == 10
    assert review.status == ReviewStatus.PENDING
    conn.close.assert_called_once()