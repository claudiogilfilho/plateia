import fs from "node:fs";
import { resolve } from "node:path";

const memoryPath = resolve(process.cwd(), "knowledge/observatory/plateia-memory.json");
const memory = JSON.parse(fs.readFileSync(memoryPath, "utf8"));
const createdAt = "2026-09-01T19:15:00.000Z";
const patternId = "pat-20260831-008";

const commonMissing = [
  "vídeo integral reproduzível no ambiente de auditoria",
  "áudio efetivamente ouvido",
  "quadros, texto na tela, cortes, ritmo e montagem",
  "retenção, impressões, fontes de tráfego e distribuição orgânica/paga",
  "baseline contemporâneo e funcional do perfil",
];

function classification(overrides) {
  return {
    taxonomyVersion: "3.0",
    container: "youtube_short",
    materialFormat: "video_curto",
    presentationFormats: ["narracao_imagens", "animacao"],
    primaryFamily: "comunidade",
    secondaryFamilies: ["storytelling", "humor"],
    functionalMix: [
      { family: "comunidade", percentage: 45 },
      { family: "storytelling", percentage: 35 },
      { family: "humor", percentage: 20 },
    ],
    objectives: ["comunidade", "comentario", "visualizacao"],
    advertisingType: "editorial_organico",
    commercialIntent: "ausente",
    advertisedEntity: { kind: "nenhuma", name: "", confidence: "high" },
    contentTopic: { label: "relatos enviados pela audiência", iabCode: null },
    segment: "entretenimento participativo",
    subsegment: "histórias dos inscritos",
    probableAudience: "público jovem interessado em histórias, animação e humor",
    awarenessStage: "indeterminado",
    productionLevel: "simple",
    creatorScale: "small",
    replicability: "high",
    durationBand: "over_60s",
    pace: "unknown",
    mechanisms: ["identificacao", "pertencimento", "curiosidade", "humor"],
    hookTypes: ["textual", "narrativo"],
    narrativeElements: ["situacao", "problema", "progressao", "payoff", "continuidade_serial", "cta"],
    proofTypes: ["depoimento"],
    ctaTypes: ["comentar", "proxima_parte"],
    distributionContext: { organicPaid: "unknown", trendDependency: "unknown" },
    confidence: "high",
    evidence: [],
    alternativeClassifications: [],
    missingInformation: [...commonMissing],
    needsHumanReview: true,
    ...overrides,
  };
}

function training({ role, eligible, claims, provenance, hypothesis = null }) {
  return {
    evidencePolicyVersion: "1.1",
    evidenceRole: role,
    evidenceLevel: role === "controlled_exploration" ? 3 : 1,
    requiredEvidenceObserved: claims.every(claim => claim.sufficient),
    supportEligible: eligible,
    claimCoverage: claims,
    provenanceAndConsent: provenance,
    replicable: [
      "Explicitar como os relatos são enviados, selecionados e transformados em pauta.",
      "Responder com voz editorial própria e indicar como a audiência participa do próximo episódio.",
    ],
    contingent: ["qualidade e volume dos envios", "moderação", "recorrência editorial", "proteção de terceiros"],
    notRecommended: [
      "expor nome, idade ou detalhes identificáveis sem autorização proporcional",
      "tratar comentários, visualizações ou razão views/seguidores como prova causal",
      "inferir cenas, áudio, ritmo, retenção ou consentimento ausentes",
    ],
    hypotheses: hypothesis ? [hypothesis] : [],
  };
}

const supportHypothesis = (observation, evidence, limitations) => ({
  name: "Relatos da audiência filtrados por voz editorial recorrente",
  targetPatternId: patternId,
  evidenceRole: "support",
  comparisonLevel: 1,
  requiredEvidenceObserved: true,
  patternType: "comunidade",
  observation,
  mechanism: "seleção de relato enviado, tratamento editorial reconhecível e convite recorrente de participação",
  evidence,
  alternativeExplanations: ["interesse pelo tema", "base prévia do canal", "novidade do relato", "distribuição da plataforma"],
  conditions: ["origem comunitária explícita", "seleção editorial", "resposta ou tratamento reconhecível", "proteção proporcional da identidade"],
  limitations,
  confidence: "high",
  stage: "observation",
});

