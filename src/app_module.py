from fastapi.middleware.cors import CORSMiddleware
from nest.core import Module, PyNestFactory

from src.auth.auth_module import AuthModule
from src.portfolio.portfolio_module import PortfolioModule
from src.redis.redis_module import RedisModule
from src.stocks.stocks_module import StocksModule
from src.users.users_module import UsersModule

from .app_controller import AppController
from .app_service import AppService
from .orm_config import config


@Module(
    imports=[UsersModule, PortfolioModule, StocksModule, AuthModule, RedisModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This App is a PyNest Application that demonstrates the use of PyNest Framework.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
)
http_server = app.get_server()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "http://localhost:3001",
    "localhost:3001",
]

http_server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@http_server.on_event("startup")
def startup():
    print("Starting PyNest Application")
    config.create_all()
