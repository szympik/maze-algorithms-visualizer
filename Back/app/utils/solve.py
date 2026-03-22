from ..algorithms.a_star import a_star_search

def solve(maze, algorithm, step_callback=None):
    if algorithm == "a_star":
        return a_star_search(maze, step_callback=step_callback)

    raise ValueError(f"Unsupported algorithm: {algorithm}")