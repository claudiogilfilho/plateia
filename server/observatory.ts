import type { ObservatoryReference } from "../drizzle/schema";
import { evaluateWithProvider } from "./aiProvider";
import { listActiveObservatoryPatterns, listAnalyzedObservatoryReferences } from "./db";
import { buildClassificationPrompt, buildObservatoryCuratorPrompt } from "./observatoryPrompt";

export const MATERIAL_FORMATS = ["video_curto", "video_longo", "reel", "corte", "arte_estatica", "fotografia", "carrossel", "copy", "hibrido", "outro"] as const;
export const PRESENTATION_FORMATS = ["camera_direta", "podcast_entrevista", "dialogo", "dramatizacao", "esquete", "reacao", "comentario", "narracao_imagens", "demonstracao", "tutorial", "transformacao", "bastidores", "depoimento", "estudo_caso", "reportagem", "animacao", "tela_gravada", "montagem", "trend", "meme", "ugc", "produto", "institucional", "manifesto", "outro"] as const;
export const CREATIVE_FAMILIES = ["educativo", "explicativo", "autoridade_opiniao", "noticia_atualidade", "storytelling", "entretenimento", "humor", "curiosidade", "demonstracao", "transformacao", "inspiracao", "identificacao", "comunidade", "polemica", "conscientizacao", "oferta_direta", "venda_indireta", "prova_estudo_caso", "depoimento", "institucional", "posicionamento_marca", "comparacao", "reacao", "hibrido"] as const;
export const OBJECTIVES = ["interromper_rolagem", "alcance", "visualizacao", "retencao", "educar", "consciencia_problema", "apresentar_solucao", "autoridade", "confianca", "identificacao", "compartilhamento", "salvamento", "comentario", "comunidade", "seguidores", "lead", "conversa", "venda", "trafego", "marca", "outro"] as const;
export const AWARENESS_STAGES = ["inconsciente", "consciente_problema", "consciente_solucao", "consciente_produto", "preparado_agir", "indeterminado"] as const;
export const MECHANISMS = ["curiosidade", "surpresa", "aproximacao", "desejo", "aversao_perda", "medo", "indignacao", "humor", "admiracao", "identificacao", "pertencimento", "confianca", "vigilancia", "urgencia", "alivio", "recompensa"] as const;

export type ObservatoryMaterialInput = {
  contentType: "post" | "carrossel" | "reel" | "copy";
  text: string;
  segmentHint: string;
  objectiveHint: string;
  sourceUrl?: string | null;
  mediaUrl?: string | null;
  mediaMimeType?: string | null;
  metrics?: Record<string, number | string | null> | null;
};

export type ObservatoryClassification = {
  materialFormat: (typeof MATERIAL_FORMATS)[number];
  presentationFormats: (typeof PRESENTATION_FORMATS)[number][];
  primaryFamily: (typeof CREATIVE_FAMILIES)[number];
  secondaryFamilies: (typeof CREATIVE_FAMILIES)[number][];
  objectives: (typeof OBJECTIVES)[number][];
  segment: string;
  subsegment: string;
  probableAudience: string;
  awarenessStage: (typeof AWARENESS_STAGES)[number];
  productionLevel: "simple" | "intermediate" | "complex" | "unknown";
  durationBand: "up_to_15s" | "16_to_30s" | "31_to_60s" | "over_60s" | "not_applicable" | "unknown";
  pace: "slow" | "moderate" | "fast" | "not_applicable" | "unknown";
  mechanisms: (typeof MECHANISMS)[number][];
  confidence: "low" | "medium" | "high";
  evidence: string[];
  alternativeClassifications: string[];
  missingInformation: string[];
  needsHumanReview: boolean;
};

export type ComparableReferenceSummary = {
  id: number;
  title: string;
  creator: string;
  similarity: number;
  comparisonLevel: 1 | 2 | 3 | 4;
  primaryFamily: string;
  segment: string;
  learning: string[];
};

