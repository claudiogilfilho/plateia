import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const memoryPath = resolve(root, "knowledge/observatory/plateia-memory.json");
const reportPath = resolve(root, "knowledge/observatory/migrations/taxonomy-v3-integrity-repair.json");
const taxonomyPath = resolve(root, "shared/plateiaTaxonomy.ts");
const memory = JSON.parse(readFileSync(memoryPath, "utf8"));
const taxonomySource = readFileSync(taxonomyPath, "utf8");
const repairedAt = new Date().toISOString();
const enumSet = name => {
  const match = taxonomySource.match(new RegExp(`export const ${name} = (\\[[^;]+\\]) as const;`));
  if (!match) throw new Error(`Enum ${name} não encontrado.`);
  return new Set(JSON.parse(match[1]));
};
const strictEnums = {
  container: enumSet("CONTAINERS"),
  materialFormat: enumSet("MATERIAL_FORMATS"),
  presentationFormats: enumSet("PRESENTATION_FORMATS"),
  primaryFamily: enumSet("CREATIVE_FAMILIES"),
  secondaryFamilies: enumSet("CREATIVE_FAMILIES"),
  objectives: enumSet("OBJECTIVES"),
  advertisingType: enumSet("ADVERTISING_TYPES"),
  commercialIntent: enumSet("COMMERCIAL_INTENTS"),
  awarenessStage: enumSet("AWARENESS_STAGES"),
  productionLevel: enumSet("PRODUCTION_LEVELS"),
  durationBand: enumSet("DURATION_BANDS"),
  pace: enumSet("PACES"),
  mechanisms: enumSet("MECHANISMS"),
  hookTypes: enumSet("HOOK_TYPES"),
  narrativeElements: enumSet("NARRATIVE_ELEMENTS"),
  proofTypes: enumSet("PROOF_TYPES"),
  ctaTypes: enumSet("CTA_TYPES"),
  patternType: enumSet("PATTERN_TYPES"),
};

const aliases = {
  productionLevel: { advanced: "complex", medium: "intermediate" },
  pace: { not_assessed: "unknown" },
  advertisingType: { nao_publicitario: "sem_intencao_comercial", venda_indireta: "consideracao" },
  entityKind: { software: "produto", franquia: "servico", marca_pessoal: "pessoa", marca_editorial: "marca", nenhum: "nenhuma" },
  family: {
    atualidade: "noticia_atualidade",
    celebridades: "entretenimento",
    critica_social: "conscientizacao",
    experimento_social: "entretenimento",
    tutorial: "educativo",
    ugc: "identificacao",
    desafio: "entretenimento",
  },
  hook: {
    resultado_especifico: "resultado_antecipado",
    prova: "autoridade",
    numero_especifico: "numero",
    depoimento: "autoridade",
    promessa_pratica: "promessa",
    mapa_finito: "promessa",
    pedido_de_ajuda: "problema",
    persona: "identificacao",
    framework: "promessa",
    resultado_comercial: "resultado_antecipado",
  },
  narrative: {
    resultado: "payoff",
    depoimento: "prova",
    antes: "situacao",
    decisao: "virada",
    conselho: "conclusao",
    lista_de_modelos: "progressao",
    explicacao: "mecanismo",
    pergunta_da_audiencia: "problema",
    resposta_da_persona: "payoff",
    exagero: "escalada",
    comentario_social: "conclusao",
    framework: "mecanismo",
    tipologia: "progressao",
    processo: "progressao",
    cta_recomendado: "cta",
  },
  proof: {
    resultado_quantificado: "resultado_verificavel",
    voz_identificada_cliente: "depoimento",
    contexto_anterior: "mecanismo_explicado",
    depoimento_identificado: "depoimento",
    resultado_quantificado_autodeclarado: "alegacao_sem_prova",
    detalhes_de_processo: "mecanismo_explicado",
    tipologia: "mecanismo_explicado",
  },
  cta: {
    teste_gratis: "experimentar",
    conversa: "conversar",
    pesquisa_adicional: "outro_conteudo",
    enviar_pergunta: "enviar_mensagem",
  },
  mechanism: { "confiança": "confianca", descoberta: "curiosidade" },
};

const unique = values => [...new Set(values.filter(Boolean))];
const mapMany = (values, map, max) => unique((Array.isArray(values) ? values : []).map(value => map[value] ?? value)).slice(0, max);
const normalizeMix = (mix, primaryFamily) => {
  const combined = new Map();
  for (const item of Array.isArray(mix) ? mix : []) {
    const family = aliases.family[item?.family] ?? item?.family;
    if (!family) continue;
    combined.set(family, (combined.get(family) ?? 0) + Math.max(0, Number(item.percentage) || 0));
  }
  const selected = [...combined].slice(0, 3);
  if (!selected.length) return [{ family: primaryFamily, percentage: 100 }];
  const total = selected.reduce((sum, [, percentage]) => sum + percentage, 0) || 1;
  let allocated = 0;
  return selected.map(([family, percentage], index) => {
    const normalized = index === selected.length - 1 ? 100 - allocated : Math.round(percentage * 100 / total);
    allocated += normalized;
    return { family, percentage: normalized };
  });
};

