# Dark / Light Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 4개 HTML 파일 전체에 ☀/🌙 토글을 헤더 우측에 추가하고, 웜 다크(Warm Dark) 팔레트를 Tailwind `dark:` 클래스로 적용한다.

**Architecture:** Tailwind CDN `darkMode: 'class'` 전략 사용. `<html>` 요소에 `dark` 클래스 토글, `localStorage('theme')`에 저장. 공통 로직은 `frontend/js/theme.js`로 분리해 4개 파일이 공유한다.

**Tech Stack:** Tailwind CSS CDN (darkMode: class), Vanilla JS, localStorage

---

## 색상 매핑 (Warm Dark)

| 역할 | 라이트 클래스 | 추가할 다크 클래스 |
|------|--------------|-----------------|
| 페이지 배경 | `bg-gray-50` / `bg-gray-100` | `dark:bg-stone-900` |
| 카드/패널 | `bg-white` | `dark:bg-stone-800` |
| 헤더 배경 | `bg-white` (border-b) | `dark:bg-stone-900 dark:border-stone-700` |
| 입력 필드 | `border` | `dark:border-stone-700 dark:bg-stone-900 dark:text-stone-100 dark:placeholder-stone-500` |
| 기본 텍스트 | `text-gray-800` | `dark:text-stone-100` |
| 보조 텍스트 | `text-gray-500` / `text-gray-400` | `dark:text-stone-400` |
| 칸반 TODO 컬럼 | `bg-yellow-50` | `dark:bg-stone-800 dark:border dark:border-yellow-800/40` |
| 칸반 DOING 컬럼 | `bg-blue-50` | `dark:bg-stone-800 dark:border dark:border-blue-800/40` |
| 칸반 DONE 컬럼 | `bg-green-50` | `dark:bg-stone-800 dark:border dark:border-green-800/40` |
| 태스크 카드 | `bg-white border` | `dark:bg-stone-900 dark:border-stone-700` |
| 채팅 내 메시지 (타인) | `bg-white border` | `dark:bg-stone-800 dark:border-stone-700` |
| 채팅 입력 영역 | `bg-white border-t` | `dark:bg-stone-900 dark:border-stone-700` |
| 에러 배너 | `bg-red-50 border-red-200 text-red-600` | `dark:bg-red-900/30 dark:border-red-800 dark:text-red-400` |
| 모달 배경 | `bg-white` | `dark:bg-stone-800` |

---

### Task 1: theme.js 공통 유틸리티 생성

**Files:**
- Create: `frontend/js/theme.js`

- [ ] **Step 1: theme.js 작성**

```javascript
// frontend/js/theme.js
function initTheme() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.classList.toggle('dark', saved === 'dark');
  updateToggleBtn();
}

function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  updateToggleBtn();
}

function updateToggleBtn() {
  const btn = document.getElementById('theme-toggle');
  if (!btn) return;
  const isDark = document.documentElement.classList.contains('dark');
  btn.textContent = isDark ? '🌙' : '☀';
}
```

- [ ] **Step 2: 브라우저에서 동작 확인**

콘솔에서 `toggleTheme()` 호출 시 `<html>` 클래스가 `dark`로 토글되는지 확인.

- [ ] **Step 3: 커밋**

```bash
git add frontend/js/theme.js
git commit -m "feat: add theme.js for dark/light mode toggle"
```

---

### Task 2: index.html — 로그인/회원가입 화면 다크모드 적용

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: `<head>`에 Tailwind config + FOUC 방지 스크립트 추가**

기존 `<head>` 내 `<script src="https://cdn.tailwindcss.com">` 앞에 삽입:

```html
<script>tailwind.config = { darkMode: 'class' }</script>
```

`</title>` 바로 아래에 FOUC 방지 인라인 스크립트 추가:

```html
<script>
  (function(){var t=localStorage.getItem('theme');if(t==='dark')document.documentElement.classList.add('dark');})();
</script>
```

- [ ] **Step 2: theme.js 로드 추가**

`</body>` 직전에 추가:

```html
<script src="/js/theme.js"></script>
<script>initTheme();</script>
```

- [ ] **Step 3: body에 다크 배경 추가**

