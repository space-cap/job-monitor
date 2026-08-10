# 03. System Architecture

## 1. 현재 구조

```text
                 Work24
                    |
                    v
        collector-work24 (Python)
          |  collect / parse / save
                    |
                    v
                 MariaDB
                    |
                    v
        job-monitor-core (Spring Boot)
          |        |          |
          v        v          v
      Thymeleaf  Rule      Slack
        Web UI   Engine   Notification
```

## 2. Collector

`collector-work24`는 독립 실행 가능한 Python 프로그램으로 설계한다.

책임:

- Work24 HTTP 요청
- 목록/상세 HTML 파싱
- 데이터 정규화
- MariaDB 저장
- 수집 실행 결과 기록

Collector는 Rule Engine이나 Slack을 직접 호출하지 않는다.

## 3. Core

`job-monitor-core`는 Java 21 + Spring Boot 4.0.7 기반이다.

책임:

- DB 조회/관리
- Thymeleaf 화면
- Rule Engine
- Slack Notification
- 관리용 REST API
- 수집/알림 상태 조회

## 4. DB 중심 구조

Collector가 수집한 결과는 바로 MariaDB에 저장한다. Core는 DB를 기준으로 데이터를 조회한다.

이 구조를 통해 Collector가 일시적으로 종료되더라도 이미 저장된 데이터와 알림 작업은 보존된다.

## 5. 향후 확장

다른 채용 사이트가 필요해질 경우 `collector-*`를 추가한다. Core의 공통 데이터 모델과 Rule/Notification은 최대한 재사용한다.
