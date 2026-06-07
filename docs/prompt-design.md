# Prompt Design

## Purpose

Mythadis Consensus Engine uses a three-stage prompt flow:

```text
Primary answer -> Reviewer critique -> Final synthesis
```

The goal is to improve the quality and usefulness of an answer by separating initial answering, quality review, and final synthesis.

## Design Goals

- Improve answer quality
- Surface uncertainty
- Reduce overconfidence
- Avoid fake certainty
- Show agreement and disagreement
- Make structured output possible
- Keep the process transparent

## Stage 1: Primary Answer

The primary prompt asks the selected model to answer the user's question directly, clearly, and usefully. It tells the model to state assumptions, distinguish facts from reasoning, avoid unsupported certainty, and mention important uncertainty.

The primary stage does not require JSON. Plain text is used so the model can focus on producing a useful answer rather than satisfying a response schema too early.

The prompt also warns the model not to invent citations, sources, data, quotes, or research. Mythadis Consensus Engine does not browse the web in V1, so the prompt tells the model to say when current or external verification would be needed.

## Stage 2: Reviewer Critique

The reviewer prompt frames the model as an objective quality reviewer, not a debate opponent.

The reviewer receives the original question and primary answer. It is asked to identify strengths, weak claims, missing context, assumptions, unclear uncertainty, possible hallucinations, and useful improvements.

The reviewer is explicitly told not to argue merely to disagree and not to rewrite the whole answer unless necessary. The purpose is to improve quality, not to create artificial conflict.

## Stage 3: Final Synthesis

The synthesis prompt receives the original question, primary answer, and reviewer critique. It asks the synthesizer to preserve useful parts of the primary answer, apply legitimate reviewer corrections, ignore weak objections, and produce the best balanced final answer.

The final prompt requests JSON so the backend can return a stable response shape to clients. This supports separate fields for the final answer, agreement points, disagreement points, uncertainties, and follow-up questions.

The prompt tells the synthesizer:

- Return valid JSON only
- Do not wrap JSON in Markdown
- Do not include commentary before or after the JSON
- Use empty arrays if a section has no items
- Make all array values strings

## JSON Output Contract

The synthesizer is expected to return:

```json
{
  "final_answer": "string",
  "agreement_points": ["string"],
  "disagreement_points": ["string"],
  "uncertainties": ["string"],
  "follow_up_questions": ["string"]
}
```

## Failure Handling

The backend tries to parse the synthesizer output as JSON. It also tolerates common formatting mistakes such as Markdown-wrapped JSON or extra text around a JSON object.

If valid structured JSON cannot be parsed, the backend does not crash. It returns the raw synthesizer output as `final_answer`, leaves the structured list fields empty, and adds this uncertainty:

```text
The synthesizer did not return valid structured JSON.
```

This fallback is error handling, not a mock AI response.

## Safety And Limitations

The prompts include safety and limitation guidance:

- Consensus does not equal truth.
- Mythadis Consensus Engine does not browse the web in V1.
- Models can still hallucinate.
- Current facts may require external verification.
- Models should not pretend to have performed external research.
- Models should not invent citations, sources, data, quotes, or research.
- Users should not use this as sole authority for medical, legal, financial, or safety-critical decisions.
- Prompts ask for concise reasoning rather than hidden chain-of-thought.

## Future Improvements

Possible later prompt and workflow improvements include:

- Third-model judging
- Optional web-grounded research mode
- Local model support
- Prompt versioning
- Confidence scoring
- Comparison across more than two reviewers