```html
<!-- 변경 전 -->
<body class="min-h-screen bg-gray-50 flex items-center justify-center px-4">

<!-- 변경 후 -->
<body class="min-h-screen bg-gray-50 dark:bg-stone-900 flex items-center justify-center px-4 transition-colors">
```

- [ ] **Step 4: 카드에 다크 스타일 + 토글 버튼 추가**

```html
<!-- 변경 전 -->
<div class="w-full max-w-sm bg-white rounded-2xl shadow-lg p-8">
  <div class="text-center mb-6">
    <span class="inline-block bg-teal-600 text-white font-bold text-xl px-4 py-2 rounded-lg">TaskFlow</span>
  </div>

<!-- 변경 후 -->
<div class="w-full max-w-sm bg-white dark:bg-stone-800 rounded-2xl shadow-lg p-8 relative">
  <button id="theme-toggle" onclick="toggleTheme()"
    class="absolute top-4 right-4 text-lg bg-gray-100 dark:bg-stone-700 rounded-full w-8 h-8 flex items-center justify-center hover:scale-110 transition-transform">
    ☀
  </button>
  <div class="text-center mb-6">
    <span class="inline-block bg-teal-600 text-white font-bold text-xl px-4 py-2 rounded-lg">TaskFlow</span>
  </div>
```

- [ ] **Step 5: 탭 버튼 다크 스타일**

```html
<!-- 변경 전 -->
<div class="flex border-b mb-6">
  <button id="tab-login" onclick="showTab('login')"
    class="flex-1 py-2 text-sm font-medium text-teal-600 border-b-2 border-teal-600">로그인</button>
  <button id="tab-signup" onclick="showTab('signup')"
    class="flex-1 py-2 text-sm font-medium text-gray-500">회원가입</button>
</div>

<!-- 변경 후 -->
<div class="flex border-b dark:border-stone-700 mb-6">
  <button id="tab-login" onclick="showTab('login')"
    class="flex-1 py-2 text-sm font-medium text-teal-600 border-b-2 border-teal-600">로그인</button>
  <button id="tab-signup" onclick="showTab('signup')"
    class="flex-1 py-2 text-sm font-medium text-gray-500 dark:text-stone-400">회원가입</button>
</div>
```

- [ ] **Step 6: 입력 필드 다크 스타일 (login + signup 공통 class)**

두 form의 모든 input에 적용:

```html
<!-- 변경 전 -->
class="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-teal-400"

<!-- 변경 후 -->
class="w-full border dark:border-stone-700 rounded-lg px-3 py-2 text-sm bg-white dark:bg-stone-900 text-gray-800 dark:text-stone-100 placeholder-gray-400 dark:placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-teal-400"
```

- [ ] **Step 7: 에러 div 다크 스타일 (login-error, signup-error)**

```html
<!-- 변경 전 -->
class="hidden bg-red-50 border border-red-200 text-red-600 text-sm rounded-lg px-3 py-2"

<!-- 변경 후 -->
class="hidden bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-sm rounded-lg px-3 py-2"
```

- [ ] **Step 8: showTab JS에서 다크 클래스 유지**

`showTab()` 함수의 탭 버튼 className 설정을 아래로 교체:

```javascript
function showTab(tab) {
  document.getElementById("form-login").classList.toggle("hidden", tab !== "login");
  document.getElementById("form-signup").classList.toggle("hidden", tab !== "signup");
  document.getElementById("tab-login").className =
    "flex-1 py-2 text-sm font-medium " + (tab === "login" ? "text-teal-600 border-b-2 border-teal-600" : "text-gray-500 dark:text-stone-400");
  document.getElementById("tab-signup").className =
    "flex-1 py-2 text-sm font-medium " + (tab === "signup" ? "text-teal-600 border-b-2 border-teal-600" : "text-gray-500 dark:text-stone-400");
}
```

- [ ] **Step 9: 회원가입 링크 텍스트 다크**

```html
<!-- 변경 전 -->
<p class="text-center text-xs text-gray-500">이미 계정이 있으신가요?

<!-- 변경 후 -->
<p class="text-center text-xs text-gray-500 dark:text-stone-400">이미 계정이 있으신가요?
```

- [ ] **Step 10: 브라우저 확인 후 커밋**

