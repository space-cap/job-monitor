from app.work24.parser import parse_list_page


def test_parse_list_page_extracts_job_card():
    html = """
    <html><body>
      <ul>
        <li>
          <a href="/company/123">테스트회사</a>
          <a href="/wk/a/b/1500/empDetail.do?empSeqno=ABC123">경비원 모집</a>
          <span>월급 270 만원 ~ 280 만원</span>
          <span>경력무관 학력무관</span>
          <span>주5일</span>
          <span>서울특별시 강남구</span>
          <span>마감일 : 2026-09-30 등록일 : 2026-08-10</span>
          <span>정보제공처 고용24</span>
        </li>
      </ul>
    </body></html>
    """

    jobs = parse_list_page(html)

    assert len(jobs) == 1
    job = jobs[0]
    assert job.title == "경비원 모집"
    assert job.company_name == "테스트회사"
    assert job.external_job_id == "ABC123"
    assert job.salary_unit == "MONTH"
    assert job.salary_min == 2_700_000
    assert job.salary_max == 2_800_000
    assert job.location == "서울특별시 강남구"
    assert job.provider_name == "고용24"
