from fastapi.background import BackgroundTasks
from nest.core import Controller, Delete, Depends, Get, Post, Put

from src.auth.auth_model import Token
from src.stocks.stocks_model import CompanyOfficers, GetStocksParams, Stock
from src.stocks.stocks_service import StocksService


@Controller("stocks")
class StocksController:

    def __init__(self, service: StocksService):
        self.service = service

    @Post("/get_stocks")
    def get_stocks(self, stocks_params: GetStocksParams, token: Token):
        return self.service.get_stocks(stocks_params, token)

    @Post("/")
    def add_stock(self, stock: Stock):
        return self.service.add_stock(stock)

    @Get("/{stock_id}")
    def get_stock(self, stock_id: int):
        return self.service.get_stock(stock_id)

    @Put("/{stock_id}")
    def update_stock(self, stock_id: int, stock: Stock):
        return self.service.update_stock(stock_id, stock)

    @Delete("/{stock_id}")
    def delete_stock(self, stock_id: int):
        return self.service.delete_stock(stock_id)

    @Get("/get_officers")
    def get_officers(self):
        return self.service.get_officers()

    @Post("/add_officer")
    def add_officer(self, officer: CompanyOfficers):
        return self.service.add_officer(officer)

    @Get("/get_officers_by_id/{stock_id}")
    def get_officers_by_id(self, stock_id: int):
        return self.service.get_officers_by_id(stock_id)

    @Get("/get_officers_by_symbol/{symbol}")
    def get_officers_by_symbol(self, symbol: str):
        return self.service.get_officers_by_symbol(symbol)

    @Put("/update_officer/{officer_id}")
    def update_officer(self, officer_id: int, officer: CompanyOfficers):
        return self.service.update_officer(officer_id, officer)

    @Delete("/delete_officer/{officer_id}")
    def delete_officer(self, officer_id: int):
        return self.service.delete_officer(officer_id)

    @Get("/get_stock_prices_by_id/{stock_id}/{timeframe}")
    def get_stock_prices_by_id(
        self, stock_id: int, timeframe: str, bg_tasks: BackgroundTasks
    ):
        return self.service.get_stock_prices_by_id(stock_id, timeframe, bg_tasks)

    @Get("/get_stock_prices_by_symbol/{symbol}")
    def get_stock_prices_by_symbol(self, symbol: str):
        return self.service.get_stock_prices_by_symbol(symbol)

    @Get("/latest_price/{stock_id}")
    def get_latest_price(self, stock_id: int):
        return self.service.get_latest_price(stock_id)
