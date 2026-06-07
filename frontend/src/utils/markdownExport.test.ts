import { describe, expect, test } from "vitest";

import type { ConsensusResponse } from "../types/consensus";
import { buildConsensusMarkdown, buildMarkdownFilename } from "./markdownExport";

const generatedAt = new Date(2026, 5, 7, 14, 5, 9);

const result: ConsensusResponse = {
  question: "What are the risks of relying on a single AI answer?",
  primary_answer: "Primary answer with\nline breaks.",
  reviewer_critique: "Reviewer critique",
  final_answer: "Final consensus answer",
  agreement_points: ["Use multiple sources", "Check assumptions"],
  disagreement_points: ["Level of risk varies"],
  uncertainties: ["Current facts may change"],
  follow_up_questions: ["Which claims need verification?"],
  models_used: {
    primary: "gpt-test",
    reviewer: "gemini-test",
    synthesizer: "gpt-test",
  },
};

describe("markdown export", () => {
  test("builds a complete consensus report", () => {
    const markdown = buildConsensusMarkdown(result, generatedAt);

    expect(markdown).toContain("# Mythadis Consensus Report");
    expect(markdown).toContain("Generated At:");
    expect(markdown).toContain("## Question");
    expect(markdown).toContain(result.question);
    expect(markdown).toContain("## Final Consensus Answer");
    expect(markdown).toContain(result.final_answer);
    expect(markdown).toContain("## Agreement Points");
    expect(markdown).toContain("- Use multiple sources");
    expect(markdown).toContain("## Disagreement Points");
    expect(markdown).toContain("- Level of risk varies");
    expect(markdown).toContain("## Uncertainties / Caveats");
    expect(markdown).toContain("- Current facts may change");
    expect(markdown).toContain("## Suggested Follow-Up Questions");
    expect(markdown).toContain("- Which claims need verification?");
    expect(markdown).toContain("## Primary Answer");
    expect(markdown).toContain("Primary answer with\nline breaks.");
    expect(markdown).toContain("## Reviewer Critique");
    expect(markdown).toContain("Reviewer critique");
    expect(markdown).toContain("Primary Provider/Model: gpt-test");
    expect(markdown).toContain("Reviewer Provider/Model: gemini-test");
    expect(markdown).toContain("Synthesizer Provider/Model: gpt-test");
    expect(markdown).toContain("Consensus does not guarantee truth.");
  });

  test("renders placeholders for empty arrays", () => {
    const markdown = buildConsensusMarkdown(
      {
        ...result,
        agreement_points: [],
        disagreement_points: [],
        uncertainties: [],
        follow_up_questions: [],
      },
      generatedAt,
    );

    expect(markdown).toContain("No agreement points returned.");
    expect(markdown).toContain("No disagreement points returned.");
    expect(markdown).toContain("No uncertainties returned.");
    expect(markdown).toContain("No follow-up questions returned.");
  });

  test("builds a safe timestamped filename", () => {
    expect(buildMarkdownFilename(generatedAt)).toBe(
      "mythadis-consensus-report-20260607-140509.md",
    );
  });

  test("does not add provider API key fields to exported markdown", () => {
    const markdown = buildConsensusMarkdown(result, generatedAt);
    const openAiKeyName = ["OPENAI", "API", "KEY"].join("_");
    const geminiKeyName = ["GEMINI", "API", "KEY"].join("_");

    expect(markdown).not.toContain(openAiKeyName);
    expect(markdown).not.toContain(geminiKeyName);
    expect(markdown).not.toContain("sk-test-secret");
  });
});
