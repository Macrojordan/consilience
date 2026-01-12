# Backend Module Guide

## Council Process Architecture

The council process runs in stages, coordinated by `council.py`:

1. **Stage 1** (`stage1_collect_responses`): Collect individual responses from all council models
2. **Stage 1.5** (`stage1_5_cross_examination`): Each model critiques all other responses to identify errors and flaws
3. **Stage 2** (`stage2_collect_rankings`): Each model ranks the anonymized responses
4. **Stage 3** (`stage3_synthesize_final`): Chairman model synthesizes final response

### Important Implementation Details

- `run_full_council()` returns a 5-tuple: `(stage1, stage1_5, stage2, stage3, metadata)`
- When modifying the council process, update **both** `send_message` and `send_message_stream` endpoints in `main.py`
- Streaming events follow pattern: `stage{N}_start` → `stage{N}_complete`
- All stage data is persisted to SQLite via `storage.add_assistant_message()`

## Storage Layer

The storage layer (`storage.py`) maintains backward compatibility while using SQLite internally:

- All functions return dictionaries matching the old JSON structure
- Stage data is stored as JSON in the `stage_data` column
- `add_assistant_message()` accepts optional `stage1_5` parameter for cross-examination data
- Use parameterized queries for all SQL operations

## Model Configuration

- `COUNCIL_MODELS` and `CHAIRMAN_MODEL` are loaded from `config.py`
- Models can be overridden via `COUNCIL_MODELS` environment variable (JSON array string)
- `openrouter.py` handles parallel model queries via `query_models_parallel()`

## Testing

- Import the backend modules by adding parent directory to sys.path
- Virtual environment is in `backend/venv/`
- Example: `python -c "import sys; sys.path.insert(0, '..'); from backend import council"`
