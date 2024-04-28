import requests

from src.stocks.stocks_controller import StocksController
from src.stocks.stocks_model import CompanyOfficers, Stock, StockPrice


class StocksClient:
    def __init__(self):
        self.controller = StocksController
        self.endpoints = [
            endpoint
            for endpoint, signature in self.controller.__dict__.items()
            if "function StocksController" in str(signature)
        ]
        self.urls = {
            endpoint: f"http://0.0.0.0:8088/{endpoint}" for endpoint in self.endpoints
        }
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    def get_stock(self, stock_id: int):
        response = requests.get(
            self.urls["get_stock"] + f"/{stock_id}", headers=self.headers
        )
        return response.json()

    def get_stocks(self):
        response = requests.get(self.urls["get_stocks"])
        return response.json()
