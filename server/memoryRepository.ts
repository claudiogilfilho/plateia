import type {
  Analysis,
  InsertAnalysis,
  InsertInstagramConnection,
  InsertObservatoryReference,
  InsertUser,
  InstagramConnection,
  ObservatoryPattern,
  ObservatoryReference,
  User,
} from "../drizzle/schema";
import type { ObservatoryHypothesisInput } from "./db";

let analysisId = 1;
let instagramConnectionId = 1;
let referenceId = 1;
let patternId = 1;

const usersByOpenId = new Map<string, User>();
const analyses: Analysis[] = [];
const instagramConnections: InstagramConnection[] = [];
const references: ObservatoryReference[] = [];
const patterns: ObservatoryPattern[] = [];

export function resetMemoryRepository() {
  analysisId = 1;
  instagramConnectionId = 1;
  referenceId = 1;
  patternId = 1;
  usersByOpenId.clear();
  analyses.splice(0);
  instagramConnections.splice(0);
  references.splice(0);
  patterns.splice(0);
}

export function memoryUpsertUser(input: InsertUser) {
  const now = new Date();
  const current = usersByOpenId.get(input.openId);
  const next: User = {
    id: current?.id ?? usersByOpenId.size + 1,
    openId: input.openId,
    name: input.name ?? current?.name ?? null,
    email: input.email ?? current?.email ?? null,
    loginMethod: input.loginMethod ?? current?.loginMethod ?? null,
    role: input.role ?? current?.role ?? "user",
    createdAt: current?.createdAt ?? now,
    updatedAt: now,
    lastSignedIn: input.lastSignedIn ?? now,
  };
  usersByOpenId.set(input.openId, next);
}

export function memoryGetUser(openId: string) {
  return usersByOpenId.get(openId);
}

export function memoryCreateAnalysis(input: Omit<InsertAnalysis, "id" | "status" | "reportJson" | "createdAt" | "updatedAt">) {
  const now = new Date();
  const record: Analysis = {
    ...input,
    mediaUrl: input.mediaUrl ?? null,
    mediaKey: input.mediaKey ?? null,
    mediaMimeType: input.mediaMimeType ?? null,
    sourceUrl: input.sourceUrl ?? null,
    sourceKind: input.sourceKind ?? null,
    sourceMediaMimeType: input.sourceMediaMimeType ?? null,
    id: analysisId++,
    status: "processing",
    reportJson: null,
    createdAt: now,
    updatedAt: now,
  };
  analyses.push(record);
  return { id: record.id };
}

export function memoryUpdateAnalysisResult(id: number, status: Analysis["status"], report: unknown) {
  const record = analyses.find(item => item.id === id);
  if (!record) return;
  record.status = status;
  record.reportJson = report ? JSON.stringify(report) : null;
  record.updatedAt = new Date();
}

export function memoryListAnalyses(userId: number) {
  return analyses.filter(item => item.userId === userId).sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
}

export function memoryGetAnalysis(id: number, userId: number) {
  return analyses.find(item => item.id === id && item.userId === userId);
}

export function memoryGetInstagramConnection(userId: number) {
  return instagramConnections.filter(item => item.userId === userId).sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime())[0];
}

export function memorySaveInstagramConnection(userId: number, input: Omit<InsertInstagramConnection, "id" | "userId" | "createdAt" | "updatedAt">) {
  const now = new Date();
  const current = memoryGetInstagramConnection(userId);
  if (current) {
    Object.assign(current, input, { updatedAt: now });
    return;
  }
  instagramConnections.push({
    ...input,
    id: instagramConnectionId++,
    userId,
    instagramUserId: input.instagramUserId ?? null,
    username: input.username ?? null,
    accountType: input.accountType ?? "business",
    status: input.status ?? "ready",
    grantedScopes: input.grantedScopes ?? null,
    accessTokenEncrypted: input.accessTokenEncrypted ?? null,
    tokenExpiresAt: input.tokenExpiresAt ?? null,
    consentVersion: input.consentVersion ?? null,
    connectedAt: input.connectedAt ?? null,
    revokedAt: input.revokedAt ?? null,
    createdAt: now,
    updatedAt: now,
  });
}

export function memoryUpdateInstagramConnectionStatus(userId: number, status: InstagramConnection["status"]) {
  const current = memoryGetInstagramConnection(userId);
  if (current) Object.assign(current, { status, updatedAt: new Date() });
}

