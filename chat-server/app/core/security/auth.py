from dependency_injector.wiring import inject, Provide
from fastapi import Cookie, Depends, Query
from jose import jwt, JWTError, ExpiredSignatureError

from app.core.config import Settings
from app.core.container import Container
from app.core.models.jwt import JwtPayload
from app.core.models.user import User


class CredentialsError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class InvalidCredentialsError(CredentialsError):
    def __init__(self):
        super().__init__("invalid credentials were provided")


class CredentialsExpiredError(CredentialsError):
    def __init__(self):
        super().__init__("credentials expired")


class NoCredentialsError(CredentialsError):
    def __init__(self):
        super().__init__("no credentials were provided")


def get_token_from_cookie(access_token: str | None = Cookie(default=None)):
    return access_token


def get_token_from_query_param(access_token: str | None = Query(default=None)):
    return access_token


@inject
def get_user(
    token: str | None = Depends(get_token_from_cookie),
    settings: Settings = Depends(Provide[Container.settings])
):
    if token is None or not token:
        raise NoCredentialsError
    try:
        decoded_token = jwt.decode(token, settings.JWT_PUBLIC_KEY, issuer=settings.JWT_ISSUER, algorithms=["RS256"])
        payload = JwtPayload(**decoded_token)
        return User(
            id=payload.user_id,
            name=payload.user_name,
        )
    except ExpiredSignatureError:
        raise CredentialsExpiredError
    except JWTError:
        raise InvalidCredentialsError
