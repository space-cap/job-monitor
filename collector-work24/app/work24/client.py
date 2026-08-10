from typing import Dict

import requests

from app.config import WORK24_BASE_URL, WORK24_PAGE_SIZE, WORK24_REQUEST_TIMEOUT


class Work24Client:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/151.0 Safari/537.36"
                ),
                "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
        )

    def fetch_list_page(self, page: int = 1) -> str:
        params: Dict[str, str] = {
            "searchMode": "Y",
            "siteClcd": "all",
            "empTpGbcd": "1",
            "currentPageNo": str(page),
            "pageIndex": str(page),
            "resultCnt": str(WORK24_PAGE_SIZE),
            "sortField": "DATE",
            "sortOrderBy": "DESC",
            "moreButtonYn": "Y",
            "keywordJobCont": "N",
            "academicGbnoEdu": "noEdu",
            "benefitSrchAndOr": "O",
        }

        response = self.session.get(
            WORK24_BASE_URL,
            params=params,
            timeout=WORK24_REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        return response.text
