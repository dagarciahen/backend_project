
import hashlib, hmac
class AuthService(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str) -> Optional[int]:
        pass

class AuthServiceV1(AuthService):
    def __init__(self, repository: ReviewerRepository) -> None:
        self.repository = repository

    def authenticate(self, username: str, password: str) -> Optional[int]:
        reviewer = self.repository.get_by_username(username)
        if reviewer is None or _verify(password, reviewer.password_hash):
            return None
        return reviewer.reviewer_id

    ##for simplicity hexadecimal salt for random hex before passwowrd to avoid collision and a sha-256 hash function to store password
    def _hash_password(password: str) -> str:
        salt = os.urandom(16).hex()
        return salt + ":" + hashlib.sha256((salt+ password).encode()).hexdigest()

    def _verify(password: str, stored_password: str) -> bool:
        salt, digest = stored.split(":")
        return hmac.compare_digest(hashlib.sha256((salt + password).encode()).hexdigest(), digest)
    
