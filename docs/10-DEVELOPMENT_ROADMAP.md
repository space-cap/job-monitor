# 10. Development Roadmap

## Phase 0 — 문서/설계

- [x] GitHub 저장소 생성
- [x] 프로젝트 비전 정의
- [x] 요구사항 정의
- [x] 아키텍처 정의
- [x] Work24 분석 계획
- [x] Collector / Rule / Slack 설계

## Phase 1 — Work24 Collector MVP

- [ ] Python 프로젝트 생성
- [ ] Work24 목록 요청
- [ ] 첫 페이지 50건 파싱
- [ ] 두 번째 페이지 파싱
- [ ] 페이지네이션 일반화
- [ ] 상세 페이지 파싱
- [ ] MariaDB 연결
- [ ] jobs UPSERT
- [ ] collection_runs 기록
- [ ] 수집 테스트

## Phase 2 — Spring Boot Core

- [ ] Maven 프로젝트 생성
- [ ] Java 21 / Spring Boot 4.0.7
- [ ] MyBatis Mapper
- [ ] 공고 목록 조회
- [ ] 공고 상세 조회
- [ ] Thymeleaf Dashboard
- [ ] Collector 상태 조회

## Phase 3 — Rule Engine

- [ ] Rule CRUD
- [ ] 키워드 매칭
- [ ] 지역 조건
- [ ] 급여 조건
- [ ] 활성/비활성
- [ ] 알림 중복 방지

## Phase 4 — Slack

- [ ] Slack 설정
- [ ] 메시지 템플릿
- [ ] 발송
- [ ] 발송 로그
- [ ] 실패 재처리

## Phase 5 — 운영 안정화

- [ ] 스케줄 실행
- [ ] 로그/모니터링
- [ ] 백업
- [ ] 장애 복구
- [ ] 테스트 자동화

## Phase 6 — 다중 사용자

MVP가 실제로 유용하다고 검증된 이후 진행한다.

- [ ] 사용자 모델
- [ ] 사용자별 Rule
- [ ] 사용자별 Slack 설정
- [ ] 인증/권한
