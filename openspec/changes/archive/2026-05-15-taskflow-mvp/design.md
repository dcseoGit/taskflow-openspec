## Context

신규 프로젝트. 기존 코드베이스 없음. FastAPI(Python) 백엔드 + Vanilla JS 프론트엔드를 단일 레포지토리로 구성하여 로컬은 SQLite, 운영은 Vercel+Neon PostgreSQL로 배포한다.

## Goals / Non-Goals

**Goals:**
- API 18개 완전 구현 (Auth 4 + Team 5 + Task 6 + Chat 3)
- 로컬 `uvicorn` 단일 명령 실행 가능
- `git push origin main` → Vercel 자동 배포
- DATABASE_URL 환경변수 하나로 로컬/운영 DB 전환

**Non-Goals:**
- WebSocket 실시간 통신
- JWT 갱신 토큰
- 자동화 테스트
- 다국어, 파일 업로드, 알림

## Decisions

### D1. 프로젝트 구조 — 단일 레포, FE는 정적 파일 서빙

```
taskflow/
  backend/
    main.py          # FastAPI 앱 진입점
    models.py        # SQLAlchemy 모델
    routers/         # auth.py, teams.py, tasks.py, chat.py
    auth.py          # JWT 유틸리티
    database.py      # DB 연결 (DATABASE_URL)
    requirements.txt
    vercel.json      # Vercel Functions 설정
  frontend/
    index.html       # 로그인/회원가입
    team.html        # 팀 선택
    kanban.html      # 칸반
    chat.html        # 채팅
    js/
      api.js         # fetch 래퍼, JWT 헤더 자동 첨부, 401 인터셉터
      kanban.js
      chat.js
    css/
      tailwind.css   # CDN import (빌드 도구 불필요)
```

**Why**: 프레임워크 없이 HTML 파일 단위로 화면을 분리하면 라우팅 없이 `location.href`로 화면 전환 가능. Day 2 범위 내 가장 단순한 구조.

### D2. DB ORM — SQLAlchemy Core (Async 불필요)

FastAPI async endpoint지만 SQLAlchemy sync session 사용. Neon은 psycopg2 드라이버, 로컬은 sqlite3.

**Why**: async SQLAlchemy는 Vercel Serverless 환경에서 connection pool 관리가 복잡. Neon의 connection pooling (Pooled connection string)으로 Serverless cold-start 대응.

### D3. 인증 — JWT HS256, python-jose

```python
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
EXPIRE_HOURS = 24
```

모든 보호 라우트는 `Depends(get_current_user)` FastAPI dependency로 JWT 검증. 비멤버 접근은 `user.team_id != team_id` 체크로 403 반환.

### D4. 칸반 드래그 — HTML5 native drag API

`draggable="true"` + `ondragstart/ondragover/ondrop` 이벤트. drop 시 `PATCH /tasks/{id}/status` 호출. 낙관적 업데이트(카드 즉시 이동) 후 API 실패 시 원위치 복구.

### D5. 채팅 폴링 — setInterval + since= ISO timestamp

```javascript
let lastSince = null;
setInterval(async () => {
  const url = lastSince
    ? `/teams/${teamId}/messages?since=${lastSince}`
    : `/teams/${teamId}/messages`;
  const msgs = await api.get(url);
  if (msgs.length) {
    appendMessages(msgs);
    lastSince = msgs.at(-1).created_at;
  }
}, 5000);
```

실패 시 exponential backoff (5s→10s→20s→40s→60s 고정).

### D6. Vercel 배포 — FastAPI as Serverless Function

```json
// backend/vercel.json
{
  "builds": [{ "src": "main.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/(.*)", "dest": "main.py" }]
}
```

프론트엔드는 `frontend/` 디렉토리에서 별도 Vercel 프로젝트로 배포하거나, FastAPI의 `StaticFiles`로 같이 서빙.

## Risks / Trade-offs

- **FastAPI Vercel cold start** → Neon Pooled connection string 사용, 첫 요청 지연 감수 (MVP 범위)
- **SQLite→PostgreSQL 방언 차이** → SQLAlchemy ORM 사용 시 대부분 호환. `AUTOINCREMENT` vs `SERIAL` 차이는 SQLAlchemy가 추상화
- **JWT localStorage XSS** → MVP 전제 (httpOnly cookie는 Day 2 범위 외로 명시됨)
- **5초 폴링 부하** → 팀당 5명 이하, 동시 50명 가정이므로 Neon Free tier 충분
- **HTML5 Drag 모바일 미지원** → 모바일은 길게 누르기 → 상태 변경 메뉴로 대체

## Migration Plan

1. `git init` + GitHub 레포 생성
2. `pip install -r requirements.txt`, `uvicorn` 로컬 실행 확인
3. Vercel 프로젝트 연결, `NEON_DATABASE_URL` + `JWT_SECRET` 환경변수 설정
4. `git push origin main` → 자동 배포 확인
