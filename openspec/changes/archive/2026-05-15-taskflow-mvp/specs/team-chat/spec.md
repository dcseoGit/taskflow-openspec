## ADDED Requirements

### Requirement: 채팅 메시지 목록 조회 (폴링)
팀 멤버는 팀 채팅 메시지를 조회할 수 있어야 한다.
- since 파라미터가 없으면 최근 50개 반환
- since={ISO timestamp}이면 해당 시각 이후 메시지만 반환 (폴링 증분)
- 응답: created_at ASC 정렬

#### Scenario: 초기 로드 (since 없음)
- **WHEN** GET /teams/{id}/messages 요청
- **THEN** HTTP 200, 최근 50개 메시지 배열 (created_at ASC)

#### Scenario: 증분 폴링 (since 있음)
- **WHEN** GET /teams/{id}/messages?since=2026-05-13T14:27:00Z 요청
- **THEN** HTTP 200, since 이후에 생성된 메시지만 반환 (없으면 빈 배열 [])

#### Scenario: 새 메시지 없음
- **WHEN** since 이후 새 메시지가 없을 때 요청
- **THEN** HTTP 200, [] 반환 (화면 변화 없음)

#### Scenario: 비멤버 접근
- **WHEN** 비멤버가 GET /teams/{id}/messages 요청
- **THEN** HTTP 403, { error: { code: "FORBIDDEN", message: "권한이 없습니다" } }

### Requirement: 메시지 전송
팀 멤버는 1000자 이내 텍스트 메시지를 팀에 전송할 수 있어야 한다.
- content 필수, 1~1000자
- 클라이언트와 서버 양쪽에서 길이 검증
- 응답에 user_email 포함 (발신자 표시용)

#### Scenario: 정상 전송
- **WHEN** POST /teams/{id}/messages { content: "안녕하세요" }
- **THEN** HTTP 201, { id, team_id, user_id, user_email, content, created_at }

#### Scenario: 1000자 초과
- **WHEN** 1001자 content로 POST 요청
- **THEN** HTTP 400, { error: { code: "TOO_LONG", message: "메시지는 1000자 이내로 입력하세요", limit: 1000, actual: 1001 } }

#### Scenario: 빈 메시지
- **WHEN** content가 "" 또는 공백만인 요청
- **THEN** HTTP 400, { error: { code: "VALIDATION_ERROR", message: "메시지를 입력하세요" } }

### Requirement: 메시지 삭제
사용자는 본인이 전송한 메시지만 삭제할 수 있어야 한다.
- owner라도 타인 메시지 삭제 불가
- 삭제 성공 시 204 반환

#### Scenario: 본인 메시지 삭제
- **WHEN** 메시지 발신자가 DELETE /messages/{id} 요청
- **THEN** HTTP 204 No Content

#### Scenario: 타인 메시지 삭제 시도
- **WHEN** 발신자가 아닌 사람이 DELETE /messages/{id} 요청
- **THEN** HTTP 403, { error: { code: "NOT_OWNER", message: "본인의 메시지만 삭제할 수 있습니다" } }

#### Scenario: team owner가 타인 메시지 삭제 시도
- **WHEN** team owner가 다른 사람의 메시지에 DELETE 요청
- **THEN** HTTP 403, { error: { code: "NOT_OWNER", message: "본인의 메시지만 삭제할 수 있습니다" } }
