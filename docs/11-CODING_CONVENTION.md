# 11. Coding Convention

## Java

- Java 21 기준
- package는 소문자
- Controller / Service / Mapper / Model 역할을 분리한다.
- 비즈니스 로직은 Controller에 넣지 않는다.
- SQL은 MyBatis Mapper XML 또는 명시적인 Mapper 인터페이스로 관리한다.
- 환경설정과 비밀정보는 환경변수로 분리한다.

## Python

- Python 3.13 기준
- PEP 8 준수
- 함수는 한 가지 책임을 갖도록 한다.
- HTTP, parser, repository를 분리한다.
- 타입 힌트를 적극적으로 사용한다.
- 예외를 무시하지 않는다.

## Git

Commit 예시:

```text
feat: add Work24 list parser
fix: handle missing salary field
docs: update Work24 analysis
refactor: separate job repository
```

작은 단위로 커밋하고 커밋 메시지는 변경 목적이 드러나게 작성한다.
