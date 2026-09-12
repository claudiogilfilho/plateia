import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { DecisionReportView, isDecisionReport } from "./DecisionReportView";

vi.mock("wouter", () => ({ Link: ({ href, children, ...props }: React.PropsWithChildren<{ href: string }>) => React.createElement("a", { href, ...props }, children) }));

const score = { score: 73, justification: "Sinal estrutural observado.", evidence: ["mudança aos 2 s"], confidence: "medium" };
const report = {
  decisionSystemVersion: "1.0", operationalVerdict: "publish_after_adjustments",
  coverage: { level: "complete", title: "Leitura completa", description: "Vídeo integral disponível." },
  technicalTruth: { durationSeconds: { status: "measured", value: 9 }, resolution: { status: "measured", value: { width: 1080, height: 1920 } }, aspectRatio: { status: "measured", value: "9:16" }, framesPerSecond: { status: "measured", value: 30 }, videoCodec: { status: "measured", value: "h264" }, fileSizeBytes: { status: "measured", value: 1_000_000 }, audioPresent: { status: "measured", value: true }, volume: { status: "not_assessed" }, silenceIntervals: { status: "not_assessed" }, sceneChanges: { status: "measured", value: [2, 4] }, averageSceneDurationSeconds: { status: "measured", value: 3 }, cutsPerMinute: { status: "measured", value: 13.3 }, limitations: [] },
  blindAudit: { observedSummary: "Resumo cego.", attentionAndRetention: score, strengths: ["Gancho claro"], risks: ["Ritmo"], limitations: [], frozenSha256: "abc", criteria: ["gancho", "clareza", "relevância", "desejo", "confiança", "retenção", "ação", "objeções"].map(name => ({ name, ...score })), lenses: ["O Apressado", "O Analítico", "O Aspiracional", "O Influenciado pela Comunidade", "O Cético"].map(name => ({ name, probableReaction: "Reação", mainObjection: "Objeção", likelyAbandonmentMoment: "3 s", reasonToContinue: "Recompensa", likelyAction: "Continuar", confidence: "medium" })), timeline: ["0–1 segundo", "1–3 segundos", "3–8 segundos", "desenvolvimento", "preparação da recompensa", "recompensa", "CTA", "encerramento e loop"].map(stage => ({ stage, timeRange: "0–1s", observed: "Cena", probableFunction: "Gancho", newInformation: "Informação", reasonToContinue: "Curiosidade", estimatedAbandonmentRisk: "medium", probableRiskCause: "Pausa", confidence: "medium", specificCorrection: "Cortar", provenance: "ai_interpretation" })), priorities: [1, 2, 3].map(() => ({ timestampOrSection: "2s", observedProblem: "Pausa", probableMechanism: "Ritmo", exactChange: "Encurtar", component: "cut", intendedMetric: "tendência estrutural", confidence: "medium", humanValidationRequired: true })), hookVariations: [], alternativeCta: "", editingGuidance: "", onScreenTextSuggestion: "", cutSuggestions: [] },
  contextualAudit: { businessEffectiveness: score, plateiaVerdict: "passed", alignment: [], incompatibilities: [], inventedOrUnsupportedInformation: [], missingInformation: [], uncommunicatedDifferentiators: [], limitations: [], confidence: "medium" },
  dualReading: { attentionAndRetention: score, businessEffectiveness: score }, benchmark: { comparisonLevel: 4, comparableReferenceCount: 0, confidence: "low", limitation: "Sem par adequado." }, comparison: null,
};

describe("relatório do sistema de decisão", () => {
  it("reconhece o contrato novo e apresenta honestamente as duas notas e o risco temporal", () => {
    expect(isDecisionReport(report)).toBe(true);
    const html = renderToStaticMarkup(<DecisionReportView report={report as never} analysisId={12} title="Reel teste" context="Objetivo: consideração" />);
    expect(html).toContain("Potencial de atenção e retenção");
    expect(html).toContain("Efetividade para o negócio");
    expect(html).toContain("Linha do tempo de risco de retenção");
    expect(html).toContain("não é retenção real");
    expect(html).toContain("Exatamente três correções prioritárias");
    expect(html).toContain("Enviar versão corrigida");
  });
});