export type ObservatoryContext = {
  promptVersion: "2.0";
  classification: ObservatoryClassification;
  comparisons: ComparableReferenceSummary[];
  patterns: Array<{ id: number; name: string; stage: "provisional" | "validated"; supportingCount: number; counterexampleCount: number; confidence: "low" | "medium" | "high"; mechanism: string }>;
  comparisonLevel: 1 | 2 | 3 | 4;
  benchmarkConfidence: "low" | "medium" | "high";
};

const classificationSchema = {
  type: "json_schema",
  json_schema: {
    name: "plateia_observatory_classification",
    strict: true,
    schema: {
      type: "object",
      properties: {
        materialFormat: { type: "string", enum: [...MATERIAL_FORMATS] },
        presentationFormats: { type: "array", minItems: 1, maxItems: 3, items: { type: "string", enum: [...PRESENTATION_FORMATS] } },
        primaryFamily: { type: "string", enum: [...CREATIVE_FAMILIES] },
        secondaryFamilies: { type: "array", maxItems: 2, items: { type: "string", enum: [...CREATIVE_FAMILIES] } },
        objectives: { type: "array", minItems: 1, maxItems: 4, items: { type: "string", enum: [...OBJECTIVES] } },
        segment: { type: "string" },
        subsegment: { type: "string" },
        probableAudience: { type: "string" },
        awarenessStage: { type: "string", enum: [...AWARENESS_STAGES] },
        productionLevel: { type: "string", enum: ["simple", "intermediate", "complex", "unknown"] },
        durationBand: { type: "string", enum: ["up_to_15s", "16_to_30s", "31_to_60s", "over_60s", "not_applicable", "unknown"] },
        pace: { type: "string", enum: ["slow", "moderate", "fast", "not_applicable", "unknown"] },
        mechanisms: { type: "array", maxItems: 6, items: { type: "string", enum: [...MECHANISMS] } },
        confidence: { type: "string", enum: ["low", "medium", "high"] },
        evidence: { type: "array", maxItems: 8, items: { type: "string" } },
        alternativeClassifications: { type: "array", maxItems: 4, items: { type: "string" } },
        missingInformation: { type: "array", maxItems: 8, items: { type: "string" } },
        needsHumanReview: { type: "boolean" },
      },
      required: ["materialFormat", "presentationFormats", "primaryFamily", "secondaryFamilies", "objectives", "segment", "subsegment", "probableAudience", "awarenessStage", "productionLevel", "durationBand", "pace", "mechanisms", "confidence", "evidence", "alternativeClassifications", "missingInformation", "needsHumanReview"],
      additionalProperties: false,
    },
  },
} as const;

const criterionSchema = {
  type: "object",
  properties: {
    assessed: { type: "boolean" },
    score: { type: "integer", minimum: 0, maximum: 100 },
    justification: { type: "string" },
    evidence: { type: "string" },
    confidence: { type: "string", enum: ["low", "medium", "high"] },
  },
  required: ["assessed", "score", "justification", "evidence", "confidence"],
  additionalProperties: false,
} as const;

