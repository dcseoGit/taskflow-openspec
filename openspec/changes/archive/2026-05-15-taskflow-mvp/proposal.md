## Why

소규모 팀이 업무 진행 상황을 한 화면에서 추적할 수 있는 MVP가 없다. 칸반과 실시간 채팅을 결합한 협업 도구를 Day 2 안에 완성하여 Vercel에 배포 가능한 상태로 만든다.

## What Changes

- 이메일/비밀번호 기반 회원가입·로그인, JWT(24h) 인증 체계 신규 구축
- 팀 생성·초대코드 발급·합류·멤버 목록·탈퇴 기능 신규 구축
- TODO/DOING/DONE 3컬럼 칸반 보드 (태스크 생성·드래그 상태 이동·삭제) 신규 구축
- 팀 단위 채팅 (5초 폴링, 1000자 제한, 발신자·시각 표시) 신규 구축
- 로컬 FastAPI+SQLite, 운영 Vercel+Neon 환경 분리 배포 파이프라인 신규 구축

## Capabilities

### New Capabilities

- `user-auth`: 회원가입(POST /auth/signup), 로그인(POST /auth/login), 로그아웃(POST /auth/logout), 내 정보(GET /auth/me). JWT 24h 발급·검증, bcrypt 비밀번호 해시, stateless 로그아웃
- `team-management`: 팀 생성(POST /teams), 초대코드 합류(POST /teams/join), 팀 정보(GET /teams/{id}), 멤버 목록(GET /teams/{id}/members), 팀 탈퇴(DELETE /teams/{id}/leave). 1인 1팀 정책, 초대코드 형식 `^[A-Z]{4}-[0-9]{4}$`
- `kanban-board`: 태스크 목록(GET /teams/{id}/tasks), 생성(POST /teams/{id}/tasks), 상세(GET /tasks/{id}), 제목·담당자 수정(PUT /tasks/{id}), 상태 변경(PATCH /tasks/{id}/status), 삭제(DELETE /tasks/{id}). assignee_id nullable, creator/owner DELETE 권한
- `team-chat`: 메시지 목록(GET /teams/{id}/messages?since=), 전송(POST /teams/{id}/messages), 삭제(DELETE /messages/{id}). 5초 폴링, 1000자 제한, 본인만 삭제
- `deployment`: 로컬 FastAPI+SQLite / 운영 Vercel Serverless Functions+Neon PostgreSQL 환경 분리. DATABASE_URL 환경변수로 전환

### Modified Capabilities

## Impact

- **신규 파일 전체**: 백엔드(FastAPI), 프론트엔드(Vanilla JS + Tailwind CSS) 코드베이스 신규 생성
- **DB**: users, teams, tasks, messages 4테이블 (SQLite 로컬 / Neon 운영)
- **API**: 18개 엔드포인트 (Auth 4 + Team 5 + Task 6 + Chat 3)
- **외부 의존성**: Python FastAPI, SQLAlchemy, bcrypt, python-jose, Neon(PostgreSQL), Vercel

## Out of Scope

- 알림 (이메일/SMS/푸시) — 채팅 폴링으로 대체
- 파일 첨부 — 텍스트 채팅만
- 전문 검색 — 단순 SELECT만
- 권한 세분화 (페이지별) — admin/member 구분만
- 다국어 — 한글 UI만
- WebSocket — 5초 폴링으로 대체
- 테스트 자동화 — 수동 동작 확인만
- JWT 갱신 토큰 — 24h 후 재로그인
- 팀 탈퇴 UI 진입점 — API만 구현
