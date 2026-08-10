-- Job Monitor / MariaDB schema
-- Target: MariaDB 12.x
-- Character set: utf8mb4
--
-- IMPORTANT:
-- 1. Application credentials must be supplied through environment variables.
-- 2. Do not commit real passwords, tokens, or Slack webhook URLs.
-- 3. The Work24 collector writes directly to this database.

CREATE DATABASE IF NOT EXISTS job_monitor
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE job_monitor;

-- ============================================================
-- Users
-- 서비스 사용자. MVP에서는 1인 사용으로 시작하지만 향후 다중 사용자 지원을 위해 둔다.
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id              BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '내부 사용자 식별자(PK)',
    email           VARCHAR(255) NOT NULL COMMENT '사용자 이메일 주소. 사용자 식별 및 로그인 확장용',
    name            VARCHAR(100) NOT NULL COMMENT '사용자 표시 이름',
    enabled         TINYINT(1) NOT NULL DEFAULT 1 COMMENT '사용자 활성화 여부. 1=활성, 0=비활성',
    created_at      DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '사용자 레코드 최초 생성 시각',
    updated_at      DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '사용자 레코드 최종 수정 시각',
    PRIMARY KEY (id),
    UNIQUE KEY uk_users_email (email),
    KEY idx_users_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Job Monitor 사용자 정보. 향후 다중 사용자 지원을 위한 기본 사용자 테이블';

