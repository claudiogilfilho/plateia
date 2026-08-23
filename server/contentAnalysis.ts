import { evaluateWithProvider } from "./aiProvider";
import type { ObservatoryClassification, ObservatoryContext } from "./observatory";

export const CONSUMERS = ["O Apressado", "O Analítico", "O Aspiracional", "O Influenciado pela Comunidade", "O Cético"] as const;
export const CRITERIA = ["gancho", "clareza", "relevância", "desejo", "confiança", "retenção", "ação", "objeções"] as const;
export const VISUAL_ONLY_EXCLUDED_CRITERIA = ["clareza", "ação", "objeções"] as const;

export type ContentAnalysis = {
  consumers: Array<{ name: (typeof CONSUMERS)[number]; overallScore: number; reaction: string; criteria: Record<(typeof CRITERIA)[number], number>; mainObjection: string }>;
  synthesis: { overallScore: number; weightedAverage: number; divergence: number; strengths: string[]; risks: string[]; recommendations: [string, string, string] };
};

const consumerContext = {
  "O Apressado": "Decide em segundos. Avalia se a abertura interrompe a rolagem e comunica valor rápido.",
  "O Analítico": "Busca lógica, especificidade, clareza da oferta e provas verificáveis antes de avançar.",
  "O Aspiracional": "Reage a estética, identidade, transformação, pertencimento e desejo de se tornar algo.",
  "O Influenciado pela Comunidade": "Valoriza identificação com pares, contexto social, sinais autênticos de confiança e relevância cultural.",
  "O Cético": "Procura exageros, ambiguidades, promessas não comprovadas e motivos claros para desconfiar.",
} as const;

const outputSchema = {
  type: "json_schema",
  json_schema: {
    name: "plateia_content_review",
    strict: true,
    schema: {
      type: "object",
      properties: {
        consumers: { type: "array", minItems: 5, maxItems: 5, items: { type: "object", properties: { name: { type: "string", enum: [...CONSUMERS] }, overallScore: { type: "integer", minimum: 0, maximum: 100 }, reaction: { type: "string" }, criteria: { type: "object", properties: { gancho: { type: "integer", minimum: 0, maximum: 100 }, clareza: { type: "integer", minimum: 0, maximum: 100 }, relevância: { type: "integer", minimum: 0, maximum: 100 }, desejo: { type: "integer", minimum: 0, maximum: 100 }, confiança: { type: "integer", minimum: 0, maximum: 100 }, retenção: { type: "integer", minimum: 0, maximum: 100 }, ação: { type: "integer", minimum: 0, maximum: 100 }, objeções: { type: "integer", minimum: 0, maximum: 100 } }, required: [...CRITERIA], additionalProperties: false }, mainObjection: { type: "string" } }, required: ["name", "overallScore", "reaction", "criteria", "mainObjection"], additionalProperties: false } },
        synthesis: { type: "object", properties: { overallScore: { type: "integer", minimum: 0, maximum: 100 }, weightedAverage: { type: "integer", minimum: 0, maximum: 100 }, divergence: { type: "integer", minimum: 0, maximum: 100 }, strengths: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 4 }, risks: { type: "array", items: { type: "string" }, minItems: 2, maxItems: 4 }, recommendations: { type: "array", items: { type: "string" }, minItems: 3, maxItems: 3 } }, required: ["overallScore", "weightedAverage", "divergence", "strengths", "risks", "recommendations"], additionalProperties: false },
      },
      required: ["consumers", "synthesis"],
      additionalProperties: false,
    },
  },
} as const;

export function validateAnalysisShape(analysis: ContentAnalysis): ContentAnalysis {
  if (analysis.consumers.length !== CONSUMERS.length) throw new Error("A análise precisa conter os cinco consumidores sintéticos.");
  const names = new Set(analysis.consumers.map(consumer => consumer.name));
  if (names.size !== CONSUMERS.length || CONSUMERS.some(name => !names.has(name))) throw new Error("Os consumidores retornados não correspondem à configuração da Platéia.");
  if (analysis.synthesis.recommendations.length !== 3) throw new Error("A Platéia precisa retornar exatamente três recomendações prioritárias.");
  return analysis;
}

