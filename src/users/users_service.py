from datetime import timedelta
from functools import lru_cache

from fastapi.exceptions import HTTPException
from nest.core.decorators.database import db_request_handler
from sqlalchemy.orm import joinedload

from src.auth.auth_model import Token
from src.auth.auth_service import AuthService
from src.orm_config import config
from src.stocks.stocks_entity import Stock as StockEntity
from src.stocks.stocks_entity import StockLatestPrice as StockLatestPriceEntity
from src.users.users_entity import FollowedStocks as FollowedStocksEntity
from src.users.users_entity import User as UserEntity
from src.users.users_model import FollowedStocks, User, UserLogin
from nest.core import Injectable

@Injectable
class UsersService:
    def __init__(self):
        self.config = config
        self.session = self.config.get_db()
        self.auth_service = AuthService()

    @db_request_handler
    def register(self, user: User):
        # Check if user with the given username already exists
        existing_user = self.auth_service.get_user_by_username(user.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        # Hash the user's password
        hashed_password = self.auth_service.get_password_hash(user.password)

        # Create new user entity
        user_entity = UserEntity(
            username=user.username, password=hashed_password, email=user.email
        )
        self.session.add(user_entity)
        self.session.commit()
        return user_entity.id

    @db_request_handler
    def login(self, user: UserLogin):
        db_user = self.auth_service.get_user_by_username(user.username)
        if not db_user or not self.auth_service.verify_password(
            user.password, db_user.password
        ):
            raise HTTPException(
                status_code=400, detail="Incorrect username or password"
            )

        # Generate JWT token
        access_token_expires = timedelta(
            minutes=self.auth_service.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = self.auth_service.create_access_token(
            data={"sub": db_user.username}, expires_delta=access_token_expires
        )

        # Return the token
        return {"access_token": access_token, "token_type": "bearer"}

    @db_request_handler
    def get_user_by_id(self, user_id: int):
        return self.session.query(UserEntity).filter(UserEntity.id == user_id).first()

    @db_request_handler
    def get_user_by_username(self, username: str):
        return (
            self.session.query(UserEntity)
            .filter(UserEntity.username == username)
            .first()
        )

    @db_request_handler
    def update_user(self, user_id: int, user: User):
        user_exist = (
            self.session.query(UserEntity).filter(UserEntity.id == user_id).first()
        )
        user_exist.username = user.username
        user_exist.password = user.password
        user_exist.email = user.email
        self.session.commit()
        return user

    @db_request_handler
    def delete_user(self, user_id: int):
        user = self.session.query(UserEntity).filter(UserEntity.id == user_id).first()
        self.session.delete(user)
        self.session.commit()
        return user

    @db_request_handler
    def followed_stocks(self, username: str):
        # Aliasing for clarity
        user = (
            self.session.query(UserEntity)
            .filter(UserEntity.username == username)
            .first()
        )
        followed_stocks = (
            self.session.query(FollowedStocksEntity)
            .filter(FollowedStocksEntity.user_id == user.id)
            .all()
        )
        stocks = []
        for followed_stock in followed_stocks:
            stock = (
                self.session.query(StockEntity)
                .filter(StockEntity.id == followed_stock.stock_id)
                .first()
            )
            stocks.append(stock)
        stocks_query = (
            self.session.query(StockEntity)
            .options(joinedload(StockEntity.stock_latest_prices))
            .join(StockLatestPriceEntity)
        )
        stocks_query = stocks_query.filter(
            StockEntity.id.in_([stock.id for stock in stocks])
        )

        return stocks_query.all()

    @db_request_handler
    def follow_stock(self, followed_stock: FollowedStocks, token: Token):
        user = self.auth_service.get_current_user(token)
        stock_id = followed_stock.stock_id
        followed_stock = FollowedStocksEntity(user_id=user.id, stock_id=stock_id)
        self.session.add(followed_stock)
        self.session.commit()
        return followed_stock.id

    @db_request_handler
    def unfollow_stock(self, followed_stock: FollowedStocks, token: Token):
        user = self.auth_service.get_current_user(token)
        stock_id = followed_stock.stock_id
        followed_stock = (
            self.session.query(FollowedStocksEntity)
            .filter(
                FollowedStocksEntity.user_id == user.id,
                FollowedStocksEntity.stock_id == stock_id,
            )
            .first()
        )
        self.session.delete(followed_stock)
        self.session.commit()
        return followed_stock.id
