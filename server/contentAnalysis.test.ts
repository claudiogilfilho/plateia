import { describe, expect, it } from "vitest";
import { CONSUMERS, CRITERIA, normalizeAnalysis, validateAnalysisShape } from "./contentAnalysis";
import { isAllowedPublicHttpsUrl } from "./publicLinks";

const criteria = Object.fromEntries(CRITERIA.map(key => [key, 70])) as Record<(typeof CRITERIA)[number], number>;

describe("validateAnalysisShape", () => {
  it("accepts the five required consumers and exactly three recommendations", () => {
    const result = validateAnalysisShape({
      consumers: CONSUMERS.map(name => ({ name, overallScore: 70, reaction: "Reação objetiva.", criteria, mainObjection: "Sem objeção crítica." })),
      synthesis: {
        overallScore: 70,
        weightedAverage: 70,
        divergence: 12,
        strengths: ["Mensagem clara.", "Chamada visível."],
        risks: ["Prova limitada.", "Gancho pouco específico."],
        recommendations: ["Melhorar o gancho.", "Adicionar prova.", "Reduzir texto."],
      },
    });

    expect(result.consumers).toHaveLength(5);
    expect(result.synthesis.recommendations).toHaveLength(3);
  });

  it("rejects a synthesis that does not have exactly three recommendations", () => {
    expect(() => validateAnalysisShape({
      consumers: CONSUMERS.map(name => ({ name, overallScore: 70, reaction: "Reação objetiva.", criteria, mainObjection: "Sem objeção crítica." })),
      synthesis: {
        overallScore: 70,
        weightedAverage: 70,
        divergence: 12,
        strengths: ["Mensagem clara.", "Chamada visível."],
        risks: ["Prova limitada.", "Gancho pouco específico."],
        recommendations: ["Melhorar o gancho.", "Adicionar prova."] as unknown as [string, string, string],
      },
    })).toThrow("exatamente três recomendações");
  });

  it("normalizes scores to the 0–100 interval and preserves the required order", () => {
    const result = normalizeAnalysis({
      consumers: CONSUMERS.map((name, index) => ({ name, overallScore: index === 0 ? 110 : 72, reaction: "Reação objetiva.", criteria: { ...criteria, gancho: index === 0 ? -10 : 70 }, mainObjection: "Sem objeção crítica." })),
      synthesis: { overallScore: 105, weightedAverage: 71.4, divergence: -4, strengths: ["Clareza inicial.", "Ação visível."], risks: ["Prova limitada.", "Ritmo lento."], recommendations: ["Melhorar o gancho.", "Adicionar prova.", "Reduzir texto."] },
    });

    expect(result.consumers[0].name).toBe("O Apressado");
    expect(result.consumers[0].overallScore).toBe(100);
    expect(result.consumers[0].criteria.gancho).toBe(0);
    expect(result.synthesis.overallScore).toBe(100);
    expect(result.synthesis.divergence).toBe(0);
  });

  it("rejects a response when one required consumer is missing", () => {
    expect(() => normalizeAnalysis({
      consumers: CONSUMERS.slice(0, 4).map(name => ({ name, overallScore: 70, reaction: "Reação objetiva.", criteria, mainObjection: "Sem objeção crítica." })),
      synthesis: { overallScore: 70, weightedAverage: 70, divergence: 12, strengths: ["Clareza inicial.", "Ação visível."], risks: ["Prova limitada.", "Ritmo lento."], recommendations: ["Melhorar o gancho.", "Adicionar prova.", "Reduzir texto."] },
    })).toThrow("cinco consumidores");
  });

  it("only accepts public HTTPS links as remote content sources", () => {
    expect(isAllowedPublicHttpsUrl("https://cdn.exemplo.com/video.mp4")).toBe(true);
    expect(isAllowedPublicHttpsUrl("http://cdn.exemplo.com/video.mp4")).toBe(false);
    expect(isAllowedPublicHttpsUrl("https://localhost:3000/video.mp4")).toBe(false);
    expect(isAllowedPublicHttpsUrl("https://192.168.1.10/video.mp4")).toBe(false);
  });
});
