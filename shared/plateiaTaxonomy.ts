export const PLATEIA_TAXONOMY_VERSION = "3.0" as const;

export const MATERIAL_FORMATS = ["video_curto", "video_longo", "reel", "corte", "arte_estatica", "fotografia", "carrossel", "copy", "story", "live", "audio", "hibrido", "outro", "indeterminado"] as const;
export const CONTAINERS = ["instagram_reel", "instagram_post", "instagram_story", "tiktok", "youtube_short", "youtube_video", "facebook_reel", "webpage", "arquivo_enviado", "indeterminado"] as const;
export const PRESENTATION_FORMATS = ["camera_direta", "podcast_entrevista", "dialogo", "dramatizacao", "esquete", "reacao", "comentario", "narracao_imagens", "demonstracao", "tutorial", "transformacao", "bastidores", "depoimento", "estudo_caso", "reportagem", "animacao", "tela_gravada", "montagem", "trend", "meme", "ugc", "produto", "institucional", "manifesto", "desafio", "personagem_marca", "outro", "indeterminado"] as const;
export const CREATIVE_FAMILIES = ["educativo", "explicativo", "autoridade_opiniao", "noticia_atualidade", "storytelling", "entretenimento", "humor", "curiosidade", "demonstracao", "transformacao", "inspiracao", "identificacao", "comunidade", "polemica", "conscientizacao", "oferta_direta", "venda_indireta", "prova_estudo_caso", "depoimento", "institucional", "posicionamento_marca", "comparacao", "reacao", "hibrido", "indeterminado"] as const;
export const OBJECTIVES = ["interromper_rolagem", "alcance", "visualizacao", "retencao", "educar", "consciencia_problema", "apresentar_solucao", "autoridade", "confianca", "identificacao", "compartilhamento", "salvamento", "comentario", "comunidade", "seguidores", "lead", "conversa", "venda", "trafego", "marca", "recompra", "outro", "indeterminado"] as const;
export const ADVERTISING_TYPES = ["sem_intencao_comercial", "editorial_organico", "conteudo_de_marca", "institucional", "produto", "oferta_direta", "resposta_direta", "geracao_de_leads", "consideracao", "conversao", "remarketing_aparente", "comparativa", "branded_content", "parceria_com_criador", "ugc_organico", "ugc_publicitario", "prova_social", "lancamento", "promocao", "publicidade_nativa", "indeterminado"] as const;
export const COMMERCIAL_INTENTS = ["ausente", "implicita", "explicita", "indeterminada"] as const;
export const AWARENESS_STAGES = ["inconsciente", "consciente_problema", "consciente_solucao", "consciente_produto", "preparado_agir", "indeterminado"] as const;
export const PRODUCTION_LEVELS = ["simple", "intermediate", "complex", "unknown"] as const;
export const DURATION_BANDS = ["up_to_15s", "16_to_30s", "31_to_60s", "over_60s", "not_applicable", "unknown"] as const;
export const PACES = ["slow", "moderate", "fast", "not_applicable", "unknown"] as const;
export const MECHANISMS = ["curiosidade", "surpresa", "aproximacao", "desejo", "aversao_perda", "medo", "indignacao", "humor", "admiracao", "identificacao", "pertencimento", "confianca", "vigilancia", "urgencia", "alivio", "recompensa", "utilidade_pratica", "prova_social", "reciprocidade", "contraste", "antecipacao", "tensao", "novidade", "autoridade"] as const;
export const HOOK_TYPES = ["visual", "verbal", "textual", "sonoro", "narrativo", "pergunta", "afirmacao_contraintuitiva", "promessa", "problema", "risco", "conflito", "demonstracao_antecipada", "resultado_antecipado", "transformacao", "identificacao", "autoridade", "numero", "novidade", "urgencia", "interrupcao_estetica", "nenhum_identificado", "indeterminado"] as const;
export const NARRATIVE_ELEMENTS = ["situacao", "personagem", "problema", "desejo", "conflito", "risco", "promessa", "mecanismo", "tentativa", "progressao", "escalada", "prova", "virada", "transformacao", "climax", "payoff", "conclusao", "cta", "loop", "continuidade_serial"] as const;
export const PROOF_TYPES = ["demonstracao", "evidencia_documental", "especialista", "dado", "fonte", "depoimento", "antes_depois", "resultado_verificavel", "mecanismo_explicado", "prova_social", "popularidade", "autoridade_percebida", "autoridade_demonstrada", "garantia", "risco_reversivel", "tratamento_objecao", "alegacao_sem_prova", "ausencia_prova_necessaria", "nenhuma", "indeterminado"] as const;
export const CTA_TYPES = ["seguir", "comentar", "compartilhar", "salvar", "clicar", "conversar", "enviar_mensagem", "cadastrar", "comprar", "proxima_parte", "outro_conteudo", "experimentar", "comparecer", "nenhum", "indeterminado"] as const;
export const PATTERN_TYPES = ["gancho", "atencao", "compreensao", "curiosidade", "narrativa", "retencao", "emocao", "identidade", "confianca", "prova", "objecao", "acao", "cta", "conversao", "comunidade", "distribuicao", "producao", "replicabilidade", "outro"] as const;

