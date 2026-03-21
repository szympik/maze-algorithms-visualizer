from Back.app.algorithms import a_star

def solve(maze, algorithm, step_callback=None):
    if algorithm == "a_star":
        return a_star(maze, step_callback=step_callback)

    raise ValueError(f"Unsupported algorithm: {algorithm}")