`http://localhost:8080` 에서 토글 클릭 시 배경·카드·입력 필드가 다크로 전환되는지 확인.

```bash
git add frontend/index.html
git commit -m "feat: dark mode for login/signup page"
```

---

### Task 3: team.html — 팀 선택 화면 다크모드 적용

**Files:**
- Modify: `frontend/team.html`

- [ ] **Step 1: `<head>` Tailwind config + FOUC 방지 + theme.js 로드**

`<script src="https://cdn.tailwindcss.com">` 앞에:
```html
<script>tailwind.config = { darkMode: 'class' }</script>
```

`</title>` 아래:
```html
<script>
  (function(){var t=localStorage.getItem('theme');if(t==='dark')document.documentElement.classList.add('dark');})();
</script>
```

`</body>` 직전:
```html
<script src="/js/theme.js"></script>
<script>initTheme();</script>
```

- [ ] **Step 2: body 다크 배경**

```html
<!-- 변경 전 -->
<body class="min-h-screen bg-gray-50">

<!-- 변경 후 -->
<body class="min-h-screen bg-gray-50 dark:bg-stone-900 transition-colors">
```

- [ ] **Step 3: 헤더에 토글 버튼 추가 + 다크 스타일**

```html
<!-- 변경 전 -->
<header class="bg-white border-b px-6 py-3 flex justify-between items-center">
  <span class="bg-teal-600 text-white font-bold px-3 py-1 rounded">TaskFlow</span>
  <div class="flex items-center gap-4">
    <span id="user-email" class="text-sm text-gray-500"></span>
    <button onclick="logout()" class="text-sm text-gray-500 hover:text-red-500">로그아웃</button>
  </div>
</header>

<!-- 변경 후 -->
<header class="bg-white dark:bg-stone-900 border-b dark:border-stone-700 px-6 py-3 flex justify-between items-center">
  <span class="bg-teal-600 text-white font-bold px-3 py-1 rounded">TaskFlow</span>
  <div class="flex items-center gap-4">
    <span id="user-email" class="text-sm text-gray-500 dark:text-stone-400"></span>
    <button id="theme-toggle" onclick="toggleTheme()"
      class="text-lg bg-gray-100 dark:bg-stone-700 rounded-full w-8 h-8 flex items-center justify-center hover:scale-110 transition-transform">☀</button>
    <button onclick="logout()" class="text-sm text-gray-500 dark:text-stone-400 hover:text-red-500">로그아웃</button>
  </div>
</header>
```

- [ ] **Step 4: 안내 배너 다크**

```html
<!-- 변경 전 -->
<div id="no-team-banner" class="bg-blue-50 border border-blue-200 text-blue-700 text-sm rounded-lg px-4 py-3 mb-6">

<!-- 변경 후 -->
<div id="no-team-banner" class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800/50 text-blue-700 dark:text-blue-300 text-sm rounded-lg px-4 py-3 mb-6">
```

- [ ] **Step 5: 두 카드 패널 다크**

```html
<!-- 변경 전 -->
<div class="bg-white rounded-xl shadow-sm border p-6">

<!-- 변경 후 -->
<div class="bg-white dark:bg-stone-800 rounded-xl shadow-sm border dark:border-stone-700 p-6">
```
(두 카드 패널 모두 동일하게 적용)

- [ ] **Step 6: 카드 제목 텍스트**

```html
<!-- 변경 전 -->
<h2 class="font-semibold text-gray-800 mb-4">

<!-- 변경 후 -->
<h2 class="font-semibold text-gray-800 dark:text-stone-100 mb-4">
```

- [ ] **Step 7: 입력 필드 다크 (team-name, invite-input)**

```html
class="w-full border dark:border-stone-700 rounded-lg px-3 py-2 text-sm bg-white dark:bg-stone-900 text-gray-800 dark:text-stone-100 placeholder-gray-400 dark:placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-teal-400"
```

- [ ] **Step 8: 초대코드 표시 박스 다크**