const references = [
  {
    id: "obs-20260901-081",
    title: "HISTÓRIAS BIZARRAS DOS INSCRITOS!!! (Parte 44)",
    creator: "Lil Elfo",
    creatorIdentity: "lil-elfo",
    sourceIdentity: "lil-elfo",
    country: "BR",
    url: "https://www.youtube.com/watch?v=Azw2nWg_ehQ",
    publishedAt: "2021-01-21",
    duration: "PT1M51S",
    createdAt,
    coverage: {
      level: "partial",
      accessible: ["título e episódio 44", "descrição original com convite para enviar histórias nos comentários", "transcrição automática integral", "47 comentários recuperados de 55 indexados", "métricas públicas", "amostra de 30 vídeos do canal"],
      missing: [...commonMissing, "autorização do responsável e anonimização dos menores citados"],
    },
    publicMetrics: { views: 3594, likes: 312, commentsIndexed: 55, commentsRecovered: 47, subscribersObserved: 38200, observedAt: "2026-09-01", sourceType: "youtube_public_metadata", causality: "not_inferred" },
    profileBaseline: { sampleSize: 30, medianViews: 871.5, minViews: 54, maxViews: 92000, temporalMatch: "not_verified", interpretation: "o vídeo está acima da mediana da amostra atual, mas a diferença temporal impede classificação relativa" },
    classification: classification({ evidence: ["A descrição chama a peça de novo episódio e convida histórias nos comentários.", "A transcrição identifica narradora de 13 anos e entrega um relato em primeira pessoa.", "Comentários contêm novos relatos e resposta do canal."], creatorScale: "medium" }),
    comparison: { level: 1, group: "histórias curtas enviadas por inscritos, selecionadas e devolvidas em série editorial", referenceIds: ["obs-20260824-038", "obs-20260831-076", "obs-20260831-077"], confidence: "high" },
    observations: ["A série é numerada e a descrição solicita novos envios.", "A transcrição entrega um relato selecionado em primeira pessoa.", "Comentários mostram continuidade de envios e resposta do canal.", "Nomes e idades de menores aparecem publicamente."],
    interpretations: ["O ciclo pauta–publicação–novo envio está diretamente observável.", "A exposição identificável de menores torna consentimento e anonimização uma condição prática, não detalhe opcional."],
    limitations: ["Sem audiovisual reproduzível, não se avaliam animação, cortes, texto na tela ou ritmo.", "O baseline não é contemporâneo.", "Consentimento não foi verificado."],
    provenance: ["public_content", "youtube_auto_transcript", "public_comments", "public_metric", "channel_sample", "observatory_inference"],
    sourceEvidence: ["https://www.youtube.com/watch?v=Azw2nWg_ehQ", "https://www.youtube.com/@LilElfo/videos"],
    training: training({ role: "target_support", eligible: true, claims: [{ claim: "origem comunitária e ciclo recorrente", requiredModalities: ["description", "transcript", "comments"], observedModalities: ["description", "transcript", "comments"], sufficient: true }], provenance: { storyOrigin: "comentários da audiência, explicitamente solicitados na descrição", consentStatus: "unknown", identityProtection: "insufficient; nome e idade de menores aparecem no material público", evidence: ["descrição original", "transcrição automática", "comentários públicos"] }, hypothesis: supportHypothesis("Episódio 44 transforma relato de inscrita em narrativa e solicita novos envios.", "Descrição, transcrição integral e comentários públicos.", ["Consentimento e proteção de identidade não verificados.", "Sem execução audiovisual e retenção."]) }),
    viralAssessment: { status: "indeterminate", observedSignal: "3.594 visualizações; amostra atual do canal com mediana 871,5", missingForRelativeAssessment: ["baseline contemporâneo", "impressões", "retenção", "origem da distribuição"], confounders: ["vídeo de 2021", "mudança do canal", "seleção da amostra"], causalClaimAllowed: false },
  },
  {
    id: "obs-20260901-082",
    title: "HISTÓRIAS BIZARRAS DOS INSCRITOS!!!",
    creator: "Jv 4nimações ;-;",
    creatorIdentity: "jv-4nimacoes",
    sourceIdentity: "jv-4nimacoes",
    country: "BR",
    url: "https://www.youtube.com/watch?v=3dWHBOdl0Sk",
    publishedAt: "2021-01-06",
    duration: "PT1M1S",
    createdAt,
    coverage: { level: "partial", accessible: ["título", "descrição", "transcrição automática integral", "17 comentários", "convites do canal para novos relatos", "métricas públicas", "amostra de 30 vídeos do canal", "segundo episódio próximo com 116 visualizações"], missing: [...commonMissing, "consentimento e proteção de identidade dos participantes"] },
    publicMetrics: { views: 108, likes: 17, comments: 17, subscribersObserved: 2480, observedAt: "2026-09-01", sourceType: "youtube_public_metadata", causality: "not_inferred" },
    profileBaseline: { sampleSize: 30, medianViews: 854, minViews: 403, maxViews: 125000, temporalMatch: "not_verified", sameSeriesComparatorViews: 116, interpretation: "baixo frente à amostra atual, mas próximo de outro episódio da série; mudança temporal impede classificação conclusiva" },
    classification: classification({ evidence: ["A transcrição reúne dois relatos em primeira pessoa sob o título histórias dos inscritos.", "O canal responde a comentários pedindo novas histórias para o dia seguinte.", "A fala final reconhece a própria animação e promete melhora."], creatorScale: "small" }),
    comparison: { level: 1, group: "histórias curtas enviadas por inscritos, selecionadas e devolvidas em série editorial", referenceIds: ["obs-20260824-038", "obs-20260831-076", "obs-20260831-077"], confidence: "high" },
    observations: ["Dois relatos aparecem em sequência na transcrição.", "O canal convida publicamente novos relatos e promete publicação seguinte.", "Um episódio próximo da mesma série tem 116 visualizações."],
    interpretations: ["A seleção e a promessa de continuidade formam ciclo editorial observável.", "Baixa visualização absoluta não impede a arquitetura, mas tampouco prova comunidade ou retorno."],
    limitations: ["Sem audiovisual reproduzível.", "Baseline atual não é contemporâneo; somente um comparador da mesma série foi localizado.", "Consentimento não foi verificado."],
    provenance: ["public_content", "youtube_auto_transcript", "public_comments", "public_metric", "channel_sample", "observatory_inference"],
    sourceEvidence: ["https://www.youtube.com/watch?v=3dWHBOdl0Sk", "https://www.youtube.com/watch?v=nOp_RbaNWPw", "https://www.youtube.com/@jv4nimacoes-179/videos"],
    training: training({ role: "target_support", eligible: true, claims: [{ claim: "relatos enviados, seleção e convite recorrente", requiredModalities: ["transcript", "comments"], observedModalities: ["transcript", "comments"], sufficient: true }], provenance: { storyOrigin: "envios solicitados e recebidos em comentários", consentStatus: "unknown", identityProtection: "unknown; relatos pessoais aparecem sem política acessível", evidence: ["transcrição automática", "comentários e respostas do canal"] }, hypothesis: supportHypothesis("O canal reúne relatos de inscritos, responde aos envios e promete novo episódio.", "Transcrição integral, comentários e episódio comparador.", ["Consentimento e anonimização não verificados.", "Sem audiovisual e retenção."]) }),
    viralAssessment: { status: "indeterminate", observedSignal: "108 visualizações e 17 comentários; outro episódio próximo tem 116 visualizações", missingForRelativeAssessment: ["baseline contemporâneo amplo", "impressões", "retenção", "distribuição"], confounders: ["vídeo de 2021", "mudança do canal", "amostra atual incompatível"], causalClaimAllowed: false },
  },
  {
    id: "obs-20260901-083",
    title: "Menino Amarelo (Histórias Dos Inscritos)",
    creator: "EuSouBR ꤶ",
    creatorIdentity: "eusoubr",
    sourceIdentity: "eusoubr",
    country: "BR",
    url: "https://www.youtube.com/watch?v=mayNLQpazhY",
    publishedAt: "2020-05-12",
    duration: "PT38S",
    createdAt,
    coverage: { level: "partial", accessible: ["título", "descrição com crédito ao canal que enviou", "transcrição automática integral", "métricas públicas", "amostra de 30 vídeos do canal"], missing: [...commonMissing, "comentários individuais", "consentimento do remetente"] },
    publicMetrics: { views: 131, likes: 9, comments: 0, subscribersObserved: 203, observedAt: "2026-09-01", sourceType: "youtube_public_metadata", causality: "not_inferred" },
    profileBaseline: { sampleSize: 30, medianViews: 93.5, minViews: 28, maxViews: 1400, temporalMatch: "unknown", interpretation: "131 está próximo da distribuição central observada; não classifica desempenho sem janela e amostra contemporânea" },
    classification: classification({ durationBand: "31_to_60s", evidence: ["A abertura anuncia história dos inscritos.", "A fala final diz que um inscrito enviou a história, reage a ela e pede compartilhamento para receber mais histórias.", "A descrição credita o canal remetente."], creatorScale: "small" }),
    comparison: { level: 1, group: "histórias curtas enviadas por inscritos, selecionadas e devolvidas em série editorial", referenceIds: ["obs-20260824-038", "obs-20260831-076", "obs-20260831-077"], confidence: "high" },
    observations: ["A transcrição explicita envio por inscrito, reação do apresentador e convite a novos envios.", "A descrição atribui a origem a outro canal."],
    interpretations: ["É o apoio mais compacto ao ciclo envio–resposta–novo convite no lote.", "A ausência de comentários limita a observação de retorno público."],
    limitations: ["Sem audiovisual reproduzível.", "Comentários indisponíveis.", "Consentimento não verificado."],
    provenance: ["public_content", "youtube_auto_transcript", "public_metric", "channel_sample", "observatory_inference"],
    sourceEvidence: ["https://www.youtube.com/watch?v=mayNLQpazhY", "https://www.youtube.com/@eusoubr1607/videos"],
    training: training({ role: "target_support", eligible: true, claims: [{ claim: "envio, resposta editorial e convite recorrente", requiredModalities: ["transcript", "description"], observedModalities: ["transcript", "description"], sufficient: true }], provenance: { storyOrigin: "outro canal/inscrito explicitamente creditado", consentStatus: "unknown", identityProtection: "partial; crédito ao canal sem política de autorização acessível", evidence: ["transcrição automática", "descrição original"] }, hypothesis: supportHypothesis("O apresentador identifica o envio, reage e pede compartilhamento para obter novas histórias.", "Transcrição integral e descrição com crédito.", ["Sem comentários, audiovisual ou consentimento verificável."]) }),
    viralAssessment: { status: "indeterminate", observedSignal: "131 visualizações; mediana de 93,5 na amostra de 30 vídeos", missingForRelativeAssessment: ["janela comparável", "impressões", "retenção", "distribuição"], confounders: ["vídeo de 2020", "mistura de formatos no canal"], causalClaimAllowed: false },
  },
  {
    id: "obs-20260901-084",
    title: "VIZINHA ENGANA MEU MARIDO E LEVA 100$ NA CARA DURA: histórias de seguidores",
    creator: "Edilma Arruda",
    creatorIdentity: "edilma-arruda",
    sourceIdentity: "edilma-arruda",
    country: "BR",
    url: "https://www.youtube.com/watch?v=gzPE8_PWjG0",
    publishedAt: "2025-05-09",
    duration: "PT1M1S",
    createdAt,
    coverage: { level: "partial", accessible: ["título", "descrição", "transcrição automática integral", "zero comentários públicos recuperados", "métricas públicas", "amostra de 30 vídeos atuais do canal"], missing: [...commonMissing, "prova de que o relato foi enviado por seguidor", "consentimento ou anonimização da vizinha e do marido"] },
    publicMetrics: { views: 85, likes: 6, comments: 0, subscribersObserved: 51800, observedAt: "2026-09-01", sourceType: "youtube_public_metadata", causality: "not_inferred" },
    profileBaseline: { sampleSize: 30, medianViews: 552.5, minViews: 143, maxViews: 12000, temporalMatch: "weak", ratioToSampleMedian: 0.154, interpretation: "sinal de baixo desempenho frente à amostra atual, mas não comparador causal nem baseline contemporâneo perfeito" },
    classification: classification({ presentationFormats: ["indeterminado"], primaryFamily: "storytelling", secondaryFamilies: ["comunidade", "identificacao"], functionalMix: [{ family: "storytelling", percentage: 60 }, { family: "comunidade", percentage: 25 }, { family: "identificacao", percentage: 15 }], evidence: ["O título usa histórias de seguidores.", "A transcrição narra o caso como experiência da própria apresentadora e termina pedindo julgamento do público.", "Nenhum comentário público foi recuperado."], creatorScale: "medium" }),
    comparison: { level: 2, group: "relato cotidiano com pergunta de julgamento ao público, mas origem comunitária não demonstrada", referenceIds: ["obs-20260901-081", "obs-20260901-082", "obs-20260901-083"], confidence: "medium" },
    observations: ["A etiqueta do título sugere origem comunitária, mas a fala apresenta o caso como experiência da narradora.", "Há CTA de julgamento.", "O vídeo tem 85 visualizações e zero comentários públicos; a amostra atual do canal tem mediana 552,5."],
    interpretations: ["Sem origem verificável, o caso não apoia o componente de história enviada.", "O baixo sinal público mostra que arquitetura ou etiqueta comunitária não garantem participação nem alcance."],
    limitations: ["Caso-limite, não contraexemplo causal.", "A amostra de baseline é posterior e heterogênea.", "Sem audiovisual ou consentimento."],
    provenance: ["public_content", "youtube_auto_transcript", "public_metric", "channel_sample", "observatory_inference"],
    sourceEvidence: ["https://www.youtube.com/watch?v=gzPE8_PWjG0", "https://www.youtube.com/@edilmaarruda_ofc/videos"],
    training: training({ role: "falsification_or_boundary", eligible: false, claims: [{ claim: "origem comunitária do relato", requiredModalities: ["transcript", "description", "origin_disclosure"], observedModalities: ["transcript", "description"], sufficient: false }], provenance: { storyOrigin: "claimed_in_title_but_not_demonstrated", consentStatus: "unknown", identityProtection: "insufficient; terceiros são descritos sem anonimização verificável", evidence: ["título", "transcrição automática", "descrição"] } }),
    viralAssessment: { status: "indeterminate", observedSignal: "85 visualizações, zero comentários e 0,154x a mediana da amostra atual", missingForRelativeAssessment: ["baseline contemporâneo", "impressões", "retenção", "origem da distribuição"], confounders: ["diferença temporal", "mistura de formatos", "seleção dos 30 vídeos atuais"], causalClaimAllowed: false },
  },
  {
    id: "obs-20260901-085",
    title: "Você sabe a origem da expressão ‘A Cobra vai Fumar’?",
    creator: "Canal 90",
    creatorIdentity: "canal-90",
    sourceIdentity: "canal-90",
    country: "BR",
    url: "https://www.youtube.com/watch?v=2E6m_DhBsOU",
    publishedAt: "2025-04-13",
    duration: "PT1M33S",
    createdAt,
    coverage: { level: "partial", accessible: ["título", "transcrição automática integral", "30 comentários recuperados de 193 indexados", "métricas públicas", "amostra de 30 vídeos do canal"], missing: [...commonMissing, "fontes históricas indicadas na descrição ou na transcrição"] },
    publicMetrics: { views: 129497, likes: 9018, commentsIndexed: 193, commentsRecovered: 30, subscribersObserved: 5710000, observedAt: "2026-09-01", sourceType: "youtube_public_metadata", causality: "not_inferred" },
    profileBaseline: { sampleSize: 30, medianViews: 236000, minViews: 97000, maxViews: 1800000, temporalMatch: "weak", interpretation: "o vídeo fica abaixo da mediana da amostra atual; formatos e datas não são plenamente compatíveis" },
    classification: classification({ presentationFormats: ["camera_direta", "narracao_imagens"], primaryFamily: "storytelling", secondaryFamilies: ["educativo", "curiosidade"], functionalMix: [{ family: "storytelling", percentage: 50 }, { family: "educativo", percentage: 35 }, { family: "curiosidade", percentage: 15 }], objectives: ["educar", "visualizacao", "comentario"], contentTopic: { label: "origem histórica da expressão A cobra vai fumar", iabCode: null }, segment: "história e cultura brasileira", subsegment: "Força Expedicionária Brasileira", probableAudience: "público geral interessado em história e cultura popular", productionLevel: "intermediate", creatorScale: "large", replicability: "medium", mechanisms: ["curiosidade", "surpresa", "identificacao", "confianca"], hookTypes: ["pergunta", "textual"], narrativeElements: ["situacao", "problema", "progressao", "payoff", "conclusao"], proofTypes: ["dado", "alegacao_sem_prova"], ctaTypes: ["nenhum"], evidence: ["A transcrição abre com pergunta literal, explica a expressão e narra sua associação à FEB.", "A fala usa números e um registro histórico, mas não fornece fontes verificáveis.", "Comentários mostram identificação e também repetem alegações sem fonte."], confidence: "medium" }),
    comparison: { level: 2, group: "storytelling histórico curto que parte de frase familiar e oferece origem/correção", referenceIds: ["obs-20260824-039", "obs-20260828-061", "obs-20260828-062"], confidence: "medium" },
    observations: ["A pergunta nomeia assunto e promessa imediatamente.", "A transcrição transforma expressão familiar em narrativa histórica com números.", "Fontes não ficaram acessíveis."],
    interpretations: ["A referência explora um padrão existente, mas não recebe apoio formal por falta de fontes proporcionais e audiovisual."],
    limitations: ["Sem audiovisual reproduzível.", "Afirmações históricas exigem checagem humana e fontes primárias.", "Canal grande limita comparabilidade com pequenos criadores."],
    provenance: ["public_content", "youtube_auto_transcript", "public_comments", "public_metric", "channel_sample", "observatory_inference"],
    sourceEvidence: ["https://www.youtube.com/watch?v=2E6m_DhBsOU", "https://www.youtube.com/@canal90/videos"],
    training: training({ role: "controlled_exploration", eligible: false, claims: [{ claim: "correção histórica verificável", requiredModalities: ["transcript", "historical_sources"], observedModalities: ["transcript"], sufficient: false }], provenance: { storyOrigin: "not_applicable", consentStatus: "not_applicable", identityProtection: "not_applicable", evidence: ["conteúdo histórico, sem relato pessoal da audiência"] } }),
    viralAssessment: { status: "indeterminate", observedSignal: "129.497 visualizações; mediana atual de 236 mil", missingForRelativeAssessment: ["coorte de Shorts contemporâneos", "impressões", "retenção", "distribuição"], confounders: ["escala do canal", "mistura de vídeos longos e curtos", "idade"], causalClaimAllowed: false },
  },
];