export function memoryCreateObservatoryReference(input: Omit<InsertObservatoryReference, "id" | "status" | "classificationJson" | "analysisJson" | "promptVersion" | "createdAt" | "updatedAt">) {
  const now = new Date();
  const record: ObservatoryReference = {
    ...input,
    sourceUrl: input.sourceUrl ?? null,
    mediaUrl: input.mediaUrl ?? null,
    mediaKey: input.mediaKey ?? null,
    mediaMimeType: input.mediaMimeType ?? null,
    metricsJson: input.metricsJson ?? null,
    id: referenceId++,
    status: "processing",
    classificationJson: null,
    analysisJson: null,
    promptVersion: "2.0",
    createdAt: now,
    updatedAt: now,
  };
  references.push(record);
  return { id: record.id };
}

export function memoryUpdateObservatoryReference(id: number, status: ObservatoryReference["status"], classification: unknown, analysis: unknown) {
  const record = references.find(item => item.id === id);
  if (!record) return;
  record.status = status;
  record.classificationJson = classification ? JSON.stringify(classification) : null;
  record.analysisJson = analysis ? JSON.stringify(analysis) : null;
  record.updatedAt = new Date();
}

export function memoryListObservatoryReferences(onlyAnalyzed = false) {
  return references
    .filter(item => !onlyAnalyzed || item.status === "analyzed")
    .sort((a, b) => b.createdAt.getTime() - a.createdAt.getTime());
}

export function memoryGetObservatoryReference(id: number) {
  return references.find(item => item.id === id);
}

export function memoryListActivePatterns() {
  return patterns
    .filter(item => item.stage === "provisional" || item.stage === "validated")
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());
}

function normalize(value: string) {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function readArray(value: string | null) {
  if (!value) return [];
  try { const parsed = JSON.parse(value); return Array.isArray(parsed) ? parsed : []; } catch { return []; }
}

export function memoryRecordObservatoryHypotheses(
  currentReferenceId: number,
  classification: { primaryFamily: string; objectives: string[]; segment: string },
  hypotheses: ObservatoryHypothesisInput[],
) {
  const processed = new Set<string>();
  for (const hypothesis of hypotheses.slice(0, 5)) {
    const name = hypothesis.name.trim().slice(0, 180);
    const objective = (classification.objectives[0] || "indeterminado").slice(0, 160);
    const segment = (classification.segment || "indeterminado").slice(0, 160);
    const fingerprint = [name, classification.primaryFamily, objective, segment].map(normalize).join("|");
    if (!name || processed.has(fingerprint)) continue;
    processed.add(fingerprint);
    const current = patterns.find(item => normalize(item.name) === normalize(name) && item.creativeFamily === classification.primaryFamily && item.objective === objective && item.segment === segment);
    const evidence = { referenceId: currentReferenceId, observation: hypothesis.observation, evidence: hypothesis.evidence, limitations: hypothesis.limitations };
    if (!current) {
      const now = new Date();
      patterns.push({
        id: patternId++, name, stage: hypothesis.stage === "contradicted" ? "contradicted" : "observation",
        creativeFamily: classification.primaryFamily, objective, segment, mechanism: hypothesis.mechanism,
        conditionsJson: JSON.stringify(hypothesis.conditions), evidenceJson: JSON.stringify([evidence]),
        supportingCount: hypothesis.stage === "contradicted" ? 0 : 1,
        counterexampleCount: hypothesis.stage === "contradicted" ? 1 : 0,
        confidence: "low", createdAt: now, updatedAt: now,
      });
      continue;
    }
    const counterexample = hypothesis.stage === "contradicted";
    const supportingCount = current.supportingCount + (counterexample ? 0 : 1);
    const counterexampleCount = current.counterexampleCount + (counterexample ? 1 : 0);
    const stage = counterexampleCount >= supportingCount && counterexampleCount >= 2 ? "contradicted" : current.stage === "validated" ? "validated" : supportingCount >= 3 ? "provisional" : "hypothesis";
    Object.assign(current, {
      stage, supportingCount, counterexampleCount,
      confidence: stage === "validated" || (stage === "provisional" && supportingCount >= 5) ? "high" : stage === "provisional" ? "medium" : "low",
      conditionsJson: JSON.stringify(Array.from(new Set([...readArray(current.conditionsJson), ...hypothesis.conditions])).slice(0, 20)),
      evidenceJson: JSON.stringify([...readArray(current.evidenceJson), evidence].slice(-20)),
      updatedAt: new Date(),
    });
  }
}
