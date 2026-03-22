const API_URL = import.meta.env.VITE_API_URL;
const WS_URL = import.meta.env.VITE_WS_URL;

//types

export type Maze = number[][];

export type GenerateMazeResponse = {
  size: number;
  maze: Maze;
};

export type SolversResponse = {
  algorithms: string[];
};

export type Point = {
  x: number;
  y: number;
};

type RawPoint = Point | [number, number];

export type StepMessage = {
  type: "step";
  x: number;
  y: number;
};

export type DoneMessage = {
  type: "done";
  path: RawPoint[];
};

export type ErrorMessage = {
  type: "error";
  message: string;
};

export type WSMessage = StepMessage | DoneMessage | ErrorMessage;

function parseRawPoint(raw: RawPoint): Point | null {
  if (Array.isArray(raw) && raw.length >= 2) {
    const row = raw[0];
    const col = raw[1];
    if (typeof row === "number" && typeof col === "number") {
      return { x: col, y: row };
    }
  }

  if (
    raw &&
    typeof raw === "object" &&
    "x" in raw &&
    "y" in raw &&
    typeof raw.x === "number" &&
    typeof raw.y === "number"
  ) {
    // Backend sends x=row, y=col; UI expects x=col, y=row.
    return { x: raw.y, y: raw.x };
  }

  return null;
}

//api calls

export async function generateMaze(size: number): Promise<GenerateMazeResponse> {
  const res = await fetch(`${API_URL}/maze/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ size }),
  });

  if (!res.ok) {
    throw new Error("Failed to generate maze");
  }

  return res.json();
}

export async function getSolvers(): Promise<SolversResponse> {
  const res = await fetch(`${API_URL}/maze/solvers`);

  if (!res.ok) {
    throw new Error("Failed to fetch solvers");
  }

  return res.json();
}

//websocket

type SolveCallbacks = {
  onStep: (point: Point) => void;
  onDone: (path: Point[]) => void;
  onError?: (message: string) => void;
};

export function solveMazeWS(
  maze: Maze,
  algorithm: string,
  callbacks: SolveCallbacks
) {
  const ws = new WebSocket(WS_URL);

  ws.onopen = () => {
    ws.send(
      JSON.stringify({
        maze,
        algorithm,
      })
    );
  };

  ws.onmessage = (event) => {
    const data: WSMessage = JSON.parse(event.data);

    switch (data.type) {
      case "step":
        callbacks.onStep({ x: data.y, y: data.x });
        break;

      case "done":
        callbacks.onDone(
          (Array.isArray(data.path) ? data.path : [])
            .map(parseRawPoint)
            .filter((p): p is Point => p !== null)
        );
        ws.close();
        break;

      case "error":
        callbacks.onError?.(data.message);
        ws.close();
        break;
    }
  };

  ws.onerror = () => {
    callbacks.onError?.("WebSocket connection error");
  };

  return ws;
}