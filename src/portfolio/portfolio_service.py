
from faker import Faker
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable
from src.orm_config import config
from src.portfolio.portfolio_entity import PortfolioItem as PortfolioItemEntity
from src.portfolio.portfolio_model import PortfolioItem


@Injectable
class PortfolioService:
    def __init__(self):
        self.config = config
        self.session = self.config.get_db()
        self.fake = Faker()

    @db_request_handler
    def get_portfolio(self):
        return self.session.query(PortfolioItemEntity).all()

    @db_request_handler
    def add_to_portfolio(self, portfolio_item: PortfolioItem):
        portfolio_item_entity = PortfolioItemEntity(
            user_id=portfolio_item.user_id,
            stock_id=portfolio_item.stock_id,
            quantity=portfolio_item.quantity,
            purchase_price=portfolio_item.purchase_price,
            purchase_date=portfolio_item.purchase_date,
        )
        self.session.add(portfolio_item_entity)
        self.session.commit()
        return portfolio_item_entity.id

    @db_request_handler
    def get_portfolio_item(self, stock_id: int):
        return (
            self.session.query(PortfolioItemEntity)
            .filter(PortfolioItemEntity.stock_id == stock_id)
            .first()
        )

    @db_request_handler
    def update_portfolio_item(self, stock_id: int, portfolio_item: PortfolioItem):
        portfolio_item_exist = (
            self.session.query(PortfolioItemEntity)
            .filter(PortfolioItemEntity.stock_id == stock_id)
            .first()
        )
        portfolio_item_exist.user_id = portfolio_item.user_id
        portfolio_item_exist.stock_id = portfolio_item.stock_id
        portfolio_item_exist.quantity = portfolio_item.quantity
        portfolio_item_exist.purchase_price = portfolio_item.purchase_price
        portfolio_item_exist.purchase_date = portfolio_item.purchase_date
        self.session.commit()
        return portfolio_item

    @db_request_handler
    def delete_portfolio_item(self, stock_id: int):
        portfolio_item = (
            self.session.query(PortfolioItemEntity)
            .filter(PortfolioItemEntity.stock_id == stock_id)
            .first()
        )
        self.session.delete(portfolio_item)
        self.session.commit()
        return portfolio_item

    def populate_portfolio(self, number_of_items: int):
        for i in range(number_of_items):
            portfolio_item = PortfolioItem(
                user_id=self.fake.random_int(min=1, max=100),
                stock_id=self.fake.random_int(min=1, max=100),
                quantity=self.fake.random_int(min=1, max=100),
                purchase_price=self.fake.random_int(min=1, max=100),
                purchase_date=self.fake.date(),
            )
            self.add_to_portfolio(portfolio_item)
