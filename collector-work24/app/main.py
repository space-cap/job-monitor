from sqlalchemy import text

from app.config import WORK24_INITIAL_START_DATE, validate_database_config
from app.database.connection import create_db_engine
from app.database.repository import save_jobs
from app.work24.client import Work24Client
from app.work24.parser import parse_list_page


def main() -> None:
    validate_database_config()
    engine = create_db_engine()
    client = Work24Client()

    page = 1
    total_parsed = 0
    total_inserted = 0
    total_updated = 0

    while True:
        html = client.fetch_list_page(page=page)
        jobs = parse_list_page(html)

        print(f"Work24 page {page} parsed jobs: {len(jobs)}")
        if not jobs:
            print("No jobs parsed. Stopping collection.")
            break

        # Work24 is sorted by registration date descending. Once the oldest
        # job on a page is before the inclusive 2026-07-01 cutoff, jobs after
        # that point are outside the initial collection range.
        page_jobs = []
        reached_cutoff = False
        for job in jobs:
            if job.posted_date is None:
                # Keep an undated record for now; it is safer not to silently
                # discard a real Work24 posting because of a parsing issue.
                page_jobs.append(job)
                continue

            if job.posted_date < WORK24_INITIAL_START_DATE:
                reached_cutoff = True
                continue

            page_jobs.append(job)

        if page_jobs:
            inserted, updated = save_jobs(engine, page_jobs)
            total_parsed += len(page_jobs)
            total_inserted += inserted
            total_updated += updated
            print(f"Page {page}: inserted={inserted}, updated={updated}")

        if reached_cutoff:
            print(
                f"Reached collection cutoff: {WORK24_INITIAL_START_DATE.isoformat()}"
            )
            break

        page += 1

    with engine.connect() as connection:
        count = connection.execute(
            text("SELECT COUNT(*) FROM jobs WHERE source_site = 'WORK24'")
        ).scalar_one()

    print(f"Total parsed in range: {total_parsed}")
    print(f"Total inserted: {total_inserted}")
    print(f"Total updated: {total_updated}")
    print(f"WORK24 jobs in DB: {count}")


if __name__ == "__main__":
    main()