```html
<!-- 변경 전 -->
<div id="invite-display" class="hidden mt-4 bg-green-50 border border-green-200 rounded-lg p-4">
  <p class="text-sm text-green-700 font-medium mb-2">✓ 팀이 생성되었습니다!</p>
  <p class="text-xs text-gray-500 mb-1">초대코드 (멤버에게 공유)</p>

<!-- 변경 후 -->
<div id="invite-display" class="hidden mt-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800/50 rounded-lg p-4">
  <p class="text-sm text-green-700 dark:text-green-300 font-medium mb-2">✓ 팀이 생성되었습니다!</p>
  <p class="text-xs text-gray-500 dark:text-stone-400 mb-1">초대코드 (멤버에게 공유)</p>
```

- [ ] **Step 9: 에러 텍스트 다크**

```html
<!-- 변경 전 -->
class="hidden text-red-500 text-xs"

<!-- 변경 후 -->
class="hidden text-red-500 dark:text-red-400 text-xs"
```

- [ ] **Step 10: 커밋**

```bash
git add frontend/team.html
git commit -m "feat: dark mode for team selection page"
```

---

### Task 4: kanban.html — 칸반 보드 다크모드 적용

**Files:**
- Modify: `frontend/kanban.html`

- [ ] **Step 1: `<head>` Tailwind config + FOUC + theme.js**

`<script src="https://cdn.tailwindcss.com">` 앞:
```html
<script>tailwind.config = { darkMode: 'class' }</script>
```

`</title>` 아래:
```html
<script>
  (function(){var t=localStorage.getItem('theme');if(t==='dark')document.documentElement.classList.add('dark');})();
</script>
```

`</body>` 직전 스크립트들 위:
```html
<script src="/js/theme.js"></script>
```

기존 마지막 `<script>` 블록 안 `init();` 위에 `initTheme();` 추가.

- [ ] **Step 2: body 다크 배경**

```html
<!-- 변경 전 -->
<body class="min-h-screen bg-gray-100">

<!-- 변경 후 -->
<body class="min-h-screen bg-gray-100 dark:bg-stone-900 transition-colors">
```

- [ ] **Step 3: 헤더 다크 + 토글 버튼**

```html
<!-- 변경 전 -->
<header class="bg-white border-b px-4 py-3 flex items-center gap-4">
  ...
  <div class="flex items-center gap-2">
    <span id="user-email" class="text-xs text-gray-400 hidden md:inline"></span>
    <button onclick="logout()" class="text-xs text-gray-500 hover:text-red-500">로그아웃</button>
  </div>
</header>

<!-- 변경 후 -->
<header class="bg-white dark:bg-stone-900 border-b dark:border-stone-700 px-4 py-3 flex items-center gap-4">
  ...
  <div class="flex items-center gap-2">
    <span id="user-email" class="text-xs text-gray-400 dark:text-stone-500 hidden md:inline"></span>
    <button id="theme-toggle" onclick="toggleTheme()"
      class="text-lg bg-gray-100 dark:bg-stone-700 rounded-full w-7 h-7 flex items-center justify-center hover:scale-110 transition-transform">☀</button>
    <button onclick="logout()" class="text-xs text-gray-500 dark:text-stone-400 hover:text-red-500">로그아웃</button>
  </div>
</header>
```

- [ ] **Step 4: 모바일 탭바 다크**

```html
<!-- 변경 전 -->
<div class="md:hidden flex border-b bg-white px-2">

<!-- 변경 후 -->
<div class="md:hidden flex border-b dark:border-stone-700 bg-white dark:bg-stone-900 px-2">
```

- [ ] **Step 5: 필터 바 다크**

```html
<!-- 변경 전 -->
<div class="px-4 py-2 flex gap-2 items-center bg-white border-b">

<!-- 변경 후 -->
<div class="px-4 py-2 flex gap-2 items-center bg-white dark:bg-stone-900 border-b dark:border-stone-700">
```

필터 버튼도 JS에서 동적으로 className을 설정하므로, `setFilter()` 함수의 className 문자열에 dark 클래스 추가:

```javascript
function setFilter(f) {
  currentFilter = f;
  ["all","me","unassigned"].forEach(x => {
    document.getElementById(`filter-${x}`).className =
      `px-3 py-1 text-xs font-medium rounded-full ${x===f ? "bg-gray-800 dark:bg-stone-600 text-white" : "bg-gray-100 dark:bg-stone-800 text-gray-600 dark:text-stone-300"}`;
  });
  loadTasks();
}
```

