#!/bin/bash
uv run python -m backend.main &
cd frontend
npm run preview -- --host 0.0.0.0 --port 5000
