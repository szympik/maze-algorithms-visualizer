# Maze Solver

Full-stack maze generator and solver — Python backend (FastAPI) and React + Vite frontend.

## Structure

- `Back/` — Python backend, API and maze algorithms
- `Front/` — React + Vite frontend
- `docker-compose.yml` — brings up backend + frontend with Docker

## Quick start (Docker)

1. Build and start services:

```bash
docker compose up -d --build
```

2. Services (default ports):

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api

## Local development (frontend)

1. Open a terminal in the `Front/` folder.
2. Install and run:

```bash
npm install
npm run dev
```

The dev server listens on port 5173 by default.

## Local development (backend)

1. Create and activate a Python virtual environment.
2. Install backend dependencies (see `Back/docker/requirements.txt`) or use the repo's `.venv` if present.
3. Run the API (example):

```bash
python Back/main.py
```

The API is available at `http://localhost:8000/api` by default (see `Front/.env` which points to this URL).

## Features

- Generate mazes of configurable size.
- Solve mazes with pathfinding (A*).
- Real-time solving updates via WebSocket.
- Visualize maze, visited nodes, and final path in the UI.

## Notes

- The frontend expects the API at `http://localhost:8000/api` (see `Front/.env`).
