import type { ObservatoryReference } from "../drizzle/schema";
import {
  ADVERTISING_TYPES, AWARENESS_STAGES, COMMERCIAL_INTENTS, CONTAINERS, CREATIVE_FAMILIES,
  CTA_TYPES, DURATION_BANDS, HOOK_TYPES, MATERIAL_FORMATS, MECHANISMS, NARRATIVE_ELEMENTS,
  OBJECTIVES, PACES, PLATEIA_TAXONOMY_VERSION, PRESENTATION_FORMATS, PRODUCTION_LEVELS,
  PROOF_TYPES, PATTERN_TYPES, TAXONOMY_ALIASES, type ObservatoryClassification,
} from "../shared/plateiaTaxonomy";
import { evaluateWithProvider } from "./aiProvider";
import { listActiveObservatoryPatterns, listAnalyzedObservatoryReferences, listCandidateObservatoryPatterns } from "./db";
import { buildClassificationPrompt, buildObservatoryCuratorPrompt } from "./observatoryPrompt";
import { listPortablePatterns, listPortableReferences } from "./portableObservatoryMemory";
import { canonicalPublicUrl } from "./publicUrlIdentity";

export { MATERIAL_FORMATS, PRESENTATION_FORMATS, CREATIVE_FAMILIES, OBJECTIVES, AWARENESS_STAGES, MECHANISMS };

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

export type { ObservatoryClassification };

export type ComparableReferenceSummary = {
  id: string | number;
  title: string;
  creator: string;
  sourceUrl?: string | null;
  similarity: number;
  comparisonLevel: 1 | 2 | 3 | 4;
  primaryFamily: string;
  segment: string;
  learning: string[];
};

export type ObservatoryPatternSummary = { id: string | number; name: string; stage: string; supportingCount: number; counterexampleCount: number; caseLimitCount?: number; confidence: "low" | "medium" | "high"; mechanism: string; source: "database" | "portable_memory" };

export type ObservatoryContext = {
  promptVersion: "3.1";
  classification: ObservatoryClassification;
  comparisons: ComparableReferenceSummary[];
  patterns: ObservatoryPatternSummary[];
  candidatePatterns: ObservatoryPatternSummary[];
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
        taxonomyVersion: { type: "string", enum: [PLATEIA_TAXONOMY_VERSION] },
        container: { type: "string", enum: [...CONTAINERS] },
        materialFormat: { type: "string", enum: [...MATERIAL_FORMATS] },
        presentationFormats: { type: "array", minItems: 1, maxItems: 3, items: { type: "string", enum: [...PRESENTATION_FORMATS] } },
        primaryFamily: { type: "string", enum: [...CREATIVE_FAMILIES] },
        secondaryFamilies: { type: "array", maxItems: 2, items: { type: "string", enum: [...CREATIVE_FAMILIES] } },
        objectives: { type: "array", minItems: 1, maxItems: 4, items: { type: "string", enum: [...OBJECTIVES] } },
        functionalMix: { type: "array", maxItems: 3, items: { type: "object", properties: { family: { type: "string", enum: [...CREATIVE_FAMILIES] }, percentage: { type: "integer", minimum: 1, maximum: 100 } }, required: ["family", "percentage"], additionalProperties: false } },
        advertisingType: { type: "string", enum: [...ADVERTISING_TYPES] },
        commercialIntent: { type: "string", enum: [...COMMERCIAL_INTENTS] },
        advertisedEntity: { type: "object", properties: { kind: { type: "string", enum: ["produto", "servico", "marca", "causa", "pessoa", "nenhuma", "indeterminado"] }, name: { type: "string" }, confidence: { type: "string", enum: ["low", "medium", "high"] } }, required: ["kind", "name", "confidence"], additionalProperties: false },
        contentTopic: { type: "object", properties: { label: { type: "string" }, iabCode: { anyOf: [{ type: "string" }, { type: "null" }] } }, required: ["label", "iabCode"], additionalProperties: false },
        segment: { type: "string" },
        subsegment: { type: "string" },
        probableAudience: { type: "string" },
        awarenessStage: { type: "string", enum: [...AWARENESS_STAGES] },
        productionLevel: { type: "string", enum: ["simple", "intermediate", "complex", "unknown"] },
        creatorScale: { type: "string", enum: ["small", "medium", "large", "unknown"] },
        replicability: { type: "string", enum: ["high", "medium", "low", "unknown"] },
        durationBand: { type: "string", enum: ["up_to_15s", "16_to_30s", "31_to_60s", "over_60s", "not_applicable", "unknown"] },
        pace: { type: "string", enum: ["slow", "moderate", "fast", "not_applicable", "unknown"] },
        mechanisms: { type: "array", maxItems: 6, items: { type: "string", enum: [...MECHANISMS] } },
        hookTypes: { type: "array", maxItems: 5, items: { type: "string", enum: [...HOOK_TYPES] } },
        narrativeElements: { type: "array", maxItems: 10, items: { type: "string", enum: [...NARRATIVE_ELEMENTS] } },
        proofTypes: { type: "array", maxItems: 6, items: { type: "string", enum: [...PROOF_TYPES] } },
        ctaTypes: { type: "array", maxItems: 4, items: { type: "string", enum: [...CTA_TYPES] } },
        distributionContext: { type: "object", properties: { organicPaid: { type: "string", enum: ["organic", "paid", "mixed", "unknown"] }, trendDependency: { type: "string", enum: ["none", "low", "high", "unknown"] } }, required: ["organicPaid", "trendDependency"], additionalProperties: false },
        confidence: { type: "string", enum: ["low", "medium", "high"] },
        evidence: { type: "array", maxItems: 8, items: { type: "string" } },
        alternativeClassifications: { type: "array", maxItems: 4, items: { type: "string" } },
        missingInformation: { type: "array", maxItems: 8, items: { type: "string" } },
        needsHumanReview: { type: "boolean" },
      },
      required: ["taxonomyVersion", "container", "materialFormat", "presentationFormats", "primaryFamily", "secondaryFamilies", "functionalMix", "objectives", "advertisingType", "commercialIntent", "advertisedEntity", "contentTopic", "segment", "subsegment", "probableAudience", "awarenessStage", "productionLevel", "creatorScale", "replicability", "durationBand", "pace", "mechanisms", "hookTypes", "narrativeElements", "proofTypes", "ctaTypes", "distributionContext", "confidence", "evidence", "alternativeClassifications", "missingInformation", "needsHumanReview"],
      additionalProperties: false,
    },
  },
} as const;