-- ============================================================
-- Jobs
-- Work24 등에서 수집한 정규화된 채용공고.
-- Work24는 여러 정보제공처의 공고를 보여주므로 source_site와 provider_name을 분리한다.
-- ============================================================
CREATE TABLE IF NOT EXISTS jobs (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Job Monitor 내부 채용공고 식별자(PK)',
    source_site              VARCHAR(30) NOT NULL DEFAULT 'WORK24' COMMENT '실제로 수집한 사이트 코드. MVP는 WORK24',
    provider_name            VARCHAR(100) NULL COMMENT 'Work24 화면에 표시되는 정보제공처. 예: 고용24, 잡코리아, 사람인',
    external_job_id          VARCHAR(150) NULL COMMENT '원본 사이트에서 확인되는 공고 고유 ID. 없을 수 있음',
    identity_hash            CHAR(64) NOT NULL COMMENT 'external_job_id가 없거나 불안정할 때 사용하는 공고 고유성 판별용 SHA-256 해시',
    company_name             VARCHAR(255) NULL COMMENT '채용을 진행하는 회사 또는 기관명',
    title                    VARCHAR(500) NOT NULL COMMENT '채용공고 제목',
    location                 VARCHAR(500) NULL COMMENT '근무 지역 또는 근무지. Work24 원문 기준',
    employment_type          VARCHAR(200) NULL COMMENT '고용형태. 예: 정규직, 계약직, 기간제, 아르바이트 등',
    job_type                 VARCHAR(100) NULL COMMENT '직무 또는 채용 유형을 보조적으로 저장하는 값',
    salary_text              VARCHAR(500) NULL COMMENT '원문에 표시된 급여 정보. 예: 월 270만원, 연봉 3,500만원',
    salary_min               DECIMAL(15,2) NULL COMMENT '파싱 가능한 경우 급여의 최소값',
    salary_max               DECIMAL(15,2) NULL COMMENT '파싱 가능한 경우 급여의 최대값',
    salary_unit              VARCHAR(30) NULL COMMENT '급여 단위. 예: HOUR, DAY, MONTH, YEAR',
    career_text              VARCHAR(200) NULL COMMENT '원문에 표시된 경력 조건',
    education_text           VARCHAR(200) NULL COMMENT '원문에 표시된 학력 조건',
    work_days                VARCHAR(200) NULL COMMENT '근무 요일 또는 주당 근무일 정보',
    work_hours               VARCHAR(300) NULL COMMENT '근무 시간 정보',
    deadline                 DATE NULL COMMENT '채용 마감일. 확인할 수 없는 경우 NULL',
    posted_date              DATE NULL COMMENT '공고 등록일. 원문에서 확인 가능한 경우 저장',
    detail_url               VARCHAR(2000) NOT NULL COMMENT 'Work24에서 상세 공고를 열기 위한 URL',
    original_url             VARCHAR(2000) NULL COMMENT '정보제공처의 원본 공고 URL. 확인 가능한 경우 저장',
    description              MEDIUMTEXT NULL COMMENT '채용공고의 주요 업무 또는 전체 설명',
    requirements             MEDIUMTEXT NULL COMMENT '지원자격 및 요구조건',
    benefits                 MEDIUMTEXT NULL COMMENT '복리후생 및 제공 혜택',
    qualifications           MEDIUMTEXT NULL COMMENT '자격증, 우대조건 등 자격 관련 상세 정보',
    work24_application       TINYINT(1) NULL COMMENT '고용24를 통한 입사지원 가능 여부. 1=가능, 0=불가, NULL=확인 안 됨',
    company_type             VARCHAR(100) NULL COMMENT '기업형태 또는 기관 유형',
    remote_work              TINYINT(1) NULL COMMENT '재택/원격근무 여부. 1=해당, 0=아님, NULL=확인 안 됨',
    shift_work               TINYINT(1) NULL COMMENT '교대근무 여부. 1=해당, 0=아님, NULL=확인 안 됨',
    alternate_day_work       TINYINT(1) NULL COMMENT '격일근무 여부. 1=해당, 0=아님, NULL=확인 안 됨',
    status                   VARCHAR(30) NOT NULL DEFAULT 'OPEN' COMMENT '공고 상태. 예: OPEN, CLOSED, UNKNOWN',
    first_seen_at            DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Collector가 이 공고를 최초 발견한 시각',
    last_seen_at             DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'Collector가 마지막으로 이 공고를 확인한 시각',
    closed_at                DATETIME(6) NULL COMMENT '공고가 종료된 것으로 확인된 시각',
    created_at               DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT 'jobs 레코드가 DB에 최초 생성된 시각',
    updated_at               DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT 'jobs 레코드가 마지막으로 변경된 시각',
    PRIMARY KEY (id),
    UNIQUE KEY uk_jobs_identity_hash (identity_hash),
    UNIQUE KEY uk_jobs_source_external (source_site, external_job_id),
    KEY idx_jobs_title (title(191)),
    KEY idx_jobs_company (company_name(191)),
    KEY idx_jobs_location (location(191)),
    KEY idx_jobs_deadline (deadline),
    KEY idx_jobs_posted_date (posted_date),
    KEY idx_jobs_status (status),
    KEY idx_jobs_source_provider (source_site, provider_name),
    KEY idx_jobs_first_seen (first_seen_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Work24 등 외부 채용사이트에서 수집한 정규화 채용공고';

-- ============================================================
-- Collection runs
-- Collector가 한 번 실행될 때마다 한 건을 기록한다.
-- ============================================================
CREATE TABLE IF NOT EXISTS collection_runs (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '수집 실행 이력 식별자(PK)',
    source_site              VARCHAR(30) NOT NULL COMMENT '수집 대상 사이트 코드. MVP는 WORK24',
    started_at               DATETIME(6) NOT NULL COMMENT 'Collector 실행 시작 시각',
    finished_at              DATETIME(6) NULL COMMENT 'Collector 실행 종료 시각. 실행 중이면 NULL',
    status                   VARCHAR(30) NOT NULL DEFAULT 'RUNNING' COMMENT '수집 실행 상태. RUNNING, SUCCESS, PARTIAL, FAILED 등',
    requested_pages          INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '이번 실행에서 요청한 페이지 수',
    collected_count          INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '파싱에 성공한 전체 공고 수',
    inserted_count           INT UNSIGNED NOT NULL DEFAULT 0 COMMENT 'DB에 신규로 저장한 공고 수',
    updated_count            INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '기존 공고 정보를 갱신한 수',
    duplicate_count          INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '이미 존재하여 신규 저장하지 않은 중복 공고 수',
    error_count              INT UNSIGNED NOT NULL DEFAULT 0 COMMENT '수집 또는 저장 중 발생한 오류 수',
    error_message            TEXT NULL COMMENT '실행 실패 또는 부분 실패 시 대표 오류 메시지',
    PRIMARY KEY (id),
    KEY idx_collection_runs_source_started (source_site, started_at),
    KEY idx_collection_runs_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='채용정보 Collector의 실행 이력 및 수집 통계';

-- ============================================================
-- Rules
-- 사용자가 어떤 채용공고를 Slack으로 받을지 정의하는 규칙.
-- ============================================================
CREATE TABLE IF NOT EXISTS rules (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '알림 규칙 식별자(PK)',
    user_id                 BIGINT UNSIGNED NULL COMMENT '규칙 소유 사용자 ID. MVP에서는 NULL 또는 단일 사용자 사용 가능',
    name                    VARCHAR(100) NOT NULL COMMENT '관리 화면에서 표시할 규칙 이름',
    enabled                 TINYINT(1) NOT NULL DEFAULT 1 COMMENT '규칙 활성화 여부. 1=활성, 0=비활성',
    keyword_expression      TEXT NULL COMMENT '포함할 키워드 또는 키워드 표현식. 예: 경비, 보안, 시설관리',
    exclude_expression      TEXT NULL COMMENT '제외할 키워드 또는 표현식. 예: 영업, 보험',
    location_expression     TEXT NULL COMMENT '근무지 필터 조건',
    salary_min               DECIMAL(15,2) NULL COMMENT '알림 대상 최소 급여 조건',
    salary_max               DECIMAL(15,2) NULL COMMENT '알림 대상 최대 급여 조건',
    created_at               DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '규칙 최초 생성 시각',
    updated_at               DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6) COMMENT '규칙 최종 수정 시각',
    PRIMARY KEY (id),
    KEY idx_rules_user_enabled (user_id, enabled),
    CONSTRAINT fk_rules_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='채용공고 필터링 및 Slack 알림 조건';

-- ============================================================
-- Notification logs
-- Rule이 특정 공고를 특정 채널로 발송한 기록.
-- ============================================================
CREATE TABLE IF NOT EXISTS notification_logs (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '알림 발송 이력 식별자(PK)',
    rule_id                 BIGINT UNSIGNED NOT NULL COMMENT '적용된 알림 규칙 ID',
    job_id                  BIGINT UNSIGNED NOT NULL COMMENT '알림을 발송한 채용공고 ID',
    channel                 VARCHAR(30) NOT NULL COMMENT '알림 채널. MVP는 SLACK',
    status                  VARCHAR(30) NOT NULL DEFAULT 'PENDING' COMMENT '발송 상태. PENDING, SENT, FAILED 등',
    sent_at                 DATETIME(6) NULL COMMENT '외부 채널에 실제 발송이 완료된 시각',
    error_message           TEXT NULL COMMENT '발송 실패 시 오류 메시지',
    created_at              DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '알림 이력 생성 시각',
    PRIMARY KEY (id),
    UNIQUE KEY uk_notification_rule_job_channel (rule_id, job_id, channel),
    KEY idx_notification_job (job_id),
    KEY idx_notification_status (status),
    CONSTRAINT fk_notification_rule
        FOREIGN KEY (rule_id) REFERENCES rules(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_notification_job
        FOREIGN KEY (job_id) REFERENCES jobs(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='채용공고의 Slack 등 알림 발송 이력';

-- ============================================================
-- Optional raw payload storage
-- 디버깅/재현 목적의 원문 보관. MVP에서는 애플리케이션에서 기본 비활성화.
-- ============================================================
CREATE TABLE IF NOT EXISTS job_raw_data (
    id                      BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '원본 데이터 레코드 식별자(PK)',
    job_id                  BIGINT UNSIGNED NOT NULL COMMENT '원본 데이터가 연결된 채용공고 ID',
    collection_run_id       BIGINT UNSIGNED NULL COMMENT '원본을 수집한 Collector 실행 ID',
    content_type            VARCHAR(100) NULL COMMENT '원본 데이터 형식. 예: text/html, application/json',
    payload                 MEDIUMTEXT NOT NULL COMMENT '수집 당시의 원문 HTML 또는 파싱 원문 데이터',
    created_at               DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) COMMENT '원본 데이터 저장 시각',
    PRIMARY KEY (id),
    KEY idx_job_raw_job (job_id),
    KEY idx_job_raw_run (collection_run_id),
    CONSTRAINT fk_job_raw_job
        FOREIGN KEY (job_id) REFERENCES jobs(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_job_raw_run
        FOREIGN KEY (collection_run_id) REFERENCES collection_runs(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='채용공고 원본 HTML/응답 데이터 보관. 디버깅 목적의 선택 기능';
