from app.client.book_client import BookClient
from app.exceptions import BookNotFoundError, InvalidCommentError, InvalidRatingError
from app.models.dto import CreateReviewDto

MAX_COMMENT_LENGTH = 1000


class ReviewValidator:
    def __init__(self, client: BookClient) -> None:
        self.client = client

    def validate_create(self, dto: CreateReviewDto) -> None:
        if not (1 <= dto.rating <= 5):
            raise InvalidRatingError()
        if not (1 <= len(dto.comment.strip()) <= MAX_COMMENT_LENGTH):
            raise InvalidCommentError()
        if self.client.get_by_id(dto.book_id) is None:
            raise BookNotFoundError()

    def validate_update(self, rating: int, comment: str) -> None:
        if not (1 <= rating <= 5):
            raise InvalidRatingError()
        if not (1 <= len(comment.strip()) <= MAX_COMMENT_LENGTH):
            raise InvalidCommentError()
