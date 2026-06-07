const steps = [
  "Generating primary answer",
  "Reviewing answer",
  "Synthesizing final response",
];

type LoadingStepsProps = {
  isVisible: boolean;
};

function LoadingSteps({ isVisible }: LoadingStepsProps) {
  if (!isVisible) {
    return null;
  }

  return (
    <section className="panel loading-panel" aria-live="polite">
      <p className="panel-kicker">Running consensus workflow...</p>
      <ol className="loading-steps">
        {steps.map((step) => (
          <li key={step}>{step}</li>
        ))}
      </ol>
    </section>
  );
}

export default LoadingSteps;
