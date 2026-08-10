import os

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
