from nest.core import Controller, Delete, Depends, Get, Post, Put

from src.auth.auth_model import Token
from src.users.users_model import FollowedStocks, User, UserLogin
from src.users.users_service import UsersService


@Controller("users")
class UsersController:

    def __init__(self, service: UsersService):
        self.service = service

    @Post("/register")
    def register(self, user: User):
        return self.service.register(user)

    @Post("/login")
    def login(self, user_login: UserLogin):
        return self.service.login(user_login)

    @Get("/followed_stocks/{username}")
    def followed_stocks(self, username: str):
        return self.service.followed_stocks(username)

    @Post("/follow_stock")
    def follow_stock(self, followed_stock: FollowedStocks, token: Token):
        return self.service.follow_stock(followed_stock, token)

    @Post("/unfollow_stock")
    def unfollow_stock(self, followed_stock: FollowedStocks, token: Token):
        return self.service.unfollow_stock(followed_stock, token)
