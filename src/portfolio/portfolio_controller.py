from nest.core import Controller, Delete, Get, Post, Put

from src.portfolio.portfolio_model import PortfolioItem
from src.portfolio.portfolio_service import PortfolioService


@Controller("portfolio")
class PortfolioController:

    def __init__(self, service: PortfolioService):
        self.service = service

    @Get("/")
    def get_portfolio(self):
        return self.service.get_portfolio()

    @Post("/")
    def add_to_portfolio(self, portfolio_item: PortfolioItem):
        return self.service.add_to_portfolio(portfolio_item)

    @Get("/{stock_id}")
    def get_portfolio_item(self, stock_id: int):
        return self.service.get_portfolio_item(stock_id)

    @Put("/{stock_id}")
    def update_portfolio_item(self, stock_id: int, portfolio_item: PortfolioItem):
        return self.service.update_portfolio_item(stock_id, portfolio_item)

    @Delete("/{stock_id}")
    def delete_portfolio_item(self, stock_id: int):
        return self.service.delete_portfolio_item(stock_id)
