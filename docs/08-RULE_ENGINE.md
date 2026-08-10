# 08. Rule Engine

## 1. 목적

수집된 모든 공고 중 사용자가 원하는 공고만 선별한다.

예:

- 제목/본문에 `경비`
- 근무지가 `강남`
- 급여가 일정 금액 이상
- 특정 고용형태

## 2. 초기 Rule

MVP에서는 복잡한 DSL보다 DB 컬럼 기반의 단순 조건부터 구현한다.

```text
keyword = 경비
location = 강남
salary_min = 2,500,000
```

## 3. 처리 흐름

```text
신규 Job
   |
   v
활성 Rule 조회
   |
   v
조건 평가
   |
   +-- 불일치 -> 종료
   |
   `-- 일치 -> Notification Queue/Service
                         |
                         v
                       Slack
```

## 4. 중복 알림

`notification_logs`에 동일 Rule + Job + Channel 기록이 있으면 다시 발송하지 않는다.

## 5. 향후 확장

- AND / OR 조건
- 제외 키워드
- 급여/근무시간 비교
- 지역 복수 선택
- 사용자별 Rule
- 우선순위/점수화
