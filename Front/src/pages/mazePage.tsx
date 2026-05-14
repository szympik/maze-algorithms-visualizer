import { useMazeSolver } from "../hooks/useMazeSolver";
import "../styles/mazePage.css";

export default function MazePage() {
  const {
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
  } = useMazeSolver();

  return (
    <div className="maze-page">
      <div className="maze-content">
        <h1 className="maze-title">Maze Solver/Creator</h1>

        <form
          className="controls"
          onSubmit={(e) => {
            e.preventDefault();
            generateNewMaze();
          }}
        >
          <label>
            Size
            <input
              type="number"
              min={5}
              max={100}
              value={size}
              onChange={(e) => setSize(Number(e.target.value) || 10)}
            />
          </label>

          <label>
            Algorithm
            <select
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
            >
              {algorithms.map((algo) => (
                <option key={algo.value} value={algo.value}>
                  {algo.label}
                </option>
              ))}
            </select>
          </label>

          <label>
            Step Delay ({stepDelayMs} ms)
            <input
              type="range"
              min={0}
              max={1000}
              step={20}
              value={stepDelayMs}
              onChange={(e) => setStepDelayMs(Number(e.target.value) || 0)}
            />
          </label>

          <button className="glass-button glossy-button" type="submit">
            <span>Generate Maze</span>
          </button>

          <button
            className="glass-button glossy-button"
            type="button"
            onClick={handleSolve}
            disabled={maze.length === 0}
          >
            <span>Solve</span>
          </button>
        </form>

        <p className="maze-status">{status}</p>
        <p className="maze-meta">
          Visited: {visited.size} | Path: {path.length}
        </p>

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
    </div>
  );
}