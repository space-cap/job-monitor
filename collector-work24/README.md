# collector-work24

Work24 채용정보를 수집하여 Job Monitor MariaDB에 저장하는 Python Collector.

## 현재 단계

현재는 **DB 연결 확인 단계**이다.

다음 단계에서 Work24 목록 1페이지(50건)를 수집하여 `jobs` 테이블에 저장한다.

## 실행 환경

- Python 3.11+
- MariaDB 12.x
- Work24

## 설치

Windows 기준:

```powershell
cd collector-work24
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 환경변수

`.env.example`을 복사하여 `.env`를 만들고 실제 DB 접속정보를 입력한다.

```text
DB_HOST=100.72.191.19
DB_PORT=3306
DB_NAME=job_monitor
DB_USER=...
DB_PASSWORD=...
```

`.env`는 `.gitignore`에 포함되어 있으므로 GitHub에 올리지 않는다.

## DB 연결 테스트

```powershell
python -m app.main
```

성공하면 다음과 비슷하게 출력된다.

```text
MariaDB connection OK: database=job_monitor, version=...
```

## 개발 원칙

1. Collector는 Work24에서 수집한다.
2. 수집한 데이터는 MariaDB에 직접 저장한다.
3. DB 비밀번호와 토큰은 코드에 하드코딩하지 않는다.
4. 최초 구현은 1페이지 50건 수집만 대상으로 한다.
5. 수집 성공 후 여러 페이지, 상세 페이지, 중복 처리, 수집 이력 순서로 확장한다.
