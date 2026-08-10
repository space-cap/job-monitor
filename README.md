# job-monitor

Work24 채용정보를 수집하고, 원하는 조건의 공고를 선별하여 Slack으로 알려주는 개인 맞춤형 채용 모니터링 시스템.

## 현재 목표

1. Work24 채용정보 수집
2. MariaDB 저장
3. Thymeleaf 화면에서 수집 결과 조회
4. 키워드/조건 기반 Rule Engine
5. 조건에 맞는 공고를 Slack으로 알림

## 현재 범위

- 수집 대상: Work24
- Collector: Python
- Core: Java 21 / Spring Boot 4.0.7 / Maven
- DB: MariaDB
- Persistence: MyBatis
- Web UI: Thymeleaf
- Notification: Slack

## Architecture

```text
Work24
   |
   v
collector-work24 (Python)
   |
   v
MariaDB
   |
   v
job-monitor-core (Spring Boot)
   |-- Thymeleaf
   |-- Rule Engine
   |-- Slack Notification
   `-- Scheduler / API
```

자세한 설계는 `docs/`를 참고한다.