const curatorSchema = {
  type: "json_schema",
  json_schema: {
    name: "plateia_observatory_reference",
    strict: true,
    schema: {
      type: "object",
      properties: {
        access: { type: "object", properties: { completeness: { type: "string", enum: ["complete", "partial", "insufficient"] }, dataQuality: { type: "string", enum: ["low", "medium", "high"] }, accessibleElements: { type: "array", items: { type: "string" } }, missingElements: { type: "array", items: { type: "string" } }, limitations: { type: "array", items: { type: "string" } } }, required: ["completeness", "dataQuality", "accessibleElements", "missingElements", "limitations"], additionalProperties: false },
        timeline: { type: "array", maxItems: 12, items: { type: "object", properties: { segment: { type: "string" }, observation: { type: "string" }, function: { type: "string" }, attentionRisk: { type: "string" }, continuationReason: { type: "string" } }, required: ["segment", "observation", "function", "attentionRisk", "continuationReason"], additionalProperties: false } },
        structuralAnalysis: { type: "object", properties: { hook: { type: "string" }, retention: { type: "string" }, narrative: { type: "string" }, emotionAndActionPrograms: { type: "array", items: { type: "string" } }, trustAndObjections: { type: "string" }, actionAndConversion: { type: "string" }, multimodalIntegration: { type: "string" } }, required: ["hook", "retention", "narrative", "emotionAndActionPrograms", "trustAndObjections", "actionAndConversion", "multimodalIntegration"], additionalProperties: false },
        scores: { type: "object", properties: { gancho: criterionSchema, clareza: criterionSchema, relevancia: criterionSchema, desejo: criterionSchema, confianca: criterionSchema, retencao: criterionSchema, acao: criterionSchema, objecoes: criterionSchema }, required: ["gancho", "clareza", "relevancia", "desejo", "confianca", "retencao", "acao", "objecoes"], additionalProperties: false },
        syntheticBrains: { type: "array", minItems: 5, maxItems: 5, items: { type: "object", properties: { name: { type: "string", enum: ["O Apressado", "O Analítico", "O Aspiracional", "O Influenciado pela Comunidade", "O Cético"] }, firstReaction: { type: "string" }, probableAbandonment: { type: "string" }, mainInterest: { type: "string" }, mainObjection: { type: "string" }, probableAction: { type: "string" }, confidence: { type: "string", enum: ["low", "medium", "high"] } }, required: ["name", "firstReaction", "probableAbandonment", "mainInterest", "mainObjection", "probableAction", "confidence"], additionalProperties: false } },
        relativePerformance: { type: "object", properties: { classification: { type: "string", enum: ["far_below", "below", "near_baseline", "above", "exceptional", "indeterminate"] }, reasoning: { type: "string" }, comparisonLevel: { type: "integer", minimum: 1, maximum: 4 }, confidence: { type: "string", enum: ["low", "medium", "high"] } }, required: ["classification", "reasoning", "comparisonLevel", "confidence"], additionalProperties: false },
        learning: { type: "object", properties: { replicable: { type: "array", maxItems: 8, items: { type: "string" } }, contingent: { type: "array", maxItems: 8, items: { type: "string" } }, notRecommended: { type: "array", maxItems: 8, items: { type: "string" } }, nextComparableContent: { type: "string" } }, required: ["replicable", "contingent", "notRecommended", "nextComparableContent"], additionalProperties: false },
        hypotheses: { type: "array", maxItems: 5, items: { type: "object", properties: { name: { type: "string" }, observation: { type: "string" }, mechanism: { type: "string" }, evidence: { type: "string" }, alternativeExplanations: { type: "array", items: { type: "string" } }, conditions: { type: "array", items: { type: "string" } }, limitations: { type: "array", items: { type: "string" } }, confidence: { type: "string", enum: ["low", "medium", "high"] }, stage: { type: "string", enum: ["observation", "hypothesis", "provisional", "validated", "contradicted", "obsolete"] } }, required: ["name", "observation", "mechanism", "evidence", "alternativeExplanations", "conditions", "limitations", "confidence", "stage"], additionalProperties: false } },
        conclusion: { type: "object", properties: { contentTypeAnswer: { type: "string" }, comparisonAnswer: { type: "string" }, comparabilityAnswer: { type: "string" }, lesson: { type: "string" }, cannotConclude: { type: "string" }, nextContent: { type: "string" }, memoryDecision: { type: "string" }, overallConfidence: { type: "string", enum: ["low", "medium", "high"] } }, required: ["contentTypeAnswer", "comparisonAnswer", "comparabilityAnswer", "lesson", "cannotConclude", "nextContent", "memoryDecision", "overallConfidence"], additionalProperties: false },
      },
      required: ["access", "timeline", "structuralAnalysis", "scores", "syntheticBrains", "relativePerformance", "learning", "hypotheses", "conclusion"],
      additionalProperties: false,
    },
  },
} as const;

function parseJsonObject(raw: string, label: string): Record<string, unknown> {
  const value = raw.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/i, "");
  const parsed = JSON.parse(value) as unknown;
  if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error(`${label} inválida.`);
  return parsed as Record<string, unknown>;
}

function strings(value: unknown, max = 8) {
  return Array.isArray(value) ? value.filter(item => typeof item === "string").slice(0, max) as string[] : [];
}

