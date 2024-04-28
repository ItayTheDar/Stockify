from sqlalchemy import Column, DateTime, Float, Integer, func

from src.orm_config import config


class PortfolioItem(config.Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer)
    stock_id = Column(Integer)
    quantity = Column(Integer)
    purchase_price = Column(Float)
    purchase_date = Column(DateTime, default=func.now())
