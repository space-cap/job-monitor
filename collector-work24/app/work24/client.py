import logging
import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.config import WORK24_BASE_URL, WORK24_PAGE_SIZE, WORK24_REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

# Exact first-page URL supplied by the user. We preserve all search conditions
# and change only pageIndex when collecting subsequent pages.
WORK24_FIRST_PAGE_URL = (
    "https://www.work24.go.kr/wk/a/b/1200/retriveDtlEmpSrchList.do?"
    "basicSetupYn=&careerTo=&keywordJobCd=&occupation=&seqNo=&cloDateEndtParam="
    "&payGbn=&templateInfo=&rot2WorkYn=&shsyWorkSecd=&resultCnt=50"
    "&keywordJobCont=N&cert=&moreButtonYn=&minPay=&codeDepth2Info=11000"
    "&currentPageNo=2&eventNo=&mode=&isChkLocCall=&major=&resrDutyExcYn="
    "&eodwYn=&sortField=DATE&staArea=&sortOrderBy=DESC&keyword="
    "&termSearchGbn=&carrEssYns=&benefitSrchAndOr=O&disableEmpHopeGbn="
    "&actServExcYn=&keywordStaAreaNm=N&maxPay=&emailApplyYn=&codeDepth1Info=11000"
    "&keywordEtcYn=&regDateStdtParam=&publDutyExcYn=&keywordJobCdSeqNo="
    "&viewType=&exJobsCd=&templateDepthNmInfo=&region=&employGbn=&empTpGbcd=1"
    "&computerPreferential=&infaYn=&cloDateStdtParam=&siteClcd=all&searchMode=Y"
    "&birthFromYY=&indArea=&careerTypes=&subEmpHopeYn=&tlmgYn=&academicGbn="
    "&templateDepthNoInfo=&foriegn=&entryRoute=&mealOfferClcd=&basicSetupYnChk="
    "&station=&holidayGbn=&srcKeyword=&academicGbnoEdu=noEdu&enterPriseGbn="
    "&cloTermSearchGbn=&birthToYY=&keywordWantedTitle=N&stationNm=&benefitGbn="
    "&keywordFlag=&notSrcKeyword=&essCertChk=&depth2SelCode=&keywordBusiNm=N"
    "&preferentialGbn=&rot3WorkYn=&regDateEndtParam=&pfMatterPreferential="
    "&pageIndex=1&termContractMmcnt=&careerFrom=&laborHrShortYn="
)


class Work24Client:
    def __init__(self, max_retries: int = 5, backoff_factor: float = 2.0) -> None:
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/151.0 Safari/537.36"
                ),
                "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://www.work24.go.kr/",
                "Connection": "keep-alive",
            }
        )

        retry_strategy = Retry(
            total=self.max_retries,
            backoff_factor=self.backoff_factor,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            raise_on_status=False,
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def fetch_list_page(self, page: int = 1) -> str:
        if page < 1:
            raise ValueError("page must be >= 1")

        base = WORK24_FIRST_PAGE_URL or WORK24_BASE_URL
        parts = urlsplit(base)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        query["resultCnt"] = str(WORK24_PAGE_SIZE)
        query["pageIndex"] = str(page)

        url = urlunsplit(
            (
                parts.scheme,
                parts.netloc,
                parts.path,
                urlencode(query),
                parts.fragment,
            )
        )

        # Retry loop for ConnectionError / RemoteDisconnected
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.get(url, timeout=WORK24_REQUEST_TIMEOUT)
                response.raise_for_status()
                response.encoding = response.apparent_encoding or "utf-8"
                return response.text
            except (requests.exceptions.RequestException, Exception) as e:
                if attempt == self.max_retries:
                    logger.error(f"[Page {page}] Final retry failed: {e}")
                    raise
                wait_time = self.backoff_factor * (2 ** (attempt - 1)) + 1.0
                print(
                    f"\n[Warning] Page {page} request failed ({e}). "
                    f"Retrying in {wait_time:.1f}s (Attempt {attempt}/{self.max_retries})..."
                )
                time.sleep(wait_time)
                # Reset session if connection was aborted
                self.session = self._create_session()

