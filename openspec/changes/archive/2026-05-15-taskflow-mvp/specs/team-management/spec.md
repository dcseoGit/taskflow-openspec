## ADDED Requirements

### Requirement: 팀 생성
인증된 사용자는 팀을 생성할 수 있으며, 생성자가 자동으로 owner가 된다.
- 팀 이름은 1~30자
- 초대코드는 서버가 자동 생성 (`^[A-Z]{4}-[0-9]{4}$` 형식, 예: FRNT-2026)
- 생성 후 users.team_id가 해당 팀 id로 업데이트됨

#### Scenario: 정상 팀 생성
- **WHEN** 인증된 사용자가 POST /teams { name: "Frontiers" } 요청
- **THEN** HTTP 201, { id, name, invite_code: "FRNT-2026", owner_id, created_at }

#### Scenario: 팀 이름 30자 초과
- **WHEN** 31자 이상 팀 이름으로 요청
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "팀 이름은 30자 이내여야 합니다" } }

### Requirement: 초대코드로 팀 합류
미가입 사용자는 초대코드를 입력해 팀에 합류할 수 있다.
- 초대코드 형식 검증: `^[A-Z]{4}-[0-9]{4}$`
- 합류 성공 시 users.team_id 업데이트
- 이미 다른 팀 소속이면 409 반환

#### Scenario: 정상 합류
- **WHEN** team_id=null인 사용자가 POST /teams/join { invite_code: "FRNT-2026" }
- **THEN** HTTP 200, { team: { id, name, member_count }, redirect: "/teams/7" }

#### Scenario: 초대코드 형식 오류
- **WHEN** "abcd1234" 같은 소문자 또는 하이픈 없는 코드로 요청
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "형식이 올바르지 않습니다" } }

#### Scenario: 존재하지 않는 초대코드
- **WHEN** 형식은 올바르지만 DB에 없는 코드로 요청
- **THEN** HTTP 404, { error: { code: "NOT_FOUND", message: "해당 초대코드를 찾을 수 없습니다" } }

#### Scenario: 이미 다른 팀 소속
- **WHEN** team_id가 이미 있는 사용자가 합류 요청
- **THEN** HTTP 409, { error: { code: "ALREADY_IN_TEAM", message: "이미 다른 팀에 소속되어 있습니다" } }

### Requirement: 팀 정보 조회
팀 멤버는 팀 기본 정보를 조회할 수 있어야 한다.

#### Scenario: 정상 조회
- **WHEN** 팀 멤버가 GET /teams/{id} 요청
- **THEN** HTTP 200, { id, name, invite_code, owner_id, member_count, created_at }

#### Scenario: 비멤버 접근
- **WHEN** 다른 팀 소속 사용자가 GET /teams/{id} 요청
- **THEN** HTTP 403, { error: { code: "FORBIDDEN", message: "권한이 없습니다" } }

### Requirement: 팀 멤버 목록 조회
팀 멤버는 같은 팀 멤버 목록을 조회할 수 있어야 한다.
- owner는 별도 표시 (owner_id 기준)
- 합류 시각(joined_at) 포함

#### Scenario: 정상 조회
- **WHEN** 팀 멤버가 GET /teams/{id}/members 요청
- **THEN** HTTP 200, [{ id, email, role: "owner"|"member", joined_at }]

#### Scenario: 비멤버 접근
- **WHEN** 비멤버가 GET /teams/{id}/members 요청
- **THEN** HTTP 403, { error: { code: "FORBIDDEN", message: "권한이 없습니다" } }

### Requirement: 팀 탈퇴
팀 멤버는 팀을 탈퇴할 수 있어야 한다.
- 탈퇴 후 users.team_id를 null로 업데이트
- owner는 탈퇴 불가 (팀 해산 기능 없음, MVP 범위 외)
- UI 진입점 없음 — API만 구현

#### Scenario: 일반 멤버 탈퇴
- **WHEN** member 역할 사용자가 DELETE /teams/{id}/leave 요청
- **THEN** HTTP 200, {}, users.team_id = null로 업데이트

#### Scenario: owner 탈퇴 시도
- **WHEN** owner가 DELETE /teams/{id}/leave 요청
- **THEN** HTTP 403, { error: { code: "OWNER_CANNOT_LEAVE", message: "팀 소유자는 탈퇴할 수 없습니다" } }
