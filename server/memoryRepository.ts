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
import { decidePatternStageFromEvidence, type PatternEvidenceCandidate, type PatternEvidenceRole } from "./patternEvidence";

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
    promptVersion: "3.0",
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
    .filter(item => item.stage === "provisional" || item.stage === "experimentally_validated")
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());
}

export function memoryListCandidatePatterns() {
  return patterns
    .filter(item => ["observation", "hypothesis", "supported_hypothesis", "provisional", "experimentally_validated"].includes(item.stage))
    .sort((a, b) => b.updatedAt.getTime() - a.updatedAt.getTime());
}

function normalize(value: string) {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function readArray(value: string | null) {
  if (!value) return [];
  try { const parsed = JSON.parse(value); return Array.isArray(parsed) ? parsed : []; } catch { return []; }
}

type StoredMemoryEvidence = PatternEvidenceCandidate & {
  observation?: string;
  evidence?: string;
  limitations?: string[];
  kind?: string;
};

function normalizeMemoryEvidence(value: any): StoredMemoryEvidence | null {
  const currentReference = references.find(reference => reference.id === Number(value?.referenceId));
  if (!currentReference) return null;
  const legacyRole = value?.kind === "counterexample" ? "counterexample" : "support";
  const role = (["support", "counterexample", "case_limit", "context"].includes(value?.role) ? value.role : legacyRole) as PatternEvidenceRole;
  return {
    referenceId: currentReference.id,
    creator: currentReference.creator,
    sourceIdentity: currentReference.creator || currentReference.sourceUrl || String(currentReference.id),
    role,
    comparisonLevel: ([1, 2, 3, 4].includes(value?.comparisonLevel) ? value.comparisonLevel : 2) as 1 | 2 | 3 | 4,
    requiredEvidenceObserved: value?.requiredEvidenceObserved !== false,
    confidence: (["low", "medium", "high"].includes(value?.confidence) ? value.confidence : "medium"),
    observation: typeof value?.observation === "string" ? value.observation : "",
    evidence: typeof value?.evidence === "string" ? value.evidence : "",
    limitations: Array.isArray(value?.limitations) ? value.limitations : [],
  };
}

export function memoryRecordObservatoryHypotheses(
  currentReferenceId: number,
  classification: { primaryFamily: string; objectives: string[]; segment: string },
  hypotheses: ObservatoryHypothesisInput[],
) {
  const currentReference = references.find(reference => reference.id === currentReferenceId);
  if (!currentReference) return;
  const processed = new Set<string>();

  for (const hypothesis of hypotheses.slice(0, 5)) {
    const name = hypothesis.name.trim().slice(0, 180);
    const objective = (classification.objectives[0] || "indeterminado").slice(0, 160);
    const segment = (classification.segment || "indeterminado").slice(0, 160);
    const targetId = typeof hypothesis.targetPatternId === "number" ? hypothesis.targetPatternId : /^\d+$/.test(hypothesis.targetPatternId || "") ? Number(hypothesis.targetPatternId) : null;
    const fingerprint = [String(targetId ?? ""), name, classification.primaryFamily, objective, segment].map(normalize).join("|");
    if (!name || processed.has(fingerprint)) continue;
    processed.add(fingerprint);

    const current = (targetId ? patterns.find(item => item.id === targetId) : undefined) ?? patterns.find(item =>
      normalize(item.name) === normalize(name) &&
      item.creativeFamily === classification.primaryFamily &&
      item.objective === objective &&
      item.segment === segment
    );
    const evidence: StoredMemoryEvidence = {
      referenceId: currentReferenceId,
      creator: currentReference.creator,
      sourceIdentity: currentReference.creator || currentReference.sourceUrl || String(currentReferenceId),
      role: hypothesis.evidenceRole,
      comparisonLevel: hypothesis.comparisonLevel,
      requiredEvidenceObserved: hypothesis.requiredEvidenceObserved,
      confidence: hypothesis.confidence,
      observation: hypothesis.observation,
      evidence: hypothesis.evidence,
      limitations: hypothesis.limitations,
    };
    const countableSupport = hypothesis.evidenceRole === "support" && hypothesis.comparisonLevel <= 2 && hypothesis.requiredEvidenceObserved && hypothesis.confidence !== "low";

    if (!current) {
      if (!countableSupport) continue;
      const now = new Date();
      const decision = decidePatternStageFromEvidence({ evidence: [evidence] });
      patterns.push({
        id: patternId++,
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
        createdAt: now,
        updatedAt: now,
      });
      continue;
    }

    const previousEvidence = readArray(current.evidenceJson)
      .map(normalizeMemoryEvidence)
      .filter((item): item is StoredMemoryEvidence => Boolean(item));
    const evidenceItems = [...previousEvidence.filter(item => Number(item.referenceId) !== currentReferenceId), evidence].slice(-50);
    const decision = decidePatternStageFromEvidence({ evidence: evidenceItems, existingStage: current.stage });
    Object.assign(current, {
      stage: decision.stage,
      supportingCount: decision.supportingCount,
      counterexampleCount: decision.counterexampleCount,
      confidence: decision.stage === "experimentally_validated" || (decision.stage === "provisional" && decision.supportingCount >= 5 && decision.counterexampleCount === 0) ? "high" : decision.stage === "provisional" ? "medium" : "low",
      conditionsJson: JSON.stringify(Array.from(new Set([...readArray(current.conditionsJson), ...hypothesis.conditions])).slice(0, 20)),
      evidenceJson: JSON.stringify(evidenceItems),
      updatedAt: new Date(),
    });
  }
}