- [ ] **Step 6: 칸반 컬럼 다크**

```html
<!-- TODO 컬럼 변경 전 -->
<div id="col-TODO" class="flex-1 bg-yellow-50 rounded-xl p-3">

<!-- 변경 후 -->
<div id="col-TODO" class="flex-1 bg-yellow-50 dark:bg-stone-800 dark:border dark:border-yellow-900/40 rounded-xl p-3">
```

```html
<!-- DOING 컬럼 변경 전 -->
<div id="col-DOING" class="flex-1 bg-blue-50 rounded-xl p-3 hidden md:block">

<!-- 변경 후 -->
<div id="col-DOING" class="flex-1 bg-blue-50 dark:bg-stone-800 dark:border dark:border-blue-900/40 rounded-xl p-3 hidden md:block">
```

```html
<!-- DONE 컬럼 변경 전 -->
<div id="col-DONE" class="flex-1 bg-green-50 rounded-xl p-3 hidden md:block">

<!-- 변경 후 -->
<div id="col-DONE" class="flex-1 bg-green-50 dark:bg-stone-800 dark:border dark:border-green-900/40 rounded-xl p-3 hidden md:block">
```

- [ ] **Step 7: 컬럼 제목 텍스트 다크**

```html
<!-- TODO 제목 변경 전 -->
<span class="font-semibold text-yellow-700 text-sm">TODO · ...
<!-- 변경 후 -->
<span class="font-semibold text-yellow-700 dark:text-yellow-400 text-sm">TODO · ...

<!-- DOING 제목 -->
<span class="font-semibold text-blue-700 dark:text-blue-400 text-sm">DOING · ...

<!-- DONE 제목 -->
<span class="font-semibold text-green-700 dark:text-green-400 text-sm">DONE · ...
```

- [ ] **Step 8: 인라인 추가 폼 입력 필드 다크 (3개 컬럼)**

```html
<!-- 변경 전 -->
class="w-full border rounded px-2 py-1.5 text-sm focus:outline-none focus:ring-1 focus:ring-teal-400"

<!-- 변경 후 -->
class="w-full border dark:border-stone-600 rounded px-2 py-1.5 text-sm bg-white dark:bg-stone-900 text-gray-800 dark:text-stone-100 placeholder-gray-400 dark:placeholder-stone-500 focus:outline-none focus:ring-1 focus:ring-teal-400"
```

담당자 드롭다운도 동일:
```html
class="flex-1 border dark:border-stone-600 rounded px-2 py-1 text-xs bg-white dark:bg-stone-900 text-gray-700 dark:text-stone-200"
```

- [ ] **Step 9: 태스크 카드 HTML (cardHTML 함수) 다크**

`cardHTML()` 함수 반환 HTML의 카드 div:

```javascript
function cardHTML(t) {
  const assignee = t.assignee ? (t.assignee.email === currentUser.email ? "@me" : "@" + t.assignee.email.split("@")[0]) : "⚠미할당";
  return `<div data-task-id="${t.id}" draggable="true"
    class="bg-white dark:bg-stone-900 rounded-lg shadow-sm border dark:border-stone-700 p-3 cursor-grab active:cursor-grabbing hover:shadow-md transition">
    <p class="text-sm font-medium text-gray-800 dark:text-stone-100 mb-1">${escHtml(t.title)}</p>
    <p class="text-xs text-gray-400 dark:text-stone-500">#${t.id} · <span class="${t.assignee ? 'text-teal-600' : 'text-orange-400'}">${assignee}</span></p>
  </div>`;
}
```

- [ ] **Step 10: 모달 다크**

```html
<!-- 모달 패널 변경 전 -->
<div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6" onclick="event.stopPropagation()">

<!-- 변경 후 -->
<div class="bg-white dark:bg-stone-800 rounded-2xl shadow-xl w-full max-w-md p-6" onclick="event.stopPropagation()">
```