const ids = new Set(memory.references.map(reference => reference.id));
const urls = new Set(memory.references.map(reference => reference.url));
for (const reference of references) {
  if (ids.has(reference.id) || urls.has(reference.url)) throw new Error(`Referência duplicada: ${reference.id}`);
  memory.references.push(reference);
}

const pattern = memory.patterns.find(item => item.id === patternId);
if (!pattern) throw new Error(`Padrão não encontrado: ${patternId}`);
for (const referenceId of ["obs-20260901-081", "obs-20260901-082", "obs-20260901-083"]) {
  if (!pattern.supportReferenceIds.includes(referenceId)) pattern.supportReferenceIds.push(referenceId);
}
if (!pattern.caseLimitReferenceIds.includes("obs-20260901-084")) pattern.caseLimitReferenceIds.push("obs-20260901-084");
pattern.evidence.push(
  { referenceId: "obs-20260901-081", role: "support", comparisonLevel: 1, requiredEvidenceObserved: true, confidence: "high", observation: "Série numerada transforma relato de inscrita em pauta e pede novos envios nos comentários.", evidence: "Descrição, transcrição integral e comentários.", limitations: ["Consentimento de menores e audiovisual não verificados."] },
  { referenceId: "obs-20260901-082", role: "support", comparisonLevel: 1, requiredEvidenceObserved: true, confidence: "high", observation: "Canal seleciona relatos, responde aos envios e promete nova publicação.", evidence: "Transcrição integral, comentários e episódio comparador.", limitations: ["Consentimento, audiovisual e retenção não verificados."] },
  { referenceId: "obs-20260901-083", role: "support", comparisonLevel: 1, requiredEvidenceObserved: true, confidence: "high", observation: "Apresentador identifica o envio, reage e convida novas histórias.", evidence: "Transcrição integral e crédito na descrição.", limitations: ["Sem comentários, audiovisual ou consentimento verificável."] },
  { referenceId: "obs-20260901-084", role: "case_limit", comparisonLevel: 2, requiredEvidenceObserved: false, confidence: "medium", observation: "Título reivindica história de seguidor, mas a fala apresenta experiência da narradora; o caso tem sinal público baixo.", evidence: "Título, transcrição integral, zero comentários e amostra atual do canal.", limitations: ["Origem comunitária ausente e baseline temporalmente fraco; não é contraexemplo causal."] },
);
pattern.supportingCount = pattern.supportReferenceIds.length;
pattern.comparableSupportCount = pattern.supportReferenceIds.length;
pattern.caseLimitCount = pattern.caseLimitReferenceIds.length;
pattern.creatorDiversityCount = 7;
pattern.sourceDiversityCount = 7;
pattern.confidence = "medium";
pattern.limitations = pattern.limitations.map(item => item
  .replace("Nenhum dos cinco apoios teve retenção, comentários ou execução audiovisual integralmente auditados.", "Os cinco apoios anteriores não tiveram retenção, comentários ou execução audiovisual integralmente auditados.")
  .replace("Dois apoios pertencem à mesma criadora; a diversidade efetiva é de quatro criadores/fontes.", "Dois apoios anteriores pertencem à mesma criadora; o lote 013 elevou a diversidade total para sete criadores/fontes."));
