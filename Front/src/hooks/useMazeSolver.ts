import { useEffect, useMemo, useRef, useState } from "react";
import {
  generateMaze,
  solveMazeWS,
  type Maze,
  type Point,
} from "../services/mazeApi";

export function useMazeSolver() {
  const [maze, setMaze] = useState<Maze>([]);
  const [visited, setVisited] = useState<Set<string>>(new Set());
  const [path, setPath] = useState<Point[]>([]);
  const [status, setStatus] = useState("Ready");
  const [size, setSize] = useState(10);
  const [algorithm, setAlgorithm] = useState("a_star");
  const [stepDelayMs, setStepDelayMs] = useState(120);

  const stepQueueRef = useRef<Point[]>([]);
  const solveDonePathRef = useRef<Point[] | null>(null);
  const stepTimerRef = useRef<number | null>(null);

  const algorithms = [
    { value: "a_star", label: "A*" },
    { value: "bfs", label: "BFS" },
    { value: "dfs", label: "DFS" },
  ];

  const generateNewMaze = async () => {
    if (stepTimerRef.current !== null) {
      window.clearInterval(stepTimerRef.current);
      stepTimerRef.current = null;
    }
    stepQueueRef.current = [];
    solveDonePathRef.current = null;

    setStatus("Generating...");
    setVisited(new Set());
    setPath([]);

    try {
      const mazeSize = Math.max(5, Math.min(100, size || 10));
      const data = await generateMaze(mazeSize);
      setMaze(data.maze);
      setStatus("Ready");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to generate maze";
      setStatus(`Error: ${message}`);
    }
  };

  const handleSolve = () => {
    if (maze.length === 0) {
      setStatus("Generate maze first");
      return;
    }

    if (stepTimerRef.current !== null) {
      window.clearInterval(stepTimerRef.current);
      stepTimerRef.current = null;
    }
    stepQueueRef.current = [];
    solveDonePathRef.current = null;

    setVisited(new Set());
    setPath([]);
    setStatus(`Solving (${algorithm})...`);

    const finalizeSolve = (solvedPath: Point[]) => {
      setPath(solvedPath);
      setStatus(`Done. Path length: ${solvedPath.length}`);
    };

    const processQueuedStep = () => {
      const next = stepQueueRef.current.shift();

      if (!next) {
        if (stepTimerRef.current !== null) {
          window.clearInterval(stepTimerRef.current);
          stepTimerRef.current = null;
        }

        if (solveDonePathRef.current) {
          const finalPath = solveDonePathRef.current;
          solveDonePathRef.current = null;
          finalizeSolve(finalPath);
        }
        return;
      }

      setVisited((prev) => {
        const newSet = new Set(prev);
        newSet.add(`${next.x}-${next.y}`);
        return newSet;
      });
    };

    solveMazeWS(maze, algorithm, {
      onStep: ({ x, y }) => {
        if (stepDelayMs <= 0) {
          setVisited((prev) => {
            const newSet = new Set(prev);
            newSet.add(`${x}-${y}`);
            return newSet;
          });
          return;
        }

        stepQueueRef.current.push({ x, y });

        if (stepTimerRef.current === null) {
          stepTimerRef.current = window.setInterval(
            processQueuedStep,
            Math.max(1, stepDelayMs)
          );
        }
      },
      onDone: (solvedPath) => {
        if (stepDelayMs <= 0 || stepQueueRef.current.length === 0) {
          finalizeSolve(solvedPath);
          return;
        }

        solveDonePathRef.current = solvedPath;
        setStatus("Finalizing visualization...");
      },
      onError: (message) => {
        if (stepTimerRef.current !== null) {
          window.clearInterval(stepTimerRef.current);
          stepTimerRef.current = null;
        }
        stepQueueRef.current = [];
        solveDonePathRef.current = null;
        setStatus(`Error: ${message}`);
      },
    });
  };

  useEffect(() => {
    return () => {
      if (stepTimerRef.current !== null) {
        window.clearInterval(stepTimerRef.current);
      }
    };
  }, []);

  const pathSet = useMemo(
    () => new Set(path.map((p) => `${p.x}-${p.y}`)),
    [path]
  );

  return {
    maze,
    visited,
    path,
    pathSet,
    status,
    size,
    setSize,
    algorithm,
    setAlgorithm,
    stepDelayMs,
    setStepDelayMs,
    algorithms,
    generateNewMaze,
    handleSolve,
  };
}