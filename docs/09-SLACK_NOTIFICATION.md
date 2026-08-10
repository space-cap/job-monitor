# 09. Slack Notification

## 1. 목적

Rule에 일치한 신규 채용공고를 Slack으로 전달한다.

## 2. 메시지 구성

```text
[채용공고]
회사: 현대자동차
제목: 빌딩 경비원
근무지: 서울 강남구
급여: 월 2,700,000원
마감일: 2026-08-20

원문 보기: <URL>
```

## 3. 처리 원칙

- Slack 인증정보는 환경변수로 관리한다.
- 발송 성공/실패를 `notification_logs`에 저장한다.
- HTTP 오류 또는 rate limit에 대비한다.
- 중복 발송을 방지한다.

## 4. 향후 확장

현재는 Slack만 사용한다. 향후 이메일, Discord, Telegram 등 다른 채널을 추가할 수 있도록 Notification Service 인터페이스를 분리한다.