모달 내 텍스트/입력:
```html
<!-- modal-id -->
<span id="modal-id" class="text-sm text-gray-400 dark:text-stone-500"></span>

<!-- modal-title input -->
<input id="modal-title" type="text" maxlength="100"
  class="w-full text-lg font-semibold border-b border-transparent dark:bg-stone-800 dark:text-stone-100 hover:border-gray-200 dark:hover:border-stone-600 focus:border-teal-400 focus:outline-none mb-4 pb-1" />

<!-- modal-assignee select -->
<select id="modal-assignee" class="w-full border dark:border-stone-600 rounded px-2 py-1.5 text-sm bg-white dark:bg-stone-900 text-gray-800 dark:text-stone-200 mb-4"></select>

<!-- creator / created 텍스트 -->
<div class="text-xs text-gray-400 dark:text-stone-500 mb-1">생성자: ...
<div class="text-xs text-gray-400 dark:text-stone-500 mb-4">생성 시각: ...
```

- [ ] **Step 11: 삭제 확인 모달 다크**

```html
<div class="bg-white dark:bg-stone-800 rounded-2xl shadow-xl w-full max-w-sm p-6 text-center">
  ...
  <h3 class="font-semibold dark:text-stone-100 mb-1">이 카드를 삭제하시겠습니까?</h3>
  <p id="confirm-title" class="text-xs text-gray-500 dark:text-stone-400 mb-5"></p>
```

- [ ] **Step 12: 멤버 패널 다크**

```html
<div class="bg-white dark:bg-stone-800 rounded-t-2xl md:rounded-2xl md:mr-6 w-full md:w-72 p-6 max-h-[70vh] overflow-y-auto">
  <div class="flex justify-between mb-4">
    <h3 class="font-semibold dark:text-stone-100">팀 멤버</h3>
```

- [ ] **Step 13: 커밋**

```bash
git add frontend/kanban.html
git commit -m "feat: dark mode for kanban board"
```

---

### Task 5: chat.html — 채팅 화면 다크모드 적용

**Files:**
- Modify: `frontend/chat.html`

- [ ] **Step 1: `<head>` Tailwind config + FOUC + theme.js**

`<script src="https://cdn.tailwindcss.com">` 앞:
```html
<script>tailwind.config = { darkMode: 'class' }</script>
```

`</title>` 아래:
```html
<script>
  (function(){var t=localStorage.getItem('theme');if(t==='dark')document.documentElement.classList.add('dark');})();
</script>
```

마지막 `<script>` 블록 안 `init();` 위에:
```html
<script src="/js/theme.js"></script>
```
`initTheme();` 호출 추가.

- [ ] **Step 2: body 다크 배경**

```html
<!-- 변경 전 -->
<body class="min-h-screen bg-gray-100 flex flex-col">

<!-- 변경 후 -->
<body class="min-h-screen bg-gray-100 dark:bg-stone-900 flex flex-col transition-colors">
```

- [ ] **Step 3: 헤더 다크 + 토글 버튼**

```html
<!-- 변경 전 -->
<header class="bg-white border-b px-4 py-3 flex items-center gap-4 shrink-0">
  ...
  <div class="flex items-center gap-2">
    <span id="poll-status" class="text-xs text-teal-500">● 5초마다 새로고침</span>
    <button onclick="logout()" class="text-xs text-gray-500 hover:text-red-500 ml-2">로그아웃</button>
  </div>

<!-- 변경 후 -->
<header class="bg-white dark:bg-stone-900 border-b dark:border-stone-700 px-4 py-3 flex items-center gap-4 shrink-0">
  ...
  <div class="flex items-center gap-2">
    <span id="poll-status" class="text-xs text-teal-500">● 5초마다 새로고침</span>
    <button id="theme-toggle" onclick="toggleTheme()"
      class="text-lg bg-gray-100 dark:bg-stone-700 rounded-full w-7 h-7 flex items-center justify-center hover:scale-110 transition-transform">☀</button>
    <button onclick="logout()" class="text-xs text-gray-500 dark:text-stone-400 hover:text-red-500 ml-2">로그아웃</button>
  </div>
```

- [ ] **Step 4: 헤더 팀 이름 다크**

```html
<span id="team-name" class="font-semibold text-gray-800 dark:text-stone-100 flex-1"></span>
```

- [ ] **Step 5: 메시지 영역 배경 다크**

```html
<!-- 변경 전 -->
<div id="messages-wrap" class="flex-1 overflow-y-auto px-4 py-3 space-y-3">

<!-- 변경 후 -->
<div id="messages-wrap" class="flex-1 overflow-y-auto px-4 py-3 space-y-3 dark:bg-stone-900">
```