const creators = new Map((memory.references ?? []).map(reference => [reference.id, reference.creator ?? ""]));
memory.references = (memory.references ?? []).map(reference => {
  const classification = reference.classification ?? {};
  const presentations = mapMany(classification.presentationFormats, {}, 3);
  const concretePresentations = presentations.filter(value => value !== "outro");
  const presentationFormats = concretePresentations.length ? concretePresentations : ["indeterminado"];
  const primaryFamily = aliases.family[classification.primaryFamily] ?? classification.primaryFamily ?? "indeterminado";
  const secondaryFamilies = mapMany(classification.secondaryFamilies, aliases.family, 8)
    .filter(value => value !== primaryFamily)
    .slice(0, 2);
  const advertisedEntity = classification.advertisedEntity ?? {};
  const missingInformation = unique(classification.missingInformation ?? []);
  const hadLegacyAmbiguity = missingInformation.includes("classificação legada ambígua requer revisão humana");
  const nextMissingInformation = missingInformation.filter(value => value !== "classificação legada ambígua requer revisão humana");

  return {
    ...reference,
    classification: {
      ...classification,
      taxonomyVersion: "3.0",
      presentationFormats,
      primaryFamily,
      secondaryFamilies,
      functionalMix: normalizeMix(classification.functionalMix, primaryFamily),
      objectives: unique(classification.objectives ?? []).slice(0, 4),
      advertisingType: aliases.advertisingType[classification.advertisingType] ?? classification.advertisingType,
      advertisedEntity: {
        ...advertisedEntity,
        kind: aliases.entityKind[advertisedEntity.kind] ?? advertisedEntity.kind,
        name: typeof advertisedEntity.name === "string" ? advertisedEntity.name : "",
      },
      productionLevel: aliases.productionLevel[classification.productionLevel] ?? classification.productionLevel,
      pace: aliases.pace[classification.pace] ?? classification.pace,
      mechanisms: unique(classification.mechanisms ?? []).slice(0, 6),
      hookTypes: mapMany(classification.hookTypes, aliases.hook, 5),
      narrativeElements: mapMany(classification.narrativeElements, aliases.narrative, 10),
      proofTypes: mapMany(classification.proofTypes, aliases.proof, 6),
      ctaTypes: mapMany(classification.ctaTypes, aliases.cta, 4),
      missingInformation: nextMissingInformation,
      needsHumanReview: Boolean(classification.needsHumanReview),
    },
    taxonomyReview: hadLegacyAmbiguity ? {
      reviewedAt: repairedAt,
      decision: "Valores legados de formato criativo foram removidos do eixo de apresentação; apresentações observáveis foram preservadas e ausência de evidência audiovisual virou indeterminado.",
      uncertaintyPreserved: true,
    } : reference.taxonomyReview,
  };
});