export function recalculateSynthesisScores(
  analysis: ContentAnalysis,
  assessedCriteria: readonly (typeof CRITERIA)[number][] = CRITERIA,
  classification?: ObservatoryClassification | null,
): ContentAnalysis {
  if (assessedCriteria.length === 0) throw new Error("A Platéia precisa de ao menos um critério avaliado.");
  const consumers = analysis.consumers.map(consumer => ({
    ...consumer,
    overallScore: weightedConsumerScore(consumer.name, consumer.criteria, assessedCriteria, classification),
  }));
  const overallScore = Math.round(consumers.reduce((sum, consumer) => sum + consumer.overallScore, 0) / consumers.length);
  const divergence = Math.max(...consumers.map(consumer => consumer.overallScore)) - Math.min(...consumers.map(consumer => consumer.overallScore));
  return { consumers, synthesis: { ...analysis.synthesis, overallScore, weightedAverage: overallScore, divergence } };
}

const consumerWeights: Record<(typeof CONSUMERS)[number], Partial<Record<(typeof CRITERIA)[number], number>>> = {
  "O Apressado": { gancho: 25, clareza: 15, relevância: 12, desejo: 8, confiança: 8, retenção: 22, ação: 5, objeções: 5 },
  "O Analítico": { gancho: 8, clareza: 20, relevância: 12, desejo: 5, confiança: 20, retenção: 8, ação: 10, objeções: 17 },
  "O Aspiracional": { gancho: 12, clareza: 8, relevância: 14, desejo: 25, confiança: 10, retenção: 12, ação: 8, objeções: 11 },
  "O Influenciado pela Comunidade": { gancho: 10, clareza: 10, relevância: 18, desejo: 12, confiança: 18, retenção: 10, ação: 8, objeções: 14 },
  "O Cético": { gancho: 6, clareza: 17, relevância: 14, desejo: 4, confiança: 24, retenção: 6, ação: 10, objeções: 19 },
};

const familyBoosts: Partial<Record<ObservatoryClassification["primaryFamily"], Partial<Record<(typeof CRITERIA)[number], number>>>> = {
  educativo: { clareza: 6, relevância: 5, retenção: 4 },
  explicativo: { clareza: 7, relevância: 4, confiança: 3 },
  entretenimento: { gancho: 6, retenção: 7, desejo: 3 },
  humor: { gancho: 5, retenção: 6, relevância: 3 },
  curiosidade: { gancho: 7, retenção: 6 },
  autoridade_opiniao: { confiança: 7, clareza: 4, objeções: 4 },
  oferta_direta: { desejo: 6, confiança: 5, ação: 7, objeções: 6 },
  venda_indireta: { desejo: 5, confiança: 5, ação: 4, objeções: 4 },
  comunidade: { relevância: 5, confiança: 5, ação: 4 },
  prova_estudo_caso: { confiança: 8, objeções: 7, clareza: 3 },
  demonstracao: { clareza: 4, desejo: 4, confiança: 5 },
  storytelling: { gancho: 4, retenção: 7, desejo: 4 },
};

function weightedConsumerScore(
  name: (typeof CONSUMERS)[number],
  scores: Record<(typeof CRITERIA)[number], number>,
  assessedCriteria: readonly (typeof CRITERIA)[number][],
  classification?: ObservatoryClassification | null,
) {
  if (!classification) return Math.round(assessedCriteria.reduce((sum, criterion) => sum + scores[criterion], 0) / assessedCriteria.length);
  const boosts = familyBoosts[classification.primaryFamily] ?? {};
  let weightedTotal = 0;
  let totalWeight = 0;
  for (const criterion of assessedCriteria) {
    const weight = (consumerWeights[name][criterion] ?? 1) + (boosts[criterion] ?? 0);
    weightedTotal += scores[criterion] * weight;
    totalWeight += weight;
  }
  return Math.round(weightedTotal / totalWeight);
}

