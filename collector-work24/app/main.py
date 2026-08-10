from sqlalchemy import text

from app.config import validate_database_config
from app.database.connection import create_db_engine
from app.database.repository import save_jobs
from app.work24.client import Work24Client
from app.work24.parser import parse_list_page


def main() -> None:
    validate_database_config()
    engine = create_db_engine()
    client = Work24Client()

    html = client.fetch_list_page(page=1)
    jobs = parse_list_page(html)

    print(f"Work24 page 1 parsed jobs: {len(jobs)}")
    if not jobs:
        raise RuntimeError(
            "No jobs were parsed from Work24. The page HTML or selectors may have changed."
        )

    inserted, updated = save_jobs(engine, jobs)

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM jobs WHERE source_site = 'WORK24'")
        ).scalar_one()

    print(f"Inserted: {inserted}")
    print(f"Updated: {updated}")
    print(f"WORK24 jobs in DB: {count}")


if __name__ == "__main__":
    main()
