## ADDED Requirements

### Requirement: 태스크 목록 조회
팀 멤버는 팀의 태스크를 필터와 함께 조회할 수 있어야 한다.
- 기본 정렬: created_at DESC
- 필터: 전체(기본), @me(assignee_id=현재사용자), 미할당(assignee_id IS NULL)
- 응답에 assignee 정보(email) 포함

#### Scenario: 전체 태스크 조회
- **WHEN** 팀 멤버가 GET /teams/{id}/tasks 요청
- **THEN** HTTP 200, 해당 팀의 모든 태스크 배열 (created_at DESC 정렬)

#### Scenario: @me 필터
- **WHEN** GET /teams/{id}/tasks?filter=me 요청
- **THEN** HTTP 200, assignee_id가 현재 사용자인 태스크만 반환

#### Scenario: 미할당 필터
- **WHEN** GET /teams/{id}/tasks?filter=unassigned 요청
- **THEN** HTTP 200, assignee_id IS NULL인 태스크만 반환

#### Scenario: 비멤버 접근
- **WHEN** 비멤버가 GET /teams/{id}/tasks 요청
- **THEN** HTTP 403, { error: { code: "FORBIDDEN", message: "권한이 없습니다" } }

### Requirement: 태스크 생성
팀 멤버는 태스크를 TODO 상태로 생성할 수 있어야 한다.
- 제목은 1~100자 필수
- assignee_id는 nullable (생략 시 미할당)
- 생성자(creator_id)는 현재 로그인 사용자로 자동 설정
- 초기 status는 항상 TODO

#### Scenario: 정상 생성 (담당자 지정)
- **WHEN** POST /teams/{id}/tasks { title: "DB 마이그레이션", assignee_id: 42 }
- **THEN** HTTP 201, { id, team_id, title, status: "TODO", creator_id, assignee_id: 42, created_at }

#### Scenario: 담당자 없이 생성
- **WHEN** POST /teams/{id}/tasks { title: "검토 필요" } (assignee_id 생략)
- **THEN** HTTP 201, { ..., assignee_id: null }

#### Scenario: 제목 100자 초과
- **WHEN** 101자 제목으로 생성 요청
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "제목은 100자 이내여야 합니다" } }

### Requirement: 태스크 단일 조회
팀 멤버는 태스크 상세 정보를 조회할 수 있어야 한다.

#### Scenario: 정상 조회
- **WHEN** 팀 멤버가 GET /tasks/{id} 요청
- **THEN** HTTP 200, { id, title, status, creator: { id, email }, assignee: { id, email } | null, created_at }

#### Scenario: 존재하지 않는 태스크
- **WHEN** GET /tasks/99999 요청 (존재하지 않음)
- **THEN** HTTP 404, { error: { code: "NOT_FOUND", message: "해당 항목을 찾을 수 없습니다" } }

### Requirement: 태스크 제목·담당자 수정
팀 멤버는 태스크 제목과 담당자를 수정할 수 있어야 한다.

#### Scenario: 제목 수정
- **WHEN** PUT /tasks/{id} { title: "수정된 제목" }
- **THEN** HTTP 200, 업데이트된 태스크 반환

#### Scenario: 담당자 변경
- **WHEN** PUT /tasks/{id} { assignee_id: 99 }
- **THEN** HTTP 200, assignee_id가 99로 업데이트된 태스크 반환

#### Scenario: 담당자 해제
- **WHEN** PUT /tasks/{id} { assignee_id: null }
- **THEN** HTTP 200, assignee_id: null인 태스크 반환

### Requirement: 태스크 상태 변경
팀 멤버는 태스크 상태를 TODO/DOING/DONE 중 하나로 변경할 수 있어야 한다.
- 유효한 값: "TODO", "DOING", "DONE"

#### Scenario: 상태 변경 (드래그 drop)
- **WHEN** PATCH /tasks/{id}/status { status: "DOING" }
- **THEN** HTTP 200, { id, status: "DOING", ... }

#### Scenario: 유효하지 않은 상태값
- **WHEN** PATCH /tasks/{id}/status { status: "INVALID" }
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "올바른 상태값이 아닙니다" } }

### Requirement: 태스크 삭제
태스크 creator 또는 team owner만 삭제할 수 있어야 한다.
- 삭제 권한: creator_id = 현재 사용자 OR 팀 owner
- 삭제 성공 시 204 반환

#### Scenario: creator가 삭제
- **WHEN** creator가 DELETE /tasks/{id} 요청
- **THEN** HTTP 204 No Content

#### Scenario: team owner가 타인 태스크 삭제
- **WHEN** team owner가 다른 사람이 만든 태스크에 DELETE 요청
- **THEN** HTTP 204 No Content

#### Scenario: 권한 없는 멤버가 삭제 시도
- **WHEN** creator도 owner도 아닌 멤버가 DELETE 요청
- **THEN** HTTP 403, { error: { code: "FORBIDDEN", message: "권한이 없습니다" } }
