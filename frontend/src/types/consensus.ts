export type HealthStatus = {
  status: string;
  service: string;
};

export type ProviderName = "openai" | "gemini";

export type ConsensusRequest = {
  question: string;
  primary_provider: ProviderName;
  reviewer_provider: ProviderName;
  synthesizer_provider: ProviderName;
};

export type ModelsUsed = {
  primary: string;
  reviewer: string;
  synthesizer: string;
};

export type ConsensusResponse = {
  question: string;
  primary_answer: string;
  reviewer_critique: string;
  final_answer: string;
  agreement_points: string[];
  disagreement_points: string[];
  uncertainties: string[];
  follow_up_questions: string[];
  models_used: ModelsUsed;
};

export type ApiError = {
  detail?: string;
};
