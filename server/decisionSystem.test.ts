import { afterEach, describe, expect, it } from "vitest";
import { resetEvaluationProvider, setEvaluationProvider } from "./aiProvider";
import { CONSUMERS, CRITERIA } from "./contentAnalysis";
import { buildDecisionReport, compareDecisionReports, evaluateBlindDecision, evaluateContextualDecision, preparePostPublicationRecord, TEMPORAL_STAGES, validateBlindDecision, type BlindDecision, type ContextualDecision } from "./decisionSystem";
import { unavailableTechnicalTruth } from "./videoTechnicalAnalysis";

const score = { score: 72, justification: "Há evidência observável.", evidence: ["sinal observado"], confidence: "medium" as const };
const blind: BlindDecision = {
  observedSummary: "O vídeo apresenta uma promessa e uma demonstração.", attentionAndRetention: score,
  criteria: CRITERIA.map(name => ({ name, ...score })),
  lenses: CONSUMERS.map(name => ({ name, probableReaction: `Reação de ${name}`, mainObjection: "Objeção específica", likelyAbandonmentMoment: "3–8 segundos", reasonToContinue: "Nova informação", likelyAction: "Continuar", confidence: "medium" })),
  timeline: TEMPORAL_STAGES.map(stage => ({ stage, timeRange: stage, observed: "Sinal observado", probableFunction: "Progressão", newInformation: "Informação", reasonToContinue: "Recompensa", estimatedAbandonmentRisk: "medium", probableRiskCause: "Ritmo", confidence: "medium", specificCorrection: "Encurtar", provenance: "ai_interpretation" })),
  strengths: ["Promessa clara"], risks: ["Ritmo irregular"],
  priorities: [0, 1, 2].map(index => ({ timestampOrSection: `${index}s`, observedProblem: "Problema", probableMechanism: "Carga", exactChange: "Cortar um segundo", component: "cut", intendedMetric: "tendência estrutural de retenção", confidence: "medium", humanValidationRequired: true })) as BlindDecision["priorities"],
  hookVariations: ["Variação"], alternativeCta: "CTA", editingGuidance: "Montagem", onScreenTextSuggestion: "Texto", cutSuggestions: ["Corte"], limitations: [],
};
const contextual: ContextualDecision = {
  businessEffectiveness: score, plateiaVerdict: "passed", alignment: ["Alinhado"], incompatibilities: [], inventedOrUnsupportedInformation: [], missingInformation: [], uncommunicatedDifferentiators: [], limitations: [], confidence: "medium",
};

afterEach(() => resetEvaluationProvider());

describe("sistema de decisão do Platéia", () => {
  it("exige oito critérios, cinco lentes, oito etapas e exatamente três prioridades", () => {
    expect(validateBlindDecision(blind)).toBe(blind);
    expect(() => validateBlindDecision({ ...blind, priorities: blind.priorities.slice(0, 2) as never })).toThrow("exatamente três");
  });

  it("nunca converte informação ausente em nota zero", () => {
    const invalid = structuredClone(blind);
    invalid.criteria[0] = { ...invalid.criteria[0], score: 0, justification: "Informação ausente", evidence: [] };
    expect(() => validateBlindDecision(invalid)).toThrow("não pode receber zero");
  });

  it("envia mídia somente à leitura cega e congela o resultado antes do contexto", async () => {
    const requests: Array<{ mediaUrl?: string | null; prompt: string }> = [];
    setEvaluationProvider({ evaluate: async request => { requests.push(request); return JSON.stringify(requests.length === 1 ? blind : contextual); } });
    const technicalTruth = unavailableTechnicalTruth("remote_media");
    const blindResult = await evaluateBlindDecision({ contentType: "reel", text: "", mediaUrl: "https://cdn.example/video.mp4", mediaMimeType: "video/mp4", technicalTruth, observatoryContext: null });
    await evaluateContextualDecision({ blind: blindResult, technicalTruth, dossier: { businessName: "Negócio" } });
    expect(requests[0].mediaUrl).toContain("video.mp4");
    expect(requests[1].mediaUrl).toBeUndefined();
    expect(requests[1].prompt).toContain("NÃO recebe vídeo");
  });

  it("declara a limitação contextual quando o dossiê não foi fornecido", async () => {
    let capturedPrompt = "";
    setEvaluationProvider({ evaluate: async request => {
      capturedPrompt = request.prompt;
      return JSON.stringify({ ...contextual, businessEffectiveness: { ...score, score: null }, plateiaVerdict: "inconclusive", limitations: ["Dossiê não informado"], confidence: "low" });
    } });
    const result = await evaluateContextualDecision({ blind, technicalTruth: unavailableTechnicalTruth(), dossier: {} });
    expect(capturedPrompt).toContain("Campos úteis fornecidos: 0");
    expect(result).toMatchObject({ plateiaVerdict: "inconclusive", businessEffectiveness: { score: null }, confidence: "low" });
  });

  it("mantém duas notas separadas e compara versões sem chamar a diferença de retenção real", () => {
    const first = buildDecisionReport({ blind, contextual, technicalTruth: unavailableTechnicalTruth(), coverage: {}, observatory: null });
    const improvedBlind = { ...blind, attentionAndRetention: { ...score, score: 80 }, risks: [] };
    const current = buildDecisionReport({ blind: improvedBlind, contextual, technicalTruth: unavailableTechnicalTruth(), coverage: {}, observatory: null });
    const comparison = compareDecisionReports(10, first, current);
    expect(comparison.recommendedVersion).toBe("current");
    expect(comparison.resolvedProblems).toContain("Ritmo irregular");
    expect(comparison.scoreChanges[0].reason).toContain("não é retenção real");
  });

  it("prepara métricas posteriores sem validar hipótese nem escrever no Observatório", () => {
    expect(preparePostPublicationRecord({ analysisId: 10, videoVersionId: "video-v2", videoSha256: "abc", correctionsApplied: ["hook"], publicationId: "post-1", metrics: { platform: "Instagram", publishedAt: "2026-09-02T12:00:00Z", distribution: "organic", views: 100 } })).toMatchObject({ analysisId: 10, videoVersionId: "video-v2", validatesHypothesisAutomatically: false, observatoryWriteAllowed: false });
  });
});
