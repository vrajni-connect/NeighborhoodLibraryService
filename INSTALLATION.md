# Neighborhood Library Service - Installation and Run Guide

## 1. Project Overview

This repository contains a full-stack Neighborhood Library Service:
- `backend/`: Python FastAPI service with SQLModel and database models.
- `frontend/`: React + Vite minimal UI.
- `docker-compose.yml`: Optional containerized setup for PostgreSQL, backend, and frontend.

## 2. Prerequisites

### Required
- Python 3.11+ (for backend)
- Node.js 18/20 (for frontend)
- npm or pnpm

### Optional (Docker setup)
- Docker
- Docker Compose

## 3. Local Setup (recommended)

### 3.1 Backend

1. Open WSL terminal.
2. Go to project root:
   ```bash
   cd /root/NeibourhoodLibraryService
   ```
3. Create Python venv (if not already):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
5. Start backend server:
   ```bash
   uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
   ```
6. Verify:
   - Open `http://127.0.0.1:8000/docs`

### 3.2 Frontend

1. In a new terminal (can run concurrently):
   ```bash
   cd /root/NeibourhoodLibraryService/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start frontend app:
   ```bash
   npm run dev -- --host 0.0.0.0 --port 5173
   ```
4. Open:
   - `http://127.0.0.1:5173`

## 4. Docker Setup (optional)

1. From project root:
   ```bash
   cd /root/NeibourhoodLibraryService
   docker compose up --build
   ```
2. Wait until all services are up.
3. Access:
   - Backend docs: `http://localhost:8000/docs`
   - Frontend app: `http://localhost:5173`

## 5. How to Use the API

### Create book
```bash
curl -X POST "http://127.0.0.1:8000/books" -H "Content-Type: application/json" -d '{"title":"1984","author":"George Orwell","total_copies":2}'
```

### Create member
```bash
curl -X POST "http://127.0.0.1:8000/members" -H "Content-Type: application/json" -d '{"name":"Alex","email":"alex@example.com"}'
```

### Borrow book
```bash
curl -X POST "http://127.0.0.1:8000/borrow?member_id=1&book_id=1"
```

### Return book
```bash
curl -X POST "http://127.0.0.1:8000/return/1"
```

### List borrowed by member
```bash
curl "http://127.0.0.1:8000/members/1/borrowed"
```

## 6. Troubleshooting

### `npm: command not found`
Install Node:
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### FastAPI not reachable
- Ensure backend is running on 8000.
- Confirm process with `ss -ltnp | grep :8000`.

### Frontend not reachable
- Ensure Vite running on 5173.
- Confirm with `ss -ltnp | grep :5173`.

## 7. File structure summary

- `.gitignore`
- `backend/`
  - `app/main.py`
  - `app/models.py`
  - `app/database.py`
  - `requirements.txt`
  - `Dockerfile`
- `frontend/`
  - `src/App.jsx`
  - `src/main.jsx`
  - `package.json`
  - `vite.config.js`
  - `Dockerfile`
- `docker-compose.yml`
- `README.md`
- `INSTALLATION.md`

---

If you want, I can also add a short quick start script `scripts/run_local.sh` to run both backend and frontend together in one command.