from src.portfolio.portfolio_controller import PortfolioController
from src.portfolio.portfolio_service import PortfolioService
from nest.core import Module


@Module(providers=[PortfolioService], controllers=[PortfolioController])
class PortfolioModule:
    ...
