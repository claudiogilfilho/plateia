import { evaluateWithProvider } from "./aiProvider";

export const CONSUMERS = ["O Apressado", "O Analítico", "O Aspiracional", "O Influenciado pela Comunidade", "O Cético"] as const;
export const CRITERIA = ["gancho", "clareza", "relevância", "desejo", "confiança", "retenção", "ação", "objeções"] as const;

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

function recordOf(value: unknown, field: string): Record<string, unknown> { if (!value || typeof value !== "object" || Array.isArray(value)) throw new Error(`${field} inválido na resposta da IA.`); return value as Record<string, unknown>; }
function textOf(value: unknown, field: string) { if (typeof value !== "string" || !value.trim()) throw new Error(`${field} inválido na resposta da IA.`); return value.trim(); }
function scoreOf(value: unknown, field: string) { const score = Number(value); if (!Number.isFinite(score)) throw new Error(`${field} precisa ser uma nota numérica.`); return Math.round(Math.max(0, Math.min(100, score))); }
function listOf(value: unknown, field: string, min: number, max: number) { if (!Array.isArray(value) || value.length < min || value.length > max) throw new Error(`${field} possui quantidade inválida de itens.`); return value.map((item, index) => textOf(item, `${field} ${index + 1}`)); }

export function normalizeAnalysis(input: unknown): ContentAnalysis {
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
  return validateAnalysisShape({ consumers, synthesis: { overallScore: scoreOf(rawSynthesis.overallScore, "Nota geral"), weightedAverage: scoreOf(rawSynthesis.weightedAverage, "Média ponderada"), divergence: scoreOf(rawSynthesis.divergence, "Divergência"), strengths: listOf(rawSynthesis.strengths, "Pontos fortes", 2, 4), risks: listOf(rawSynthesis.risks, "Riscos", 2, 4), recommendations: listOf(rawSynthesis.recommendations, "Recomendações", 3, 3) as [string, string, string] } });
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

export async function evaluateContent(input: { contentType: "post" | "carrossel" | "reel" | "copy"; text: string; product: string; objective: string; targetAudience: string; mediaUrl?: string | null; mediaMimeType?: string | null; sourceUrl?: string | null }): Promise<ContentAnalysis> {
  const prompt = `Você é o motor de avaliação da Platéia, uma plataforma brasileira de pré-avaliação de conteúdo para redes sociais.

Avalie o material abaixo sem afirmar que ele prevê vendas. Simule lentes comportamentais para os cinco consumidores obrigatórios e avalie todos os oito critérios obrigatórios. Notas mais altas em “objeções” significam menor barreira percebida; notas baixas significam maior resistência ou risco. Seja específico, prático, respeitoso e escreva em português do Brasil.

Conteúdo: ${input.contentType}
Produto relacionado: ${input.product || "Não informado"}
Objetivo da publicação: ${input.objective || "Não informado"}
Público-alvo declarado: ${input.targetAudience || "Não informado"}
Texto ou legenda: ${input.text || "Não informado"}
Link de origem: ${input.sourceUrl || "Não informado"}

Contexto dos consumidores:
${CONSUMERS.map(name => `- ${name}: ${consumerContext[name]}`).join("\n")}

Regras:
1. Use somente estes nomes de consumidores: ${CONSUMERS.join(", ")}.
2. Avalie exatamente estes critérios: ${CRITERIA.join(", ")}.
3. Recomendações deve conter exatamente três sugestões, em ordem de prioridade e acionáveis.
4. Identifique pontos fortes e riscos concretos do material.
5. Não invente depoimentos, resultados, clientes, dados de performance ou provas sociais.
6. Se houver somente um link de origem sem mídia anexada, trate-o apenas como referência e avalie somente o texto e o contexto fornecidos; não invente o conteúdo do link.
7. Seja conciso: reações e objeções com até 180 caracteres; itens de síntese com até 160 caracteres.`;
  const request = { mediaUrl: input.mediaUrl, mediaMimeType: input.mediaMimeType, responseFormat: outputSchema };
  try { return normalizeAnalysis(parseStructuredEvaluation(await evaluateWithProvider({ prompt, ...request }))); }
  catch (firstError) {
    try { return normalizeAnalysis(parseStructuredEvaluation(await evaluateWithProvider({ prompt: `${prompt}\n\nA resposta anterior ficou inválida ou incompleta. Refaça a avaliação e retorne somente um JSON completo, conciso e compatível com o esquema.`, ...request }))); }
    catch { throw new Error(`A IA retornou uma leitura incompleta duas vezes. ${firstError instanceof Error ? firstError.message : ""}`); }
  }
}