function oneOf<T extends readonly string[]>(value: unknown, allowed: T, fallback: T[number]): T[number] {
  return typeof value === "string" && (allowed as readonly string[]).includes(value) ? value as T[number] : fallback;
}

export function normalizeClassification(raw: unknown): ObservatoryClassification {
  const value = raw && typeof raw === "object" && !Array.isArray(raw) ? raw as Record<string, unknown> : {};
  const presentations = strings(value.presentationFormats, 3).filter(item => (PRESENTATION_FORMATS as readonly string[]).includes(item)) as ObservatoryClassification["presentationFormats"];
  const secondary = strings(value.secondaryFamilies, 2).filter(item => (CREATIVE_FAMILIES as readonly string[]).includes(item)) as ObservatoryClassification["secondaryFamilies"];
  const objectives = strings(value.objectives, 4).filter(item => (OBJECTIVES as readonly string[]).includes(item)) as ObservatoryClassification["objectives"];
  const mechanisms = strings(value.mechanisms, 6).filter(item => (MECHANISMS as readonly string[]).includes(item)) as ObservatoryClassification["mechanisms"];
  return {
    materialFormat: oneOf(value.materialFormat, MATERIAL_FORMATS, "outro"),
    presentationFormats: presentations.length ? presentations : ["outro"],
    primaryFamily: oneOf(value.primaryFamily, CREATIVE_FAMILIES, "hibrido"),
    secondaryFamilies: secondary,
    objectives: objectives.length ? objectives : ["outro"],
    segment: typeof value.segment === "string" && value.segment.trim() ? value.segment.trim() : "indeterminado",
    subsegment: typeof value.subsegment === "string" && value.subsegment.trim() ? value.subsegment.trim() : "indeterminado",
    probableAudience: typeof value.probableAudience === "string" && value.probableAudience.trim() ? value.probableAudience.trim() : "indeterminado",
    awarenessStage: oneOf(value.awarenessStage, AWARENESS_STAGES, "indeterminado"),
    productionLevel: oneOf(value.productionLevel, ["simple", "intermediate", "complex", "unknown"] as const, "unknown"),
    durationBand: oneOf(value.durationBand, ["up_to_15s", "16_to_30s", "31_to_60s", "over_60s", "not_applicable", "unknown"] as const, "unknown"),
    pace: oneOf(value.pace, ["slow", "moderate", "fast", "not_applicable", "unknown"] as const, "unknown"),
    mechanisms,
    confidence: oneOf(value.confidence, ["low", "medium", "high"] as const, "low"),
    evidence: strings(value.evidence),
    alternativeClassifications: strings(value.alternativeClassifications, 4),
    missingInformation: strings(value.missingInformation),
    needsHumanReview: value.needsHumanReview !== false,
  };
}

export async function classifyObservatoryMaterial(input: ObservatoryMaterialInput) {
  const raw = await evaluateWithProvider({
    prompt: buildClassificationPrompt(input),
    mediaUrl: input.mediaUrl,
    mediaMimeType: input.mediaMimeType,
    responseFormat: classificationSchema,
  });
  return normalizeClassification(parseJsonObject(raw, "Classificação"));
}

function normalized(value: string) {
  return value.trim().toLocaleLowerCase("pt-BR");
}

function overlaps(left: string[], right: string[]) {
  const rightSet = new Set(right);
  return left.some(item => rightSet.has(item));
}

export function scoreClassificationSimilarity(target: ObservatoryClassification, candidate: ObservatoryClassification) {
  let score = 0;
  if (target.primaryFamily === candidate.primaryFamily) score += 30;
  if (overlaps([target.primaryFamily, ...target.secondaryFamilies], [candidate.primaryFamily, ...candidate.secondaryFamilies])) score += 10;
  if (overlaps(target.objectives, candidate.objectives)) score += 18;
  if (normalized(target.segment) === normalized(candidate.segment)) score += 15;
  if (overlaps(target.presentationFormats, candidate.presentationFormats)) score += 8;
  if (target.materialFormat === candidate.materialFormat) score += 6;
  if (target.awarenessStage === candidate.awarenessStage) score += 4;
  if (target.productionLevel === candidate.productionLevel) score += 3;
  if (target.durationBand === candidate.durationBand) score += 3;
  if (target.pace === candidate.pace) score += 3;
  if (overlaps(target.mechanisms, candidate.mechanisms)) score += 10;
  return Math.min(100, score);
}

