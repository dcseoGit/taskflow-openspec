# user-auth Spec

## Purpose

사용자 인증 기능을 제공한다. 이메일+비밀번호 기반 회원가입/로그인을 처리하고, JWT 토큰으로 API 인증을 수행한다.

## Requirements

### Requirement: 회원가입
시스템은 이메일+비밀번호로 회원가입을 처리하고 즉시 JWT를 발급해야 한다.
- 이메일은 RFC 5322 형식이어야 하며 중복 불가
- 비밀번호는 8자 이상이어야 하며 bcrypt로 해시 저장
- 성공 시 HTTP 201과 JWT 토큰 반환

#### Scenario: 정상 회원가입
- **WHEN** POST /auth/signup { email: "user@example.com", password: "pass1234" } 요청
- **THEN** HTTP 201, { token: "<jwt>", user: { id, email, team_id: null } } 반환

#### Scenario: 이메일 중복
- **WHEN** 이미 존재하는 이메일로 POST /auth/signup 요청
- **THEN** HTTP 409, { error: { code: "EMAIL_TAKEN", message: "이미 가입된 이메일입니다" } }

#### Scenario: 이메일 형식 오류
- **WHEN** "user@invalid" 같은 잘못된 형식으로 요청
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "올바른 이메일 형식이 아닙니다" } }

#### Scenario: 비밀번호 8자 미만
- **WHEN** 7자 이하 비밀번호로 요청
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "비밀번호는 8자 이상이어야 합니다" } }

### Requirement: 로그인
시스템은 이메일+비밀번호 검증 후 JWT(24h)를 발급해야 한다.
- 이메일 존재 여부를 응답에서 노출하지 않는다 (보안)
- 성공 시 users.team_id를 함께 반환하여 클라이언트가 분기 처리

#### Scenario: 정상 로그인 (팀 미가입)
- **WHEN** 올바른 이메일+비밀번호로 POST /auth/login, 해당 사용자 team_id가 null
- **THEN** HTTP 200, { token: "<jwt>", user: { id, email, team_id: null } }

#### Scenario: 정상 로그인 (팀 가입됨)
- **WHEN** 올바른 이메일+비밀번호로 POST /auth/login, 해당 사용자 team_id가 7
- **THEN** HTTP 200, { token: "<jwt>", user: { id, email, team_id: 7 } }

#### Scenario: 잘못된 자격증명
- **WHEN** 존재하지 않는 이메일 또는 틀린 비밀번호로 요청
- **THEN** HTTP 401, { error: { code: "INVALID_CREDENTIALS", message: "이메일 또는 비밀번호가 일치하지 않습니다" } }

### Requirement: 로그아웃
시스템은 로그아웃 API를 제공하며 서버 측 상태를 변경하지 않는다.
- JWT 블랙리스트 없음. 클라이언트가 토큰을 삭제하는 것이 실질적 로그아웃
- 유효/만료 토큰 모두 HTTP 200 반환

#### Scenario: 정상 로그아웃
- **WHEN** POST /auth/logout (Authorization 헤더 있음)
- **THEN** HTTP 200, {} 반환

### Requirement: 내 정보 조회
인증된 사용자는 현재 자신의 정보를 조회할 수 있어야 한다.

#### Scenario: 정상 조회
- **WHEN** 유효한 JWT로 GET /auth/me 요청
- **THEN** HTTP 200, { id, email, team_id } 반환

#### Scenario: 토큰 없음/만료
- **WHEN** JWT 없이 또는 만료된 JWT로 GET /auth/me 요청
- **THEN** HTTP 401, { error: { code: "TOKEN_EXPIRED", message: "인증이 만료되었습니다" } }

### Requirement: JWT 만료 처리
모든 보호 엔드포인트는 만료된 JWT에 대해 401을 반환해야 한다.

#### Scenario: 만료 토큰으로 API 호출
- **WHEN** 24시간 경과한 JWT로 보호 엔드포인트 호출
- **THEN** HTTP 401, { error: { code: "TOKEN_EXPIRED", message: "인증이 만료되었습니다" } }
