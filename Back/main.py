from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .app.api.api import router as api_router

app = FastAPI(title="Maze Solver API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Maze Solver API"}