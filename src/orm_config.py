import os

from dotenv import load_dotenv
from nest.core.database.orm_provider import OrmProvider

load_dotenv()

config = OrmProvider(
    db_type="postgresql",
    config_params=dict(
        host=os.getenv("POSTGRESQL_HOST"),
        db_name=os.getenv("POSTGRESQL_DB_NAME"),
        user=os.getenv("POSTGRESQL_USER"),
        password=os.getenv("POSTGRESQL_PASSWORD"),
        port=int(os.getenv("POSTGRESQL_PORT")),
    ),
)


REDIS_CONFIG = {
    "host": os.getenv("REDIS_HOST", "localhost"),
    "port": os.getenv("REDIS_PORT", 6379),
    "db": os.getenv("REDIS_DB", 0),
}
