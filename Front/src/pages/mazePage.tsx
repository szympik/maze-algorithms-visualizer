import { useEffect, useState, useMemo } from "react";
import { generateMaze, solveMazeWS, type Maze, type Point } from "../services/mazeApi";
import "./mazePage.css";

export default function MazePage() {
  const [maze, setMaze] = useState<Maze>([]);
  const [visited, setVisited] = useState<Set<string>>(new Set());
  const [path, setPath] = useState<Point[]>([]);
  const [status, setStatus] = useState("Ready");

  const generateNewMaze = async () => {
    setStatus("Generating...");
    setVisited(new Set());
    setPath([]);

    try {
      const data = await generateMaze(10);
      setMaze(data.maze);
      setStatus("Ready");
    } catch (err: any) {
      setStatus(`Error: ${err?.message ?? "Failed to generate maze"}`);
    }
  };

  

  const handleSolve = () => {
    if (maze.length === 0) {
      return;
    }

    setVisited(new Set());
    setPath([]);
    setStatus("Solving...");

    solveMazeWS(maze, "a_star", {
      onStep: ({ x, y }) => {
        setVisited((prev) => {
          const newSet = new Set(prev);
          newSet.add(`${x}-${y}`);
          return newSet;
        });
      },
      onDone: (solvedPath) => {
        console.log("Maze solved! Path:", solvedPath);
        setPath(solvedPath);
        setStatus(`Done. Path length: ${solvedPath.length}`);
      },
      onError: (message) => {
        setStatus(`Error: ${message}`);
      },
    });
  };

  const pathSet = useMemo(
    () => new Set(path.map((p) => `${p.x}-${p.y}`)),
    [path]
  );

  return (
    <>
      <div>
      <h1>Maze</h1>

      
      <p>{status}</p>
      <p>Visited: {visited.size} | Path: {path.length}</p>

      <div className="maze-container">
        {maze.map((row, y) => (
          <div key={y} className="maze-row">
            {row.map((cell, x) => {
              const key = `${x}-${y}`;
              const isVisited = visited.has(key);
              const isPath = pathSet.has(key);

              const cellClass = isPath
                ? "path"
                : isVisited
                ? "visited"
                : cell === 1
                ? "wall"
                : "open";

              return <div key={x} className={`maze-cell ${cellClass}`} />;
            })}
          </div>
        ))}
      </div>
      </div>

      <div className="controls">
      <button onClick={handleSolve} disabled={maze.length === 0}>
        Solve
      </button>
         <button onClick={generateNewMaze}>
        Generate Maze
      </button>
    </div>  
    </>
  );
}