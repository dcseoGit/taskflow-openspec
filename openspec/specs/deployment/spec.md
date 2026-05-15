# deployment Spec

## Purpose

로컬 개발 환경 실행, 환경변수 기반 DB 전환, Vercel 자동 배포, 표준 에러 응답 형식을 정의한다.

## Requirements

### Requirement: 로컬 개발 환경 단일 명령 실행
개발자는 단일 명령으로 로컬 서버를 실행할 수 있어야 한다.
- 백엔드: `uvicorn backend.main:app --reload --port 8000`
- 프론트엔드: `backend/main.py`의 StaticFiles로 `frontend/` 서빙 (별도 서버 불필요)
- DB: `taskflow.db` SQLite 파일 자동 생성

#### Scenario: 로컬 서버 실행
- **WHEN** `uvicorn backend.main:app --reload` 실행 (DATABASE_URL 미설정)
- **THEN** SQLite `taskflow.db` 자동 생성, http://localhost:8000 에서 프론트+백엔드 동작

#### Scenario: DB 자동 초기화
- **WHEN** 서버 최초 실행 시 DB 파일 없음
- **THEN** SQLAlchemy `create_all()`로 4테이블 자동 생성

### Requirement: 환경변수로 DB 전환
DATABASE_URL 환경변수 하나로 로컬 SQLite와 운영 Neon PostgreSQL을 전환할 수 있어야 한다.

#### Scenario: 로컬 SQLite 사용
- **WHEN** DATABASE_URL 미설정 또는 `sqlite:///./taskflow.db`
- **THEN** SQLite 파일 DB 사용

#### Scenario: 운영 Neon 사용
- **WHEN** DATABASE_URL=`postgresql://...neon.tech/taskflow?sslmode=require`
- **THEN** Neon PostgreSQL 연결, SQLite 파일 미생성

### Requirement: Vercel 자동 배포
main 브랜치 push 시 Vercel이 자동으로 프론트엔드와 백엔드를 배포해야 한다.

#### Scenario: main push 자동 배포
- **WHEN** `git push origin main`
- **THEN** Vercel이 백엔드(Serverless Functions)와 프론트엔드(정적 파일) 자동 빌드 및 배포

#### Scenario: 운영 환경변수 설정
- **WHEN** Vercel 프로젝트에 `DATABASE_URL`, `JWT_SECRET` 환경변수 설정됨
- **THEN** 배포 후 API가 Neon PostgreSQL에 연결되어 정상 동작

### Requirement: 에러 응답 표준화
모든 4xx/5xx 응답은 동일한 구조를 가져야 한다.
- 형태: `{ "error": { "code": "<SCREAMING_SNAKE>", "message": "<한국어>" } }`
- code는 기계 판독용 (INVALID_CREDENTIALS, FORBIDDEN 등)
- message는 사용자에게 직접 표시 가능한 한국어

#### Scenario: 표준 에러 형태 확인
- **WHEN** 어떤 4xx/5xx 에러가 발생하든
- **THEN** 응답 body가 반드시 `{ "error": { "code": string, "message": string } }` 형태
