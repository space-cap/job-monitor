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

## 3. 테이블 목록

| 테이블 | 설명 | 주요 역할 |
|---|---|---|
| `users` | Job Monitor 사용자 정보 | 향후 다중 사용자 및 사용자별 규칙 지원 |
| `jobs` | 수집된 채용공고 | 시스템의 핵심 채용정보 저장 |
| `collection_runs` | Collector 실행 이력 | 수집 상태와 통계 확인 |
| `rules` | 채용공고 필터/알림 규칙 | 경비, 미화, 보안 등의 조건 관리 |
| `notification_logs` | 알림 발송 이력 | Slack 중복 발송 방지 및 발송 결과 기록 |
| `job_raw_data` | 선택적 원본 데이터 | 파서 디버깅 및 수집 결과 재현 |

## 4. 컬럼 상세

### 4.1 `users` — 사용자

향후 여러 사람이 Job Monitor를 사용할 수 있도록 사용자 정보를 저장한다. MVP에서는 한 명만 사용해도 된다.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | BIGINT UNSIGNED | 내부 사용자 식별자(PK) |
| `email` | VARCHAR(255) | 사용자 이메일. 사용자 식별 및 로그인 확장용 |
| `name` | VARCHAR(100) | 화면에 표시할 사용자 이름 |
| `enabled` | TINYINT(1) | 사용자 활성화 여부. 1=활성, 0=비활성 |
| `created_at` | DATETIME(6) | 사용자 레코드 최초 생성 시각 |
| `updated_at` | DATETIME(6) | 사용자 레코드 최종 수정 시각 |

### 4.2 `jobs` — 채용공고

Work24 등 외부 채용사이트에서 수집한 채용공고의 표준화된 데이터를 저장한다.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | BIGINT UNSIGNED | Job Monitor 내부 채용공고 식별자(PK) |
| `source_site` | VARCHAR(30) | 실제로 수집한 사이트 코드. MVP는 `WORK24` |
| `provider_name` | VARCHAR(100) | Work24 화면에 표시되는 정보제공처. 예: 고용24, 잡코리아, 사람인 |
| `external_job_id` | VARCHAR(150) | 원본 사이트에서 확인되는 공고 고유 ID. 없을 수 있음 |
| `identity_hash` | CHAR(64) | 공고의 고유성을 판별하기 위한 SHA-256 해시. 원본 ID가 없거나 불안정할 때 사용 |
| `company_name` | VARCHAR(255) | 채용 회사 또는 기관명 |
| `title` | VARCHAR(500) | 채용공고 제목 |
| `location` | VARCHAR(500) | 근무 지역 또는 근무지 |
| `employment_type` | VARCHAR(200) | 고용형태. 예: 정규직, 계약직, 기간제, 아르바이트 |
| `job_type` | VARCHAR(100) | 직무 또는 채용 유형을 보조적으로 저장 |
| `salary_text` | VARCHAR(500) | 원문 급여 표현. 예: 월 270만원, 연봉 3,500만원 |
| `salary_min` | DECIMAL(15,2) | 파싱 가능한 경우 급여 최소값 |
| `salary_max` | DECIMAL(15,2) | 파싱 가능한 경우 급여 최대값 |
| `salary_unit` | VARCHAR(30) | 급여 단위. 예: HOUR, DAY, MONTH, YEAR |
| `career_text` | VARCHAR(200) | 원문 경력 조건 |
| `education_text` | VARCHAR(200) | 원문 학력 조건 |
| `work_days` | VARCHAR(200) | 근무 요일 또는 주당 근무일 |
| `work_hours` | VARCHAR(300) | 근무 시간 |
| `deadline` | DATE | 채용 마감일. 확인할 수 없으면 NULL |
| `posted_date` | DATE | 공고 등록일. 확인할 수 없으면 NULL |
| `detail_url` | VARCHAR(2000) | Work24 상세 공고 URL |
| `original_url` | VARCHAR(2000) | 정보제공처 원본 공고 URL. 확인 가능한 경우 저장 |
| `description` | MEDIUMTEXT | 주요 업무 또는 채용공고 설명 |
| `requirements` | MEDIUMTEXT | 지원자격 및 요구조건 |
| `benefits` | MEDIUMTEXT | 복리후생 및 제공 혜택 |
| `qualifications` | MEDIUMTEXT | 자격증, 우대조건 등 자격 관련 상세 정보 |
| `work24_application` | TINYINT(1) | 고용24 입사지원 가능 여부. 1=가능, 0=불가, NULL=확인 안 됨 |
| `company_type` | VARCHAR(100) | 기업형태 또는 기관 유형 |
| `remote_work` | TINYINT(1) | 재택/원격근무 여부. 1=해당, 0=아님, NULL=확인 안 됨 |
| `shift_work` | TINYINT(1) | 교대근무 여부. 1=해당, 0=아님, NULL=확인 안 됨 |
| `alternate_day_work` | TINYINT(1) | 격일근무 여부. 1=해당, 0=아님, NULL=확인 안 됨 |
| `status` | VARCHAR(30) | 공고 상태. 예: OPEN, CLOSED, UNKNOWN |
| `first_seen_at` | DATETIME(6) | Collector가 공고를 최초 발견한 시각 |
| `last_seen_at` | DATETIME(6) | Collector가 공고를 마지막으로 확인한 시각 |
| `closed_at` | DATETIME(6) | 공고 종료가 확인된 시각 |
| `created_at` | DATETIME(6) | 우리 DB에 최초 생성된 시각 |
| `updated_at` | DATETIME(6) | 우리 DB에서 마지막으로 변경된 시각 |

