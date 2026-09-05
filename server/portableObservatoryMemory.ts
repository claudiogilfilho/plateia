import memory from "../knowledge/observatory/plateia-memory.json";
import { canonicalPublicUrl } from "./publicUrlIdentity";

export type PortableReferenceCandidate = {
  id: string;
  title: string;
  creator: string;
  sourceUrl: string;
  classification: unknown;
  learning: string[];
};

type RawReference = {
  id?: unknown;
  title?: unknown;
  creator?: unknown;
  url?: unknown;
  classification?: any;
  replicable?: unknown;
  training?: { replicable?: unknown };
};

type RawPattern = {
  id?: unknown;
  name?: unknown;
  statement?: unknown;
  stage?: unknown;
  status?: unknown;
  creativeFamily?: unknown;
  objective?: unknown;
  segment?: unknown;
  mechanism?: unknown;
  supportReferenceIds?: unknown;
  supportingCount?: unknown;
  comparableSupportCount?: unknown;
  counterexampleCount?: unknown;
  caseLimitCount?: unknown;
  confidence?: unknown;
};

type RawHypothesis = {
  id?: unknown;
  statement?: unknown;
  status?: unknown;
  supportReferenceIds?: unknown;
  reasonNotPromoted?: unknown;
  consolidatedIntoPatternId?: unknown;
};

function text(value: unknown, fallback = "") { return typeof value === "string" && value.trim() ? value.trim() : fallback; }
function texts(value: unknown, max = 8) { return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string").slice(0, max) : []; }

export function listPortableReferences(): PortableReferenceCandidate[] {
  const references = (memory as { references?: RawReference[] }).references ?? [];
  const seen = new Set<string>();
  return references.flatMap(reference => {
    const sourceUrl = text(reference.url);
    const canonical = canonicalPublicUrl(sourceUrl);
    if (!sourceUrl || seen.has(canonical)) return [];
    seen.add(canonical);
    return [{
      id: text(reference.id, `portable-${seen.size}`),
      title: text(reference.title, "Referência sem título"),
      creator: text(reference.creator, "Criador não informado"),
      sourceUrl,
      classification: reference.classification,
      learning: texts(reference.training?.replicable ?? reference.replicable, 3),
    }];
  });
}

function normalizedPattern(pattern: RawPattern, index: number) {
  return {
    id: text(pattern.id, `portable-pattern-${index + 1}`),
    name: text(pattern.name ?? pattern.statement, "Hipótese sem título"),
    stage: text(pattern.stage ?? pattern.status, "hypothesis"),
    creativeFamily: text(pattern.creativeFamily, "indeterminado").replace(/^família\s+/i, ""),
    objective: text(pattern.objective, "indeterminado").replace(/^objetivo\s+/i, "").split(/\s+ou\s+/)[0],
    segment: text(pattern.segment, "indeterminado"),
    mechanism: Array.isArray(pattern.mechanism) ? texts(pattern.mechanism).join(", ") : text(pattern.mechanism),
    supportingCount: Number(pattern.supportingCount ?? pattern.comparableSupportCount ?? (Array.isArray(pattern.supportReferenceIds) ? pattern.supportReferenceIds.length : 0)) || 0,
    counterexampleCount: Number(pattern.counterexampleCount) || 0,
    caseLimitCount: Number(pattern.caseLimitCount) || 0,
    confidence: (["low", "medium", "high"].includes(text(pattern.confidence)) ? text(pattern.confidence) : "low") as "low" | "medium" | "high",
    source: "portable_memory" as const,
  };
}

export function listPortablePatterns() {
  const raw = memory as { references?: RawReference[]; patterns?: RawPattern[]; hypotheses?: RawHypothesis[] };
  const references = raw.references ?? [];
  const referencesById = new Map(references.map(reference => [text(reference.id), reference]));
  const patterns = (raw.patterns ?? []).map(normalizedPattern);
  const patternIds = new Set(patterns.map(pattern => pattern.id));
  const hypotheses = (raw.hypotheses ?? []).flatMap((hypothesis, index) => {
    if (text(hypothesis.consolidatedIntoPatternId)) return [];
    const id = text(hypothesis.id, `portable-hypothesis-${index + 1}`);
    if (patternIds.has(id)) return [];
    const supportReferenceIds = texts(hypothesis.supportReferenceIds, 100);
    const firstReference = referencesById.get(supportReferenceIds[0]);
    const classification = firstReference?.classification ?? {};
    const objectives = texts(classification.objectives, 4);
    const mechanisms = texts(classification.mechanisms, 6);
    const supportingCount = new Set(supportReferenceIds).size;
    return [{
      id,
      name: text(hypothesis.statement, "Hipótese sem título"),
      stage: supportingCount >= 2 ? "supported_hypothesis" : "observation",
      creativeFamily: text(classification.primaryFamily, "indeterminado"),
      objective: objectives[0] ?? "indeterminado",
      segment: text(classification.segment, "indeterminado"),
      mechanism: mechanisms.join(", "),
      supportingCount,
      counterexampleCount: 0,
      caseLimitCount: 0,
      confidence: "low" as const,
      source: "portable_memory" as const,
      reasonNotPromoted: text(hypothesis.reasonNotPromoted),
    }];
  });
  return [...patterns, ...hypotheses];
}

export const PORTABLE_MEMORY_STATS = {
  referenceCount: ((memory as { references?: unknown[] }).references ?? []).length,
  patternCount: ((memory as { patterns?: unknown[] }).patterns ?? []).length,
  hypothesisCount: ((memory as { hypotheses?: unknown[] }).hypotheses ?? []).length,
  activeHypothesisCount: ((memory as { hypotheses?: RawHypothesis[] }).hypotheses ?? []).filter(hypothesis => !text(hypothesis.consolidatedIntoPatternId)).length,
  taxonomyVersion: text((memory as { taxonomyVersion?: unknown }).taxonomyVersion, "legacy"),
};