- [ ] **Step 6: empty state 다크**

```html
<!-- 변경 전 -->
<p class="text-gray-500 font-medium">아직 대화가 없습니다</p>
<p class="text-gray-400 text-sm mt-1">첫 메시지를 보내 팀원과 대화를 시작하세요</p>

<!-- 변경 후 -->
<p class="text-gray-500 dark:text-stone-400 font-medium">아직 대화가 없습니다</p>
<p class="text-gray-400 dark:text-stone-500 text-sm mt-1">첫 메시지를 보내 팀원과 대화를 시작하세요</p>
```

- [ ] **Step 7: 타인 메시지 말풍선 다크 (msgHTML 함수)**

`msgHTML()` 함수에서 타인 메시지 부분:

```javascript
  return `<div class="flex justify-start mb-1" data-msg-id="${m.id}">
    <div>
      <div class="text-xs text-gray-400 dark:text-stone-500 mb-0.5">${escHtml(m.user_email.split("@")[0])} · ${time}</div>
      <div class="bg-white dark:bg-stone-800 border dark:border-stone-700 text-gray-800 dark:text-stone-100 text-sm rounded-2xl rounded-bl-sm px-3 py-2 max-w-xs shadow-sm">${escHtml(m.content)}</div>
    </div>
  </div>`;
```

본인 메시지 시간 텍스트:
```javascript
<div class="text-xs text-gray-400 dark:text-stone-500 text-right mb-0.5">나 · ${time}</div>
```

- [ ] **Step 8: 입력 영역 다크**

```html
<!-- 변경 전 -->
<div class="bg-white border-t px-4 py-3 shrink-0">

<!-- 변경 후 -->
<div class="bg-white dark:bg-stone-900 border-t dark:border-stone-700 px-4 py-3 shrink-0">
```

연결 끊김 배너:
```html
<!-- 변경 전 -->
<div id="disconnect-banner" class="hidden bg-red-50 border border-red-200 text-red-600 text-xs rounded-lg px-3 py-2 mb-2 flex items-center gap-2">

<!-- 변경 후 -->
<div id="disconnect-banner" class="hidden bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 text-xs rounded-lg px-3 py-2 mb-2 flex items-center gap-2">
```

textarea:
```html
<!-- 변경 전 -->
class="w-full border rounded-xl px-3 py-2 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-teal-400 overflow-hidden"

<!-- 변경 후 -->
class="w-full border dark:border-stone-700 rounded-xl px-3 py-2 text-sm resize-none bg-white dark:bg-stone-800 text-gray-800 dark:text-stone-100 placeholder-gray-400 dark:placeholder-stone-500 focus:outline-none focus:ring-2 focus:ring-teal-400 overflow-hidden"
```

- [ ] **Step 9: 커밋**

```bash
git add frontend/chat.html
git commit -m "feat: dark mode for chat page"
```

---

### Task 6: 최종 확인 및 배포

- [ ] **Step 1: 로컬 서버 기동 후 전체 확인**

```bash
uvicorn backend.main:app --reload --port 8080
```

체크리스트:
- [ ] index.html: 토글 클릭 → 배경/카드/입력 전환
- [ ] team.html: 헤더 토글 → 전체 전환, 카드 패널 다크
- [ ] kanban.html: 헤더 토글 → 3컬럼 배경, 카드, 모달 전환
- [ ] chat.html: 헤더 토글 → 말풍선, 입력창 전환
- [ ] 페이지 이동 시 테마 유지 (localStorage 공유)
- [ ] 새로고침 후 테마 유지 (FOUC 없음)

- [ ] **Step 2: .gitignore에 `.superpowers/` 추가**

```bash
echo ".superpowers/" >> .gitignore
git add .gitignore
```

- [ ] **Step 3: 전체 커밋 및 배포**

```bash
git add -A
git commit -m "feat: add dark/light mode toggle (warm dark palette)"
git push origin main
vercel deploy --prod --yes
```

- [ ] **Step 4: 프로덕션 URL에서 최종 확인**

`https://taskflow-openspec-eosin.vercel.app` 에서 동일하게 동작하는지 확인.
