import type {
  ApiError,
  ConsensusRequest,
  ConsensusResponse,
  HealthStatus,
} from "../types/consensus";

const backendUrl =
  import.meta.env.VITE_API_BASE_URL ??
  import.meta.env.VITE_BACKEND_URL ??
  "http://localhost:8000";

export async function checkHealth(): Promise<HealthStatus> {
  const response = await fetch(`${backendUrl}/health`);

  if (!response.ok) {
    throw new Error(`Backend health check failed with ${response.status}`);
  }

  return response.json();
}

export async function runConsensus(
  request: ConsensusRequest,
): Promise<ConsensusResponse> {
  let response: Response;

  try {
    response = await fetch(`${backendUrl}/consensus/run`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });
  } catch {
    throw new Error("Unable to reach backend. Make sure the backend is running on port 8000.");
  }

  if (!response.ok) {
    throw new Error(await readErrorMessage(response));
  }

  return response.json();
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as ApiError;
    if (body.detail) {
      return body.detail;
    }
  } catch {
    return "The backend returned an unreadable error response.";
  }

  return `Backend request failed with status ${response.status}.`;
}

export { checkHealth as getBackendHealth };
