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
  classification?: unknown;
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
  confidence?: unknown;
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

export function listPortablePatterns() {
  const patterns = (memory as { patterns?: RawPattern[] }).patterns ?? [];
  return patterns.map((pattern, index) => ({
    id: text(pattern.id, `portable-pattern-${index + 1}`),
    name: text(pattern.name ?? pattern.statement, "Hipótese sem título"),
    stage: text(pattern.stage ?? pattern.status, "hypothesis"),
    creativeFamily: text(pattern.creativeFamily, "indeterminado").replace(/^família\s+/i, ""),
    objective: text(pattern.objective, "indeterminado").replace(/^objetivo\s+/i, "").split(/\s+ou\s+/)[0],
    segment: text(pattern.segment, "indeterminado"),
    mechanism: Array.isArray(pattern.mechanism) ? texts(pattern.mechanism).join(", ") : text(pattern.mechanism),
    supportingCount: Number(pattern.supportingCount ?? pattern.comparableSupportCount ?? (Array.isArray(pattern.supportReferenceIds) ? pattern.supportReferenceIds.length : 0)) || 0,
    counterexampleCount: Number(pattern.counterexampleCount) || 0,
    confidence: (["low", "medium", "high"].includes(text(pattern.confidence)) ? text(pattern.confidence) : "low") as "low" | "medium" | "high",
    source: "portable_memory" as const,
  }));
}

export const PORTABLE_MEMORY_STATS = {
  referenceCount: ((memory as { references?: unknown[] }).references ?? []).length,
  patternCount: ((memory as { patterns?: unknown[] }).patterns ?? []).length,
  taxonomyVersion: text((memory as { taxonomyVersion?: unknown }).taxonomyVersion, "legacy"),
};