export function comparisonLevel(target: ObservatoryClassification, candidate: ObservatoryClassification, score: number): 1 | 2 | 3 | 4 {
  const sameFamily = target.primaryFamily === candidate.primaryFamily;
  const sameObjective = overlaps(target.objectives, candidate.objectives);
  const sameSegment = normalized(target.segment) === normalized(candidate.segment);
  if (sameFamily && sameObjective && sameSegment && score >= 65) return 1;
  if (sameFamily && sameObjective && score >= 48) return 2;
  if (overlaps(target.mechanisms, candidate.mechanisms) && score >= 25) return 3;
  return 4;
}

function parseClassification(reference: ObservatoryReference) {
  if (!reference.classificationJson) return null;
  try { return normalizeClassification(JSON.parse(reference.classificationJson)); } catch { return null; }
}

function referenceLearning(reference: ObservatoryReference) {
  if (!reference.analysisJson) return [];
  try {
    const value = JSON.parse(reference.analysisJson) as { learning?: { replicable?: unknown } };
    return strings(value.learning?.replicable, 3);
  } catch { return []; }
}

export function rankComparableReferences(target: ObservatoryClassification, references: ObservatoryReference[], excludeId?: number) {
  return references.flatMap(reference => {
    if (reference.id === excludeId) return [];
    const classification = parseClassification(reference);
    if (!classification) return [];
    const similarity = scoreClassificationSimilarity(target, classification);
    const level = comparisonLevel(target, classification, similarity);
    if (level === 4) return [];
    return [{ id: reference.id, title: reference.title, creator: reference.creator, similarity, comparisonLevel: level, primaryFamily: classification.primaryFamily, segment: classification.segment, learning: referenceLearning(reference) } satisfies ComparableReferenceSummary];
  }).sort((a, b) => a.comparisonLevel - b.comparisonLevel || b.similarity - a.similarity).slice(0, 8);
}

export async function buildObservatoryContext(input: ObservatoryMaterialInput, excludeId?: number): Promise<ObservatoryContext> {
  const classification = await classifyObservatoryMaterial(input);
  const [references, activePatterns] = await Promise.all([listAnalyzedObservatoryReferences(), listActiveObservatoryPatterns()]);
  const comparisons = rankComparableReferences(classification, references, excludeId);
  const patterns = activePatterns.filter(pattern =>
    pattern.creativeFamily === classification.primaryFamily &&
    (normalized(pattern.segment) === normalized(classification.segment) || classification.objectives.includes(pattern.objective as ObservatoryClassification["objectives"][number]))
  ).slice(0, 8).map(pattern => ({ id: pattern.id, name: pattern.name, stage: pattern.stage as "provisional" | "validated", supportingCount: pattern.supportingCount, counterexampleCount: pattern.counterexampleCount, confidence: pattern.confidence, mechanism: pattern.mechanism }));
  const bestLevel = comparisons[0]?.comparisonLevel ?? 4;
  return {
    promptVersion: "2.0",
    classification,
    comparisons,
    patterns,
    comparisonLevel: bestLevel,
    benchmarkConfidence: bestLevel === 1 && comparisons.length >= 3 ? "high" : bestLevel <= 2 && comparisons.length >= 2 ? "medium" : "low",
  };
}

export async function analyzeObservatoryReference(input: ObservatoryMaterialInput, context: ObservatoryContext) {
  const raw = await evaluateWithProvider({
    prompt: buildObservatoryCuratorPrompt(input, context.classification, context.comparisons),
    mediaUrl: input.mediaUrl,
    mediaMimeType: input.mediaMimeType,
    responseFormat: curatorSchema,
  });
  return parseJsonObject(raw, "Ficha do Observatório");
}
