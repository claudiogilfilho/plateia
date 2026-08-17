import { describe, expect, it, vi } from "vitest";
import { CONSUMERS, CRITERIA, normalizeAnalysis, parseStructuredEvaluation, validateAnalysisShape } from "./contentAnalysis";
import { createAnalysisInputSchema } from "./analysisRouter";
import { isAllowedPublicHttpsUrl, isInstagramPublicationUrl, resolveInstagramMaterial } from "./publicLinks";

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

  it("recognizes public Instagram post and Reel links", () => {
    expect(isInstagramPublicationUrl("https://www.instagram.com/reel/C1Example/")) .toBe(true);
    expect(isInstagramPublicationUrl("https://instagram.com/p/C1Example/?utm_source=x")) .toBe(true);
    expect(isInstagramPublicationUrl("https://www.instagram.com/explore/")) .toBe(false);
  });

  it("extracts the public preview image and caption from an Instagram embed", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response('<meta property="og:image" content="https://cdn.instagram.example/preview.jpg"><meta property="og:description" content="Legenda pública">', { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/C1Example/");
    expect(material).toEqual({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: "Legenda pública" });
    fetchMock.mockRestore();
  });

  it("captures a public caption even when Instagram does not expose a preview image", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response('<meta name="twitter:description" content="Legenda captada automaticamente">', { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/C1Example/");
    expect(material).toEqual({ mediaUrl: null, mediaMimeType: null, caption: "Legenda captada automaticamente" });
    fetchMock.mockRestore();
  });

  it("uses structured public metadata as a caption fallback", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response('<script type="application/ld+json">{"caption":"Legenda vinda do JSON-LD"}</script>', { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/C1Example/");
    expect(material).toEqual({ mediaUrl: null, mediaMimeType: null, caption: "Legenda vinda do JSON-LD" });
    fetchMock.mockRestore();
  });

  it("accepts the minimum required material for copy, uploaded visual content and public Instagram links", () => {
    const shared = { product: "", objective: "", targetAudience: "" };
    expect(createAnalysisInputSchema.safeParse({ ...shared, contentType: "copy", contentText: "Uma copy curta para avaliar." }).success).toBe(true);
    expect(createAnalysisInputSchema.safeParse({ ...shared, contentType: "post", contentText: "", media: { fileName: "post.png", mimeType: "image/png", base64: "a".repeat(20) } }).success).toBe(true);
    expect(createAnalysisInputSchema.safeParse({ ...shared, contentType: "reel", contentText: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } }).success).toBe(true);
    expect(createAnalysisInputSchema.safeParse({ ...shared, contentType: "post", contentText: "" }).success).toBe(false);
    expect(createAnalysisInputSchema.safeParse({ ...shared, contentType: "copy", contentText: "" }).success).toBe(false);
  });

  it("parses JSON returned inside an optional code fence", () => {
    expect(parseStructuredEvaluation("```json\n{\"ok\":true}\n```")) .toEqual({ ok: true });
    expect(() => parseStructuredEvaluation('{"ok":')).toThrow("incompleta");
  });
});
