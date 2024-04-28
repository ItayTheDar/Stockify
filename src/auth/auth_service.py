from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from nest.core import Injectable
from nest.core.decorators.database import db_request_handler

from src.auth.auth_model import Token, TokenData
from src.orm_config import config
from src.users.users_entity import User


@Injectable
class AuthService:
    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self):
        self.orm_config = config
        self.session = self.orm_config.get_db()
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @staticmethod
    def get_password_hash(password):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    @db_request_handler
    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def get_current_user(self, token: Token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            token_str = token.access_token
            payload = jwt.decode(
                token_str, self.SECRET_KEY, algorithms=[self.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(sub=username, exp=payload.get("exp"))
        except Exception as e:
            raise credentials_exception
        user = self.get_user_by_username(username=token_data.sub)
        if user is None:
            raise credentials_exception
        return user
