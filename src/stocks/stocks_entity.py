from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import relationship

from src.orm_config import config


class CompanyOfficer(config.Base):
    __tablename__ = "company_officers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    max_age = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    title = Column(String)
    year_born = Column(Integer, nullable=True)
    fiscal_year = Column(Integer, nullable=True)
    total_pay = Column(BigInteger, nullable=True)
    exercised_value = Column(BigInteger, nullable=True)
    unexercised_value = Column(BigInteger, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    company_id = Column(Integer, ForeignKey("stocks.id"))


class Stock(config.Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String, nullable=False, unique=True)
    address1 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    country = Column(String)
    phone = Column(String)
    website = Column(String)
    industry = Column(String)
    industry_disp = Column(String)
    sector = Column(String)
    sector_disp = Column(String)
    long_business_summary = Column(String)
    full_time_employees = Column(Integer)
    audit_risk = Column(Integer)
    board_risk = Column(Integer)
    compensation_risk = Column(Integer)
    share_holder_rights_risk = Column(Integer)
    overall_risk = Column(Integer)
    governance_epoch_date = Column(BigInteger)
    compensation_as_of_epoch_date = Column(BigInteger)
    max_age = Column(Integer)
    exchange = Column(String)
    quote_type = Column(String)
    short_name = Column(String)
    long_name = Column(String)
    uuid = Column(String)
    message_board_id = Column(String)
    financial_currency = Column(String)
    market_cap = Column(BigInteger, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    officers = relationship("CompanyOfficer", backref="stocks")
    stock_prices = relationship("StockPrice", backref="stocks")
    stock_latest_prices = relationship("StockLatestPrice", backref="stocks")
    followed_stocks = relationship("FollowedStocks", backref="stocks")


class StockPrice(config.Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"))
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
    date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())


class StockLatestPrice(config.Base):
    __tablename__ = "stock_latest_prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), unique=True)
    latest_price = Column(Float)
    two_days_ago_price = Column(Float)
    change = Column(Float)
    change_percent = Column(Float)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
