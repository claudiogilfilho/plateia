import { and, desc, eq, inArray } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { Analysis, InsertAnalysis, InsertInstagramConnection, InsertObservatoryReference, InsertUser, InstagramConnection, ObservatoryReference, analyses, instagramConnections, observatoryPatterns, observatoryReferences, users } from "../drizzle/schema";
import { ENV } from './_core/env';
import { buildRevokedInstagramConnectionPatch } from "./instagramIntegration";
import { decidePatternStageFromEvidence, type PatternEvidenceCandidate, type PatternEvidenceRole } from "./patternEvidence";
import {
  memoryCreateAnalysis,
  memoryCreateObservatoryReference,
  memoryGetAnalysis,
  memoryGetInstagramConnection,
  memoryGetObservatoryReference,
  memoryGetUser,
  memoryListActivePatterns,
  memoryListCandidatePatterns,
  memoryListAnalyses,
  memoryListObservatoryReferences,
  memoryRecordObservatoryHypotheses,
  memorySaveInstagramConnection,
  memoryUpdateAnalysisResult,
  memoryUpdateInstagramConnectionStatus,
  memoryUpdateObservatoryReference,
  memoryUpsertUser,
} from "./memoryRepository";

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    memoryUpsertUser(user);
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    return memoryGetUser(openId);
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

export async function createAnalysis(analysis: Omit<InsertAnalysis, "id" | "status" | "reportJson" | "createdAt" | "updatedAt">) {
  const db = await getDb();
  if (!db) return memoryCreateAnalysis(analysis);
  const result = await db.insert(analyses).values(analysis);
  return { id: Number(result[0].insertId) };
}

export async function updateAnalysisResult(id: number, status: "completed" | "needs_content" | "failed", report: unknown) {
  const db = await getDb();
  if (!db) return memoryUpdateAnalysisResult(id, status, report);
  await db.update(analyses).set({ status, reportJson: report ? JSON.stringify(report) : null }).where(eq(analyses.id, id));
}

export async function listAnalysesForUser(userId: number): Promise<Analysis[]> {
  const db = await getDb();
  if (!db) return memoryListAnalyses(userId);
  return db.select().from(analyses).where(eq(analyses.userId, userId)).orderBy(desc(analyses.createdAt));
}

export async function getAnalysisByIdForUser(id: number, userId: number): Promise<Analysis | undefined> {
  const db = await getDb();
  if (!db) return memoryGetAnalysis(id, userId);
  const result = await db.select().from(analyses).where(and(eq(analyses.id, id), eq(analyses.userId, userId))).limit(1);
  return result[0];
}

export async function getInstagramConnectionForUser(userId: number): Promise<InstagramConnection | undefined> {
  const db = await getDb();
  if (!db) return memoryGetInstagramConnection(userId);
  const result = await db.select().from(instagramConnections).where(eq(instagramConnections.userId, userId)).orderBy(desc(instagramConnections.updatedAt)).limit(1);
  return result[0];
}

export async function revokeInstagramConnectionForUser(userId: number) {
  const db = await getDb();
  if (!db) return memoryUpdateInstagramConnectionStatus(userId, "revoked");
  await db.update(instagramConnections).set(buildRevokedInstagramConnectionPatch()).where(eq(instagramConnections.userId, userId));
}

export async function saveInstagramConnectionForUser(userId: number, connection: Omit<InsertInstagramConnection, "id" | "userId" | "createdAt" | "updatedAt">) {
  const db = await getDb();
  if (!db) return memorySaveInstagramConnection(userId, connection);
  const existing = await getInstagramConnectionForUser(userId);
  if (existing) {
    await db.update(instagramConnections).set(connection).where(eq(instagramConnections.id, existing.id));
    return;
  }
  await db.insert(instagramConnections).values({ ...connection, userId });
}

export async function updateInstagramConnectionStatus(userId: number, status: "ready" | "connected" | "expired" | "revoked" | "error") {
  const db = await getDb();
  if (!db) return memoryUpdateInstagramConnectionStatus(userId, status);
  await db.update(instagramConnections).set({ status }).where(eq(instagramConnections.userId, userId));
}

export async function createObservatoryReference(reference: Omit<InsertObservatoryReference, "id" | "status" | "classificationJson" | "analysisJson" | "promptVersion" | "createdAt" | "updatedAt">) {
  const db = await getDb();
  if (!db) return memoryCreateObservatoryReference(reference);
  const result = await db.insert(observatoryReferences).values(reference);
  return { id: Number(result[0].insertId) };
}