#### `jobs`에서 특히 헷갈리기 쉬운 컬럼

- `source_site`: **우리가 어디에서 수집했는가?** → 현재는 `WORK24`
- `provider_name`: **Work24가 이 공고의 정보제공처로 표시한 곳은 어디인가?** → 예: 고용24, 잡코리아
- `external_job_id`: **원본 사이트가 부여한 공고 ID는 무엇인가?**
- `identity_hash`: **원본 ID가 없을 때 같은 공고인지 판단하기 위한 우리 쪽 식별값**
- `detail_url`: **사용자가 Work24에서 공고를 확인할 URL**
- `original_url`: **정보제공처의 원본 URL. 확인 가능한 경우만 저장**
- `first_seen_at`: **우리가 처음 발견한 시간**
- `last_seen_at`: **가장 최근에 다시 확인한 시간**
- `created_at`: **우리 DB 레코드가 처음 만들어진 시간**
- `updated_at`: **우리 DB 레코드가 마지막으로 수정된 시간**

### 4.3 `collection_runs` — 수집 실행 이력

Collector가 한 번 실행될 때마다 한 건을 기록한다. Thymeleaf Dashboard에서 수집 상태와 통계를 보여주는 기반이 된다.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | BIGINT UNSIGNED | 수집 실행 이력 식별자(PK) |
| `source_site` | VARCHAR(30) | 수집 대상 사이트 코드. MVP는 `WORK24` |
| `started_at` | DATETIME(6) | Collector 실행 시작 시각 |
| `finished_at` | DATETIME(6) | Collector 실행 종료 시각. 실행 중이면 NULL |
| `status` | VARCHAR(30) | 실행 상태. 예: RUNNING, SUCCESS, PARTIAL, FAILED |
| `requested_pages` | INT UNSIGNED | 이번 실행에서 요청한 페이지 수 |
| `collected_count` | INT UNSIGNED | 파싱에 성공한 전체 공고 수 |
| `inserted_count` | INT UNSIGNED | 신규로 DB에 저장한 공고 수 |
| `updated_count` | INT UNSIGNED | 기존 공고 정보를 갱신한 수 |
| `duplicate_count` | INT UNSIGNED | 이미 존재하여 신규 저장하지 않은 중복 공고 수 |
| `error_count` | INT UNSIGNED | 수집 또는 저장 중 발생한 오류 수 |
| `error_message` | TEXT | 실패 또는 부분 실패 시 대표 오류 메시지 |

예를 들어 한 번의 수집 결과가 다음과 같이 표현될 수 있다.

```text
요청 페이지 : 2
수집        : 100건
신규        : 73건
수정        : 12건
중복        : 15건
오류        : 0건
```

### 4.4 `rules` — 알림 규칙

사용자가 어떤 채용공고를 받아볼지 정의한다. 최종 목표인 **"경비 키워드를 등록해 두면 수집 후 경비 관련 공고만 Slack으로 보내기"**를 구현하는 핵심 테이블이다.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | BIGINT UNSIGNED | 알림 규칙 식별자(PK) |
| `user_id` | BIGINT UNSIGNED | 규칙을 소유한 사용자 ID. 다중 사용자 지원용 |
| `name` | VARCHAR(100) | 관리 화면에 표시할 규칙 이름. 예: 강남 경비 |
| `enabled` | TINYINT(1) | 규칙 활성화 여부. 1=활성, 0=비활성 |
| `keyword_expression` | TEXT | 포함할 키워드. 예: 경비, 보안, 시설관리 |
| `exclude_expression` | TEXT | 제외할 키워드. 예: 영업, 보험 |
| `location_expression` | TEXT | 근무지 필터 조건 |
| `salary_min` | DECIMAL(15,2) | 알림 대상 최소 급여 조건 |
| `salary_max` | DECIMAL(15,2) | 알림 대상 최대 급여 조건 |
| `created_at` | DATETIME(6) | 규칙 최초 생성 시각 |
| `updated_at` | DATETIME(6) | 규칙 최종 수정 시각 |

예:

```text
규칙명       : 강남 경비
포함 키워드  : 경비, 보안
제외 키워드  : 영업
지역         : 강남구
최소 급여    : 2,500,000
활성화       : 예
```

