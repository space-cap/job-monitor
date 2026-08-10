import os
from datetime import date

from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "job_monitor")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

WORK24_BASE_URL = os.getenv(
    "WORK24_BASE_URL",
    "https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do",
)
WORK24_PAGE_SIZE = int(os.getenv("WORK24_PAGE_SIZE", "50"))
WORK24_REQUEST_TIMEOUT = int(os.getenv("WORK24_REQUEST_TIMEOUT", "20"))
WORK24_INITIAL_START_DATE = date.fromisoformat(
    os.getenv("WORK24_INITIAL_START_DATE", "2026-07-01")
)
WORK24_REQUEST_DELAY_MIN = float(os.getenv("WORK24_REQUEST_DELAY_MIN", "1.5"))
WORK24_REQUEST_DELAY_MAX = float(os.getenv("WORK24_REQUEST_DELAY_MAX", "3.0"))

if WORK24_REQUEST_DELAY_MIN < 0 or WORK24_REQUEST_DELAY_MAX < 0:
    raise ValueError("WORK24 request delays must be >= 0")
if WORK24_REQUEST_DELAY_MIN > WORK24_REQUEST_DELAY_MAX:
    raise ValueError("WORK24_REQUEST_DELAY_MIN must be <= WORK24_REQUEST_DELAY_MAX")


def validate_database_config() -> None:
    missing = [
        name
        for name, value in {
            "DB_USER": DB_USER,
            "DB_PASSWORD": DB_PASSWORD,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(
            "Missing database environment variables: " + ", ".join(missing)
        )
