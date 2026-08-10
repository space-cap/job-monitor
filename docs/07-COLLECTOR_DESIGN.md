# 07. Collector Design

## 1. 역할

`collector-work24`는 Work24에서 데이터를 수집하여 MariaDB에 저장하는 독립 Python 프로그램이다.

## 2. 처리 흐름

```text
Scheduler / 실행 명령
        |
        v
Work24 HTTP Client
        |
        v
List Parser
        |
        v
Detail Parser
        |
        v
Normalizer
        |
        v
Repository
        |
        v
MariaDB
```

## 3. 모듈 구조

```text
collector-work24/
├── src/
│   ├── config/
│   ├── http/
│   ├── parser/
│   ├── model/
│   ├── repository/
│   └── collector/
├── tests/
├── requirements.txt
├── .env.example
└── main.py
```

## 4. 수집과 저장

Collector는 JSON을 Core로 전달하는 중간 계층을 두지 않고 MariaDB에 직접 저장한다. 이를 통해 수집 결과가 즉시 영속화되고 Core가 나중에 독립적으로 처리할 수 있다.

## 5. 중복 처리

`source + source_job_id`를 공고의 논리적 식별자로 사용한다. 신규 공고는 INSERT하고 기존 공고는 필요한 필드를 UPDATE한다.

## 6. 실패 처리

- HTTP timeout
- 4xx/5xx
- HTML selector 불일치
- 상세 페이지 접근 실패
- DB connection 실패

각 오류는 로그와 `collection_runs`에 남긴다.

## 7. 실행 방식

초기에는 수동 실행으로 검증하고 이후 운영 환경에서 cron, systemd timer 또는 별도 scheduler를 사용할 수 있다. Collector 내부에 복잡한 비즈니스 Rule을 넣지 않는다.