### 4.5 `notification_logs` — 알림 발송 이력

Rule에 의해 특정 채용공고가 Slack 등으로 발송된 기록을 저장한다.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | BIGINT UNSIGNED | 알림 발송 이력 식별자(PK) |
| `rule_id` | BIGINT UNSIGNED | 어떤 규칙으로 발송했는지 식별 |
| `job_id` | BIGINT UNSIGNED | 어떤 채용공고를 발송했는지 식별 |
| `channel` | VARCHAR(30) | 발송 채널. MVP는 `SLACK` |
| `status` | VARCHAR(30) | 발송 상태. 예: PENDING, SENT, FAILED |
| `sent_at` | DATETIME(6) | 외부 채널 발송 완료 시각 |
| `error_message` | TEXT | 발송 실패 시 오류 메시지 |
| `created_at` | DATETIME(6) | 알림 이력 생성 시각 |

`rule_id + job_id + channel`을 UNIQUE로 두어 같은 공고가 같은 규칙과 같은 채널로 중복 발송되는 것을 방지한다.

### 4.6 `job_raw_data` — 선택적 원본 데이터

Collector가 받은 원본 HTML 또는 응답 데이터를 선택적으로 보관한다. 파서가 잘못 동작했을 때 원인을 확인하거나, 파서 수정 전후 결과를 비교할 때 유용하다.

MVP에서는 기본적으로 사용하지 않는다. 원문을 장기간 보관할 경우 저장공간, 개인정보, 이용약관 및 보존 필요성을 별도로 검토한다.

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | BIGINT UNSIGNED | 원본 데이터 식별자(PK) |
| `job_id` | BIGINT UNSIGNED | 원본 데이터와 연결된 채용공고 ID |
| `collection_run_id` | BIGINT UNSIGNED | 이 원본을 수집한 Collector 실행 ID |
| `content_type` | VARCHAR(100) | 원본 형식. 예: `text/html`, `application/json` |
| `payload` | MEDIUMTEXT | 수집 당시 원본 HTML 또는 파싱 원문 |
| `created_at` | DATETIME(6) | 원본 데이터 저장 시각 |

## 5. 테이블 관계

```text
users
  │
  └──────────────< rules
                     │
                     └──────────────< notification_logs >──────────── jobs
                                                                    │
                                                                    └──< job_raw_data

collection_runs
  │
  └──────────────< job_raw_data
```

- 한 사용자는 여러 개의 `rules`를 가질 수 있다.
- 하나의 `rule`은 여러 `notification_logs`를 만든다.
- 하나의 `job`은 여러 번 수집될 수 있고, 여러 Rule에 의해 여러 번 알림 대상이 될 수 있다.
- 하나의 `job`에 여러 원본 데이터를 남길 수 있다.
- 하나의 `collection_run`에 여러 원본 데이터가 연결될 수 있다.

## 6. 인덱스 전략

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

## 7. 중복 방지 전략

Collector는 같은 공고를 여러 번 만나게 된다. 따라서 다음 순서로 동일 공고 여부를 판단한다.

1. 원본 사이트에서 안정적인 `external_job_id`를 확인할 수 있으면 사용한다.
2. 원본 ID가 없거나 신뢰하기 어려우면 `identity_hash`를 사용한다.
3. 기존 공고이면 `last_seen_at`을 갱신한다.
4. 신규 공고이면 `first_seen_at`과 `created_at`을 기록한다.

현재 DDL에는 다음 두 UNIQUE 제약을 둔다.

```text
(source_site, external_job_id)
identity_hash
```

## 8. 수집/저장 원칙

1. Collector는 Work24 목록 페이지에서 기본 정보를 수집한다.
2. 필요한 경우 상세 페이지를 방문하여 추가 정보를 보강한다.
3. 수집 데이터는 Collector가 MariaDB에 직접 저장한다.
4. 기존 공고는 `last_seen_at`을 갱신한다.
5. 신규 공고는 `first_seen_at`을 기록한다.
6. 마감 여부는 Collector가 확인 가능한 범위에서 `status`를 갱신한다.
7. Slack 발송 여부는 `jobs`에 넣지 않고 `notification_logs`에서 관리한다.
8. Collector가 중단되더라도 이미 DB에 저장된 공고와 수집 이력은 유지되어야 한다.

## 9. 보안

DB 접속정보, 비밀번호, Slack Webhook URL은 GitHub에 저장하지 않는다. 환경변수 또는 운영 비밀관리 기능을 사용한다.

애플리케이션은 가능하면 MariaDB `root` 계정이 아닌 Job Monitor 전용 DB 사용자를 사용한다.

## 10. DDL

실제 실행 가능한 초기 스키마는 [`database/schema.sql`](../database/schema.sql)에 관리한다.

`schema.sql`에는 모든 테이블과 주요 컬럼에 MariaDB `COMMENT`를 작성하여 DB 자체에서도 컬럼의 의미를 확인할 수 있도록 했다.
