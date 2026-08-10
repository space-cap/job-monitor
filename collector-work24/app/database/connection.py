from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER


def create_db_engine() -> Engine:
    if not DB_USER or not DB_PASSWORD:
        raise RuntimeError("DB_USER and DB_PASSWORD must be configured")

    url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    )
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=1800,
    )
