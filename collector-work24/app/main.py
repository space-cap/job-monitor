from sqlalchemy import text

from app.config import validate_database_config
from app.database.connection import create_db_engine


def main() -> None:
    validate_database_config()
    engine = create_db_engine()

    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE(), VERSION()"))
        database, version = result.one()

    print(f"MariaDB connection OK: database={database}, version={version}")


if __name__ == "__main__":
    main()
