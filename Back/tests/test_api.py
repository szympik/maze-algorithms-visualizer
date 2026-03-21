import pytest
from fastapi.testclient import TestClient

from Back.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health_check(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_get_solvers(client):
    resp = client.get("/api/maze/solvers")
    assert resp.status_code == 200
    assert resp.json() == {"algorithms": ["a_star"]}


def test_generate_maze_returns_grid(client):
    size = 2
    resp = client.post("/api/maze/generate", json={"size": size})
    assert resp.status_code == 200

    body = resp.json()
    assert body["size"] == size

    maze = body["maze"]
    assert isinstance(maze, list)
    assert maze
    assert all(isinstance(row, list) for row in maze)
    assert all(cell in (0, 1) for row in maze for cell in row)

    start = (0, 1)
    end = (len(maze) - 1, len(maze[0]) - 2)
    assert maze[start[0]][start[1]] == 1
    assert maze[end[0]][end[1]] == 1
