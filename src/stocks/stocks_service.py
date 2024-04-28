import json
import logging
import pickle
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

from faker import Faker
from fastapi.background import BackgroundTasks
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable
from sqlalchemy import desc, or_
from sqlalchemy.orm import joinedload

from src.auth.auth_model import Token
from src.auth.auth_service import AuthService
from src.orm_config import config
from src.redis.redis_service import RedisInput, RedisService
from src.stocks.stocks_entity import CompanyOfficer as CompanyOfficersEntity
from src.stocks.stocks_entity import Stock as StockEntity
from src.stocks.stocks_entity import StockLatestPrice as StockLatestPriceEntity
from src.stocks.stocks_entity import StockPrice as StockPriceEntity
from src.stocks.stocks_model import CompanyOfficers, GetStocksParams, Stock

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@Injectable
class StocksService:
    def __init__(self, auth_service: AuthService, redis_service: RedisService):
        self.config = config
        self.session = self.config.get_db()
        self.fake = Faker()
        self.stocks_path = Path(__file__).parent / "data" / "stocks.json"
        self.stocks = self.get_stocks_symbols()
        self.auth_service = auth_service
        self.redis_service = redis_service

    def get_stocks_symbols(self):
        with open(self.stocks_path) as f:
            data = json.load(f)
        return data

    @db_request_handler
    def get_stocks(self, stocks_params: GetStocksParams, token: Token):
        self.auth_service.get_current_user(token)
        query = stocks_params.query
        page = stocks_params.page
        limit = stocks_params.limit

        stocks_query = (
            self.session.query(StockEntity)
            .options(joinedload(StockEntity.stock_latest_prices))
            .join(StockLatestPriceEntity)
            .filter(
                or_(
                    StockEntity.short_name.isnot(None),
                    StockEntity.long_name.isnot(None),
                )
            )
            .order_by(desc(StockEntity.market_cap), StockEntity.id)
        )
        # Filter by query if provided
        if query:
            stocks_query = stocks_query.filter(
                or_(
                    StockEntity.symbol.ilike(f"%{query}%"),
                    StockEntity.short_name.ilike(f"%{query}%"),
                )
            )

        # Apply pagination
        offset = (page - 1) * limit
        stocks = stocks_query.offset(offset).limit(limit).all()

        return stocks

    @db_request_handler
    def add_stock(self, stock: Stock):
        stock_entity = StockEntity(**stock.dict(),)
        self.session.add(stock_entity)
        self.session.commit()
        return stock_entity.id

    @db_request_handler
    def get_stock(self, stock_id: int):
        return (
            self.session.query(StockEntity).filter(StockEntity.id == stock_id).first()
        )

    @db_request_handler
    def update_stock(self, stock_id: int, stock: Stock):
        self.session.query(StockEntity).filter(StockEntity.id == stock_id).update(
            **stock.dict()
        )
        self.session.commit()
        return {"message": f"Stock {stock.symbol} updated"}

    @db_request_handler
    def delete_stock(self, stock_id: int):
        self.session.query(StockEntity).filter(StockEntity.id == stock_id).delete()
        self.session.commit()
        return {"message": f"Stock {stock_id} deleted"}

    @db_request_handler
    def get_officers(self):
        return self.session.query(CompanyOfficersEntity).all()

    @db_request_handler
    def add_officer(self, officer: CompanyOfficers):
        officer_entity = CompanyOfficersEntity(**officer.dict())
        self.session.add(officer_entity)
        self.session.commit()
        return officer.id

    @db_request_handler
    def get_officers_by_id(self, stock_id: int):
        redis_key = f"officers_{stock_id}"
        res = self.redis_service.get(redis_key)
        if res:
            return pickle.loads(res)
        else:
            res = (
                self.session.query(CompanyOfficersEntity)
                .filter(CompanyOfficersEntity.company_id == stock_id)
                .all()
            )
            redis_input = RedisInput(key=redis_key, value=pickle.dumps(res))
            self.redis_service.set(redis_input)
            return res

    @db_request_handler
    def get_officers_by_symbol(self, symbol: str):
        redis_key = f"officers_{symbol}"
        res = self.redis_service.get(redis_key)
        if res:
            return pickle.loads(res)
        else:
            query = (
                self.session.query(CompanyOfficersEntity)
                .join(StockEntity, CompanyOfficersEntity.company_id == StockEntity.id)
                .filter(StockEntity.symbol == symbol)
            )
            officers = query.all()
            redis_input = RedisInput(key=redis_key, value=pickle.dumps(officers))
            self.redis_service.set(redis_input)
            return officers

    @db_request_handler
    def update_officer(self, officer_id: int, officer: CompanyOfficers):
        self.session.query(CompanyOfficersEntity).filter(
            CompanyOfficersEntity.id == officer_id
        ).update(**officer.dict())
        self.session.commit()
        return {"message": f"Officer {officer_id} updated"}

    @db_request_handler
    def delete_officer(self, officer_id: int):
        self.session.query(CompanyOfficersEntity).filter(
            CompanyOfficersEntity.id == officer_id
        ).delete()
        self.session.commit()
        return {"message": f"Officer {officer_id} deleted"}

    @db_request_handler
    def get_stock_prices_by_id(
        self, stock_id: int, timeframe: str, bg_task: BackgroundTasks
    ):
        def helper(records_count_mapping: dict, stock_id: int, timeframe: str):
            redis_key = f"stock_price_{stock_id}_{timeframe}_{datetime.now().strftime('%Y-%m-%d')}"
            res = self.redis_service.get(redis_key)
            if res:
                return pickle.loads(res)
            if timeframe not in records_count_mapping:
                raise ValueError(f"Invalid timeframe: {timeframe}")

            records_count = records_count_mapping[timeframe]

            query = (
                self.session.query(StockPriceEntity)
                .filter(StockPriceEntity.stock_id == stock_id)
                .order_by(desc(StockPriceEntity.date))
            )

            if records_count:
                query = query.limit(records_count)

            res = query.all()
            redis_input = RedisInput(key=redis_key, value=pickle.dumps(res))
            self.redis_service.set(redis_input)
            logger.info(f"Redis key: {redis_key} Inserted into redis")
            return res

        redis_key = (
            f"stock_price_{stock_id}_{timeframe}_{datetime.now().strftime('%Y-%m-%d')}"
        )
        res = self.redis_service.get(redis_key)
        if res:
            return pickle.loads(res)
        else:
            # Calculate the number of records based on the timeframe
            records_count_mapping = {
                "7d": 7,
                "14d": 14,
                "1m": 21,  # Assuming about 21 trading days in a month
                "6m": 126,  # Assuming about 21 trading days in a month x 6
                "1y": 252,  # Assuming about 252 trading days in a year
                "5y": 1260,  # 252 trading days x 5
                "max": None,
            }
            for t_frame in records_count_mapping:
                if t_frame != timeframe:
                    bg_task.add_task(helper, records_count_mapping, stock_id, t_frame)
            res = helper(records_count_mapping, stock_id, timeframe)
            return res

    @db_request_handler
    def get_stock_prices_by_symbol(self, symbol: str):
        query = (
            self.session.query(StockPriceEntity)
            .join(StockEntity, StockPriceEntity.stock_id == StockEntity.id)
            .filter(StockEntity.symbol == symbol)
            .order_by(desc(StockPriceEntity.date))
        )
        return query.all()

    @db_request_handler
    def get_latest_price(self, stock_id: int):
        latest_price_entry = (
            self.session.query(StockPriceEntity)
            .filter(StockPriceEntity.stock_id == stock_id)
            .order_by(desc(StockPriceEntity.date))
            .first()
        )

        if latest_price_entry:
            return latest_price_entry.close
        else:
            return None  # Or handle this scenario appropriately

    def fetch_market_cap(self, stock):
        if stock.market_cap:
            return
        else:
            stock.market_cap = 0
            self.session.commit()
            return
        # yf_ticker = yf.Ticker(stock.symbol)
        # try:
        #     market_cap = yf_ticker.info['marketCap']
        # except:
        #     print(f"Could not fetch market cap for {stock.symbol}")
        #     return
        # stock.market_cap = market_cap
        # self.session.commit()
        # print(f"Updated market cap for {stock.symbol}")

    def populate_market_cap(self):
        stocks = self.session.query(StockEntity).all()

        # Define the number of threads you want to use.
        # It's usually a good idea not to exceed the number of available CPUs.
        num_threads = 10

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            executor.map(self.fetch_market_cap, reversed(stocks))
