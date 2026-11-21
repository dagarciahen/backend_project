from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config.database_settings import Database
from app.repository.reviewer_repository import MariaDBReviewerRepository
from app.services.auth_service import AuthService, AuthServiceV1

## for simplicity will implement simple authentication with user and password to send in the header of the request
##to avoid a reviewer impersonate another reviewer and send userid on the post.review request

##https://fastapi.tiangolo.com/tutorial/security/get-current-user/#create-a-get-current-user-dependency

security = HTTPBasic()

def get_auth_service() -> AuthService:
    return AuthServiceV1(MariaDBReviewerRepository(Database()))

def get_current_reviewer_id(credentials: Annotated[HTTPBasicCredentials, Depends(security)], auth: Annotated[AuthService, Depends(get_auth_service)]) -> int:
    reviewer_id = auth.authenticate(credentials.username, credentials.password)
    if reviewer_id is None:
        raise HTTPException(status_code=401, detail = "invalid credentiuals", headers= {"WWW-Authenticate": "Basic"})
    return reviewer_id 