export async function updateObservatoryReferenceResult(
  id: number,
  status: "analyzed" | "needs_content" | "failed",
  classification: unknown,
  analysis: unknown,
) {
  const db = await getDb();
  if (!db) return memoryUpdateObservatoryReference(id, status, classification, analysis);
  await db.update(observatoryReferences).set({
    status,
    classificationJson: classification ? JSON.stringify(classification) : null,
    analysisJson: analysis ? JSON.stringify(analysis) : null,
  }).where(eq(observatoryReferences.id, id));
}

export async function listObservatoryReferences(): Promise<ObservatoryReference[]> {
  const db = await getDb();
  if (!db) return memoryListObservatoryReferences();
  return db.select().from(observatoryReferences).orderBy(desc(observatoryReferences.createdAt));
}

export async function listAnalyzedObservatoryReferences(): Promise<ObservatoryReference[]> {
  const db = await getDb();
  if (!db) return memoryListObservatoryReferences(true);
  return db.select().from(observatoryReferences)
    .where(eq(observatoryReferences.status, "analyzed"))
    .orderBy(desc(observatoryReferences.createdAt));
}

export async function getObservatoryReferenceById(id: number): Promise<ObservatoryReference | undefined> {
  const db = await getDb();
  if (!db) return memoryGetObservatoryReference(id);
  const result = await db.select().from(observatoryReferences).where(eq(observatoryReferences.id, id)).limit(1);
  return result[0];
}

export async function listActiveObservatoryPatterns() {
  const db = await getDb();
  if (!db) return memoryListActivePatterns();
  return db.select().from(observatoryPatterns)
    .where(inArray(observatoryPatterns.stage, ["provisional", "experimentally_validated"]))
    .orderBy(desc(observatoryPatterns.updatedAt));
}

export async function listCandidateObservatoryPatterns() {
  const db = await getDb();
  if (!db) return memoryListCandidatePatterns();
  return db.select().from(observatoryPatterns)
    .where(inArray(observatoryPatterns.stage, ["observation", "hypothesis", "supported_hypothesis", "provisional", "experimentally_validated"]))
    .orderBy(desc(observatoryPatterns.updatedAt));
}

export type ObservatoryHypothesisInput = {
  name: string;
  targetPatternId: string | number | null;
  evidenceRole: PatternEvidenceRole;
  comparisonLevel: 1 | 2 | 3 | 4;
  requiredEvidenceObserved: boolean;
  patternType: string;
  observation: string;
  mechanism: string;
  evidence: string;
  alternativeExplanations: string[];
  conditions: string[];
  limitations: string[];
  confidence: "low" | "medium" | "high";
  stage: "observation" | "hypothesis" | "contradicted" | "inconclusive";
};

type StoredPatternEvidence = PatternEvidenceCandidate & {
  observation?: string;
  evidence?: string;
  limitations?: string[];
  kind?: string;
};

function jsonArray(value: string | null) {
  if (!value) return [];
  try { const parsed = JSON.parse(value); return Array.isArray(parsed) ? parsed : []; } catch { return []; }
}

