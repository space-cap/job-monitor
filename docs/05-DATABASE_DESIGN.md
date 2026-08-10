# 05. Database Design

## 1. 설계 목적

Job Monitor의 데이터 중심은 MariaDB이다.

```text
Work24
  ↓
collector-work24 (Python)
  ↓
MariaDB
  ↓
job-monitor-core (Spring Boot)
  ↓
Thymeleaf / Rule Engine / Slack
```

Collector는 수집한 채용정보를 DB에 직접 저장한다. Core는 DB에 저장된 데이터를 조회하고 규칙을 적용하며 Slack 알림을 처리한다.

## 2. 실제 Work24 목록 화면 기준

현재 Work24 채용정보 상세검색 화면에서 목록에는 다음 정보가 노출된다.

- 회사명
- 채용공고명
- 정보제공처
- 기업형태
- 급여
- 경력
- 학력
- 근무형태/근무시간
- 근무지
- 마감일
- 등록일
- 고용24 입사지원 가능 여부

Work24는 여러 정보제공처의 채용정보를 함께 보여주므로 `source_site`와 `provider_name`을 분리한다. 현재 MVP의 수집 대상은 Work24이지만, 목록의 정보제공처는 고용24, 잡코리아, 사람인 등으로 달라질 수 있다.

실제 화면에서도 예를 들어 정보제공처가 '고용24'로 표시되고, 급여·경력·학력·근무조건·지역·마감일·등록일이 함께 노출되는 것을 확인할 수 있다. citeturn1view0

## 3. 핵심 테이블

### 3.1 jobs

정규화된 채용공고를 저장한다.

주요 컬럼:

- `id`: 내부 PK
- `source_site`: 현재 `WORK24`
- `provider_name`: Work24에 표시되는 정보제공처
- `external_job_id`: 원본 사이트에서 식별 가능한 공고 ID
- `identity_hash`: 원본 ID가 없을 때 사용하는 안정적인 중복 식별값
- `company_name`
- `title`
- `location`
- `employment_type`
- `salary_text`
- `salary_min`, `salary_max`, `salary_unit`
- `career_text`
- `education_text`
- `work_days`, `work_hours`
- `deadline`, `posted_date`
- `detail_url`, `original_url`
- `description`, `requirements`, `benefits`, `qualifications`
- `work24_application`
- `company_type`
- `remote_work`, `shift_work`, `alternate_day_work`
- `status`
- `first_seen_at`, `last_seen_at`, `closed_at`
- `created_at`, `updated_at`

중복 방지를 위해 `identity_hash`를 unique로 관리하고, 원본 ID가 확보되는 경우 `source_site + external_job_id`도 unique로 관리한다.

### 3.2 collection_runs

Collector 실행 이력을 저장한다.

- 실행 시작/종료 시간
- 상태
- 요청 페이지 수
- 수집 건수
- 신규 저장 건수
- 수정 건수
- 중복 건수
- 오류 건수
- 오류 메시지

이를 통해 Thymeleaf의 Collector 상태 화면과 수집 통계를 구현할 수 있다.

### 3.3 users

현재는 1인 사용을 전제로 개발하지만, 향후 여러 사용자가 각자 규칙을 등록할 수 있도록 최소한의 사용자 테이블을 미리 둔다.

### 3.4 rules

사용자의 채용공고 필터 조건을 저장한다.

MVP에서는 다음을 중심으로 시작한다.

- 키워드 표현식
- 제외 키워드
- 지역 조건
- 최소/최대 급여
- 활성화 여부

예: `경비`, `시설관리`, `미화`, `보안`

### 3.5 notification_logs

Rule에 의해 Slack 등으로 발송된 기록을 저장한다.

`rule_id + job_id + channel` unique 제약으로 동일 공고가 동일 Rule/채널로 중복 발송되는 것을 방지한다.

### 3.6 job_raw_data

원본 HTML 또는 파싱 원문을 선택적으로 보관한다.

MVP에서는 기본적으로 비활성화한다. 디버깅 또는 파서 변경 검증에 필요할 때만 사용하고, 저장 용량 및 이용약관/개인정보·불필요한 원문 보존 여부를 검토한다.

## 4. 인덱스 전략

초기 검색/조회에서 다음을 우선한다.

- 공고 제목
- 회사명
- 근무지
- 등록일
- 마감일
- 상태
- 정보제공처
- 최초 수집 시각

키워드 검색은 MVP에서는 DB의 `LIKE` 검색으로 시작하고, 데이터량과 검색 성능을 확인한 후 전문검색(Full-Text) 또는 별도 검색 구조를 검토한다.

## 5. 수집/저장 원칙

1. Collector는 목록 페이지에서 수집한다.
2. 가능한 경우 상세 페이지에서 추가 정보를 보강한다.
3. `external_job_id` 또는 `identity_hash`로 중복을 판별한다.
4. 기존 공고는 `last_seen_at`을 갱신한다.
5. 신규 공고는 `first_seen_at`을 기록한다.
6. 마감 여부는 Collector가 확인 가능한 범위에서 `status`를 갱신한다.
7. Slack 발송 여부는 `jobs`가 아니라 `notification_logs`에서 관리한다.

## 6. 보안

DB 접속정보, 비밀번호, Slack Webhook URL은 GitHub에 저장하지 않는다. 환경변수 또는 운영 비밀관리 기능을 사용한다.

애플리케이션은 가능하면 MariaDB `root` 계정이 아닌 전용 DB 사용자를 사용한다.

## 7. DDL

실제 실행 가능한 초기 스키마는 [`database/schema.sql`](../database/schema.sql)에 관리한다.
