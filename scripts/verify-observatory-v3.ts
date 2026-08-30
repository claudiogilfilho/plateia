import { decidePatternStage, decidePatternStageFromEvidence } from "../server/patternEvidence";
import { listPortablePatterns, listPortableReferences, PORTABLE_MEMORY_STATS } from "../server/portableObservatoryMemory";
import { assessViralityEvidence, safeRate } from "../server/virality";
import { canonicalPublicUrl } from "../server/publicUrlIdentity";
import { auditObservatoryMemory } from "../server/observatoryMemoryAudit";

const references = listPortableReferences();
const audit = auditObservatoryMemory();
const portablePatterns = listPortablePatterns();
const caseLimitDecision = decidePatternStageFromEvidence({ evidence: [
  { referenceId: "support", creator: "A", sourceIdentity: "A", role: "support", comparisonLevel: 1, requiredEvidenceObserved: true, confidence: "medium" },
  { referenceId: "limit-1", creator: "B", sourceIdentity: "B", role: "case_limit", comparisonLevel: 2, requiredEvidenceObserved: false, confidence: "medium" },
  { referenceId: "limit-2", creator: "C", sourceIdentity: "C", role: "case_limit", comparisonLevel: 2, requiredEvidenceObserved: false, confidence: "medium" },
  { referenceId: "limit-3", creator: "D", sourceIdentity: "D", role: "case_limit", comparisonLevel: 2, requiredEvidenceObserved: false, confidence: "medium" },
] });
const incompleteDecision = decidePatternStageFromEvidence({ evidence: [
  { referenceId: "incomplete", creator: "A", sourceIdentity: "A", role: "support", comparisonLevel: 1, requiredEvidenceObserved: false, confidence: "high" },
] });
const checks = {
  preservesTrainedCorpus: references.length >= 35,
  portableCountMatchesRawMemory: references.length === PORTABLE_MEMORY_STATS.referenceCount,
  allUrlsAreUnique: new Set(references.map(reference => canonicalPublicUrl(reference.sourceUrl))).size === references.length,
  rawTaxonomyAndPatternIntegrity: audit.issues.length === 0,
  taxonomyIsV3: PORTABLE_MEMORY_STATS.taxonomyVersion === "3.0",
  safeRateWorks: safeRate(20, 1000) === 0.02 && safeRate(20, 0) === null,
  noFalseVirality: assessViralityEvidence({ viewsObserved: "3,1 mi" }).status === "indeterminate",
  creatorDiversityRequired: decidePatternStage({ supportingCount: 3, counterexampleCount: 0, supportingCreators: ["A", "A", "A"] }).stage === "supported_hypothesis",
  independentSupportPromotes: decidePatternStage({ supportingCount: 3, counterexampleCount: 0, supportingCreators: ["A", "B", "A"] }).stage === "provisional",
  caseLimitsDoNotCountAsCounterexamples: caseLimitDecision.stage === "observation" && caseLimitDecision.supportingCount === 1 && caseLimitDecision.counterexampleCount === 0 && caseLimitDecision.caseLimitCount === 3,
  incompleteEvidenceDoesNotSupport: incompleteDecision.supportingCount === 0 && incompleteDecision.stage === "hypothesis",
  isolatedHypothesesAreRetrievable: portablePatterns.length >= PORTABLE_MEMORY_STATS.patternCount + PORTABLE_MEMORY_STATS.hypothesisCount && portablePatterns.some(pattern => pattern.id === "hyp-20260830-033"),
};

const failed = Object.entries(checks).filter(([, passed]) => !passed).map(([name]) => name);
if (failed.length) throw new Error(`Verificação v3 falhou: ${failed.join(", ")}${audit.issues.length ? ` | ${audit.issues.join(", ")}` : ""}`);
console.log(JSON.stringify({ ok: true, checks, references: references.length, patterns: audit.patternCount }, null, 2));
