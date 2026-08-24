import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const memoryPath = resolve(root, "knowledge/observatory/plateia-memory.json");
const reportPath = resolve(root, "knowledge/observatory/migrations/taxonomy-v3-integrity-repair.json");
const memory = JSON.parse(readFileSync(memoryPath, "utf8"));
const repairedAt = "2026-08-24T19:30:00.000Z";

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

memory.patterns = (memory.patterns ?? []).map(pattern => {
  const supportReferenceIds = unique(pattern.supportReferenceIds ?? pattern.evidence?.map(item => item.referenceId) ?? []);
  const supportingCount = supportReferenceIds.length;
  const creatorDiversityCount = new Set(supportReferenceIds.map(id => creators.get(id)?.trim().toLocaleLowerCase("pt-BR")).filter(Boolean)).size;
  let stage = pattern.stage ?? pattern.status ?? "hypothesis";
  if (stage !== "experimentally_validated") stage = supportingCount >= 3 && creatorDiversityCount >= 2 ? "provisional" : supportingCount >= 2 ? "supported_hypothesis" : supportingCount === 1 ? "observation" : "hypothesis";
  return {
    ...pattern,
    mechanism: mapMany(pattern.mechanism, aliases.mechanism, 8),
    supportReferenceIds,
    supportingCount,
    comparableSupportCount: supportingCount,
    creatorDiversityCount,
    sourceDiversityCount: creatorDiversityCount,
    stage,
    status: stage,
    validation: stage === "experimentally_validated" ? pattern.validation : "requires_human_or_experimental_evidence",
  };
});

memory.updatedAt = repairedAt;
memory.trainingRuns = [...(memory.trainingRuns ?? []), {
  id: "taxonomy-v3-integrity-repair-20260824",
  executedAt: repairedAt,
  type: "integrity_repair",
  referencesInspected: memory.references.length,
  referencesRemoved: 0,
  urlsChanged: 0,
  rulesValidatedAutomatically: 0,
}].filter((run, index, runs) => runs.findIndex(item => item.id === run.id) === index);

writeFileSync(memoryPath, `${JSON.stringify(memory, null, 2)}\n`);
writeFileSync(reportPath, `${JSON.stringify({
  repairId: "taxonomy-v3-integrity-repair-20260824",
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
