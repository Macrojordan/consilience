# PRD: Consilience Upgrade (High-Precision)

## Introduction
Upgrade "LLM Council" to "Consilience". This is a targeted refactor. We will swap the JSON storage for SQLite, inject "Stage 1.5 (Cross-Examination)" into the existing run_full_council pipeline, and apply a Cyberpunk reskin.

## Goals
**Persistence**: Refactor backend/storage.py to use SQLite while keeping the exact same public API to prevent breaking backend/main.py.

**Logic**: Update backend/council.py to insert stage1_5_cross_examination.

**Config**: Move hardcoded models in backend/config.py to environment variables.

**UI**: Update ChatInterface.jsx and App.jsx to handle the new stage and apply the "Consilience" visual theme.

## User Stories

### US-001: SQLite Adapter Implementation
**Description**: Replace the internals of backend/storage.py without changing its function signatures, ensuring seamless integration with backend/main.py.

**Acceptance Criteria**:
- [ ] Create backend/database.py with sqlite3 connection and a init_db() function.
- [ ] Schema: Create tables conversations (id, title, created_at) and messages (conversation_id, role, content, stage_data JSON).
- [ ] Refactor backend/storage.py:
  - Rewrite create_conversation, get_conversation, add_user_message to query SQLite.
  - Crucial: Keep returning dictionaries that match the old JSON structure so the frontend doesn't break.
- [ ] Typecheck passes.

### US-002: Update Assistant Message Signature
**Description**: The add_assistant_message function is currently too rigid. It needs to support the new Stage 1.5 data.

**Acceptance Criteria**:
- [ ] Update backend/storage.py: Change signature of add_assistant_message to accept an optional stage1_5 argument:
```python
def add_assistant_message(
    conversation_id: str,
    stage1: List[Dict],
    stage2: List[Dict],
    stage3: Dict,
    stage1_5: Optional[List[Dict]] = None  # New argument
)
```
- [ ] Ensure stage1_5 data is persisted to the database (in the messages table).
- [ ] Typecheck passes.

### US-003: Dynamic Model Configuration
**Description**: Stop hardcoding models in backend/config.py.

**Acceptance Criteria**:
- [ ] Update backend/config.py to load COUNCIL_MODELS from a JSON string in .env (e.g., COUNCIL_MODELS=["openai/gpt-4", ...]).
- [ ] Update backend/council.py to use these imported variables.
- [ ] Verify backend/openrouter.py still functions with the new config.
- [ ] Typecheck passes.

### US-004: Implement Stage 1.5 (Cross-Examination)
**Description**: Add the logic where models critique each other before the final ranking.

**Acceptance Criteria**:
- [ ] Create backend/council.py -> stage1_5_cross_examination(user_query, stage1_results).
- [ ] Logic: Send a prompt to each model asking them to identify "hallucinations or errors" in the other anonymous responses.
- [ ] Update run_full_council in backend/council.py to call this new stage between Stage 1 and Stage 2.
- [ ] Update backend/main.py:
  - Update send_message to pass stage1_5 results to storage.add_assistant_message.
  - Update send_message_stream to yield stage1_5_start and stage1_5_complete events.

### US-005: Frontend State Management (App.jsx)
**Description**: The React app needs to know how to handle the new SSE events.

**Acceptance Criteria**:
- [ ] Update frontend/src/App.jsx:
  - Add stage1_5 state to the assistantMessage object structure.
  - Add case 'stage1_5_start': and case 'stage1_5_complete': to the handleSendMessage switch statement.
- [ ] Verify the state updates correctly during streaming.
- [ ] Verify in browser using dev-browser skill.

### US-006: Frontend Rendering (ChatInterface.jsx)
**Description**: Display the cross-examination results in the UI.

**Acceptance Criteria**:
- [ ] Create frontend/src/components/Stage1_5.jsx to display the critiques.
- [ ] Update frontend/src/components/ChatInterface.jsx:
  - Import and render <Stage1_5 /> between Stage 1 and Stage 2.
  - Pass the stage1_5 data from the message prop.
- [ ] Verify in browser using dev-browser skill.

### US-007: Consilience Cyberpunk Reskin
**Description**: Apply the new visual identity.

**Acceptance Criteria**:
- [ ] Update frontend/src/index.css:
  - Set background to #050505.
  - Update text colors to "Cyber Green", "Warm Amber", "Electric Blue".
- [ ] Update frontend/src/components/Sidebar.jsx: Give it a glassmorphism/HUD look.
- [ ] Verify in browser that the "Control Deck" vibe is achieved.

## Functional Requirements
**FR-1**: backend/storage.py must maintain backward compatibility with backend/main.py calls until main.py is explicitly updated in US-004.

**FR-2**: The system must handle cases where COUNCIL_MODELS environment variable is missing (fallback to defaults).

## Non-Goals
- Migrating existing .json conversation files to the new SQLite DB (we will start with a fresh DB).
- Complex Graph visualizations (List view only for now).
