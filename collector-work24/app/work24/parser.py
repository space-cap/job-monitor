import hashlib
import re
from datetime import datetime
from typing import Iterable, Optional
from urllib.parse import parse_qs, urljoin, urlparse

from bs4 import BeautifulSoup, Tag

from app.config import WORK24_BASE_URL
from app.work24.models import Job

DATE_RE = re.compile(r"(20\d{2}-\d{2}-\d{2})")
SALARY_RE = re.compile(r"(?P<unit>시급|일급|월급|연봉)\s*(?P<min>[\d,]+)\s*만원?(?:\s*[~-]\s*(?P<max>[\d,]+)\s*만원?)?")


def _clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _parse_date(value: str):
    match = DATE_RE.search(value)
    if not match:
        return None
    return datetime.strptime(match.group(1), "%Y-%m-%d").date()


def _parse_salary(value: str):
    match = SALARY_RE.search(value.replace(" ", ""))
    if not match:
        return None, None, None

    unit_map = {"시급": "HOUR", "일급": "DAY", "월급": "MONTH", "연봉": "YEAR"}
    minimum = int(match.group("min").replace(",", "")) * 10000
    maximum = match.group("max")
    maximum_value = int(maximum.replace(",", "")) * 10000 if maximum else None
    return minimum, maximum_value, unit_map[match.group("unit")]


def _extract_external_id(url: str) -> Optional[str]:
    query = parse_qs(urlparse(url).query)
    for key in ("empSeqno", "empSeqNo", "seqNo", "joNo", "recruitNo", "wantedAuthNo"):
        values = query.get(key)
        if values and values[0]:
            return values[0]
    match = re.search(r"(?:empSeqno|empSeqNo|seqNo|joNo|recruitNo)[=/_-]([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else None


def _identity_hash(company: Optional[str], title: str, location: Optional[str], deadline, detail_url: str) -> str:
    stable = "|".join(
        [
            _clean(company or ""),
            _clean(title),
            _clean(location or ""),
            deadline.isoformat() if deadline else "",
            detail_url,
        ]
    )
    return hashlib.sha256(stable.encode("utf-8")).hexdigest()


def _card_for_title(title_link: Tag) -> Tag:
    current = title_link
    for _ in range(7):
        if not isinstance(current, Tag) or current.parent is None:
            break
        current = current.parent
        text = _clean(current.get_text(" ", strip=True))
        if DATE_RE.search(text) and len(text) < 2500:
            return current
    return title_link.parent if isinstance(title_link.parent, Tag) else title_link


def _text_lines(card: Tag) -> list[str]:
    return [_clean(x) for x in card.stripped_strings if _clean(x)]


def _parse_card(title_link: Tag) -> Job:
    card = _card_for_title(title_link)
    title = _clean(title_link.get_text(" ", strip=True))
    detail_url = urljoin(WORK24_BASE_URL, title_link.get("href", ""))
    lines = _text_lines(card)

    # The company is normally the link immediately before the title link.
    company_name = None
    previous_links = title_link.find_all_previous("a", limit=3)
    for link in previous_links:
        candidate = _clean(link.get_text(" ", strip=True))
        if candidate and candidate != title:
            company_name = candidate
            break

    full_text = " | ".join(lines)
    salary_text = next((line for line in lines if re.search(r"(?:시급|일급|월급|연봉)", line)), None)
    salary_min, salary_max, salary_unit = _parse_salary(salary_text or "")

    work_days = next((line for line in lines if re.search(r"주\s*[1-7]일", line)), None)
    work_hours = next((line for line in lines if re.search(r"\d{1,2}:\d{2}", line)), None)
    location = next(
        (line for line in lines if any(token in line for token in ("특별시", "광역시", "도 ", "시 ", "군 ", "구 ", "읍 ", "면 ", "동 "))),
        None,
    )

    deadline = _parse_date(full_text.split("등록일", 1)[0])
    posted_part = full_text.split("등록일", 1)[1] if "등록일" in full_text else ""
    posted_date = _parse_date(posted_part)

    provider_name = None
    if "정보제공처 고용24" in full_text:
        provider_name = "고용24"

    company_type = "공공" if "공공" in lines else None
    work24_application = True if "고용24 입사지원 가능" in full_text else None

    external_job_id = _extract_external_id(detail_url)
    identity_hash = _identity_hash(company_name, title, location, deadline, detail_url)

    return Job(
        title=title,
        detail_url=detail_url,
        identity_hash=identity_hash,
        external_job_id=external_job_id,
        company_name=company_name,
        provider_name=provider_name,
        location=location,
        salary_text=salary_text,
        salary_min=salary_min,
        salary_max=salary_max,
        salary_unit=salary_unit,
        work_days=work_days,
        work_hours=work_hours,
        deadline=deadline,
        posted_date=posted_date,
        company_type=company_type,
        work24_application=work24_application,
    )


def parse_list_page(html: str) -> list[Job]:
    soup = BeautifulSoup(html, "html.parser")
    links: Iterable[Tag] = soup.select('a[href*="/wk/a/b/1500/"]')

    jobs: list[Job] = []
    seen: set[str] = set()
    for link in links:
        title = _clean(link.get_text(" ", strip=True))
        if not title or len(title) > 500:
            continue
        href = link.get("href", "")
        if not href:
            continue
        url = urljoin(WORK24_BASE_URL, href)
        if url in seen:
            continue
        seen.add(url)
        jobs.append(_parse_card(link))

    return jobs
