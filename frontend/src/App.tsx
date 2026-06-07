import { useEffect, useState } from "react";

import { checkHealth, runConsensus } from "./api/client";
import ErrorMessage from "./components/ErrorMessage";
import LoadingSteps from "./components/LoadingSteps";
import QuestionForm from "./components/QuestionForm";
import ResultPanel from "./components/ResultPanel";
import StatusBanner from "./components/StatusBanner";
import type {
  ConsensusRequest,
  ConsensusResponse,
  HealthStatus,
  ProviderName,
} from "./types/consensus";

const maxQuestionLength = 8000;

function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [isChecking, setIsChecking] = useState(false);
  const [healthError, setHealthError] = useState("");
  const [question, setQuestion] = useState("");
  const [primaryProvider, setPrimaryProvider] = useState<ProviderName>("openai");
  const [reviewerProvider, setReviewerProvider] = useState<ProviderName>("gemini");
  const [synthesizerProvider, setSynthesizerProvider] = useState<ProviderName>("openai");
  const [validationError, setValidationError] = useState("");
  const [apiError, setApiError] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<ConsensusResponse | null>(null);

  useEffect(() => {
    handleHealthCheck();
  }, []);

  async function handleHealthCheck() {
    setIsChecking(true);
    setHealthError("");

    try {
      const result = await checkHealth();
      setHealth(result);
    } catch {
      setHealth(null);
      setHealthError("Backend is unavailable. Start the backend and try again.");
    } finally {
      setIsChecking(false);
    }
  }

  async function handleSubmit(request: ConsensusRequest) {
    const trimmedQuestion = request.question.trim();

    if (!trimmedQuestion) {
      setValidationError("Question is required.");
      return;
    }

    if (trimmedQuestion.length > maxQuestionLength) {
      setValidationError(`Question must be ${maxQuestionLength} characters or fewer.`);
      return;
    }

    setValidationError("");
    setApiError("");
    setResult(null);
    setIsRunning(true);

    try {
      const response = await runConsensus({
        ...request,
        question: trimmedQuestion,
      });
      setResult(response);
    } catch (error) {
      setApiError(
        error instanceof Error
          ? error.message
          : "Unable to run consensus. Try again after checking the backend.",
      );
    } finally {
      setIsRunning(false);
    }
  }

  function handleClear() {
    setQuestion("");
    setValidationError("");
    setApiError("");
    setResult(null);
    setPrimaryProvider("openai");
    setReviewerProvider("gemini");
    setSynthesizerProvider("openai");
  }

  return (
    <main className="app-shell">
      <section className="intro" aria-labelledby="app-title">
        <p className="eyebrow">Mythadis Labs</p>
        <h1 id="app-title">Mythadis Consensus Engine</h1>
        <p className="tagline">The books are fiction. The questions are real.</p>
        <p className="intro-copy">
          Ask a question. One AI answers, another reviews, and a final synthesis
          highlights agreement, disagreement, and uncertainty.
        </p>
      </section>

      <section className="workspace" aria-label="Consensus workspace">
        <div className="status-row">
          <StatusBanner health={health} error={healthError} isChecking={isChecking} />
          <button
            className="secondary-button"
            type="button"
            onClick={handleHealthCheck}
            disabled={isChecking}
          >
            {isChecking ? "Checking..." : "Check backend"}
          </button>
        </div>

        <QuestionForm
          question={question}
          primaryProvider={primaryProvider}
          reviewerProvider={reviewerProvider}
          synthesizerProvider={synthesizerProvider}
          isLoading={isRunning}
          validationError={validationError}
          onQuestionChange={setQuestion}
          onPrimaryProviderChange={setPrimaryProvider}
          onReviewerProviderChange={setReviewerProvider}
          onSynthesizerProviderChange={setSynthesizerProvider}
          onSubmit={handleSubmit}
          onClear={handleClear}
        />

        <LoadingSteps isVisible={isRunning} />
        <ErrorMessage message={apiError} />
        <ResultPanel result={result} />
      </section>
    </main>
  );
}

export default App;
