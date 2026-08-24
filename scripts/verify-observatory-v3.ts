import { decidePatternStage } from "../server/patternEvidence";
import { listPortableReferences, PORTABLE_MEMORY_STATS } from "../server/portableObservatoryMemory";
import { assessViralityEvidence, safeRate } from "../server/virality";
import { canonicalPublicUrl } from "../server/publicUrlIdentity";
import { auditObservatoryMemory } from "../server/observatoryMemoryAudit";

const references = listPortableReferences();
const audit = auditObservatoryMemory();
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
};

const failed = Object.entries(checks).filter(([, passed]) => !passed).map(([name]) => name);
if (failed.length) throw new Error(`Verificação v3 falhou: ${failed.join(", ")}${audit.issues.length ? ` | ${audit.issues.join(", ")}` : ""}`);
console.log(JSON.stringify({ ok: true, checks, references: references.length, patterns: audit.patternCount }, null, 2));
