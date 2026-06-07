def build_primary_prompt(question: str) -> str:
    return f"""Answer the user's question clearly and directly.

State any assumptions you are making. Avoid unsupported certainty, and mention uncertainty where it matters.

Question:
{question}
"""


def build_reviewer_prompt(question: str, primary_answer: str) -> str:
    return f"""Review the primary answer objectively.

Identify strengths, weak claims, missing context, and uncertainty. Do not argue just to argue, and do not rewrite the whole answer unless needed.

Original question:
{question}

Primary answer:
{primary_answer}
"""


def build_synthesis_prompt(question: str, primary_answer: str, reviewer_critique: str) -> str:
    return f"""Use the original question, primary answer, and reviewer critique to produce a balanced final result.

Return JSON only. Do not include Markdown fences, commentary, or text outside the JSON object.

The JSON object must match this shape:
{{
  "final_answer": "string",
  "agreement_points": ["string"],
  "disagreement_points": ["string"],
  "uncertainties": ["string"],
  "follow_up_questions": ["string"]
}}

Original question:
{question}

Primary answer:
{primary_answer}

Reviewer critique:
{reviewer_critique}
"""
