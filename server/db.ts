import { and, desc, eq, inArray } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { Analysis, InsertAnalysis, InsertInstagramConnection, InsertObservatoryReference, InsertUser, InstagramConnection, ObservatoryReference, analyses, instagramConnections, observatoryPatterns, observatoryReferences, users } from "../drizzle/schema";
import { ENV } from './_core/env';
import { buildRevokedInstagramConnectionPatch } from "./instagramIntegration";
import {
  memoryCreateAnalysis,
  memoryCreateObservatoryReference,
  memoryGetAnalysis,
  memoryGetInstagramConnection,
  memoryGetObservatoryReference,
  memoryGetUser,
  memoryListActivePatterns,
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
    .where(inArray(observatoryPatterns.stage, ["provisional", "validated"]))
    .orderBy(desc(observatoryPatterns.updatedAt));
}

export type ObservatoryHypothesisInput = {
  name: string;
  observation: string;
  mechanism: string;
  evidence: string;
  conditions: string[];
  limitations: string[];
  confidence: "low" | "medium" | "high";
  stage: "observation" | "hypothesis" | "provisional" | "validated" | "contradicted" | "obsolete";
};

function jsonArray(value: string | null) {
  if (!value) return [];
  try { const parsed = JSON.parse(value); return Array.isArray(parsed) ? parsed : []; } catch { return []; }
}

function normalizedPatternPart(value: string) {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
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
  const processed = new Set<string>();
  for (const hypothesis of hypotheses.slice(0, 5)) {
    const name = hypothesis.name.trim().slice(0, 180);
    const objective = (classification.objectives[0] || "indeterminado").slice(0, 160);
    const segment = (classification.segment || "indeterminado").slice(0, 160);
    const fingerprint = [name, classification.primaryFamily, objective, segment].map(normalizedPatternPart).join("|");
    if (!name || processed.has(fingerprint)) continue;
    processed.add(fingerprint);
    const existing = existingPatterns.find(pattern =>
      normalizedPatternPart(pattern.name) === normalizedPatternPart(name) &&
      pattern.creativeFamily === classification.primaryFamily && pattern.objective === objective && pattern.segment === segment
    );
    const evidence = { referenceId, observation: hypothesis.observation, evidence: hypothesis.evidence, limitations: hypothesis.limitations };
    if (!existing) {
      await db.insert(observatoryPatterns).values({
        name,
        stage: hypothesis.stage === "contradicted" ? "contradicted" : "observation",
        creativeFamily: classification.primaryFamily,
        objective,
        segment,
        mechanism: hypothesis.mechanism,
        conditionsJson: JSON.stringify(hypothesis.conditions),
        evidenceJson: JSON.stringify([evidence]),
        supportingCount: hypothesis.stage === "contradicted" ? 0 : 1,
        counterexampleCount: hypothesis.stage === "contradicted" ? 1 : 0,
        confidence: "low",
      });
      continue;
    }
    const isCounterexample = hypothesis.stage === "contradicted";
    const supportingCount = existing.supportingCount + (isCounterexample ? 0 : 1);
    const counterexampleCount = existing.counterexampleCount + (isCounterexample ? 1 : 0);
    const stage = counterexampleCount >= supportingCount && counterexampleCount >= 2
      ? "contradicted" as const
      : existing.stage === "validated" ? "validated" as const
      : supportingCount >= 3 ? "provisional" as const : "hypothesis" as const;
    await db.update(observatoryPatterns).set({
      stage,
      supportingCount,
      counterexampleCount,
      confidence: stage === "validated" || (stage === "provisional" && supportingCount >= 5) ? "high" : stage === "provisional" ? "medium" : "low",
      conditionsJson: JSON.stringify(Array.from(new Set([...jsonArray(existing.conditionsJson), ...hypothesis.conditions])).slice(0, 20)),
      evidenceJson: JSON.stringify([...jsonArray(existing.evidenceJson), evidence].slice(-20)),
    }).where(eq(observatoryPatterns.id, existing.id));
  }
}
