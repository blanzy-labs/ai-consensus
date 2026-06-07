import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, test, vi } from "vitest";

import App from "./App";
import { checkHealth, runConsensus } from "./api/client";
import type { ConsensusResponse } from "./types/consensus";
import { downloadMarkdown } from "./utils/markdownExport";

vi.mock("./api/client", () => ({
  checkHealth: vi.fn(),
  runConsensus: vi.fn(),
}));

vi.mock("./utils/markdownExport", async () => {
  const actual = await vi.importActual<typeof import("./utils/markdownExport")>(
    "./utils/markdownExport",
  );

  return {
    ...actual,
    downloadMarkdown: vi.fn(),
  };
});

const mockedCheckHealth = vi.mocked(checkHealth);
const mockedRunConsensus = vi.mocked(runConsensus);
const mockedDownloadMarkdown = vi.mocked(downloadMarkdown);

const successfulResponse: ConsensusResponse = {
  question: "What are the risks of relying on one AI answer?",
  primary_answer: "Primary answer",
  reviewer_critique: "Reviewer critique",
  final_answer: "Final answer",
  agreement_points: ["Agreement"],
  disagreement_points: ["Disagreement"],
  uncertainties: ["Uncertainty"],
  follow_up_questions: ["Follow up?"],
  models_used: {
    primary: "gpt-test",
    reviewer: "gemini-test",
    synthesizer: "gpt-test",
  },
};

describe("App", () => {
  afterEach(() => {
    cleanup();
  });

  beforeEach(() => {
    mockedCheckHealth.mockResolvedValue({
      status: "ok",
      service: "mythadis-consensus-engine-backend",
    });
    mockedRunConsensus.mockReset();
    mockedDownloadMarkdown.mockReset();
  });

  test("renders title and tagline", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: "Mythadis Consensus Engine" })).toBeInTheDocument();
    expect(screen.getByText("The books are fiction. The questions are real.")).toBeInTheDocument();
  });

  test("rejects an empty question", () => {
    render(<App />);

    fireEvent.click(screen.getByRole("button", { name: "Run consensus" }));

    expect(screen.getByText("Question is required.")).toBeInTheDocument();
    expect(mockedRunConsensus).not.toHaveBeenCalled();
  });

  test("shows provider selector defaults", () => {
    render(<App />);

    expect(screen.getByLabelText("Primary responder")).toHaveValue("openai");
    expect(screen.getByLabelText("Reviewer")).toHaveValue("gemini");
    expect(screen.getByLabelText("Synthesizer")).toHaveValue("openai");
  });

  test("shows loading state after submit", async () => {
    mockedRunConsensus.mockImplementation(() => new Promise(() => undefined));
    render(<App />);

    fireEvent.change(screen.getByLabelText("Question"), {
      target: { value: "What should I compare?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Run consensus" }));

    expect(await screen.findByText("Running consensus workflow...")).toBeInTheDocument();
    expect(screen.getByText("Generating primary answer")).toBeInTheDocument();
    expect(mockedRunConsensus).toHaveBeenCalledWith({
      question: "What should I compare?",
      primary_provider: "openai",
      reviewer_provider: "gemini",
      synthesizer_provider: "openai",
    });
  });

  test("renders successful consensus result", async () => {
    mockedRunConsensus.mockResolvedValue(successfulResponse);
    render(<App />);

    fireEvent.change(screen.getByLabelText("Question"), {
      target: { value: "What are the risks of relying on one AI answer?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Run consensus" }));

    expect(await screen.findByText("Final answer")).toBeInTheDocument();
    expect(screen.getByText("Agreement")).toBeInTheDocument();
    expect(screen.getByText("Disagreement")).toBeInTheDocument();
    expect(screen.getByText("Uncertainty")).toBeInTheDocument();
    expect(screen.getByText("Follow up?")).toBeInTheDocument();
    expect(screen.getByText("Primary answer")).toBeInTheDocument();
    expect(screen.getByText("Reviewer critique")).toBeInTheDocument();
    expect(screen.getAllByText("gpt-test")).toHaveLength(2);
    expect(screen.getByRole("button", { name: "Export Markdown" })).toBeInTheDocument();
  });

  test("does not show export button before a result exists", () => {
    render(<App />);

    expect(screen.queryByRole("button", { name: "Export Markdown" })).not.toBeInTheDocument();
  });

  test("clicking export downloads markdown after a result exists", async () => {
    mockedRunConsensus.mockResolvedValue(successfulResponse);
    render(<App />);

    fireEvent.change(screen.getByLabelText("Question"), {
      target: { value: "What are the risks of relying on one AI answer?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Run consensus" }));

    fireEvent.click(await screen.findByRole("button", { name: "Export Markdown" }));

    expect(mockedDownloadMarkdown).toHaveBeenCalledTimes(1);
    expect(mockedDownloadMarkdown.mock.calls[0][0]).toMatch(
      /^mythadis-consensus-report-\d{8}-\d{6}\.md$/,
    );
    expect(mockedDownloadMarkdown.mock.calls[0][1]).toContain("# Mythadis Consensus Report");
  });

  test("renders backend error message", async () => {
    mockedRunConsensus.mockRejectedValue(
      new Error("OpenAI API key is not configured. Set the backend key in your .env file."),
    );
    render(<App />);

    fireEvent.change(screen.getByLabelText("Question"), {
      target: { value: "What should I compare?" },
    });
    fireEvent.click(screen.getByRole("button", { name: "Run consensus" }));

    await waitFor(() => {
      expect(screen.getByRole("alert")).toHaveTextContent(
        "OpenAI API key is not configured. Set the backend key in your .env file.",
      );
    });
  });
});
