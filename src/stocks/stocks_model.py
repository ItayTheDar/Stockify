from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class ModelID(BaseModel):
    id: Optional[int]


class CompanyOfficers(ModelID):
    max_age: Optional[int]
    name: str
    age: Optional[int]
    title: Union[str, None]
    year_born: Optional[int]
    fiscal_year: Optional[int]
    total_pay: Optional[int]
    exercised_value: Optional[int]
    unexercised_value: Optional[int]
    company_id: int


class Stock(ModelID):
    address1: Optional[str]
    city: Optional[str]
    state: Optional[str]
    zip: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    industry: Optional[str]
    industry_disp: Optional[str]
    sector: Optional[str]
    sector_disp: Optional[str]
    long_business_summary: Optional[str]
    full_time_employees: Optional[int]
    audit_risk: Optional[int]
    board_risk: Optional[int]
    compensation_risk: Optional[int]
    share_holder_rights_risk: Optional[int]
    overall_risk: Optional[int]
    governance_epoch_date: Optional[int]
    compensation_as_of_epoch_date: Optional[int]
    max_age: Optional[int]
    exchange: Optional[str]
    quote_type: Optional[str]
    symbol: Optional[str]
    short_name: Optional[str]
    long_name: Optional[str]
    uuid: Optional[str]
    message_board_id: Optional[str]
    financial_currency: Optional[str]


class StockPrice(ModelID):
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: Optional[int]
    stock_id: int


class StockLatestPrice(ModelID):
    stock_id: int
    latest_price: float
    two_days_ago_price: float
    change: float
    change_percent: float


class GetStocksParams(BaseModel):
    limit: int
    page: int
    query: str
