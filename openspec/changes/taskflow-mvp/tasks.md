## 1. 프로젝트 초기 설정

- [x] 1.1 디렉토리 구조 생성 (backend/, frontend/, backend/routers/)
- [x] 1.2 backend/requirements.txt 작성 (fastapi, uvicorn, sqlalchemy, bcrypt, python-jose, psycopg[binary], python-dotenv)
- [x] 1.3 backend/database.py 작성 — DATABASE_URL 환경변수로 SQLite/PostgreSQL 전환
- [x] 1.4 backend/models.py 작성 — users, teams, tasks, messages 4테이블 SQLAlchemy 모델
- [x] 1.5 backend/main.py 작성 — FastAPI 앱, 라우터 등록, frontend/ StaticFiles 서빙
- [x] 1.6 .env.example 작성 (DATABASE_URL, JWT_SECRET)
- [x] 1.7 로컬 서버 실행 확인 (uvicorn backend.main:app --reload)

## 2. 인증 API (Auth 4개)

- [x] 2.1 backend/auth.py — JWT 발급(create_token), 검증(get_current_user) 유틸리티
- [x] 2.2 POST /auth/signup — 이메일 중복 체크, bcrypt 해시, 201+JWT 반환
- [x] 2.3 POST /auth/login — bcrypt 검증, 200+JWT+user(team_id 포함) 반환
- [x] 2.4 POST /auth/logout — 200 {} 반환 (stateless)
- [x] 2.5 GET /auth/me — JWT 검증, 현재 사용자 정보 반환
- [x] 2.6 에러 응답 표준 미들웨어/핸들러 — { error: { code, message } } 형태 통일

## 3. 팀 API (Team 5개)

- [x] 3.1 팀 멤버십 검증 의존성 — get_team_member(user, team_id) → 403 if not member
- [x] 3.2 POST /teams — 팀 생성, invite_code 자동 생성(XXXX-9999 형식), users.team_id 업데이트
- [x] 3.3 POST /teams/join — 초대코드 형식 검증, 존재 확인, users.team_id 업데이트
- [x] 3.4 GET /teams/{id} — 팀 정보 + member_count 반환 (멤버만 접근)
- [x] 3.5 GET /teams/{id}/members — 멤버 목록, owner/member 역할 구분
- [x] 3.6 DELETE /teams/{id}/leave — 멤버 탈퇴, owner 탈퇴 방지

## 4. 칸반 API (Task 6개)

- [x] 4.1 GET /teams/{id}/tasks — filter 파라미터(me/unassigned), created_at DESC 정렬
- [x] 4.2 POST /teams/{id}/tasks — 태스크 생성, status=TODO 고정, creator_id=현재사용자
- [x] 4.3 GET /tasks/{id} — 단일 태스크 상세 (assignee 이메일 포함)
- [x] 4.4 PUT /tasks/{id} — 제목·assignee_id 수정
- [x] 4.5 PATCH /tasks/{id}/status — 상태 변경 (TODO/DOING/DONE 검증)
- [x] 4.6 DELETE /tasks/{id} — creator 또는 team owner만 삭제

## 5. 채팅 API (Chat 3개)

- [x] 5.1 GET /teams/{id}/messages — since= 파라미터 지원, 없으면 최근 50개, ASC 정렬
- [x] 5.2 POST /teams/{id}/messages — 1000자 검증, user_email 포함 응답
- [x] 5.3 DELETE /messages/{id} — 본인만 삭제, owner도 타인 메시지 삭제 불가

## 6. 프론트엔드 — 공통

- [x] 6.1 frontend/js/api.js — fetch 래퍼, Authorization 헤더 자동 첨부, 401 인터셉터(localStorage 삭제 + /login redirect)
- [x] 6.2 Tailwind CSS CDN 설정 (모든 HTML 파일 공통 head)
- [x] 6.3 반응형 breakpoint 설정 (md:768px 모바일/데스크탑 분기)

## 7. 프론트엔드 — 인증 화면

- [x] 7.1 frontend/index.html — 로그인/회원가입 탭 전환, 입력 validation, 처리중 버튼 비활성화
- [x] 7.2 로그인 성공 후 분기 — team_id null → team.html, 있으면 kanban.html
- [x] 7.3 회원가입/로그인 에러 인라인 표시 (이메일 중복, 자격증명 오류)

## 8. 프론트엔드 — 팀 선택 화면

- [x] 8.1 frontend/team.html — 팀 만들기 + 초대코드 합류 양쪽 폼
- [x] 8.2 팀 생성 성공 시 초대코드 표시 + 복사 버튼
- [x] 8.3 초대코드 입력 validation (정규식 ^[A-Z]{4}-[0-9]{4}$)
- [x] 8.4 team_id null 아닌 사용자 접근 시 kanban.html로 redirect

## 9. 프론트엔드 — 칸반 화면

- [x] 9.1 frontend/kanban.html — 3컬럼 레이아웃(TODO/DOING/DONE), 헤더 네비게이션
- [x] 9.2 태스크 카드 렌더링 — 제목, #id, @assignee 표시, 빈 컬럼 empty state
- [x] 9.3 + 버튼 → 인라인 입력 폼 (Enter 저장, Esc 취소, 담당자 드롭다운)
- [x] 9.4 HTML5 drag API 구현 — draggable, ondragover, ondrop, PATCH 호출, 낙관적 업데이트
- [x] 9.5 카드 클릭 → 상세 모달 (제목수정, 상태변경, 담당자변경, 삭제)
- [x] 9.6 삭제 확인 다이얼로그, 권한 없는 사용자는 삭제 버튼 숨김
- [x] 9.7 필터 버튼 (전체/@me/미할당) 구현
- [x] 9.8 모바일 반응형 — 1컬럼 탭 전환(스와이프 대신 탭 클릭), 카드 길게 누르기 상태 변경 메뉴

## 10. 프론트엔드 — 채팅 화면

- [x] 10.1 frontend/chat.html — 말풍선 레이아웃, 발신자/시각 표시, 1000자 카운터
- [x] 10.2 5초 폴링 setInterval + since= 증분 로직 구현
- [x] 10.3 네트워크 실패 시 exponential backoff (5→10→20→40→60s) + 상태 표시
- [x] 10.4 메시지 전송 후 자동 스크롤 하단 고정
- [x] 10.5 본인 메시지 호버 시 삭제 아이콘 표시, 타인 메시지는 아이콘 없음
- [x] 10.6 빈 채팅 empty state (메시지 0건일 때)
- [x] 10.7 모바일 반응형 — 풀스크린, 키보드 올라올 때 영역 축소(visualViewport)

## 11. 배포 설정

- [x] 11.1 backend/vercel.json 작성 — @vercel/python, API 라우트 설정
- [x] 11.2 루트 vercel.json 또는 프로젝트 설정 — 프론트 정적 파일 서빙
- [x] 11.3 GitHub 레포 생성, .gitignore 설정 (.env, taskflow.db, __pycache__)
- [ ] 11.4 Vercel 프로젝트 연결, DATABASE_URL + JWT_SECRET 환경변수 설정
- [ ] 11.5 git push origin main → Vercel 자동 배포 확인
- [ ] 11.6 Neon 연결 확인 — 회원가입/로그인/칸반/채팅 전체 정상 동작 검증
