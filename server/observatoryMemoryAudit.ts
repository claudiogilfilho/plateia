import memory from "../knowledge/observatory/plateia-memory.json";
import {
  ADVERTISING_TYPES, AWARENESS_STAGES, COMMERCIAL_INTENTS, CONTAINERS, CREATIVE_FAMILIES,
  CTA_TYPES, DURATION_BANDS, HOOK_TYPES, MATERIAL_FORMATS, MECHANISMS, NARRATIVE_ELEMENTS,
  OBJECTIVES, PACES, PATTERN_TYPES, PRESENTATION_FORMATS, PRODUCTION_LEVELS, PROOF_TYPES,
} from "../shared/plateiaTaxonomy";
import { decidePatternStage } from "./patternEvidence";
import { canonicalPublicUrl } from "./publicUrlIdentity";

type RawClassification = Record<string, any>;
type RawReference = { id?: string; url?: string; creator?: string; classification?: RawClassification };
type RawPattern = { id?: string; stage?: string; status?: string; patternType?: string; mechanism?: string[]; supportReferenceIds?: string[]; supportingCount?: number; comparableSupportCount?: number; counterexampleCount?: number; creatorDiversityCount?: number };

const allowed = (values: readonly string[]) => new Set(values);
const allowedValues = {
  container: allowed(CONTAINERS), materialFormat: allowed(MATERIAL_FORMATS), presentationFormats: allowed(PRESENTATION_FORMATS),
  primaryFamily: allowed(CREATIVE_FAMILIES), secondaryFamilies: allowed(CREATIVE_FAMILIES), objectives: allowed(OBJECTIVES),
  advertisingType: allowed(ADVERTISING_TYPES), commercialIntent: allowed(COMMERCIAL_INTENTS), awarenessStage: allowed(AWARENESS_STAGES),
  productionLevel: allowed(PRODUCTION_LEVELS), durationBand: allowed(DURATION_BANDS), pace: allowed(PACES), mechanisms: allowed(MECHANISMS),
  hookTypes: allowed(HOOK_TYPES), narrativeElements: allowed(NARRATIVE_ELEMENTS), proofTypes: allowed(PROOF_TYPES), ctaTypes: allowed(CTA_TYPES),
};

const checkScalar = (issues: string[], id: string, field: keyof typeof allowedValues, value: unknown) => {
  if (typeof value !== "string" || !allowedValues[field].has(value)) issues.push(`${id}.${field}:${String(value)}`);
};
const checkList = (issues: string[], id: string, field: keyof typeof allowedValues, value: unknown, min: number, max: number) => {
  if (!Array.isArray(value) || value.length < min || value.length > max) return issues.push(`${id}.${field}.cardinality`);
  for (const item of value) if (typeof item !== "string" || !allowedValues[field].has(item)) issues.push(`${id}.${field}:${String(item)}`);
  if (new Set(value).size !== value.length) issues.push(`${id}.${field}.duplicates`);
};

export function auditObservatoryMemory() {
  const issues: string[] = [];
  const references = ((memory as any).references ?? []) as RawReference[];
  const patterns = ((memory as any).patterns ?? []) as RawPattern[];
  const referenceIds = new Set<string>();
  const urls = new Set<string>();
  const referenceById = new Map<string, RawReference>();

  for (const reference of references) {
    const id = reference.id?.trim() || "reference-without-id";
    if (referenceIds.has(id)) issues.push(`${id}.duplicateId`);
    referenceIds.add(id);
    referenceById.set(id, reference);
    const url = canonicalPublicUrl(reference.url ?? "");
    if (!url) issues.push(`${id}.missingUrl`);
    else if (urls.has(url)) issues.push(`${id}.duplicateUrl`);
    else urls.add(url);

    const classification = reference.classification ?? {};
    if (classification.taxonomyVersion !== "3.0") issues.push(`${id}.taxonomyVersion`);
    checkScalar(issues, id, "container", classification.container);
    checkScalar(issues, id, "materialFormat", classification.materialFormat);
    checkList(issues, id, "presentationFormats", classification.presentationFormats, 1, 3);
    if (classification.presentationFormats?.includes("outro") && classification.presentationFormats.length > 1) issues.push(`${id}.presentationFormats.redundantOutro`);
    checkScalar(issues, id, "primaryFamily", classification.primaryFamily);
    checkList(issues, id, "secondaryFamilies", classification.secondaryFamilies, 0, 2);
    checkList(issues, id, "objectives", classification.objectives, 1, 4);
    checkScalar(issues, id, "advertisingType", classification.advertisingType);
    checkScalar(issues, id, "commercialIntent", classification.commercialIntent);
    checkScalar(issues, id, "awarenessStage", classification.awarenessStage);
    checkScalar(issues, id, "productionLevel", classification.productionLevel);
    checkScalar(issues, id, "durationBand", classification.durationBand);
    checkScalar(issues, id, "pace", classification.pace);
    checkList(issues, id, "mechanisms", classification.mechanisms, 0, 6);
    checkList(issues, id, "hookTypes", classification.hookTypes, 0, 5);
    checkList(issues, id, "narrativeElements", classification.narrativeElements, 0, 10);
    checkList(issues, id, "proofTypes", classification.proofTypes, 0, 6);
    checkList(issues, id, "ctaTypes", classification.ctaTypes, 0, 4);
    const mix = Array.isArray(classification.functionalMix) ? classification.functionalMix : [];
    if (mix.length < 1 || mix.length > 3 || mix.reduce((sum: number, item: any) => sum + Number(item?.percentage || 0), 0) !== 100) issues.push(`${id}.functionalMix`);
    for (const item of mix) if (!allowedValues.primaryFamily.has(item?.family) || !Number.isInteger(item?.percentage) || item.percentage < 1 || item.percentage > 100) issues.push(`${id}.functionalMix:${String(item?.family)}`);
    const entity = classification.advertisedEntity ?? {};
    if (!["produto", "servico", "marca", "causa", "pessoa", "nenhuma", "indeterminado"].includes(entity.kind) || typeof entity.name !== "string") issues.push(`${id}.advertisedEntity`);
  }

  for (const pattern of patterns) {
    const id = pattern.id ?? "pattern-without-id";
    const supportIds = Array.from(new Set(pattern.supportReferenceIds ?? []));
    if (supportIds.some(referenceId => !referenceById.has(referenceId))) issues.push(`${id}.unknownSupportReference`);
    if (Number(pattern.supportingCount ?? pattern.comparableSupportCount ?? 0) !== supportIds.length) issues.push(`${id}.supportingCount`);
    if (!PATTERN_TYPES.includes(pattern.patternType as any)) issues.push(`${id}.patternType`);
    if (!Array.isArray(pattern.mechanism) || pattern.mechanism.some(value => !allowedValues.mechanisms.has(value))) issues.push(`${id}.mechanism`);
    const creators = supportIds.map(referenceId => referenceById.get(referenceId)?.creator ?? "");
    const expected = decidePatternStage({ supportingCount: supportIds.length, counterexampleCount: Number(pattern.counterexampleCount) || 0, supportingCreators: creators, existingStage: pattern.stage ?? pattern.status });
    if (pattern.creatorDiversityCount !== expected.creatorDiversityCount) issues.push(`${id}.creatorDiversityCount`);
    if ((pattern.stage ?? pattern.status) !== expected.stage) issues.push(`${id}.stage`);
  }

  return { issues, referenceCount: references.length, uniqueUrlCount: urls.size, patternCount: patterns.length };
}
