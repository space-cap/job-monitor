# docs/

이 디렉토리는 `job-monitor` 프로젝트의 설계 문서를 담는다.

## 문서 목록

| 번호 | 문서 | 설명 |
|------|------|------|
| 01 | [PROJECT_VISION](./01-PROJECT_VISION.md) | 프로젝트 목적, 핵심 사용자 시나리오, 장기 방향 |
| 02 | [REQUIREMENTS](./02-REQUIREMENTS.md) | MVP 기능 요구사항, 비기능 요구사항, MVP 제외 항목 |
| 03 | [SYSTEM_ARCHITECTURE](./03-SYSTEM_ARCHITECTURE.md) | Collector/Core 역할 분리, DB 중심 구조 설명 |
| 04 | [TECH_STACK](./04-TECH_STACK.md) | Python/Java/MariaDB 기술 선택과 이유 |
| 05 | [DATABASE_DESIGN](./05-DATABASE_DESIGN.md) | 핵심 테이블 구조 및 설계 원칙 |
| 06 | [WORK24_ANALYSIS](./06-WORK24_ANALYSIS.md) | Work24 수집 대상 분석, 파싱 전략, 주의사항 |
| 07 | [COLLECTOR_DESIGN](./07-COLLECTOR_DESIGN.md) | collector-work24 Python 모듈 구조 및 처리 흐름 |
| 08 | [RULE_ENGINE](./08-RULE_ENGINE.md) | 공고 선별 Rule 정의, 처리 흐름, 향후 확장 |
| 09 | [SLACK_NOTIFICATION](./09-SLACK_NOTIFICATION.md) | Slack 알림 방식, 메시지 포맷, 실패 처리 |
| 10 | [DEVELOPMENT_ROADMAP](./10-DEVELOPMENT_ROADMAP.md) | Phase별 개발 체크리스트 |
| 11 | [CODING_CONVENTION](./11-CODING_CONVENTION.md) | Java/Python/Git 코딩 규칙 |
| 12 | [TODO](./12-TODO.md) | 지금 당장 해야 할 일 목록 |

## 의사결정 기록 (ADR)

| 번호 | 문서 | 결정 |
|------|------|------|
| ADR-001 | [collector-python-core-spring-boot](./decision/ADR-001-collector-python-core-spring-boot.md) | Collector는 Python, Core는 Spring Boot를 사용한다 |

## 읽는 순서

처음 이 프로젝트를 파악하는 경우 다음 순서로 읽는 것을 권장한다.

```
01 → 02 → 03 → 04 → ADR-001 → 05 → 06 → 07 → 08 → 09 → 10
```