function normalizedPatternPart(value: string) {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function normalizedStoredEvidence(value: any, referenceMetadata: Map<number, { creator: string; sourceIdentity: string }>): StoredPatternEvidence | null {
  const referenceId = Number(value?.referenceId);
  if (!Number.isInteger(referenceId) || referenceId <= 0) return null;
  const metadata = referenceMetadata.get(referenceId) ?? { creator: "", sourceIdentity: "" };
  const legacyRole = value?.kind === "counterexample" ? "counterexample" : "support";
  const role = (["support", "counterexample", "case_limit", "context"].includes(value?.role) ? value.role : legacyRole) as PatternEvidenceRole;
  const comparisonLevel = ([1, 2, 3, 4].includes(value?.comparisonLevel) ? value.comparisonLevel : 2) as 1 | 2 | 3 | 4;
  return {
    referenceId,
    creator: metadata.creator,
    sourceIdentity: metadata.sourceIdentity,
    role,
    comparisonLevel,
    requiredEvidenceObserved: value?.requiredEvidenceObserved !== false,
    confidence: (["low", "medium", "high"].includes(value?.confidence) ? value.confidence : "medium"),
    observation: typeof value?.observation === "string" ? value.observation : "",
    evidence: typeof value?.evidence === "string" ? value.evidence : "",
    limitations: Array.isArray(value?.limitations) ? value.limitations : [],
  };
}

export async function recordObservatoryHypotheses(
  referenceId: number,
  classification: { primaryFamily: string; objectives: string[]; segment: string },
  hypotheses: ObservatoryHypothesisInput[],
) {
  const db = await getDb();
  if (hypotheses.length === 0) return;
  if (!db) return memoryRecordObservatoryHypotheses(referenceId, classification, hypotheses);
  const existingPatterns = await db.select().from(observatoryPatterns);
  const referenceRows = await db.select({ id: observatoryReferences.id, creator: observatoryReferences.creator, sourceUrl: observatoryReferences.sourceUrl }).from(observatoryReferences);
  const referenceMetadata = new Map(referenceRows.map(reference => [
    reference.id,
    { creator: reference.creator, sourceIdentity: reference.creator || reference.sourceUrl || String(reference.id) },
  ]));
  const currentMetadata = referenceMetadata.get(referenceId) ?? { creator: "", sourceIdentity: String(referenceId) };
  const processed = new Set<string>();

  for (const hypothesis of hypotheses.slice(0, 5)) {
    const name = hypothesis.name.trim().slice(0, 180);
    const objective = (classification.objectives[0] || "indeterminado").slice(0, 160);
    const segment = (classification.segment || "indeterminado").slice(0, 160);
    const targetId = typeof hypothesis.targetPatternId === "number" ? hypothesis.targetPatternId : /^\d+$/.test(hypothesis.targetPatternId || "") ? Number(hypothesis.targetPatternId) : null;
    const fingerprint = [String(targetId ?? ""), name, classification.primaryFamily, objective, segment].map(normalizedPatternPart).join("|");
    if (!name || processed.has(fingerprint)) continue;
    processed.add(fingerprint);

    const existing = (targetId ? existingPatterns.find(pattern => pattern.id === targetId) : undefined) ?? existingPatterns.find(pattern =>
      normalizedPatternPart(pattern.name) === normalizedPatternPart(name) &&
      pattern.creativeFamily === classification.primaryFamily &&
      pattern.objective === objective &&
      pattern.segment === segment
    );
    const evidence: StoredPatternEvidence = {
      referenceId,
      creator: currentMetadata.creator,
      sourceIdentity: currentMetadata.sourceIdentity,
      role: hypothesis.evidenceRole,
      comparisonLevel: hypothesis.comparisonLevel,
      requiredEvidenceObserved: hypothesis.requiredEvidenceObserved,
      confidence: hypothesis.confidence,
      observation: hypothesis.observation,
      evidence: hypothesis.evidence,
      limitations: hypothesis.limitations,
    };
    const countableSupport = hypothesis.evidenceRole === "support" && hypothesis.comparisonLevel <= 2 && hypothesis.requiredEvidenceObserved && hypothesis.confidence !== "low";

    if (!existing) {
      if (!countableSupport) continue;
      const decision = decidePatternStageFromEvidence({ evidence: [evidence] });
      await db.insert(observatoryPatterns).values({
        name,
        patternType: hypothesis.patternType,
        stage: decision.stage,
        creativeFamily: classification.primaryFamily,
        objective,
        segment,
        mechanism: hypothesis.mechanism,
        conditionsJson: JSON.stringify(hypothesis.conditions),
        evidenceJson: JSON.stringify([evidence]),
        supportingCount: decision.supportingCount,
        counterexampleCount: decision.counterexampleCount,
        confidence: "low",
      });
      continue;
    }

    const previousEvidence = jsonArray(existing.evidenceJson)
      .map(item => normalizedStoredEvidence(item, referenceMetadata))
      .filter((item): item is StoredPatternEvidence => Boolean(item));
    const evidenceItems = [...previousEvidence.filter(item => Number(item.referenceId) !== referenceId), evidence].slice(-50);
    const decision = decidePatternStageFromEvidence({ evidence: evidenceItems, existingStage: existing.stage });
    await db.update(observatoryPatterns).set({
      stage: decision.stage,
      supportingCount: decision.supportingCount,
      counterexampleCount: decision.counterexampleCount,
      confidence: decision.stage === "experimentally_validated" || (decision.stage === "provisional" && decision.supportingCount >= 5 && decision.counterexampleCount === 0) ? "high" : decision.stage === "provisional" ? "medium" : "low",
      conditionsJson: JSON.stringify(Array.from(new Set([...jsonArray(existing.conditionsJson), ...hypothesis.conditions])).slice(0, 20)),
      evidenceJson: JSON.stringify(evidenceItems),
    }).where(eq(observatoryPatterns.id, existing.id));
  }
}
