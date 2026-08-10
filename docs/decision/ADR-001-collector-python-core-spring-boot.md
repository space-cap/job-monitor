# ADR-001: Collector는 Python, Core는 Spring Boot를 사용한다

## Status

Accepted

## Context

이 프로젝트의 수집 작업은 HTML 요청, 파싱, 페이지네이션, 향후 브라우저 자동화 등 크롤링 중심이다. 반면 Core는 DB 조회, Rule Engine, Slack 알림, Thymeleaf 화면과 향후 사용자/권한 관리가 중심이다.

## Decision

- `collector-work24`: Python 3.13
- `job-monitor-core`: Java 21 + Spring Boot 4.0.7
- 공통 저장소: MariaDB

Collector는 Work24 데이터를 수집하여 DB에 직접 저장한다. Core는 DB를 기준으로 비즈니스 로직을 수행한다.

## Consequences

장점:

- 각 영역에 적합한 기술을 사용할 수 있다.
- Work24 HTML 구조 변경이 Core에 직접 영향을 주지 않는다.
- Collector와 Core를 독립적으로 실행/장애처리할 수 있다.

단점:

- Python과 Java 두 런타임을 관리해야 한다.
- DB schema 변경 시 두 애플리케이션의 호환성을 관리해야 한다.

## Revisit

실제 운영 규모가 커져 배포/운영 복잡도가 높아질 경우 Collector와 Core의 배포 방식을 재검토한다.
