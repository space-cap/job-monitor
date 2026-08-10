# 05. Database Design

## 1. 설계 원칙

- 공고의 원본 식별자를 기준으로 중복을 방지한다.
- 검색에 자주 사용하는 컬럼에는 인덱스를 둔다.
- Collector와 Core가 동일한 데이터 계약을 사용한다.
- 알림 상태와 수집 상태를 분리한다.

## 2. 핵심 테이블

### jobs

채용공고의 공통 정보를 저장한다.

예상 컬럼:

- id
- source
- source_job_id
- title
- company_name
- location
- salary_text
- employment_type
- career_text
- education_text
- deadline
- detail_url
- description
- first_seen_at
- last_seen_at
- created_at
- updated_at

`source + source_job_id`는 unique로 관리한다.

### job_raw_data

필요한 경우 원본 HTML 또는 파싱 원문을 보존한다. 초기 MVP에서는 저장 크기와 개인정보/약관을 검토한 후 활성화한다.

### collection_runs

수집 실행 이력을 기록한다.

예상 컬럼:

- id
- source
- started_at
- finished_at
- status
- requested_pages
- collected_count
- inserted_count
- updated_count
- duplicate_count
- error_count
- error_message

### rules

사용자가 등록한 검색/알림 조건을 저장한다.

예상 컬럼:

- id
- name
- enabled
- keyword_expression
- location_expression
- salary_min
- created_at
- updated_at

### notification_logs

공고별 Rule 알림 이력을 저장한다.

예상 컬럼:

- id
- rule_id
- job_id
- channel
- status
- sent_at
- error_message

`rule_id + job_id + channel`은 중복 알림 방지를 위한 unique 후보이다.

## 3. 보안

DB 접속정보, 비밀번호, Slack Webhook URL은 GitHub에 저장하지 않는다. 환경변수 또는 운영 비밀관리 기능을 사용한다.
