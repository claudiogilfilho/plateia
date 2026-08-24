export type PatternStage = "observation" | "hypothesis" | "supported_hypothesis" | "provisional" | "experimentally_validated" | "contradicted" | "inconclusive" | "archived";

export function decidePatternStage(input: {
  supportingCount: number;
  counterexampleCount: number;
  supportingCreators: string[];
  existingStage?: string;
}): { stage: PatternStage; creatorDiversityCount: number; eligibleForProvisional: boolean } {
  const creatorDiversityCount = new Set(input.supportingCreators.map(value => value.trim().toLocaleLowerCase("pt-BR")).filter(Boolean)).size;
  if (input.existingStage === "experimentally_validated" || input.existingStage === "validated") return { stage: "experimentally_validated", creatorDiversityCount, eligibleForProvisional: true };
  if (input.counterexampleCount >= input.supportingCount && input.counterexampleCount >= 2) return { stage: "contradicted", creatorDiversityCount, eligibleForProvisional: false };
  const eligibleForProvisional = input.supportingCount >= 3 && creatorDiversityCount >= 2;
  if (eligibleForProvisional) return { stage: "provisional", creatorDiversityCount, eligibleForProvisional };
  if (input.supportingCount >= 2) return { stage: "supported_hypothesis", creatorDiversityCount, eligibleForProvisional };
  return { stage: input.supportingCount === 1 ? "observation" : "hypothesis", creatorDiversityCount, eligibleForProvisional };
}
