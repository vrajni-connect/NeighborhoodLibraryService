# Neighborhood Library Service

This project is a Python FastAPI backend + React frontend for a neighborhood library service with PostgreSQL.

## Project Structure

- `backend/` - FastAPI app using SQLModel with PostgreSQL.
- `frontend/` - React Vite minimal UI.
- `docker-compose.yml` - launches PostgreSQL, backend, frontend.

## Setup (Docker Compose)

1. From project root:
   ```bash
   docker compose up --build
   ```
2. Verify:
   - Backend: http://localhost:8000/docs
   - Frontend: http://localhost:5173

## Backend without Docker (local Python)

1. Create virtual env:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Start PostgreSQL (local or docker):
   ```bash
   docker run --name library-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=library -p 5432:5432 -d postgres:15
   ```
3. Run API:
   ```bash
   export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/library
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## API Endpoints

- `POST /books` create book
- `PUT /books/{id}` update book
- `GET /books` list books
- `POST /members` create member
- `PUT /members/{id}` update member
- `GET /members` list members
- `POST /borrow?member_id=&book_id=` borrow
- `POST /return/{borrow_id}` return
- `GET /members/{id}/borrowed` list borrows
- `GET /borrows?active_only=true` list borrows

## Quick Testing (curl)

Create book:
```bash
curl -X POST "http://localhost:8000/books" -H "Content-Type: application/json" -d '{"title":"1984","author":"Orwell","total_copies":2}'
```

Create member:
```bash
curl -X POST "http://localhost:8000/members" -H "Content-Type: application/json" -d '{"name":"Alex","email":"alex@example.com"}'
```

Borrow:
```bash
curl -X POST "http://localhost:8000/borrow?member_id=1&book_id=1"
```

Return:
```bash
curl -X POST "http://localhost:8000/return/1"
```

## What input is required on terminal

To run in this repo from scratch:
1. `docker compose up --build`
2. Open `http://localhost:8000/docs` and `http://localhost:5173`.

For local backend only:
1. In `backend`: `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Ensure Postgres is running.
4. `DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/library uvicorn app.main:app --reload`
