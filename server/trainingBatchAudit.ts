export const CONCENTRATED_BATCH_POLICY_VERSION = "1.1";

type ClaimCoverage = {
  requiredModalities?: unknown;
  observedModalities?: unknown;
  sufficient?: unknown;
};

type TrainingReference = {
  id?: string;
  url?: string;
  training?: {
    evidencePolicyVersion?: string;
    supportEligible?: boolean;
    requiredEvidenceObserved?: boolean;
    claimCoverage?: ClaimCoverage[];
    provenanceAndConsent?: {
      storyOrigin?: string;
      consentStatus?: string;
      identityProtection?: string;
      evidence?: string[];
    };
  };
};

type TrainingRun = {
  id?: string;
  batchPolicyVersion?: string;
  requestedBatchSize?: number;
  candidatesFound?: number;
  analyzed?: number;
  referenceIds?: string[];
  targetReferenceIds?: string[];
  falsificationOrBoundaryReferenceIds?: string[];
  controlledExplorationReferenceIds?: string[];
  targetKnowledgeId?: string;
  hypothesesCreated?: string[];
  validatedPatternsCreated?: number;
  validationEvidence?: { humanReviewId?: string; experimentId?: string };
};

const unique = (values: string[]) => new Set(values).size === values.length;
const clean = (value: unknown) => Array.isArray(value) ? value.filter(item => typeof item === "string" && item.trim()) as string[] : [];

function claimCoverageIsSound(reference: TrainingReference) {
  const claims = reference.training?.claimCoverage;
  if (!Array.isArray(claims) || !claims.length) return false;
  return claims.every(claim => {
    const required = new Set(clean(claim.requiredModalities));
    const observed = new Set(clean(claim.observedModalities));
    const actuallySufficient = required.size > 0 && Array.from(required).every(item => observed.has(item));
    return claim.sufficient === actuallySufficient;
  });
}

function provenanceIsExplicit(reference: TrainingReference) {
  const value = reference.training?.provenanceAndConsent;
  return Boolean(value?.storyOrigin && value?.consentStatus && value?.identityProtection && Array.isArray(value.evidence));
}

export function auditConcentratedTrainingRun(run: TrainingRun, references: TrainingReference[]) {
  const issues: string[] = [];
  if (run.batchPolicyVersion !== CONCENTRATED_BATCH_POLICY_VERSION) return issues;

  const id = run.id || "training-run-without-id";
  const referenceIds = clean(run.referenceIds);
  const targetIds = clean(run.targetReferenceIds);
  const boundaryIds = clean(run.falsificationOrBoundaryReferenceIds);
  const explorationIds = clean(run.controlledExplorationReferenceIds);
  const roleIds = [...targetIds, ...boundaryIds, ...explorationIds];
  const referenceById = new Map(references.map(reference => [String(reference.id), reference]));

  if (!run.targetKnowledgeId) issues.push(`${id}.targetKnowledgeId`);
  if ((run.candidatesFound ?? 0) < 15) issues.push(`${id}.candidatePoolMinimum`);
  if (targetIds.length < 3) issues.push(`${id}.targetReferenceQuota`);
  if (boundaryIds.length < 1) issues.push(`${id}.boundaryReferenceQuota`);
  if (explorationIds.length < 1) issues.push(`${id}.explorationReferenceQuota`);
  if ((run.hypothesesCreated?.length ?? 0) > 1) issues.push(`${id}.newHypothesisLimit`);
  if (!unique(referenceIds) || !unique(roleIds)) issues.push(`${id}.duplicateReferenceRole`);
  if (referenceIds.length !== Number(run.analyzed ?? run.requestedBatchSize ?? 0)) issues.push(`${id}.referenceCount`);
  if (new Set(roleIds).size !== referenceIds.length || referenceIds.some(referenceId => !roleIds.includes(referenceId))) issues.push(`${id}.roleCoverage`);
  if (referenceIds.some(referenceId => !referenceById.has(referenceId))) issues.push(`${id}.unknownReference`);

  const urls = referenceIds.map(referenceId => referenceById.get(referenceId)?.url?.trim()).filter(Boolean);
  if (new Set(urls).size !== urls.length) issues.push(`${id}.duplicateUrl`);

  for (const referenceId of referenceIds) {
    const reference = referenceById.get(referenceId);
    if (!reference) continue;
    if (reference.training?.evidencePolicyVersion !== CONCENTRATED_BATCH_POLICY_VERSION) issues.push(`${referenceId}.evidencePolicyVersion`);
    if (!claimCoverageIsSound(reference)) issues.push(`${referenceId}.claimCoverage`);
    if (!provenanceIsExplicit(reference)) issues.push(`${referenceId}.provenanceAndConsent`);
    if (reference.training?.supportEligible && (!reference.training.requiredEvidenceObserved || reference.training.claimCoverage?.some(claim => claim.sufficient !== true))) issues.push(`${referenceId}.ineligibleSupport`);
  }

  const hasValidationEvidence = Boolean(run.validationEvidence?.humanReviewId || run.validationEvidence?.experimentId);
  if ((run.validatedPatternsCreated ?? 0) > 0 && !hasValidationEvidence) issues.push(`${id}.automaticValidation`);
  return issues;
}
