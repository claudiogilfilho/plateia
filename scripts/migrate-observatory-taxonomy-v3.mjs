import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { dirname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const memoryPath = resolve(root, "knowledge/observatory/plateia-memory.json");
const reportPath = resolve(root, "knowledge/observatory/migrations/taxonomy-v3-report.json");
const write = process.argv.includes("--write");
const memory = JSON.parse(readFileSync(memoryPath, "utf8"));
const migrationId = "taxonomy-v3-2026-08-24";

const aliases = {
  materialFormat: { short_vertical: "video_curto", video_exact_duration_unknown: "outro" },
  presentationFormat: { explicativo: "outro", storytelling: "outro", humor: "outro", curiosidade: "outro", review: "comentario", sketch: "esquete", recorte_entrevista: "podcast_entrevista", cobertura_evento: "reportagem", celebridades: "outro", rua: "outro", personagem_de_marca: "personagem_marca", serial: "outro", branded_content: "produto", desafio_serial: "desafio" },
  objective: { acao: "outro", entretenimento: "visualizacao", entreter: "visualizacao", venda_indireta: "venda", consciencia_solucao: "apresentar_solucao", decisao_compra: "venda", atualidade: "alcance", posicionamento_marca: "marca" },
  mechanism: { "confiança": "confianca", descoberta: "curiosidade", comunidade: "pertencimento" },
};

const ambiguous = [];
const appliedAliases = {};
const recordAlias = (axis, from, to, id) => {
  if (from === to) return;
  const key = `${axis}:${from}->${to}`;
  appliedAliases[key] = (appliedAliases[key] || 0) + 1;
  if (to === "outro") ambiguous.push({ referenceId: id, axis, sourceValue: from, migratedValue: to, requiresHumanReview: true });
};
const mapOne = (axis, value, id) => {
  if (typeof value !== "string") return value;
  const mapped = aliases[axis]?.[value] ?? value;
  recordAlias(axis, value, mapped, id);
  return mapped;
};
const mapMany = (axis, values, id) => Array.isArray(values) ? [...new Set(values.map(value => mapOne(axis, value, id)))] : [];
const containerFromUrl = url => {
  if (/youtube\.com\/shorts|youtu\.be/i.test(url)) return /shorts/i.test(url) ? "youtube_short" : "youtube_video";
  if (/youtube\.com/i.test(url)) return "youtube_video";
  if (/tiktok\.com/i.test(url)) return "tiktok";
  if (/instagram\.com\/reel/i.test(url)) return "instagram_reel";
  if (/instagram\.com/i.test(url)) return "instagram_post";
  if (/facebook\.com/i.test(url)) return "facebook_reel";
  return "webpage";
};
const durationBand = (duration, legacy) => {
  if (legacy && ["up_to_15s", "16_to_30s", "31_to_60s", "over_60s", "not_applicable", "unknown"].includes(legacy)) return legacy;
  const match = typeof duration === "string" && duration.match(/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/);
  if (!match) return "unknown";
  const seconds = Number(match[1] || 0) * 3600 + Number(match[2] || 0) * 60 + Number(match[3] || 0);
  return seconds <= 15 ? "up_to_15s" : seconds <= 30 ? "16_to_30s" : seconds <= 60 ? "31_to_60s" : "over_60s";
};
const inferAdType = classification => {
  const presentations = classification.presentationFormats || [];
  const families = [classification.primaryFamily, ...(classification.secondaryFamilies || [])];
  if (presentations.includes("produto") || families.includes("oferta_direta")) return "produto";
  if (families.includes("institucional") || families.includes("posicionamento_marca")) return "conteudo_de_marca";
  return "indeterminado";
};
const inferPatternType = pattern => {
  const value = `${pattern.name || pattern.statement || ""} ${Array.isArray(pattern.mechanism) ? pattern.mechanism.join(" ") : pattern.mechanism || ""}`.toLocaleLowerCase("pt-BR");
  if (/gancho|primeiros segundos|abertura/.test(value)) return "gancho";
  if (/reten|progress|continuidade|recapitular/.test(value)) return "retencao";
  if (/prova|autoridade|credibilidade/.test(value)) return "prova";
  if (/cta|chamada|participa|coment/.test(value)) return "cta";
  if (/curios|pergunta|contradi/.test(value)) return "curiosidade";
  if (/confian|cético|obje/.test(value)) return "confianca";
  return "outro";
};

memory.references = (memory.references || []).map(reference => {
  const legacy = reference.classification || {};
  if (legacy.taxonomyVersion === "3.0" && reference.migration?.id === migrationId) return reference;
  const materialFormat = mapOne("materialFormat", legacy.materialFormat, reference.id) || "indeterminado";
  const presentationFormats = mapMany("presentationFormat", legacy.presentationFormats, reference.id);
  const objectives = mapMany("objective", legacy.objectives, reference.id);
  const mechanisms = mapMany("mechanism", legacy.mechanisms, reference.id);
  const adType = inferAdType({ ...legacy, presentationFormats });
  const commercial = adType === "indeterminado" ? "indeterminada" : "implicita";
  const needsHumanReview = Boolean(legacy.needsHumanReview) || ambiguous.some(item => item.referenceId === reference.id);
  return {
    ...reference,
    classification: {
      taxonomyVersion: "3.0",
      container: containerFromUrl(reference.url || ""),
      materialFormat,
      presentationFormats: presentationFormats.length ? presentationFormats : ["indeterminado"],
      primaryFamily: legacy.primaryFamily || "indeterminado",
      secondaryFamilies: legacy.secondaryFamilies || [],
      functionalMix: [{ family: legacy.primaryFamily || "indeterminado", percentage: 100 }],
      objectives: objectives.length ? objectives : ["indeterminado"],
      advertisingType: adType,
      commercialIntent: commercial,
      advertisedEntity: { kind: "indeterminado", name: "", confidence: "low" },
      contentTopic: { label: legacy.segment || "indeterminado", iabCode: null },
      segment: legacy.segment || "indeterminado",
      subsegment: legacy.subsegment || "indeterminado",
      probableAudience: legacy.probableAudience || "indeterminado",
      awarenessStage: legacy.awarenessStage || "indeterminado",
      productionLevel: legacy.productionLevel || "unknown",
      creatorScale: "unknown",
      replicability: reference.training?.replicable?.length || reference.replicable?.length ? "medium" : "unknown",
      durationBand: durationBand(reference.duration, legacy.durationBand),
      pace: legacy.pace || "unknown",
      mechanisms,
      hookTypes: [],
      narrativeElements: [],
      proofTypes: [],
      ctaTypes: [],
      distributionContext: { organicPaid: "unknown", trendDependency: "unknown" },
      confidence: legacy.confidence || "low",
      evidence: legacy.evidence || [],
      alternativeClassifications: legacy.alternativeClassifications || [],
      missingInformation: [...new Set([...(legacy.missingInformation || []), ...(needsHumanReview ? ["classificação legada ambígua requer revisão humana"] : [])])],
      needsHumanReview,
    },
    migration: { id: migrationId, legacyClassification: legacy, reversibleViaGit: true },
  };
});

const creatorsByReference = new Map(memory.references.map(reference => [reference.id, reference.creator || ""]));
const patternChanges = [];
memory.patterns = (memory.patterns || []).map(pattern => {
  const supportIds = pattern.supportReferenceIds || pattern.evidence?.map(item => item.referenceId).filter(Boolean) || [];
  const creatorDiversityCount = new Set(supportIds.map(id => creatorsByReference.get(id)).filter(Boolean).map(value => value.toLocaleLowerCase("pt-BR"))).size;
  const supportingCount = Number(pattern.supportingCount ?? pattern.comparableSupportCount ?? supportIds.length) || 0;
  let stage = pattern.stage || pattern.status || "hypothesis";
  if (stage === "validated") stage = "experimentally_validated";
  if (stage === "obsolete") stage = "archived";
  if (stage === "provisional" && (supportingCount < 3 || creatorDiversityCount < 2)) stage = "supported_hypothesis";
  if (stage !== (pattern.stage || pattern.status)) patternChanges.push({ patternId: pattern.id, from: pattern.stage || pattern.status, to: stage, reason: "mínimo de 3 referências comparáveis e 2 criadores independentes" });
  return { ...pattern, taxonomyVersion: "3.0", patternType: pattern.patternType || inferPatternType(pattern), stage, status: stage, supportingCount, creatorDiversityCount, sourceDiversityCount: creatorDiversityCount, validation: stage === "experimentally_validated" ? pattern.validation : "requires_human_or_experimental_evidence" };
});

memory.taxonomyVersion = "3.0";
memory.policy = { ...(memory.policy || {}), provisionalMinimumComparableSupport: 3, provisionalMinimumIndependentCreators: 2, validatedRequiresHumanOrExperimentalEvidence: true, missingIsNotZero: true, absoluteViewsDoNotDefineVirality: true, viralityRequiresRelativeBaseline: true };
memory.migrationHistory = [...(memory.migrationHistory || []).filter(item => item.id !== migrationId), { id: migrationId, migratedAt: "2026-08-24T12:00:00.000Z", referenceCount: memory.references.length, reversibleViaGit: true, legacySnapshot: "reference.migration.legacyClassification" }];
memory.updatedAt = "2026-08-24T12:00:00.000Z";

const previousReport = existsSync(reportPath) ? JSON.parse(readFileSync(reportPath, "utf8")) : {};
const report = {
  migrationId,
  taxonomyVersion: "3.0",
  mode: write ? "write" : "check",
  referencesInspected: memory.references.length,
  patternsInspected: memory.patterns.length,
  aliasesApplied: Object.keys(appliedAliases).length ? appliedAliases : previousReport.aliasesApplied || {},
  ambiguousClassifications: ambiguous.length ? ambiguous : previousReport.ambiguousClassifications || [],
  patternStageChanges: patternChanges.length ? patternChanges : previousReport.patternStageChanges || [],
  guarantees: ["nenhuma referência removida", "URLs preservadas", "classificação anterior preservada por referência", "migração idempotente", "reversível por Git"],
};

if (write) {
  mkdirSync(dirname(reportPath), { recursive: true });
  writeFileSync(memoryPath, `${JSON.stringify(memory, null, 2)}\n`);
  writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
}
console.log(JSON.stringify(report, null, 2));
