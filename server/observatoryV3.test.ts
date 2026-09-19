import { describe, expect, it } from "vitest";
import { normalizeClassification, rankPortableReferences } from "./observatory";
import { decidePatternStage } from "./patternEvidence";
import { listPortableReferences, PORTABLE_MEMORY_STATS } from "./portableObservatoryMemory";
import { assessViralityEvidence, safeRate } from "./virality";
import { auditObservatoryMemory } from "./observatoryMemoryAudit";
import { auditConcentratedTrainingRun } from "./trainingBatchAudit";

describe("Observatório Platéia v3", () => {
  it("preserva o corpus treinado e mantém contagens e URLs consistentes", () => {
    const references = listPortableReferences();
    expect(PORTABLE_MEMORY_STATS.referenceCount).toBeGreaterThanOrEqual(35);
    expect(references).toHaveLength(PORTABLE_MEMORY_STATS.referenceCount);
    expect(new Set(references.map(reference => reference.sourceUrl.toLowerCase())).size).toBe(references.length);
  });

  it("audita a taxonomia bruta, cardinalidades e apoios dos padrões", () => {
    expect(auditObservatoryMemory()).toMatchObject({ issues: [], referenceCount: PORTABLE_MEMORY_STATS.referenceCount });
  });

  it("migra aliases legados sem transformar ambiguidade em certeza", () => {
    const result = normalizeClassification({ materialFormat: "short_vertical", presentationFormats: ["review", "explicativo"], primaryFamily: "educativo", objectives: ["entreter"], mechanisms: ["confiança"] });
    expect(result).toMatchObject({ taxonomyVersion: "3.0", materialFormat: "video_curto", presentationFormats: ["comentario", "outro"], objectives: ["visualizacao"], mechanisms: ["confianca"] });
    expect(result.advertisingType).toBe("indeterminado");
    expect(result.needsHumanReview).toBe(true);
  });

  it("recupera referências por semelhança funcional, não apenas por recipiente", () => {
    const target = normalizeClassification({ materialFormat: "reel", presentationFormats: ["camera_direta"], primaryFamily: "educativo", objectives: ["educar"], segment: "saúde", awarenessStage: "consciente_problema", mechanisms: ["curiosidade"] });
    const ranked = rankPortableReferences(target);
    expect(ranked.every(reference => reference.comparisonLevel < 4)).toBe(true);
    expect(ranked.every(reference => reference.primaryFamily === "educativo" || reference.similarity >= 25)).toBe(true);
  });

  it("não promove três apoios do mesmo criador a padrão provisório", () => {
    expect(decidePatternStage({ supportingCount: 3, counterexampleCount: 0, supportingCreators: ["A", "A", "A"] })).toMatchObject({ stage: "supported_hypothesis", eligibleForProvisional: false });
    expect(decidePatternStage({ supportingCount: 3, counterexampleCount: 0, supportingCreators: ["A", "B", "A"] })).toMatchObject({ stage: "provisional", eligibleForProvisional: true });
  });

  it("não preserva validação sem revisão humana ou experimento identificável", () => {
    expect(decidePatternStage({ supportingCount: 3, counterexampleCount: 0, supportingCreators: ["A", "B", "C"], existingStage: "experimentally_validated" }).stage).toBe("provisional");
    expect(decidePatternStage({ supportingCount: 3, counterexampleCount: 0, supportingCreators: ["A", "B", "C"], existingStage: "experimentally_validated", hasHumanOrExperimentalValidation: true }).stage).toBe("experimentally_validated");
  });

  it("rejeita lote disperso, sem caso-limite e com hipótese nova em excesso", () => {
    const issues = auditConcentratedTrainingRun({
      id: "bad", batchPolicyVersion: "1.1", requestedBatchSize: 5, candidatesFound: 5, analyzed: 5,
      referenceIds: [], targetKnowledgeId: "pattern", targetReferenceIds: ["a", "b"],
      falsificationOrBoundaryReferenceIds: [], controlledExplorationReferenceIds: [], hypothesesCreated: ["h1", "h2"],
    }, []);
    expect(issues).toEqual(expect.arrayContaining(["bad.candidatePoolMinimum", "bad.targetReferenceQuota", "bad.boundaryReferenceQuota", "bad.explorationReferenceQuota", "bad.newHypothesisLimit"]));
  });

  it("mantém viralidade indeterminada sem baseline e calcula somente taxas com denominador", () => {
    expect(safeRate(20, 1000)).toBe(0.02);
    expect(safeRate(20, 0)).toBeNull();
    expect(assessViralityEvidence({ viewsObserved: "3,1 mi" })).toMatchObject({ status: "indeterminate", causalClaimAllowed: false });
    expect(assessViralityEvidence({ views: 10000, shares: 300, creatorMedianViews: 1000, cohortMedianViews: 1500, observedAt: "2026-08-24", organicPaid: "organic" })).toMatchObject({ status: "high_shareability", causalClaimAllowed: false });
  });
});
