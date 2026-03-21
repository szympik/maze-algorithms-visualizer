from ..utils.solve import solve
from ..utils.maze import Maze
from fastapi import FastAPI, HTTPException, WebSocket, APIRouter, WebSocketDisconnect
import asyncio
from pydantic import BaseModel


router = APIRouter()

#health check
@router.get("/health")
def health_check():
    return {"status": "healthy"}

#maze generation
class MazeRequest(BaseModel):
    size: int

@router.post("/maze/generate")
def generate_maze_endpoint(request: MazeRequest):
    maze = Maze(request.size)
    maze.create_maze()

    return {
        "size": request.size,
        "maze": [[0 if not cell.walkable else 1 for cell in row] for row in maze.grid],
    }

@router.get("/maze/solvers")
def get_solvers():
    return {
        "algorithms": ["a_star"]
    }

#maze solving
class MazeSolveRequest(BaseModel):
    maze: list[list[int]]
    algorithm: str

@router.websocket("/ws/maze/solve")
async def solve_ws(websocket: WebSocket):
    await websocket.accept()

    data = await websocket.receive_json()

    maze = Maze(0)
    maze.json_to_maze(data["maze"])

    algorithm = data.get("algorithm", "a_star")

    def step_callback(current, open_list):
        asyncio.create_task(websocket.send_json({
            "type": "step",
            "x": current[0],
            "y": current[1],
        }))

    path = solve(maze, algorithm, step_callback=step_callback)

    await websocket.send_json({
        "type": "done",
        "path": path
    })

