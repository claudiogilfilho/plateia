export type PatternStage = "observation" | "hypothesis" | "supported_hypothesis" | "provisional" | "experimentally_validated" | "contradicted" | "inconclusive" | "archived";
export type PatternEvidenceRole = "support" | "counterexample" | "case_limit" | "context";

export type PatternEvidenceCandidate = {
  referenceId: string | number;
  creator: string;
  sourceIdentity?: string;
  role: PatternEvidenceRole;
  comparisonLevel: 1 | 2 | 3 | 4;
  requiredEvidenceObserved: boolean;
  confidence: "low" | "medium" | "high";
};

function unique(values: string[]) {
  return new Set(values.map(value => value.trim().toLocaleLowerCase("pt-BR")).filter(Boolean)).size;
}

export function isEligiblePatternEvidence(evidence: PatternEvidenceCandidate) {
  return (
    (evidence.role === "support" || evidence.role === "counterexample") &&
    evidence.comparisonLevel <= 2 &&
    evidence.requiredEvidenceObserved &&
    evidence.confidence !== "low"
  );
}

export function summarizePatternEvidence(evidence: PatternEvidenceCandidate[]) {
  const uniqueByReference = new Map<string, PatternEvidenceCandidate>();
  for (const item of evidence) uniqueByReference.set(String(item.referenceId), item);
  const items = Array.from(uniqueByReference.values());
  const supports = items.filter(item => item.role === "support" && isEligiblePatternEvidence(item));
  const counterexamples = items.filter(item => item.role === "counterexample" && isEligiblePatternEvidence(item));
  const caseLimits = items.filter(item => item.role === "case_limit");
  return {
    supports,
    counterexamples,
    caseLimits,
    supportingCount: supports.length,
    counterexampleCount: counterexamples.length,
    caseLimitCount: caseLimits.length,
    creatorDiversityCount: unique(supports.map(item => item.creator)),
    sourceDiversityCount: unique(supports.map(item => item.sourceIdentity || item.creator)),
  };
}

export function decidePatternStage(input: {
  supportingCount: number;
  counterexampleCount: number;
  supportingCreators: string[];
  supportingSources?: string[];
  existingStage?: string;
  hasHumanOrExperimentalValidation?: boolean;
}): { stage: PatternStage; creatorDiversityCount: number; sourceDiversityCount: number; eligibleForProvisional: boolean } {
  const creatorDiversityCount = unique(input.supportingCreators);
  const sourceDiversityCount = unique(input.supportingSources ?? input.supportingCreators);
  if ((input.existingStage === "experimentally_validated" || input.existingStage === "validated") && input.hasHumanOrExperimentalValidation) {
    return { stage: "experimentally_validated", creatorDiversityCount, sourceDiversityCount, eligibleForProvisional: true };
  }
  if (input.counterexampleCount >= input.supportingCount && input.counterexampleCount >= 2) {
    return { stage: "contradicted", creatorDiversityCount, sourceDiversityCount, eligibleForProvisional: false };
  }
  const eligibleForProvisional = input.supportingCount >= 3 && creatorDiversityCount >= 2 && sourceDiversityCount >= 2;
  if (eligibleForProvisional) return { stage: "provisional", creatorDiversityCount, sourceDiversityCount, eligibleForProvisional };
  if (input.supportingCount >= 2) return { stage: "supported_hypothesis", creatorDiversityCount, sourceDiversityCount, eligibleForProvisional };
  if (input.supportingCount === 1) return { stage: "observation", creatorDiversityCount, sourceDiversityCount, eligibleForProvisional };
  return { stage: input.counterexampleCount ? "inconclusive" : "hypothesis", creatorDiversityCount, sourceDiversityCount, eligibleForProvisional };
}

export function decidePatternStageFromEvidence(input: {
  evidence: PatternEvidenceCandidate[];
  existingStage?: string;
  hasHumanOrExperimentalValidation?: boolean;
}) {
  const summary = summarizePatternEvidence(input.evidence);
  return {
    ...summary,
    ...decidePatternStage({
      supportingCount: summary.supportingCount,
      counterexampleCount: summary.counterexampleCount,
      supportingCreators: summary.supports.map(item => item.creator),
      supportingSources: summary.supports.map(item => item.sourceIdentity || item.creator),
      existingStage: input.existingStage,
      hasHumanOrExperimentalValidation: input.hasHumanOrExperimentalValidation,
    }),
  };
}