const criterionSchema = {
  type: "object",
  properties: {
    assessed: { type: "boolean" },
    score: { anyOf: [{ type: "integer", minimum: 0, maximum: 100 }, { type: "null" }] },
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
        hypotheses: { type: "array", maxItems: 5, items: { type: "object", properties: { name: { type: "string" }, patternType: { type: "string", enum: [...PATTERN_TYPES] }, observation: { type: "string" }, mechanism: { type: "string" }, evidence: { type: "string" }, alternativeExplanations: { type: "array", items: { type: "string" } }, conditions: { type: "array", items: { type: "string" } }, limitations: { type: "array", items: { type: "string" } }, confidence: { type: "string", enum: ["low", "medium", "high"] }, stage: { type: "string", enum: ["observation", "hypothesis", "contradicted", "inconclusive"] } }, required: ["name", "patternType", "observation", "mechanism", "evidence", "alternativeExplanations", "conditions", "limitations", "confidence", "stage"], additionalProperties: false } },
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

function aliased(value: unknown, aliases: Record<string, string>) {
  return typeof value === "string" ? aliases[value] ?? value : value;
}

function listOfKnown<T extends readonly string[]>(value: unknown, allowed: T, aliases: Record<string, string> = {}, max = 8): T[number][] {
  return strings(value, max).map(item => aliases[item] ?? item).filter(item => (allowed as readonly string[]).includes(item)) as T[number][];
}

export function normalizeClassification(raw: unknown): ObservatoryClassification {
  const value = raw && typeof raw === "object" && !Array.isArray(raw) ? raw as Record<string, unknown> : {};
  const presentations = listOfKnown(value.presentationFormats, PRESENTATION_FORMATS, TAXONOMY_ALIASES.presentationFormat, 3);
  const secondary = listOfKnown(value.secondaryFamilies, CREATIVE_FAMILIES, {}, 2);
  const objectives = listOfKnown(value.objectives, OBJECTIVES, TAXONOMY_ALIASES.objective, 4);
  const mechanisms = listOfKnown(value.mechanisms, MECHANISMS, TAXONOMY_ALIASES.mechanism, 8);
  const entity = value.advertisedEntity && typeof value.advertisedEntity === "object" && !Array.isArray(value.advertisedEntity) ? value.advertisedEntity as Record<string, unknown> : {};
  const topic = value.contentTopic && typeof value.contentTopic === "object" && !Array.isArray(value.contentTopic) ? value.contentTopic as Record<string, unknown> : {};
  const distribution = value.distributionContext && typeof value.distributionContext === "object" && !Array.isArray(value.distributionContext) ? value.distributionContext as Record<string, unknown> : {};
  const rawFunctionalMix = Array.isArray(value.functionalMix) ? value.functionalMix.flatMap(item => {
    if (!item || typeof item !== "object" || Array.isArray(item)) return [];
    const mix = item as Record<string, unknown>;
    const family = oneOf(mix.family, CREATIVE_FAMILIES, "indeterminado");
    const percentage = Math.max(1, Math.min(100, Math.round(Number(mix.percentage) || 0)));
    return percentage ? [{ family, percentage }] : [];
  }).slice(0, 3) : [];
  const rawMixTotal = rawFunctionalMix.reduce((sum, item) => sum + item.percentage, 0);
  const functionalMix = rawFunctionalMix.length && rawMixTotal > 0
    ? rawFunctionalMix.map((item, index) => ({ ...item, percentage: index === rawFunctionalMix.length - 1 ? 100 - rawFunctionalMix.slice(0, -1).reduce((sum, previous) => sum + Math.round(previous.percentage * 100 / rawMixTotal), 0) : Math.round(item.percentage * 100 / rawMixTotal) }))
    : [];
  const primaryFamily = oneOf(value.primaryFamily, CREATIVE_FAMILIES, "indeterminado");
  return {
    taxonomyVersion: PLATEIA_TAXONOMY_VERSION,
    container: oneOf(value.container, CONTAINERS, "indeterminado"),
    materialFormat: oneOf(aliased(value.materialFormat, TAXONOMY_ALIASES.materialFormat), MATERIAL_FORMATS, "indeterminado"),
    presentationFormats: presentations.length ? presentations : ["indeterminado"],
    primaryFamily,
    secondaryFamilies: secondary,
    functionalMix: functionalMix.length ? functionalMix : [{ family: primaryFamily, percentage: 100 }],
    objectives: objectives.length ? objectives : ["indeterminado"],
    advertisingType: oneOf(value.advertisingType, ADVERTISING_TYPES, "indeterminado"),
    commercialIntent: oneOf(value.commercialIntent, COMMERCIAL_INTENTS, "indeterminada"),
    advertisedEntity: { kind: oneOf(entity.kind, ["produto", "servico", "marca", "causa", "pessoa", "nenhuma", "indeterminado"] as const, "indeterminado"), name: typeof entity.name === "string" ? entity.name.trim() : "", confidence: oneOf(entity.confidence, ["low", "medium", "high"] as const, "low") },
    contentTopic: { label: typeof topic.label === "string" && topic.label.trim() ? topic.label.trim() : "indeterminado", iabCode: typeof topic.iabCode === "string" ? topic.iabCode : null },
    segment: typeof value.segment === "string" && value.segment.trim() ? value.segment.trim() : "indeterminado",
    subsegment: typeof value.subsegment === "string" && value.subsegment.trim() ? value.subsegment.trim() : "indeterminado",
    probableAudience: typeof value.probableAudience === "string" && value.probableAudience.trim() ? value.probableAudience.trim() : "indeterminado",
    awarenessStage: oneOf(value.awarenessStage, AWARENESS_STAGES, "indeterminado"),
    productionLevel: oneOf(value.productionLevel, PRODUCTION_LEVELS, "unknown"),
    creatorScale: oneOf(value.creatorScale, ["small", "medium", "large", "unknown"] as const, "unknown"),
    replicability: oneOf(value.replicability, ["high", "medium", "low", "unknown"] as const, "unknown"),
    durationBand: oneOf(value.durationBand, DURATION_BANDS, "unknown"),
    pace: oneOf(value.pace, PACES, "unknown"),
    mechanisms,
    hookTypes: listOfKnown(value.hookTypes, HOOK_TYPES, {}, 5),
    narrativeElements: listOfKnown(value.narrativeElements, NARRATIVE_ELEMENTS, {}, 10),
    proofTypes: listOfKnown(value.proofTypes, PROOF_TYPES, {}, 6),
    ctaTypes: listOfKnown(value.ctaTypes, CTA_TYPES, {}, 4),
    distributionContext: { organicPaid: oneOf(distribution.organicPaid, ["organic", "paid", "mixed", "unknown"] as const, "unknown"), trendDependency: oneOf(distribution.trendDependency, ["none", "low", "high", "unknown"] as const, "unknown") },
    confidence: oneOf(value.confidence, ["low", "medium", "high"] as const, "low"),
    evidence: strings(value.evidence),
    alternativeClassifications: strings(value.alternativeClassifications, 4),
    missingInformation: strings(value.missingInformation),
    needsHumanReview: value.needsHumanReview !== false || primaryFamily === "indeterminado" || (rawFunctionalMix.length > 0 && rawMixTotal !== 100),
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
  const unknown = new Set(["indeterminado", "indeterminada", "unknown", "not_applicable"]);
  const rightSet = new Set(right.filter(item => !unknown.has(item)));
  return left.some(item => !unknown.has(item) && rightSet.has(item));
}

function known(value: string) { return !["indeterminado", "indeterminada", "unknown", "not_applicable"].includes(value); }

export function scoreClassificationSimilarity(target: ObservatoryClassification, candidate: ObservatoryClassification) {
  let score = 0;
  if (known(target.primaryFamily) && target.primaryFamily === candidate.primaryFamily) score += 30;
  if (overlaps([target.primaryFamily, ...target.secondaryFamilies], [candidate.primaryFamily, ...candidate.secondaryFamilies])) score += 10;
  if (overlaps(target.objectives, candidate.objectives)) score += 18;
  if (known(target.segment) && normalized(target.segment) === normalized(candidate.segment)) score += 15;
  if (overlaps(target.presentationFormats, candidate.presentationFormats)) score += 8;
  if (known(target.materialFormat) && target.materialFormat === candidate.materialFormat) score += 6;
  if (known(target.awarenessStage) && target.awarenessStage === candidate.awarenessStage) score += 4;
  if (known(target.productionLevel) && target.productionLevel === candidate.productionLevel) score += 3;
  if (known(target.durationBand) && target.durationBand === candidate.durationBand) score += 3;
  if (known(target.pace) && target.pace === candidate.pace) score += 3;
  if (overlaps(target.mechanisms, candidate.mechanisms)) score += 10;
  if (target.advertisingType === candidate.advertisingType && target.advertisingType !== "indeterminado") score += 10;
  if (target.commercialIntent === candidate.commercialIntent && target.commercialIntent !== "indeterminada") score += 5;
  if (overlaps(target.hookTypes, candidate.hookTypes)) score += 5;
  if (overlaps(target.proofTypes, candidate.proofTypes)) score += 4;
  if (overlaps(target.ctaTypes, candidate.ctaTypes)) score += 4;
  if (target.creatorScale === "small" && candidate.creatorScale === "large" && candidate.replicability === "low") score -= 12;
  return Math.max(0, Math.min(100, score));
}

export function comparisonLevel(target: ObservatoryClassification, candidate: ObservatoryClassification, score: number): 1 | 2 | 3 | 4 {
  const sameFamily = known(target.primaryFamily) && target.primaryFamily === candidate.primaryFamily;
  const sameObjective = overlaps(target.objectives, candidate.objectives);
  const sameSegment = known(target.segment) && normalized(target.segment) === normalized(candidate.segment);
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
    return [{ id: reference.id, title: reference.title, creator: reference.creator, sourceUrl: reference.sourceUrl, similarity, comparisonLevel: level, primaryFamily: classification.primaryFamily, segment: classification.segment, learning: referenceLearning(reference) } satisfies ComparableReferenceSummary];
  }).sort((a, b) => a.comparisonLevel - b.comparisonLevel || b.similarity - a.similarity).slice(0, 8);
}

export function rankPortableReferences(target: ObservatoryClassification) {
  return listPortableReferences().flatMap(reference => {
    const classification = normalizeClassification(reference.classification);
    const similarity = scoreClassificationSimilarity(target, classification);
    const level = comparisonLevel(target, classification, similarity);
    if (level === 4) return [];
    return [{ id: reference.id, title: reference.title, creator: reference.creator, sourceUrl: reference.sourceUrl, similarity, comparisonLevel: level, primaryFamily: classification.primaryFamily, segment: classification.segment, learning: reference.learning } satisfies ComparableReferenceSummary];
  }).sort((a, b) => a.comparisonLevel - b.comparisonLevel || b.similarity - a.similarity).slice(0, 12);
}

export async function buildObservatoryContext(input: ObservatoryMaterialInput, excludeId?: number): Promise<ObservatoryContext> {
  const classification = await classifyObservatoryMaterial(input);
  const [references, activePatterns, candidatePatterns] = await Promise.all([
    listAnalyzedObservatoryReferences(),
    listActiveObservatoryPatterns(),
    listCandidateObservatoryPatterns(),
  ]);
  const databaseComparisons = rankComparableReferences(classification, references, excludeId);
  const comparisons = [...databaseComparisons, ...rankPortableReferences(classification)]
    .sort((a, b) => a.comparisonLevel - b.comparisonLevel || b.similarity - a.similarity)
    .filter((reference, index, all) => {
      const key = reference.sourceUrl ? canonicalPublicUrl(reference.sourceUrl) : `${reference.title}|${reference.creator}`.toLocaleLowerCase("pt-BR");
      return all.findIndex(candidate => (candidate.sourceUrl ? canonicalPublicUrl(candidate.sourceUrl) : `${candidate.title}|${candidate.creator}`.toLocaleLowerCase("pt-BR")) === key) === index;
    })
    .slice(0, 8);
  const relevant = (pattern: { creativeFamily: string; segment: string; objective: string }) =>
    pattern.creativeFamily === classification.primaryFamily &&
    (normalized(pattern.segment) === normalized(classification.segment) || classification.objectives.includes(pattern.objective as ObservatoryClassification["objectives"][number]));
  const summarizeDatabasePattern = (pattern: typeof activePatterns[number]): ObservatoryPatternSummary => ({
    id: pattern.id,
    name: pattern.name,
    stage: pattern.stage,
    supportingCount: pattern.supportingCount,
    counterexampleCount: pattern.counterexampleCount,
    caseLimitCount: 0,
    confidence: pattern.confidence,
    mechanism: pattern.mechanism,
    source: "database",
  });
  const databasePatterns = activePatterns.filter(relevant).map(summarizeDatabasePattern);
  const databaseCandidates = candidatePatterns.filter(relevant).map(summarizeDatabasePattern);
  const portableCandidates = listPortablePatterns().filter(relevant);
  const patterns = [...databasePatterns, ...portableCandidates]
    .filter(pattern => ["provisional", "experimentally_validated", "validated"].includes(pattern.stage))
    .slice(0, 8);
  const allCandidates = [...databaseCandidates, ...portableCandidates]
    .filter(pattern => !["contradicted", "inconclusive", "archived"].includes(pattern.stage))
    .filter((pattern, index, all) => all.findIndex(candidate => String(candidate.id) === String(pattern.id) && candidate.source === pattern.source) === index)
    .sort((left, right) => {
      const priority = (pattern: { stage: string; supportingCount: number }) => pattern.stage === "supported_hypothesis" && pattern.supportingCount === 2 ? 0 : pattern.supportingCount === 1 ? 1 : pattern.stage === "provisional" ? 2 : 3;
      return priority(left) - priority(right) || right.supportingCount - left.supportingCount;
    })
    .slice(0, 12);
  const bestLevel = comparisons[0]?.comparisonLevel ?? 4;
  return {
    promptVersion: "3.1",
    classification,
    comparisons,
    patterns,
    candidatePatterns: allCandidates,
    comparisonLevel: bestLevel,
    benchmarkConfidence: bestLevel === 1 && comparisons.length >= 3 ? "high" : bestLevel <= 2 && comparisons.length >= 2 ? "medium" : "low",
  };
}

export async function analyzeObservatoryReference(input: ObservatoryMaterialInput, context: ObservatoryContext) {
  const raw = await evaluateWithProvider({
    prompt: buildObservatoryCuratorPrompt(input, context.classification, context.comparisons, context.candidatePatterns),
    mediaUrl: input.mediaUrl,
    mediaMimeType: input.mediaMimeType,
    responseFormat: curatorSchema,
  });
  return parseJsonObject(raw, "Ficha do Observatório");
}
