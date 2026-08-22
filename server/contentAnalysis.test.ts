import { afterEach, describe, expect, it, vi } from "vitest";
import { builtInEvaluationProvider, setEvaluationProvider } from "./aiProvider";
import { applyVisualOnlyScope, CONSUMERS, CRITERIA, evaluateContent, normalizeAnalysis, parseStructuredEvaluation, recalculateSynthesisScores, validateAnalysisShape } from "./contentAnalysis";
import { createAnalysisInputSchema } from "./analysisRouter";
import { isAllowedPublicHttpsUrl, isInstagramPublicationUrl, resolveInstagramMaterial } from "./publicLinks";

const criteria = Object.fromEntries(CRITERIA.map(key => [key, 70])) as Record<(typeof CRITERIA)[number], number>;

afterEach(() => setEvaluationProvider(builtInEvaluationProvider));

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
    expect(result.consumers[0].overallScore).toBe(61);
    expect(result.consumers[0].criteria.gancho).toBe(0);
    expect(result.synthesis.overallScore).toBe(68);
    expect(result.synthesis.weightedAverage).toBe(68);
    expect(result.synthesis.divergence).toBe(9);
  });

  it("recalculates the synthesis instead of trusting inconsistent summary scores returned by the model", () => {
    const result = recalculateSynthesisScores({
      consumers: CONSUMERS.map((name, index) => ({ name, overallScore: 1, reaction: "Reação objetiva.", criteria: { ...criteria, gancho: 40 + index * 10 }, mainObjection: "Sem objeção crítica." })),
      synthesis: { overallScore: 99, weightedAverage: 0, divergence: 100, strengths: ["Mensagem clara.", "Chamada visível."], risks: ["Prova limitada.", "Ritmo lento."], recommendations: ["Melhorar o gancho.", "Adicionar prova.", "Reduzir texto."] },
    });

    expect(result.consumers.map(consumer => consumer.overallScore)).toEqual([66, 68, 69, 70, 71]);
    expect(result.synthesis).toMatchObject({ overallScore: 69, weightedAverage: 69, divergence: 5 });
  });

  it("recalculates the consolidated score with visual criteria only", () => {
    const scoped = applyVisualOnlyScope({
      consumers: CONSUMERS.map((name, index) => ({ name, overallScore: 0, reaction: "Reação objetiva.", criteria: { gancho: 60 + index, clareza: 10, relevância: 70 + index, desejo: 80 + index, confiança: 90 + index, retenção: 50 + index, ação: 20, objeções: 30 }, mainObjection: "Sem objeção crítica." })),
      synthesis: { overallScore: 0, weightedAverage: 0, divergence: 0, strengths: ["Mensagem clara.", "Boa estética."], risks: ["Prova limitada.", "Ritmo lento."], recommendations: ["Melhorar gancho.", "Adicionar prova.", "Reduzir texto."] },
    });
    expect(scoped.consumers[0].overallScore).toBe(70);
    expect(scoped.synthesis.overallScore).toBe(72);
    expect(scoped.synthesis.weightedAverage).toBe(72);
    expect(scoped.synthesis.divergence).toBe(4);
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
    expect(material).toEqual({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", videoUrl: null, coverImageUrl: "https://cdn.instagram.example/preview.jpg", caption: "Legenda pública" });
    fetchMock.mockRestore();
  });

  it("captures a public caption even when Instagram does not expose a preview image", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response('<meta name="twitter:description" content="Legenda captada automaticamente">', { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/C1Example/");
    expect(material).toEqual({ mediaUrl: null, mediaMimeType: null, videoUrl: null, coverImageUrl: null, caption: "Legenda captada automaticamente" });
    fetchMock.mockRestore();
  });

  it("uses structured public metadata as a caption fallback", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response('<script type="application/ld+json">{"caption":"Legenda vinda do JSON-LD"}</script>', { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/C1Example/");
    expect(material).toEqual({ mediaUrl: null, mediaMimeType: null, videoUrl: null, coverImageUrl: null, caption: "Legenda vinda do JSON-LD" });
    fetchMock.mockRestore();
  });

  it("extracts video and caption from current structured Instagram embed data", async () => {
    const html = '<script>window.__data={"shortcode_media":{"video_url":"https://cdn.instagram.example/reel.mp4","thumbnail_src":"https://cdn.instagram.example/cover.jpg","edge_media_to_caption":{"edges":[{"node":{"text":"Legenda estruturada do Reel"}}]}}}</script>';
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(html, { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/DcGe0hCTe8l/");
    expect(material).toEqual({ mediaUrl: "https://cdn.instagram.example/reel.mp4", mediaMimeType: "video/mp4", videoUrl: "https://cdn.instagram.example/reel.mp4", coverImageUrl: "https://cdn.instagram.example/cover.jpg", caption: "Legenda estruturada do Reel" });
    fetchMock.mockRestore();
  });

  it("decodes shortcode media nested in the escaped contextJSON used by current embeds", async () => {
    const html = '<script>"contextJSON":"{\\"gql_data\\":{\\"shortcode_media\\":{\\"video_url\\":\\"https://cdn.instagram.example/context.mp4\\",\\"edge_media_to_caption\\":{\\"edges\\":[{\\"node\\":{\\"text\\":\\"Legenda do contextJSON\\"}}]}}}}"</script>';
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(html, { status: 200 }));
    const material = await resolveInstagramMaterial("https://www.instagram.com/reel/DcGe0hCTe8l/");
    expect(material).toEqual({ mediaUrl: "https://cdn.instagram.example/context.mp4", mediaMimeType: "video/mp4", videoUrl: "https://cdn.instagram.example/context.mp4", coverImageUrl: null, caption: "Legenda do contextJSON" });
    fetchMock.mockRestore();
  });

  it("normalizes the plural /reels/ public URL before requesting the Instagram embed", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response('<meta property="og:description" content="Legenda de Reel">', { status: 200 }));
    await resolveInstagramMaterial("https://www.instagram.com/reels/C1Example/");
    expect(fetchMock.mock.calls[0]?.[0]).toBe("https://www.instagram.com/reel/C1Example/embed/captioned/");
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

  it("instructs the provider not to recommend fabricated proof or numeric social proof", async () => {
    let prompt = "";
    setEvaluationProvider({ evaluate: async request => {
      prompt = request.prompt;
      return JSON.stringify({ consumers: CONSUMERS.map(name => ({ name, overallScore: 70, reaction: "Reação objetiva.", criteria, mainObjection: "Sem objeção crítica." })), synthesis: { overallScore: 70, weightedAverage: 70, divergence: 0, strengths: ["Mensagem clara.", "Ação visível."], risks: ["Prova limitada.", "Ritmo lento."], recommendations: ["Melhorar o gancho.", "Adicionar prova real.", "Reduzir texto."] } });
    } });

    await evaluateContent({ contentType: "copy", text: "Uma copy para teste.", product: "Produto", objective: "Conversão", targetAudience: "Público", analysisScope: "standard" });
    expect(prompt).toContain("nunca sugira inserir números, avaliações, depoimentos ou selos inexistentes");
  });

  it("replaces unverified proof, testimonial and numeric recommendations before persistence", () => {
    const result = normalizeAnalysis({
      consumers: CONSUMERS.map(name => ({ name, overallScore: 70, reaction: "Reação objetiva.", criteria, mainObjection: "Sem objeção crítica." })),
      synthesis: { overallScore: 70, weightedAverage: 70, divergence: 0, strengths: ["Mensagem clara.", "Ação visível."], risks: ["Prova limitada.", "Ritmo lento."], recommendations: ["Junte-se a mais de 5.000 clientes.", "Inclua um depoimento de cliente.", "Adicione um selo de excelência."] },
    });
    expect(result.synthesis.recommendations).toEqual([
      "Torne o benefício principal mais específico e visível nos primeiros segundos.",
      "Apresente somente evidências reais e verificáveis que a marca já possua, como demonstração, processo ou informação de produto.",
      "Conclua com uma chamada para ação simples e coerente com o objetivo da publicação.",
    ]);
  });
});