export const TAXONOMY_ALIASES = {
  materialFormat: { short_vertical: "video_curto", video_exact_duration_unknown: "outro" },
  presentationFormat: { explicativo: "outro", storytelling: "outro", humor: "outro", curiosidade: "outro", review: "comentario", sketch: "esquete", recorte_entrevista: "podcast_entrevista", cobertura_evento: "reportagem", celebridades: "outro", rua: "outro", personagem_de_marca: "personagem_marca", serial: "outro", branded_content: "produto", desafio_serial: "desafio" },
  objective: { acao: "outro", entretenimento: "visualizacao", entreter: "visualizacao", venda_indireta: "venda", consciencia_solucao: "apresentar_solucao", decisao_compra: "venda", atualidade: "alcance", posicionamento_marca: "marca" },
  mechanism: { "confiança": "confianca", descoberta: "curiosidade", comunidade: "pertencimento" },
} as const;

export type ElementOf<T extends readonly string[]> = T[number];
export type ObservatoryClassification = {
  taxonomyVersion: typeof PLATEIA_TAXONOMY_VERSION;
  container: ElementOf<typeof CONTAINERS>;
  materialFormat: ElementOf<typeof MATERIAL_FORMATS>;
  presentationFormats: ElementOf<typeof PRESENTATION_FORMATS>[];
  primaryFamily: ElementOf<typeof CREATIVE_FAMILIES>;
  secondaryFamilies: ElementOf<typeof CREATIVE_FAMILIES>[];
  functionalMix: Array<{ family: ElementOf<typeof CREATIVE_FAMILIES>; percentage: number }>;
  objectives: ElementOf<typeof OBJECTIVES>[];
  advertisingType: ElementOf<typeof ADVERTISING_TYPES>;
  commercialIntent: ElementOf<typeof COMMERCIAL_INTENTS>;
  advertisedEntity: { kind: "produto" | "servico" | "marca" | "causa" | "pessoa" | "nenhuma" | "indeterminado"; name: string; confidence: "low" | "medium" | "high" };
  contentTopic: { label: string; iabCode: string | null };
  segment: string;
  subsegment: string;
  probableAudience: string;
  awarenessStage: ElementOf<typeof AWARENESS_STAGES>;
  productionLevel: ElementOf<typeof PRODUCTION_LEVELS>;
  creatorScale: "small" | "medium" | "large" | "unknown";
  replicability: "high" | "medium" | "low" | "unknown";
  durationBand: ElementOf<typeof DURATION_BANDS>;
  pace: ElementOf<typeof PACES>;
  mechanisms: ElementOf<typeof MECHANISMS>[];
  hookTypes: ElementOf<typeof HOOK_TYPES>[];
  narrativeElements: ElementOf<typeof NARRATIVE_ELEMENTS>[];
  proofTypes: ElementOf<typeof PROOF_TYPES>[];
  ctaTypes: ElementOf<typeof CTA_TYPES>[];
  distributionContext: { organicPaid: "organic" | "paid" | "mixed" | "unknown"; trendDependency: "none" | "low" | "high" | "unknown" };
  confidence: "low" | "medium" | "high";
  evidence: string[];
  alternativeClassifications: string[];
  missingInformation: string[];
  needsHumanReview: boolean;
};
