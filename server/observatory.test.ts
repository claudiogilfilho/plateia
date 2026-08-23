import { describe, expect, it } from "vitest";
import type { ObservatoryReference } from "../drizzle/schema";
import { comparisonLevel, normalizeClassification, rankComparableReferences, scoreClassificationSimilarity, type ObservatoryClassification } from "./observatory";
import { createObservatoryReferenceInputSchema } from "./observatoryRouter";

const target: ObservatoryClassification = {
  materialFormat: "reel",
  presentationFormats: ["camera_direta"],
  primaryFamily: "educativo",
  secondaryFamilies: ["autoridade_opiniao"],
  objectives: ["educar", "salvamento"],
  segment: "marketing",
  subsegment: "conteúdo",
  probableAudience: "criadores",
  awarenessStage: "consciente_problema",
  productionLevel: "simple",
  durationBand: "31_to_60s",
  pace: "moderate",
  mechanisms: ["curiosidade", "confiança"],
  confidence: "high",
  evidence: ["Explica um conceito em câmera direta."],
  alternativeClassifications: [],
  missingInformation: [],
  needsHumanReview: false,
};

function reference(id: number, title: string, classification: ObservatoryClassification): ObservatoryReference {
  return {
    id, createdByUserId: 1, title, creator: "@criador", contentType: "reel", sourceKind: "published_post",
    sourceUrl: "https://www.instagram.com/reel/exemplo/", contentText: "", mediaUrl: null, mediaKey: null,
    mediaMimeType: null, segmentHint: "", objectiveHint: "", metricsJson: null, status: "analyzed",
    classificationJson: JSON.stringify(classification),
    analysisJson: JSON.stringify({ learning: { replicable: ["Abra com uma pergunta específica."] } }),
    promptVersion: "2.0", createdAt: new Date(), updatedAt: new Date(),
  };
}

describe("Observatório Platéia", () => {
  it("normaliza a resposta do classificador e pede revisão quando faltam dados", () => {
    const result = normalizeClassification({ primaryFamily: "valor_inventado", presentationFormats: ["camera_direta", "inválido"] });
    expect(result.primaryFamily).toBe("hibrido");
    expect(result.presentationFormats).toEqual(["camera_direta"]);
    expect(result.segment).toBe("indeterminado");
    expect(result.needsHumanReview).toBe(true);
  });

  it("prioriza pares da mesma família, objetivo e segmento", () => {
    const close = { ...target };
    const mechanismOnly = { ...target, primaryFamily: "storytelling" as const, secondaryFamilies: [], objectives: ["comunidade" as const], segment: "saúde" };
    const unrelated = { ...target, primaryFamily: "oferta_direta" as const, secondaryFamilies: [], objectives: ["venda" as const], segment: "imóveis", mechanisms: ["urgencia" as const] };
    expect(comparisonLevel(target, close, scoreClassificationSimilarity(target, close))).toBe(1);
    expect(comparisonLevel(target, mechanismOnly, scoreClassificationSimilarity(target, mechanismOnly))).toBe(3);
    const ranked = rankComparableReferences(target, [reference(3, "Sem relação", unrelated), reference(2, "Mesmo mecanismo", mechanismOnly), reference(1, "Par direto", close)]);
    expect(ranked.map(item => item.title)).toEqual(["Par direto", "Mesmo mecanismo"]);
    expect(ranked[0]).toMatchObject({ comparisonLevel: 1, learning: ["Abra com uma pergunta específica."] });
  });

  it("aceita copy isolada e exige fonte para material visual", () => {
    expect(createObservatoryReferenceInputSchema.safeParse({ contentType: "copy", contentText: "Copy exemplar" }).success).toBe(true);
    expect(createObservatoryReferenceInputSchema.safeParse({ contentType: "reel", contentText: "" }).success).toBe(false);
    expect(createObservatoryReferenceInputSchema.safeParse({ contentType: "reel", source: { url: "https://www.instagram.com/reel/exemplo/", kind: "published_post" } }).success).toBe(true);
  });
});
