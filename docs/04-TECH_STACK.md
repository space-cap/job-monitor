# 04. Tech Stack

## Collector

- Python 3.13
- Requests: HTTP 수집
- BeautifulSoup4 + lxml: HTML 파싱
- Playwright: JavaScript 렌더링이 필요한 경우의 보조 수단
- PyMySQL: MariaDB 저장
- python-dotenv: 로컬 환경변수 관리
- tenacity: retry가 필요한 경우 사용

## Core

- Java 21
- Spring Boot 4.0.7
- Maven
- Jar
- Spring Web
- Thymeleaf
- MyBatis Framework
- Spring Boot DevTools
- MariaDB Driver
- Validation
- Lombok
- Actuator

## Database

- MariaDB 12.2.x 계열
- DB schema는 Core가 관리하는 것을 원칙으로 한다.

## 선택 이유

Collector는 HTML 수집/파싱 생태계가 강한 Python을 사용한다. Core는 DB 중심의 비즈니스 로직, Rule Engine, 알림, 웹 화면을 담당하므로 Java/Spring Boot를 사용한다.

Collector와 Core의 언어는 달라도 MariaDB를 공통 저장소로 사용한다.
