# Backend - FastAPI (Realtime Pair)

## Setup (local, without Docker)

1. Python 3.10+
2. Create virtualenv and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Setup Postgres and run migrations.sql to create rooms table.
4. Create .env with DATABASE_URL (example in .env.example)
5. Run server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
6. Open http://localhost:8000/docs to explore the API.
