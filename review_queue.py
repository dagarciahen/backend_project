from abc import abstractmethod, ABC
from models import ReviewCreated


class ReviewQueue(ABC):
    @abstractmethod
    def publish_review_created(self, event: ReviewCreated) -> None:
        pass

    