pattern.limitations = [...new Set([...pattern.limitations, "O lote 013 observou transcrições e comentários integrais, mas não conseguiu reproduzir a mídia audiovisual no ambiente.", "Relatos de menores com nome e idade expostos mostram que consentimento e anonimização devem ser auditados antes da replicação.", "Um caso com baixo sinal público reforça que a arquitetura editorial não garante desempenho."])];

for (const hypothesis of memory.hypotheses) {
  const mapping = {
    "hyp-20260824-013": "pat-20260831-008",
    "hyp-20260824-014": "pat-20260828-006",
    "hyp-20260824-016": "pat-20260829-007",
  };
  if (mapping[hypothesis.id]) hypothesis.consolidatedIntoPatternId = mapping[hypothesis.id];
}

memory.trainingRuns.push({
  id: "run-20260901-supervised-013",
  executedAt: createdAt,
  batchPolicyVersion: "1.1",
  requestedBatchSize: 5,
  candidatesFound: 61,
  referenceIds: references.map(reference => reference.id),
  targetKnowledgeId: patternId,
  targetReferenceIds: ["obs-20260901-081", "obs-20260901-082", "obs-20260901-083"],
  falsificationOrBoundaryReferenceIds: ["obs-20260901-084"],
  controlledExplorationReferenceIds: ["obs-20260901-085"],
  discarded: [
    { url: "https://www.youtube.com/watch?v=iIJ-jqy_7Tw", reason: "o título diz histórias dos inscritos, mas a transcrição descreve história própria e não demonstra envio da audiência" },
    { url: "https://www.youtube.com/watch?v=XWtOEzF1lO4", reason: "sem transcrição e sem mídia reproduzível para observar o mecanismo" },
    { url: "https://www.youtube.com/watch?v=09tQhEieZeE", reason: "vídeo indisponível durante a verificação" },
    { url: "https://www.youtube.com/watch?v=j2qcMYXhBxg", reason: "vídeo indisponível durante a verificação" },
  ],
  analyzed: 5,
  brazilianReferences: 5,
  internationalReferences: 0,
  smallOrMediumCreatorReferences: 4,
  coverageSummary: { complete: 0, partial: 5, insufficient: 0 },
  audiovisualAcquisition: { attempted: true, succeeded: 0, failure: "CDN de mídia do YouTube expirou por timeout; metadados, transcrições automáticas e comentários permaneceram acessíveis", effect: "cenas, áudio ouvido, texto na tela, cortes e ritmo ficaram não mensurados" },
  commentsCoverage: { fullOrDeclaredZero: 4, partialSample: 1 },
  baselineCoverage: { sampledProfiles: 5, contemporaneousBaselines: 0, limitation: "amostras públicas de canal não garantem coorte temporal e funcional" },
  patternsCreated: [],
  patternsStrengthened: [patternId],
  patternsRefined: [patternId],
  hypothesesCreated: [],
  hypothesesStrengthened: [],
  validatedPatternsCreated: 0,
  contradictionsFound: [],
  caseLimitsFound: ["rótulo histórias de seguidores sem origem comunitária demonstrada", "baixo sinal público sem baseline contemporâneo suficiente para atribuição causal"],
  safetyFindings: ["comentários e relatos expõem nomes e idades de menores; consentimento e anonimização não foram verificáveis"],
  evidenceGateSummary: { targetSupportsEligible: 3, targetSupportsRejected: 0, boundaryCases: 1, explorationReferences: 1, duplicateUrls: 0, independentCreatorsAddedToPattern: 3, newHypotheses: 0 },
  outcome: "Três apoios pequenos ampliaram a diversidade do padrão; um caso-limite mostrou baixo sinal público e origem comunitária não comprovada. O padrão permanece provisório e sem alegação de desempenho.",
  nextTarget: "obter vídeo curto brasileiro com arquivo audiovisual diretamente acessível, consentimento documentado, comentários, baseline contemporâneo e um teste de baixo desempenho funcionalmente comparável",
  limitations: ["Nenhuma mídia audiovisual integral foi reproduzida.", "Transcrição automática pode conter erros.", "Baselines públicos não foram contemporâneos.", "Consentimento e autenticidade dos relatos não foram verificados.", "Nenhum resultado autoriza causalidade ou validação."],
});

memory.updatedAt = createdAt;
fs.writeFileSync(memoryPath, `${JSON.stringify(memory, null, 2)}\n`);
console.log(JSON.stringify({ added: references.length, references: memory.references.length, patterns: memory.patterns.length, run: "013" }, null, 2));
