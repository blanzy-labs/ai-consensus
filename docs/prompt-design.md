# Prompt Design

Prompt templates live in `backend/app/llm/prompts.py`.

## Primary Answer

The primary prompt asks the model to answer the user's question clearly, state assumptions, avoid unsupported certainty, and mention uncertainty where relevant.

## Reviewer Critique

The reviewer prompt includes the original question and primary answer. It asks for an objective critique that identifies strengths, weak claims, missing context, and uncertainty without arguing just to argue or rewriting the whole answer unnecessarily.

## Final Synthesis

The synthesis prompt includes the original question, primary answer, and reviewer critique. It asks for JSON only with:

- `final_answer`
- `agreement_points`
- `disagreement_points`
- `uncertainties`
- `follow_up_questions`

JSON is requested so the backend can return a stable structured response to clients. Because LLMs can still return malformed output, the backend includes an invalid JSON fallback: it keeps the raw synthesizer output as the final answer and adds an uncertainty explaining that structured JSON was not returned.
