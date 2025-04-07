from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from app.core import get_settings

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl=f"{get_settings().get_api_prefix}/auth/login",
    scheme_name="JWT",
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str, expires_delta: int | None = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(tz=UTC) + expires_delta
    else:
        expires_delta = datetime.now(tz=UTC) + timedelta(minutes=get_settings().ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, get_settings().JWT_SECRET_KEY, get_settings().JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str, expires_delta: int | None = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now(tz=UTC) + expires_delta
    else:
        expires_delta = datetime.now(tz=UTC) + timedelta(
            minutes=get_settings().REFRESH_TOKEN_EXPIRE_MINUTES,
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, get_settings().JWT_REFRESH_SECRET_KEY, get_settings().JWT_ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            get_settings().JWT_REFRESH_SECRET_KEY,
            algorithms=[get_settings().JWT_ALGORITHM],
        )
        return payload
    except jwt.JWTError:
        return None


def get_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
