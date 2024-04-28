from datetime import datetime

from pydantic import BaseModel


class PortfolioItem(BaseModel):
    user_id: int
    stock_id: int
    quantity: int
    purchase_price: float
    purchase_date: datetime
