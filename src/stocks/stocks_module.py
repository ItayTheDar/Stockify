from src.stocks.stocks_controller import StocksController
from src.stocks.stocks_service import StocksService
from nest.core import Module


@Module(controllers=[StocksController], providers=[StocksService], imports=[])
class StocksModule:
    ...
