import type { ConsensusResponse } from "../types/consensus";

type ResultPanelProps = {
  result: ConsensusResponse | null;
};

function ResultPanel({ result }: ResultPanelProps) {
  if (!result) {
    return null;
  }

  return (
    <section className="result-stack" aria-label="Consensus result">
      <article className="panel final-answer">
        <p className="panel-kicker">Final Consensus Answer</p>
        <h2>{result.question}</h2>
        <p>{result.final_answer}</p>
      </article>

      <div className="result-grid">
        <ListSection title="Agreement Points" items={result.agreement_points} />
        <ListSection title="Disagreement Points" items={result.disagreement_points} />
        <ListSection title="Uncertainties / Caveats" items={result.uncertainties} />
        <ListSection title="Suggested Follow-Up Questions" items={result.follow_up_questions} />
      </div>

      <article className="panel">
        <h2>Primary Answer</h2>
        <p className="long-text">{result.primary_answer}</p>
      </article>

      <article className="panel">
        <h2>Reviewer Critique</h2>
        <p className="long-text">{result.reviewer_critique}</p>
      </article>

      <article className="panel">
        <h2>Models Used</h2>
        <dl className="models-list">
          <div>
            <dt>Primary</dt>
            <dd>{result.models_used.primary}</dd>
          </div>
          <div>
            <dt>Reviewer</dt>
            <dd>{result.models_used.reviewer}</dd>
          </div>
          <div>
            <dt>Synthesizer</dt>
            <dd>{result.models_used.synthesizer}</dd>
          </div>
        </dl>
      </article>
    </section>
  );
}

type ListSectionProps = {
  title: string;
  items: string[];
};

function ListSection({ title, items }: ListSectionProps) {
  return (
    <article className="panel">
      <h2>{title}</h2>
      {items.length > 0 ? (
        <ul className="result-list">
          {items.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ul>
      ) : (
        <p className="empty-state">No items returned.</p>
      )}
    </article>
  );
}

export default ResultPanel;
