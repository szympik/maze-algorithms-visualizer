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

## Favicon / app icon

- The HTML favicon link is in `index.html` (Front/index.html). I updated it to point to `src/assets/maze_icon.png`.
- For production builds it's recommended to place the favicon in `Front/public` and reference it as `/favicon.png` or `/favicon.ico` to ensure the file is copied as-is.

## Notes

- To see favicon changes you may need to clear browser cache or restart the dev server.
- If you want, I can:
  - copy `Front/src/assets/maze_icon.png` into `Front/public` and update `index.html` to `/favicon.png`, and generate a `favicon.ico`.
