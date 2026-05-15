# Dark / Light Mode 토글 설계

## 결정 사항

- **토글 위치**: 헤더 우측 (네비게이션 옆), 4개 화면 공통
- **다크 팔레트**: 웜 다크 (Warm Dark) — stone/brown 계열 (`#1c1917` 베이스)
- **토글 아이콘**: ☀ (라이트) / 🌙 (다크)
- **상태 저장**: `localStorage('theme')` — 페이지 로드 시 깜빡임 없이 즉시 적용

## 색상 팔레트

| 토큰 | 라이트 | 다크 (Warm) |
|------|--------|-------------|
| bg-primary | `gray-50` (#f8fafc) | `stone-900` (#1c1917) |
| bg-card | `white` | `stone-800` (#292524) |
| border | `gray-200` | `stone-700` (#44403c) |
| text-primary | `gray-800` | `stone-100` (#f5f5f4) |
| text-muted | `gray-400` | `stone-400` (#a8a29e) |
| header-bg | `teal-600` | `stone-800` (border 강조) |
| TODO col | `yellow-50` | `stone-800` (border yellow) |
| DOING col | `blue-50` | `stone-800` (border blue) |
| DONE col | `green-50` | `stone-800` (border green) |

## 구현 방식

**Tailwind CDN `darkMode: 'class'` 전략**

```html
<script>tailwind.config = { darkMode: 'class' }</script>
<script src="https://cdn.tailwindcss.com"></script>
```

- `<html>` 요소에 `dark` 클래스 토글
- 모든 요소에 `dark:` 접두어 클래스 추가
- `localStorage.getItem('theme')` → 페이지 `<head>`에서 즉시 적용 (FOUC 방지)

## 공통 모듈 (`theme.js`)

```js
function initTheme() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.classList.toggle('dark', saved === 'dark');
}
function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateToggleBtn();
}
function updateToggleBtn() {
  const isDark = document.documentElement.classList.contains('dark');
  const btn = document.getElementById('theme-toggle');
  if (btn) btn.textContent = isDark ? '🌙' : '☀';
}
```

## 적용 범위

- `frontend/js/theme.js` — 공통 테마 유틸리티 신규 생성
- `frontend/index.html` — 로그인/회원가입 화면
- `frontend/team.html` — 팀 선택 화면
- `frontend/kanban.html` — 칸반 보드
- `frontend/chat.html` — 채팅 화면

## 비기능 요구사항

- 페이지 전환 시 테마 유지 (localStorage 공유)
- FOUC(깜빡임) 없음 — `<head>` 최상단에서 즉시 적용
- 모바일 동일 적용
