from fastapi import APIRouter, Depends, Form, HTTPException, status
from src.api.jewelers.jew_schemas import JewelerSchema
from src.auth import utils as auth_utils
from pydantic import BaseModel
from fastapi.security import HTTPBearer


http_bearer = HTTPBearer()


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


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
            # detail=f"invalid token error",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: UserSchema = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


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
