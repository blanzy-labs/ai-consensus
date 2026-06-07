import type { FormEvent } from "react";

import type { ConsensusRequest, ProviderName } from "../types/consensus";
import ModelSelector from "./ModelSelector";

const maxQuestionLength = 8000;

type QuestionFormProps = {
  question: string;
  primaryProvider: ProviderName;
  reviewerProvider: ProviderName;
  synthesizerProvider: ProviderName;
  isLoading: boolean;
  validationError: string;
  onQuestionChange: (question: string) => void;
  onPrimaryProviderChange: (provider: ProviderName) => void;
  onReviewerProviderChange: (provider: ProviderName) => void;
  onSynthesizerProviderChange: (provider: ProviderName) => void;
  onSubmit: (request: ConsensusRequest) => void;
  onClear: () => void;
};

function QuestionForm({
  question,
  primaryProvider,
  reviewerProvider,
  synthesizerProvider,
  isLoading,
  validationError,
  onQuestionChange,
  onPrimaryProviderChange,
  onReviewerProviderChange,
  onSynthesizerProviderChange,
  onSubmit,
  onClear,
}: QuestionFormProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    onSubmit({
      question,
      primary_provider: primaryProvider,
      reviewer_provider: reviewerProvider,
      synthesizer_provider: synthesizerProvider,
    });
  }

  return (
    <form className="panel question-form" onSubmit={handleSubmit}>
      <label className="field">
        <span>Question</span>
        <textarea
          value={question}
          maxLength={maxQuestionLength}
          disabled={isLoading}
          placeholder="Ask a question worth checking from more than one angle."
          onChange={(event) => onQuestionChange(event.target.value)}
        />
      </label>

      <div className="form-meta">
        <span>{question.length}/{maxQuestionLength} characters</span>
        {validationError ? <span className="validation-error">{validationError}</span> : null}
      </div>

      <div className="selector-grid" aria-label="Provider selectors">
        <ModelSelector
          id="primary-provider"
          label="Primary responder"
          value={primaryProvider}
          disabled={isLoading}
          onChange={onPrimaryProviderChange}
        />
        <ModelSelector
          id="reviewer-provider"
          label="Reviewer"
          value={reviewerProvider}
          disabled={isLoading}
          onChange={onReviewerProviderChange}
        />
        <ModelSelector
          id="synthesizer-provider"
          label="Synthesizer"
          value={synthesizerProvider}
          disabled={isLoading}
          onChange={onSynthesizerProviderChange}
        />
      </div>

      <div className="button-row">
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Running..." : "Run consensus"}
        </button>
        <button className="secondary-button" type="button" disabled={isLoading} onClick={onClear}>
          Clear
        </button>
      </div>
    </form>
  );
}

export default QuestionForm;
