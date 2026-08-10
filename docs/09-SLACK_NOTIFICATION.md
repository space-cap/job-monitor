# 09. Slack Notification

## 1. 목적

Rule에 일치한 신규 채용공고를 Slack으로 전달한다.

## 2. 발송 방식

### Incoming Webhook (MVP)

MVP에서는 **Slack Incoming Webhook**을 사용한다.

- 설정이 단순하고 별도 OAuth 없이 즉시 사용 가능하다.
- Webhook URL 하나로 특정 채널에 메시지를 보낼 수 있다.
- Webhook URL은 환경변수 `SLACK_WEBHOOK_URL`로 관리한다.

### Slack API (향후)

사용자별 채널, DM 발송, 메시지 업데이트가 필요해질 경우 Slack Web API (`chat.postMessage`)로 전환한다.
Bot Token은 환경변수 `SLACK_BOT_TOKEN`으로 관리한다.

## 3. 메시지 포맷

### MVP: 텍스트 포맷

```text
[채용공고]
회사: 현대자동차
제목: 빌딩 경비원
근무지: 서울 강남구
급여: 월 2,700,000원
마감일: 2026-08-20

원문 보기: <URL>
```

### 향후: Slack Block Kit

더 풍부한 메시지 레이아웃이 필요한 경우 Block Kit을 사용한다.

```json
{
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "📋 새로운 채용공고" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*회사*\n현대자동차" },
        { "type": "mrkdwn", "text": "*근무지*\n서울 강남구" },
        { "type": "mrkdwn", "text": "*급여*\n월 2,700,000원" },
        { "type": "mrkdwn", "text": "*마감일*\n2026-08-20" }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "원문 보기" },
          "url": "<URL>"
        }
      ]
    }
  ]
}
```

## 4. 발송 흐름

```text
Rule Engine
    |
    v
중복 확인 (notification_logs 조회)
    |
    +-- 이미 발송됨 --> 종료
    |
    `-- 미발송 --> Slack HTTP POST
                        |
              +---------+---------+
              |                   |
           성공 (2xx)          실패 (4xx/5xx)
              |                   |
    notification_logs          notification_logs
    status=SUCCESS             status=FAILED
                                   |
                                재처리 대상으로 기록
```

## 5. 처리 원칙

- Slack 인증정보는 환경변수로 관리한다. 코드나 문서에 저장하지 않는다.
- 발송 성공/실패를 `notification_logs`에 저장한다.
- 동일 Rule + 동일 Job + 동일 Channel 조합은 중복 발송하지 않는다.
- HTTP 오류(5xx) 또는 rate limit(429) 발생 시 재처리 가능하도록 상태를 보존한다.

## 6. 실패 처리

| 상황 | 대응 |
|------|------|
| 4xx (잘못된 요청) | 재처리 불가 — FAILED로 기록, 로그 남김 |
| 5xx (서버 오류) | 재처리 가능 — FAILED로 기록, 이후 재발송 시도 |
| 429 (rate limit) | `Retry-After` 헤더 확인 후 대기, 재시도 |
| Webhook URL 만료 | 환경변수 재설정 필요 — FAILED로 기록, 알람 |
| 네트워크 타임아웃 | 재처리 가능 — FAILED로 기록 |

재처리 로직은 Core의 Scheduler가 주기적으로 `notification_logs.status = 'FAILED'`인 건을 조회하여 재발송한다.
재시도는 최대 3회로 제한하고 이후에는 `PERMANENT_FAILED`로 전환한다.

## 7. 환경변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `SLACK_WEBHOOK_URL` | Incoming Webhook URL | `https://hooks.slack.com/services/...` |
| `SLACK_CHANNEL` | 기본 발송 채널 (선택) | `#job-alerts` |
| `SLACK_TIMEOUT_SECONDS` | HTTP 요청 타임아웃 (기본 5) | `5` |

## 8. 향후 확장

현재는 Slack만 사용한다. 향후 이메일, Discord, Telegram 등 다른 채널을 추가할 수 있도록 Notification Service 인터페이스를 분리한다.

```java
// 향후 인터페이스 예시
public interface NotificationChannel {
    NotificationResult send(NotificationMessage message);
    String channelType();
}
```

각 채널은 독립적으로 구현하고, `notification_logs`의 `channel` 컬럼으로 구분한다.