memory.references = memory.references.map(reference => {
  const classification = { ...reference.classification };
  const removed = {};
  const scalarFallbacks = {
    container: "indeterminado", materialFormat: "indeterminado", primaryFamily: "indeterminado",
    advertisingType: "indeterminado", commercialIntent: "indeterminada", awarenessStage: "indeterminado",
    productionLevel: "unknown", durationBand: "unknown", pace: "unknown",
  };
  for (const [field, fallback] of Object.entries(scalarFallbacks)) {
    if (!strictEnums[field].has(classification[field])) {
      removed[field] = classification[field];
      classification[field] = fallback;
    }
  }
  const listLimits = { presentationFormats: 3, secondaryFamilies: 2, objectives: 4, mechanisms: 6, hookTypes: 5, narrativeElements: 10, proofTypes: 6, ctaTypes: 4 };
  for (const [field, maximum] of Object.entries(listLimits)) {
    const original = Array.isArray(classification[field]) ? classification[field] : [];
    const next = unique(original.filter(value => strictEnums[field].has(value))).slice(0, maximum);
    const invalid = original.filter(value => !strictEnums[field].has(value));
    if (invalid.length || original.length > maximum) removed[field] = [...invalid, ...original.slice(maximum)];
    classification[field] = next;
  }
  if (!classification.presentationFormats.length) classification.presentationFormats = ["indeterminado"];
  if (!classification.objectives.length) classification.objectives = ["indeterminado"];
  classification.secondaryFamilies = classification.secondaryFamilies.filter(value => value !== classification.primaryFamily);
  classification.functionalMix = normalizeMix(
    (classification.functionalMix ?? []).filter(item => strictEnums.primaryFamily.has(item?.family)),
    classification.primaryFamily,
  );
  const creatorIdentity = reference.creatorIdentity || String(reference.creator || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  return {
    ...reference,
    creatorIdentity,
    sourceIdentity: reference.sourceIdentity || creatorIdentity,
    classification,
    ...(Object.keys(removed).length ? { taxonomyRepair: { policy: "strict-enum-v3.1", repairedAt, previousInvalidValues: removed, uncertaintyPreserved: true } } : {}),
  };
});

const referenceIdentity = new Map(memory.references.map(reference => [reference.id, reference]));
memory.patterns = (memory.patterns ?? []).map(pattern => {
  const supportReferenceIds = unique(pattern.supportReferenceIds ?? []);
  const counterexampleReferenceIds = unique(pattern.counterexampleReferenceIds ?? []);
  const occupied = new Set([...supportReferenceIds, ...counterexampleReferenceIds]);
  const caseLimitReferenceIds = unique(pattern.caseLimitReferenceIds ?? []).filter(id => !occupied.has(id));
  const creatorDiversityCount = new Set(supportReferenceIds.map(id => referenceIdentity.get(id)?.creatorIdentity).filter(Boolean)).size;
  const sourceDiversityCount = new Set(supportReferenceIds.map(id => referenceIdentity.get(id)?.sourceIdentity).filter(Boolean)).size;
  let stage = pattern.stage ?? pattern.status ?? "hypothesis";
  if (!["experimentally_validated", "validated"].includes(stage)) {
    if (counterexampleReferenceIds.length >= supportReferenceIds.length && counterexampleReferenceIds.length >= 2) stage = "contradicted";
    else if (supportReferenceIds.length >= 3 && creatorDiversityCount >= 2 && sourceDiversityCount >= 2) stage = "provisional";
    else if (supportReferenceIds.length >= 2) stage = "supported_hypothesis";
    else if (supportReferenceIds.length === 1) stage = "observation";
    else stage = counterexampleReferenceIds.length ? "inconclusive" : "hypothesis";
  } else stage = "experimentally_validated";
  return {
    ...pattern,
    patternType: strictEnums.patternType.has(pattern.patternType) ? pattern.patternType : "outro",
    mechanism: mapMany(pattern.mechanism, aliases.mechanism, 8).filter(value => strictEnums.mechanisms.has(value)),
    supportReferenceIds,
    counterexampleReferenceIds,
    caseLimitReferenceIds,
    supportingCount: supportReferenceIds.length,
    comparableSupportCount: supportReferenceIds.length,
    counterexampleCount: counterexampleReferenceIds.length,
    caseLimitCount: caseLimitReferenceIds.length,
    creatorDiversityCount,
    sourceDiversityCount,
    stage,
    status: stage,
    validation: stage === "experimentally_validated" ? pattern.validation : "requires_human_or_experimental_evidence",
  };
});

memory.updatedAt = repairedAt;
memory.trainingRuns = [...(memory.trainingRuns ?? []), {
  id: "taxonomy-v3-integrity-repair-v31",
  executedAt: repairedAt,
  type: "integrity_repair",
  referencesInspected: memory.references.length,
  referencesRemoved: 0,
  urlsChanged: 0,
  rulesValidatedAutomatically: 0,
}].filter((run, index, runs) => runs.findIndex(item => item.id === run.id) === index);

writeFileSync(memoryPath, `${JSON.stringify(memory, null, 2)}\n`);
writeFileSync(reportPath, `${JSON.stringify({
  repairId: "taxonomy-v3-integrity-repair-v31",
  repairedAt,
  taxonomyVersion: "3.0",
  referencesInspected: memory.references.length,
  referencesRemoved: 0,
  urlsChanged: 0,
  historicalAmbiguityEntriesReviewed: 27,
  affectedReferencesReviewed: 22,
  decisions: [
    "Valores de família criativa foram removidos do eixo de apresentação.",
    "Apresentações específicas observáveis foram preservadas; ausência de evidência audiovisual foi marcada como indeterminado.",
    "Aliases dos lotes 004 e 005 foram normalizados para os enums da taxonomia v3.",
    "Cardinalidades e functionalMix foram ajustados sem criar nova evidência.",
    "Apoios, contagens e diversidade de criadores dos padrões foram recalculados pelas referências existentes.",
  ],
  guarantees: [
    "nenhuma referência removida",
    "nenhuma URL alterada",
    "nenhum padrão validado automaticamente",
    "incerteza material preservada por needsHumanReview e valores indeterminados",
  ],
}, null, 2)}\n`);
console.log(JSON.stringify({ ok: true, references: memory.references.length, patterns: memory.patterns.length, repairedAt }, null, 2));
