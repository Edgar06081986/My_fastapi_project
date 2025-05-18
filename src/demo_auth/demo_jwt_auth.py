from fastapi import APIRouter, Depends, Form, HTTPException, status
from src.api_v1.jewelers.jew_schemas import JewelerSchema
from src.auth import utils as auth_utils
from pydantic import BaseModel


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/jwt", tags=["JWT"])

john = JewelerSchema(
    username="john",
    password=auth_utils.hash_password("qwerty"),
    email="john@example.com",
)
sam = JewelerSchema(
    username="sam",
    password=auth_utils.hash_password("secret"),
)

jewelers_db: dict[str, JewelerSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_jeweler(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (jeweler := jewelers_db.get(username)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hashed_password=jeweler.password,
    ):
        raise unauthed_exc

    if not jeweler.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not active",
        )

    return jeweler


@router.post("/login/", response_model=TokenInfo)
def auth_jeweler_issue_jwt(
    jeweler: JewelerSchema = Depends(validate_auth_jeweler),
):
    jwt_payload = {
        "sub": jeweler.username,
        "username": jeweler.username,
        "email": jeweler.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