function recordOf(value: unknown, field: string): Record<string, unknown> { if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${field} inválido na resposta da IA.`); return value as Record<string, unknown>; }
function textOf(value: unknown, field: string) { if (typeof value !== "string" || !value.trim()) throw new Error(`${field} inválido na resposta da IA.`); return value.trim(); }
function scoreOf(value: unknown, field: string) { const score = Number(value); if (!Number.isFinite(score)) throw new Error(`${field} precisa ser uma nota numérica.`); return Math.round(Math.max(0, Math.min(100, score))); }
function listOf(value: unknown, field: string, min: number, max: number) { if (!Array.isArray(value) || value.length < min || value.length > max) throw new Error(`${field} possui quantidade inválida de itens.`); return value.map((item, index) => textOf(item, `${field} ${index + 1}`)); }

const safeRecommendations = [
  "Torne o benefício principal mais específico e visível nos primeiros segundos.",
  "Apresente somente evidências reais e verificáveis que a marca já possua, como demonstração, processo ou informação de produto.",
  "Conclua com uma chamada para ação simples e coerente com o objetivo da publicação.",
] as const;

function usesUnverifiedSocialProof(recommendation: string) {
  return /\d|\b(depoimentos?|testemunhos?|avalia[cç][õo]es?|reviews?|selos?|premiad[oa]s?|mais de|milhares de|prova social|clientes?)\b/i.test(recommendation);
}

export function sanitizeRecommendations(recommendations: string[]): [string, string, string] {
  return recommendations.map((recommendation, index) => usesUnverifiedSocialProof(recommendation) ? safeRecommendations[index] : recommendation) as [string, string, string];
}

export function normalizeAnalysis(input: unknown, classification?: ObservatoryClassification | null): ContentAnalysis {
  const raw = recordOf(input, "Avaliação");
  if (!Array.isArray(raw.consumers) || raw.consumers.length !== CONSUMERS.length) throw new Error("A análise precisa conter os cinco consumidores sintéticos.");
  const rawConsumers = raw.consumers.map(item => recordOf(item, "Consumidor"));
  const seen = new Set(rawConsumers.map(item => item.name));
  if (seen.size !== CONSUMERS.length || CONSUMERS.some(name => !seen.has(name))) throw new Error("Os consumidores retornados não correspondem à configuração da Platéia.");
  const consumers = CONSUMERS.map(name => {
    const consumer = rawConsumers.find(item => item.name === name);
    if (!consumer) throw new Error("Consumidor ausente na resposta da IA.");
    const rawCriteria = recordOf(consumer.criteria, `Critérios de ${name}`);
    return { name, overallScore: scoreOf(consumer.overallScore, `Nota geral de ${name}`), reaction: textOf(consumer.reaction, `Reação de ${name}`), criteria: Object.fromEntries(CRITERIA.map(criterion => [criterion, scoreOf(rawCriteria[criterion], `${criterion} de ${name}`)])) as Record<(typeof CRITERIA)[number], number>, mainObjection: textOf(consumer.mainObjection, `Objeção de ${name}`) };
  });
  const rawSynthesis = recordOf(raw.synthesis, "Síntese");
  scoreOf(rawSynthesis.overallScore, "Nota geral");
  scoreOf(rawSynthesis.weightedAverage, "Média ponderada");
  scoreOf(rawSynthesis.divergence, "Divergência");
  return validateAnalysisShape(recalculateSynthesisScores({ consumers, synthesis: { overallScore: 0, weightedAverage: 0, divergence: 0, strengths: listOf(rawSynthesis.strengths, "Pontos fortes", 2, 4), risks: listOf(rawSynthesis.risks, "Riscos", 2, 4), recommendations: sanitizeRecommendations(listOf(rawSynthesis.recommendations, "Recomendações", 3, 3)) } }, CRITERIA, classification));
}

export function applyVisualOnlyScope(analysis: ContentAnalysis, classification?: ObservatoryClassification | null): ContentAnalysis {
  const visualCriteria = CRITERIA.filter(criterion => !VISUAL_ONLY_EXCLUDED_CRITERIA.includes(criterion as (typeof VISUAL_ONLY_EXCLUDED_CRITERIA)[number]));
  return recalculateSynthesisScores(analysis, visualCriteria, classification);
}

export function parseStructuredEvaluation(raw: string) {
  const trimmed = raw.trim().replace(/^```(?:json)?\s*/i, "").replace(/\s*```$/i, "");
  try { return JSON.parse(trimmed); } catch {
    const start = trimmed.indexOf("{");
    const end = trimmed.lastIndexOf("}");
    if (start >= 0 && end > start) return JSON.parse(trimmed.slice(start, end + 1));
    throw new Error("A IA retornou uma avaliação incompleta.");
  }
}

export async function evaluateContent(input: { contentType: "post" | "carrossel" | "reel" | "copy"; text: string; product: string; objective: string; targetAudience: string; mediaUrl?: string | null; mediaMimeType?: string | null; sourceUrl?: string | null; analysisScope?: "standard" | "visual_only"; observatoryContext?: ObservatoryContext | null }): Promise<ContentAnalysis> {
  const observatoryContext = input.observatoryContext
    ? `\nClassificação automática multiaxial: ${JSON.stringify(input.observatoryContext.classification)}\nNível de comparação disponível: ${input.observatoryContext.comparisonLevel}\nConfiança do benchmark: ${input.observatoryContext.benchmarkConfidence}\nReferências comparáveis recuperadas: ${input.observatoryContext.comparisons.length ? input.observatoryContext.comparisons.map(reference => `${reference.title} (${reference.creator || "criador não informado"}), similaridade ${reference.similarity}, nível ${reference.comparisonLevel}; aprendizados: ${reference.learning.join(" | ") || "sem aprendizado consolidado"}`).join("\n") : "nenhuma referência adequada; faça somente avaliação estrutural e declare a limitação"}\nPadrões provisórios ou validados relevantes: ${input.observatoryContext.patterns.length ? input.observatoryContext.patterns.map(pattern => `${pattern.name} (${pattern.stage}; ${pattern.supportingCount} apoios, ${pattern.counterexampleCount} contraexemplos; confiança ${pattern.confidence})`).join("\n") : "nenhum; não invente regras"}`
    : "\nO Observatório ainda não forneceu classificação ou referências comparáveis. Não invente benchmark.";
  const prompt = `Você é o motor de avaliação da Platéia, uma plataforma brasileira de pré-avaliação de conteúdo para redes sociais.

Avalie o material abaixo sem afirmar que ele prevê vendas. Simule lentes comportamentais para os cinco consumidores obrigatórios e avalie todos os oito critérios obrigatórios. Notas mais altas em “objeções” significam menor barreira percebida; notas baixas significam maior resistência ou risco. Seja específico, prático, respeitoso e escreva em português do Brasil.

Conteúdo: ${input.contentType}
Produto relacionado: ${input.product || "Não informado"}
Objetivo da publicação: ${input.objective || "Não informado"}
Público-alvo declarado: ${input.targetAudience || "Não informado"}
Texto ou legenda: ${input.text || "Não informado"}
Link de origem: ${input.sourceUrl || "Não informado"}
Escopo da leitura: ${input.analysisScope === "visual_only" ? "Somente elementos visuais disponíveis. Não avalie, deduza ou critique uma legenda/copy inexistente." : "Material visual e texto disponíveis."}
${observatoryContext}

Contexto dos consumidores:
${CONSUMERS.map(name => `- ${name}: ${consumerContext[name]}`).join("\n")}

Regras:
1. Use somente estes nomes de consumidores: ${CONSUMERS.join(", ")}.
2. Avalie exatamente estes critérios: ${CRITERIA.join(", ")}.
3. Recomendações deve conter exatamente três sugestões, em ordem de prioridade e acionáveis.
4. Identifique pontos fortes e riscos concretos do material.
5. Não invente depoimentos, resultados, clientes, dados de performance ou provas sociais. Nas recomendações, nunca sugira inserir números, avaliações, depoimentos ou selos inexistentes; oriente a usar apenas evidências reais e verificáveis que a marca já possua.
6. Se houver somente um link de origem sem mídia anexada, trate-o apenas como referência e avalie somente o texto e o contexto fornecidos; não invente o conteúdo do link.
7. Quando o escopo for somente visual, baseie-se apenas no material visual. Não invente ou suponha CTA, promessa, preço, legenda ou qualquer texto que não esteja visível.
8. Seja conciso: reações e objeções com até 180 caracteres; itens de síntese com até 160 caracteres.`;
  const request = { mediaUrl: input.mediaUrl, mediaMimeType: input.mediaMimeType, responseFormat: outputSchema };
  try { return normalizeAnalysis(parseStructuredEvaluation(await evaluateWithProvider({ prompt, ...request })), input.observatoryContext?.classification); }
  catch (firstError) {
    try { return normalizeAnalysis(parseStructuredEvaluation(await evaluateWithProvider({ prompt: `${prompt}\n\nA resposta anterior ficou inválida ou incompleta. Refaça a avaliação e retorne somente um JSON completo, conciso e compatível com o esquema.`, ...request })), input.observatoryContext?.classification); }
    catch { throw new Error(`A IA retornou uma leitura incompleta duas vezes. ${firstError instanceof Error ? firstError.message : ""}`); }
  }
}
