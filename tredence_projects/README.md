# Realtime Pair Project - Final Submission (Full-stack with Docker)

## What is included
- backend/: FastAPI backend with REST endpoints, WebSocket endpoint, Postgres persistence
- frontend/: Vite + React minimal frontend (textarea editor) with autocomplete UI
- docker-compose.yml: runs postgres, backend, frontend for local demo
- migrations.sql: SQL to create `rooms` table

## Quick demo (Docker)
1. Ensure Docker and Docker Compose are installed.
2. From project root, run:
   ```bash
   docker compose up --build
   ```
3. Wait for services to start:
   - Frontend: http://localhost:5173
   - Backend API docs: http://localhost:8000/docs
   - Postgres exposed on 5432 (if needed)

## Notes for reviewers / HR
- Room creation: POST /rooms -> returns `roomId`
- WebSocket endpoint: ws://<host>:8000/ws/{roomId}
- Autocomplete: POST /autocomplete with { code, cursorPosition, language }
- Persistence: backend uses Postgres to store canonical room code; migrations.sql included.
- Sync strategy: last-write-wins; server broadcasts updates to clients in same room.
- Limitations & improvements are in backend/README.md

Good luck with your submission — this is a full working project ready to run locally or deploy.
