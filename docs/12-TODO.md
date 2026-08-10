# 12. TODO

## 1단계 — DB 기반 준비

- [x] Work24 목록 화면의 주요 노출 필드 확인
- [x] MariaDB schema 작성
- [x] `jobs` / `collection_runs` / `rules` / `notification_logs` 기본 구조 정의
- [ ] MariaDB 서버에 `job_monitor` 데이터베이스 생성/적용
- [ ] 애플리케이션 전용 DB 사용자 생성
- [ ] 실제 DB 연결 테스트

## 2단계 — Work24 Collector

- [ ] Work24 HTML 구조를 실제 HTTP 응답으로 확인
- [ ] 목록 selector 확정
- [ ] 상세 selector 확정
- [ ] 공고 고유 ID 추출 방식 확인
- [ ] 페이지네이션 동작 확인
- [ ] Python 프로젝트 초기화
- [ ] 첫 페이지 50건 수집
- [ ] 첫 50건 DB 저장
- [ ] 중복 저장 방지 검증
- [ ] 2페이지 수집 및 페이지 이동 검증
- [ ] 수집 실행 이력(`collection_runs`) 저장

## 3단계 — Spring Boot Core

- [ ] Spring Boot 4.0.7 프로젝트 초기화
- [ ] MariaDB + MyBatis 연결
- [ ] Job 목록 조회
- [ ] Job 상세 조회
- [ ] Collector 실행 이력 조회

## 4단계 — Thymeleaf

- [ ] 채용공고 목록 화면
- [ ] 검색/필터 화면
- [ ] 채용공고 상세 화면
- [ ] Collector 상태 화면
- [ ] Dashboard

## 5단계 — Rule / Slack

- [ ] Rule CRUD
- [ ] 키워드 매칭
- [ ] 제외 키워드
- [ ] 지역 조건
- [ ] 급여 조건
- [ ] Slack 발송
- [ ] 알림 로그
- [ ] 중복 알림 방지

## 6단계 — 다중 사용자

- [ ] 사용자 관리
- [ ] 사용자별 Rule 분리
- [ ] 사용자별 Slack 설정
- [ ] 인증/권한

## 설계 원칙

현재 필요한 기능보다 앞서 과도한 범용화를 하지 않는다. 먼저 Work24 MVP를 실제로 동작시키고, 수집 데이터와 운영 경험을 바탕으로 필요한 추상화를 추가한다.
