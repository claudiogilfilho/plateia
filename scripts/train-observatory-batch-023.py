#!/usr/bin/env python3
import json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "knowledge/observatory/plateia-memory.json"
memory = json.loads(DB.read_text(encoding="utf-8"))

BATCH_IDS = {f"obs-20260911-{value}" for value in range(131, 136)}
memory["references"] = [item for item in memory["references"] if item.get("id") not in BATCH_IDS]
memory["patterns"] = [item for item in memory["patterns"] if item.get("id") != "pat-20260911-011"]
memory["trainingRuns"] = [item for item in memory["trainingRuns"] if item.get("id") != "run-20260911-supervised-023"]
for item in memory["hypotheses"]:
    if item.get("id") == "hyp-20260830-033" and item.get("previousStatement"):
        item["statement"] = item.pop("previousStatement")
        item["status"] = "observed_not_promoted"
        item["supportReferenceIds"] = [value for value in item.get("supportReferenceIds", []) if value not in BATCH_IDS]
        for key in ["promotedPatternId", "consolidatedIntoPatternId", "promotionReason"]:
            item.pop(key, None)

NOW = "2026-09-11T11:34:38.000Z"
OBSERVED = "2026-09-11"
MISSING_AV = [
    "vídeo integral auditado quadro a quadro",
    "imagem em movimento efetivamente analisada",
    "áudio ouvido",
    "texto na tela",
    "edição",
    "ritmo",
    "curva de retenção",
    "baseline funcional contemporâneo",
    "impressões e fontes de tráfego",
    "mídia paga",
]


def make_ref(*, id, title, creator, identity, country, url, published, duration,
             metrics, accessible, missing, classification, comparison,
             observations, interpretations, scores, lenses, replicable,
             limitations, role, evidence_level, support, claims,
             provenance_consent, provenance):
    return {
        "id": id,
        "title": title,
        "creator": creator,
        "creatorIdentity": identity,
        "sourceIdentity": identity,
        "country": country,
        "url": url,
        "publishedAt": published,
        "duration": duration,
        "createdAt": NOW,
        "coverage": {"level": "partial", "accessible": accessible, "missing": missing},
        "publicMetrics": {
            **metrics,
            "observedAt": OBSERVED,
            "sourceType": "youtube_public_metadata_transcript_description_and_comments_after_public_search",
            "causality": "not_inferred",
        },
        "classification": classification,
        "comparison": comparison,
        "observations": observations,
        "interpretations": interpretations,
        "scores": scores,
        "fiveLenses": lenses,
        "hypotheses": [],
        "replicable": replicable,
        "limitations": limitations,
        "provenance": provenance,
        "sourceEvidence": [url],
        "training": {
            "evidencePolicyVersion": "1.1",
            "evidenceRole": role,
            "evidenceLevel": evidence_level,
            "requiredEvidenceObserved": support,
            "supportEligible": support,
            "claimCoverage": claims,
            "provenanceAndConsent": provenance_consent,
            "replicable": replicable,
            "contingent": limitations,
            "notRecommended": [
                "copiar frase, personagem ou roteiro",
                "tratar volume de comentários, visualizações ou tamanho do canal como prova de aprendizagem",
                "confundir pedido de engajamento com exercício aplicado",
                "inferir cenas, áudio, edição, ritmo, retenção ou causalidade não observados",
            ],
            "hypotheses": [],
        },
        "viralAssessment": {
            "status": "indeterminate",
            "observedSignal": metrics.get("viewsObserved", "não mensurado"),
            "missingForRelativeAssessment": ["baseline funcional contemporâneo", "retenção", "impressões", "fontes de tráfego", "mídia paga"],
            "confounders": ["tamanho do canal", "distribuição", "idade do vídeo", "tema", "oferta"],
            "causalClaimAllowed": False,
        },
    }


refs = [
    make_ref(
        id="obs-20260911-131",
        title='POST ou AFTER? Como dizer "DEPOIS" em inglês?',
        creator="ANAEL THE TEACHER",
        identity="anael-the-teacher",
        country="BR",
        url="https://www.youtube.com/shorts/7Hmnq1jVmTI",
        published="2026-02-11",
        duration="PT41S",
        metrics={"viewsObserved": "150", "likesObserved": "não disponível", "commentsObserved": "0 declarado", "subscriberCountObserved": "2,58 mil"},
        accessible=["título", "criadora", "descrição integral", "data exata", "duração", "transcrição automática integral com timestamps", "fala por substituição textual", "150 visualizações", "zero comentários declarado", "2,58 mil inscritos"],
        missing=MISSING_AV,
        classification={
            "taxonomyVersion": "3.0", "container": "youtube_short", "materialFormat": "video_curto",
            "presentationFormats": ["tutorial"], "primaryFamily": "educativo", "secondaryFamilies": ["comunidade", "venda_indireta"],
            "functionalMix": [{"family": "educativo", "percentage": 65}, {"family": "comunidade", "percentage": 20}, {"family": "venda_indireta", "percentage": 15}],
            "objectives": ["educar", "comentario", "seguidores"], "advertisingType": "geracao_de_leads", "commercialIntent": "explicita",
            "advertisedEntity": {"kind": "servico", "name": "aulas ANAEL THE TEACHER", "confidence": "high"},
            "contentTopic": {"label": "diferença de uso entre post e after", "iabCode": None},
            "segment": "educação e idiomas", "subsegment": "vocabulário de inglês para brasileiros", "probableAudience": "brasileiros iniciantes ou intermediários em inglês",
            "awarenessStage": "consciente_problema", "productionLevel": "simple", "creatorScale": "small", "replicability": "high",
            "durationBand": "31_to_60s", "pace": "unknown", "mechanisms": ["utilidade_pratica", "recompensa", "pertencimento"],
            "hookTypes": ["pergunta", "problema"], "narrativeElements": ["problema", "mecanismo", "conclusao", "cta"],
            "proofTypes": ["mecanismo_explicado"], "ctaTypes": ["comentar", "seguir"],
            "distributionContext": {"organicPaid": "unknown", "trendDependency": "low"}, "confidence": "high",
            "evidence": ["A fala distingue os dois usos e a descrição pede uma frase com after nos comentários.", "A publicação declara zero comentários; isso não prova ausência de prática fora da plataforma."],
            "alternativeClassifications": ["comunidade como família secundária"], "missingInformation": MISSING_AV, "needsHumanReview": True,
        },
        comparison={"level": 2, "group": "aula de idioma cujo CTA pede aplicação do conteúdo em uma frase", "referenceIds": ["obs-20260830-075", "obs-20260911-132", "obs-20260911-133"], "confidence": "high"},
        observations=["A explicação diferencia uso cotidiano e uso formal antes do CTA.", "A descrição transforma o comentário em tarefa delimitada: produzir uma frase com o termo ensinado.", "Zero comentários foi registrado como métrica pública, não como nota nem prova de falha."],
        interpretations=["O CTA mantém continuidade semântica com a aula.", "Sem respostas observadas, não se sabe se a tarefa foi executada ou compreendida."],
        scores={"gancho": 86, "clareza": 90, "relevancia": 87, "desejo": 70, "confianca": 80, "retencao": "not_assessed", "acao": 91, "objecoes": 82},
        lenses={"apressado": "Entende a dúvida e a distinção na fala transcrita.", "analitico": "Recebe regra e exemplos; a execução visual não foi auditada.", "aspiracional": "A tarefa oferece uso imediato, sem prometer fluência.", "comunidade": "Pode responder com frase, mas não houve resposta pública.", "cetico": "Não há base para afirmar aprendizagem ou engajamento."},
        replicable=["Pedir uma produção curta usando exatamente o item ensinado.", "Definir a unidade de resposta, como uma frase, em vez de pedir comentário genérico."],
        limitations=["A instrução mais específica está na descrição; a fala pede comentário de forma menos delimitada.", "Zero comentários não é contraexemplo sem alcance comparável e baseline.", "Audiovisual e retenção não foram auditados."],
        role="target_support", evidence_level=2, support=True,
        claims=[
            {"claim": "a publicação ensina uma distinção de uso", "requiredModalities": ["transcript", "description"], "observedModalities": ["transcript", "description"], "sufficient": True},
            {"claim": "o CTA pede uma frase que aplique o conteúdo", "requiredModalities": ["description"], "observedModalities": ["description"], "sufficient": True},
        ],
        provenance_consent={"storyOrigin": "explicação didática original da criadora", "consentStatus": "not_applicable", "identityProtection": "not_applicable", "evidence": ["nenhuma história pessoal ou pessoa terceira é usada na cobertura textual"]},
        provenance=["public_content", "youtube_public_metadata", "youtube_automatic_transcript", "youtube_public_description", "public_metric", "observatory_inference"],
    ),
    make_ref(
        id="obs-20260911-132",
        title="LIE X LAY — entenda em menos de 2 minutos",
        creator="Teacher Natália de Oliveira",
        identity="teacher-natalia-de-oliveira",
        country="BR",
        url="https://www.youtube.com/watch?v=IQEATjqQiXc",
        published="2024-06-11",
        duration="PT1M38S",
        metrics={"viewsObserved": "39", "likesObserved": "não disponível", "commentsObserved": "não disponível", "subscriberCountObserved": "2,2 mil"},
        accessible=["título", "criadora", "descrição integral", "data exata", "duração", "transcrição automática integral com timestamps", "fala por substituição textual", "39 visualizações", "2,2 mil inscritos"],
        missing=MISSING_AV + ["comentários públicos"],
        classification={
            "taxonomyVersion": "3.0", "container": "youtube_video", "materialFormat": "video_longo",
            "presentationFormats": ["tutorial"], "primaryFamily": "educativo", "secondaryFamilies": ["comunidade", "identificacao"],
            "functionalMix": [{"family": "educativo", "percentage": 70}, {"family": "comunidade", "percentage": 20}, {"family": "identificacao", "percentage": 10}],
            "objectives": ["educar", "comentario", "salvamento"], "advertisingType": "editorial_organico", "commercialIntent": "implicita",
            "advertisedEntity": {"kind": "servico", "name": "conteúdo educacional Teacher Natália", "confidence": "medium"},
            "contentTopic": {"label": "diferença entre lie e lay", "iabCode": None},
            "segment": "educação e idiomas", "subsegment": "gramática e vocabulário de inglês", "probableAudience": "brasileiros que confundem verbos de forma semelhante",
            "awarenessStage": "consciente_problema", "productionLevel": "simple", "creatorScale": "small", "replicability": "high",
            "durationBand": "over_60s", "pace": "unknown", "mechanisms": ["utilidade_pratica", "recompensa", "identificacao"],
            "hookTypes": ["problema", "promessa"], "narrativeElements": ["problema", "mecanismo", "conclusao", "cta"],
            "proofTypes": ["mecanismo_explicado"], "ctaTypes": ["comentar", "salvar"],
            "distributionContext": {"organicPaid": "unknown", "trendDependency": "low"}, "confidence": "high",
            "evidence": ["A fala explica significados, transitividade e exemplos antes de pedir uma frase com um dos verbos.", "Comentários e respostas da criadora não ficaram acessíveis."],
            "alternativeClassifications": [], "missingInformation": MISSING_AV + ["comentários públicos"], "needsHumanReview": True,
        },
        comparison={"level": 2, "group": "aula de idioma cujo CTA pede aplicação do conteúdo em uma frase", "referenceIds": ["obs-20260830-075", "obs-20260911-131", "obs-20260911-133"], "confidence": "high"},
        observations=["A diferença entre os verbos é explicada por regras e exemplos.", "A fala encerra pedindo uma frase com um dos verbos para que a professora possa ajudar.", "A ajuda prometida não pôde ser verificada sem comentários acessíveis."],
        interpretations=["A tarefa exige recuperação e produção, não apenas opinião.", "A promessa de feedback é contingente à moderação e não foi demonstrada."],
        scores={"gancho": 84, "clareza": 88, "relevancia": 88, "desejo": 68, "confianca": 82, "retencao": "not_assessed", "acao": 93, "objecoes": 84},
        lenses={"apressado": "Entende rapidamente a confusão tratada.", "analitico": "Recebe distinção e exemplos; ASR pode errar palavras inglesas.", "aspiracional": "Pode aplicar a regra numa frase própria.", "comunidade": "Há convite a receber ajuda, mas a interação não foi observada.", "cetico": "Sem comentários, não há prova do feedback anunciado."},
        replicable=["Encerrar uma explicação com uma produção que use a regra recém-ensinada.", "Oferecer feedback somente quando houver capacidade real de moderação."],
        limitations=["Transcrição automática pode confundir lie, lay e flexões.", "Comentários e feedback não foram observados.", "Audiovisual e retenção não foram auditados."],
        role="target_support", evidence_level=2, support=True,
        claims=[
            {"claim": "a diferença entre dois verbos é explicada", "requiredModalities": ["transcript"], "observedModalities": ["transcript"], "sufficient": True},
            {"claim": "a fala pede uma frase que aplique um dos verbos", "requiredModalities": ["transcript"], "observedModalities": ["transcript"], "sufficient": True},
        ],
        provenance_consent={"storyOrigin": "explicação didática original da criadora", "consentStatus": "not_applicable", "identityProtection": "not_applicable", "evidence": ["nenhuma história pessoal ou pessoa terceira é usada"]},
        provenance=["public_content", "youtube_public_metadata", "youtube_automatic_transcript", "youtube_public_description", "public_metric", "observatory_inference"],
    ),
    make_ref(
        id="obs-20260911-133",
        title="From To vs From Through: você sabe as diferenças?",
        creator="Fluency Academy",
        identity="fluency-academy",
        country="BR",
        url="https://www.youtube.com/watch?v=67x9KP7uaG8",
        published="2022-07-11",
        duration="PT1M38S",
        metrics={"viewsObserved": "3.436", "likesObserved": "não disponível", "commentsObserved": "14 integralmente extraídos", "subscriberCountObserved": "1,04 milhão"},
        accessible=["título", "criador", "descrição integral", "data exata", "duração", "transcrição automática integral com timestamps", "fala por substituição textual", "3.436 visualizações", "14 comentários integralmente extraídos", "1,04 milhão de inscritos"],
        missing=MISSING_AV,
        classification={
            "taxonomyVersion": "3.0", "container": "youtube_video", "materialFormat": "video_longo",
            "presentationFormats": ["tutorial"], "primaryFamily": "educativo", "secondaryFamilies": ["comunidade", "venda_indireta"],
            "functionalMix": [{"family": "educativo", "percentage": 65}, {"family": "comunidade", "percentage": 20}, {"family": "venda_indireta", "percentage": 15}],
            "objectives": ["educar", "comentario", "lead", "venda"], "advertisingType": "geracao_de_leads", "commercialIntent": "explicita",
            "advertisedEntity": {"kind": "servico", "name": "turmas e portal Fluency Academy", "confidence": "high"},
            "contentTopic": {"label": "diferença entre from to e from through", "iabCode": None},
            "segment": "educação e idiomas", "subsegment": "gramática prática de inglês", "probableAudience": "brasileiros estudantes de inglês",
            "awarenessStage": "consciente_problema", "productionLevel": "simple", "creatorScale": "large", "replicability": "high",
            "durationBand": "over_60s", "pace": "unknown", "mechanisms": ["utilidade_pratica", "recompensa", "pertencimento", "confianca"],
            "hookTypes": ["pergunta", "problema"], "narrativeElements": ["problema", "mecanismo", "progressao", "conclusao", "cta"],
            "proofTypes": ["mecanismo_explicado"], "ctaTypes": ["comentar", "cadastrar", "seguir"],
            "distributionContext": {"organicPaid": "unknown", "trendDependency": "low"}, "confidence": "high",
            "evidence": ["A descrição pede uma frase usando uma das estruturas.", "Entre 14 comentários, um aluno publica uma frase e uma dúvida recebe explicação da marca seguida de confirmação do entendimento."],
            "alternativeClassifications": ["venda indireta como família secundária"], "missingInformation": MISSING_AV, "needsHumanReview": True,
        },
        comparison={"level": 2, "group": "aula de idioma cujo CTA pede aplicação do conteúdo em uma frase", "referenceIds": ["obs-20260830-075", "obs-20260911-131", "obs-20260911-132"], "confidence": "high"},
        observations=["A explicação contrasta alcance temporal das duas estruturas.", "A descrição pede uma frase em inglês usando uma delas.", "A amostra integral de 14 comentários contém uma produção de aluno e uma sequência dúvida, explicação da marca e confirmação do aluno."],
        interpretations=["Há ao menos uma instância observável de prática e uma de feedback.", "Uma interação não demonstra aprendizagem em escala; o tamanho do canal e a oferta são confundidores."],
        scores={"gancho": 85, "clareza": 89, "relevancia": 88, "desejo": 72, "confianca": 86, "retencao": "not_assessed", "acao": 94, "objecoes": 84},
        lenses={"apressado": "Entende a distinção e recebe exemplos compactos.", "analitico": "Pode conferir regra, frase de aluno e resposta explicativa.", "aspiracional": "A tarefa permite testar uso próprio.", "comunidade": "Há uma pequena evidência de resposta e retorno, não de comunidade ampla.", "cetico": "O canal é grande e comercial; a interação observada não autoriza causalidade."},
        replicable=["Pedir uma frase que aplique uma escolha ensinada.", "Responder dúvidas com a regra por trás da resposta, não apenas elogiar."],
        limitations=["Canal grande e oferta comercial limitam comparações de desempenho.", "Apenas uma produção e uma troca explicativa foram observadas.", "Audiovisual, retenção e baseline não foram auditados."],
        role="target_support", evidence_level=2, support=True,
        claims=[
            {"claim": "o CTA pede uma frase que aplique o conteúdo", "requiredModalities": ["description"], "observedModalities": ["description"], "sufficient": True},
            {"claim": "há uma produção de aluno e uma troca explicativa", "requiredModalities": ["comments"], "observedModalities": ["comments"], "sufficient": True},
        ],
        provenance_consent={"storyOrigin": "explicação didática e comentários públicos", "consentStatus": "public_comments_only", "identityProtection": "usernames_not_reproduced", "evidence": ["o registro preserva a função das respostas sem copiar nomes ou texto integral"]},
        provenance=["public_content", "youtube_public_metadata", "youtube_automatic_transcript", "youtube_public_description", "youtube_public_comments", "public_metric", "observatory_inference"],
    ),
    make_ref(
        id="obs-20260911-134",
        title="Teste seu nível de inglês em 3 minutes; comente seu nível",
        creator="Online English and Portuguese Courses",
        identity="online-english-and-portuguese-courses",
        country="unknown",
        url="https://www.youtube.com/watch?v=qhkYu-kaH6E",
        published="2026-07-11",
        duration="PT3M34S",
        metrics={"viewsObserved": "1.971", "likesObserved": "130", "commentsObserved": "2 integralmente extraídos", "subscriberCountObserved": "19,7 mil"},
        accessible=["título", "criador", "descrição integral", "data exata", "duração", "transcrição automática integral com timestamps", "fala por substituição textual", "1.971 visualizações", "130 curtidas", "2 comentários integralmente extraídos", "19,7 mil inscritos"],
        missing=MISSING_AV,
        classification={
            "taxonomyVersion": "3.0", "container": "youtube_video", "materialFormat": "video_longo",
            "presentationFormats": ["desafio", "tutorial"], "primaryFamily": "educativo", "secondaryFamilies": ["curiosidade", "venda_indireta"],
            "functionalMix": [{"family": "educativo", "percentage": 60}, {"family": "curiosidade", "percentage": 25}, {"family": "venda_indireta", "percentage": 15}],
            "objectives": ["educar", "comentario", "venda"], "advertisingType": "oferta_direta", "commercialIntent": "explicita",
            "advertisedEntity": {"kind": "produto", "name": "aulas intensivas e e-book", "confidence": "high"},
            "contentTopic": {"label": "quiz de tradução e autoavaliação de nível de inglês", "iabCode": None},
            "segment": "educação e idiomas", "subsegment": "quiz de vocabulário em inglês", "probableAudience": "estudantes de inglês que querem autoavaliar vocabulário",
            "awarenessStage": "consciente_problema", "productionLevel": "simple", "creatorScale": "medium", "replicability": "high",
            "durationBand": "over_60s", "pace": "unknown", "mechanisms": ["curiosidade", "recompensa", "utilidade_pratica"],
            "hookTypes": ["pergunta", "promessa"], "narrativeElements": ["promessa", "progressao", "cta"],
            "proofTypes": ["mecanismo_explicado"], "ctaTypes": ["comentar", "seguir", "comprar"],
            "distributionContext": {"organicPaid": "unknown", "trendDependency": "unknown"}, "confidence": "high",
            "evidence": ["A fala apresenta sucessivas perguntas de tradução com respostas.", "A descrição pede acerto, palavra desejada e nível; não exige aplicar uma unidade ensinada numa produção."],
            "alternativeClassifications": ["curiosidade como família principal"], "missingInformation": MISSING_AV, "needsHumanReview": True,
        },
        comparison={"level": 2, "group": "aula de idioma com CTA de comentário ligado ao tema, mas sem produção aplicada delimitada", "referenceIds": ["obs-20260911-131", "obs-20260911-132", "obs-20260911-133"], "confidence": "high"},
        observations=["O quiz permite responder mentalmente a traduções.", "O CTA pede autoavaliação ou preferência, não uma frase que use o conteúdo.", "Os dois comentários disponíveis não contêm resposta substantiva ao exercício; isso não prova que o CTA falhou."],
        interpretations=["É um caso-limite entre CTA temático e exercício produtivo.", "Autoavaliação pode gerar participação, mas não demonstra aplicação ou feedback."],
        scores={"gancho": 84, "clareza": 86, "relevancia": 82, "desejo": 70, "confianca": 62, "retencao": "not_assessed", "acao": 69, "objecoes": 64},
        lenses={"apressado": "Entende que é um teste de nível.", "analitico": "Recebe itens e respostas, mas o CTA mede autoimagem, não produção.", "aspiracional": "Pode se reconhecer num nível declarado.", "comunidade": "Há convite a comentar, sem troca substantiva observada.", "cetico": "Número de acertos não foi ligado a critério validado de nível."},
        replicable=["Separar CTA de autoavaliação de tarefa de aplicação.", "Se a meta for prática, pedir resposta produtiva e oferecer critério de feedback."],
        limitations=["Não é contraexemplo: falta baseline e a previsão de aprendizagem não foi medida.", "O teste não apresenta validação de nível na cobertura.", "Audiovisual e retenção não foram auditados."],
        role="falsification_or_boundary", evidence_level=2, support=False,
        claims=[
            {"claim": "o CTA pede autoavaliação e preferência", "requiredModalities": ["description"], "observedModalities": ["description"], "sufficient": True},
            {"claim": "o CTA não exige uma frase que aplique o conteúdo", "requiredModalities": ["description", "transcript"], "observedModalities": ["description", "transcript"], "sufficient": True},
        ],
        provenance_consent={"storyOrigin": "quiz didático e comentários públicos", "consentStatus": "public_comments_only", "identityProtection": "usernames_not_reproduced", "evidence": ["nenhuma história pessoal é usada e os comentários foram resumidos sem nomes"]},
        provenance=["public_content", "youtube_public_metadata", "youtube_automatic_transcript", "youtube_public_description", "youtube_public_comments", "public_metric", "observatory_inference"],
    ),
    make_ref(
        id="obs-20260911-135",
        title="Casal feliz e verdadeiro — Desabafo de um japonês",
        creator="Desabafo de um Japonês / ator Henrique Kimura",
        identity="desabafo-de-um-japones-henrique-kimura",
        country="BR",
        url="https://www.youtube.com/shorts/XjeUfrCPYQo",
        published="2026-07-23",
        duration="PT10S",
        metrics={"viewsObserved": "13.591", "likesObserved": "104", "commentsObserved": "não disponível", "subscriberCountObserved": "44,9 mil"},
        accessible=["título", "criador e ator", "descrição integral", "data exata", "duração", "13.591 visualizações", "104 curtidas", "44,9 mil inscritos"],
        missing=MISSING_AV + ["transcrição", "fala", "comentários públicos", "cenas e desfecho"],
        classification={
            "taxonomyVersion": "3.0", "container": "youtube_short", "materialFormat": "video_curto",
            "presentationFormats": ["esquete"], "primaryFamily": "humor", "secondaryFamilies": ["identificacao", "entretenimento"],
            "functionalMix": [{"family": "humor", "percentage": 60}, {"family": "identificacao", "percentage": 25}, {"family": "entretenimento", "percentage": 15}],
            "objectives": ["visualizacao", "identificacao", "compartilhamento"], "advertisingType": "editorial_organico", "commercialIntent": "ausente",
            "advertisedEntity": {"kind": "nenhuma", "name": "", "confidence": "medium"},
            "contentTopic": {"label": "humor de personagem sobre cotidiano brasileiro e casal", "iabCode": None},
            "segment": "humor de situação", "subsegment": "casal e cotidiano brasileiro", "probableAudience": "público brasileiro de humor curto",
            "awarenessStage": "inconsciente", "productionLevel": "intermediate", "creatorScale": "medium", "replicability": "medium",
            "durationBand": "up_to_15s", "pace": "unknown", "mechanisms": ["humor", "identificacao"],
            "hookTypes": ["identificacao"], "narrativeElements": [], "proofTypes": ["nenhuma"], "ctaTypes": ["nenhum"],
            "distributionContext": {"organicPaid": "unknown", "trendDependency": "unknown"}, "confidence": "low",
            "evidence": ["Título e descrição atribuem o conteúdo a um personagem nervoso e ao cotidiano brasileiro.", "Sem vídeo ou fala não se observa a situação, escalada ou recompensa."],
            "alternativeClassifications": ["entretenimento como família principal"], "missingInformation": MISSING_AV + ["transcrição", "cenas e desfecho"], "needsHumanReview": True,
        },
        comparison={"level": 4, "group": "exploração controlada de humor de personagem; não comparável ao alvo educacional", "referenceIds": [], "confidence": "low"},
        observations=["O título promete um recorte de casal e a descrição posiciona um personagem recorrente ligado ao cotidiano brasileiro.", "Nenhuma cena, fala, conflito, escalada ou recompensa ficou acessível."],
        interpretations=["A descrição delimita território cultural e personagem, mas não permite ensinar a execução do humor."],
        scores={"gancho": 72, "clareza": 68, "relevancia": "not_assessed", "desejo": "not_assessed", "confianca": "not_assessed", "retencao": "not_assessed", "acao": "not_assessed", "objecoes": "not_assessed"},
        lenses={"apressado": "Reconhece casal e humor pelo título.", "analitico": "Não consegue verificar premissa ou payoff.", "aspiracional": "Não mensurado.", "comunidade": "O território brasileiro é declarado, mas identificação não foi observada.", "cetico": "Métricas e descrição não substituem a cena."},
        replicable=["Somente a delimitação explícita de personagem e território cultural pôde ser observada; a estrutura humorística não deve ser ensinada."],
        limitations=["Cobertura insuficiente para analisar cenas, fala, escalada, ritmo ou payoff.", "Métricas absolutas não demonstram eficácia.", "Nenhuma hipótese foi criada."],
        role="controlled_exploration", evidence_level=4, support=False,
        claims=[
            {"claim": "a descrição posiciona personagem e cotidiano brasileiro", "requiredModalities": ["title", "description"], "observedModalities": ["title", "description"], "sufficient": True},
            {"claim": "a execução humorística foi observada", "requiredModalities": ["video_or_frames", "transcript"], "observedModalities": [], "sufficient": False},
        ],
        provenance_consent={"storyOrigin": "personagem ficcional declarado na descrição", "consentStatus": "not_applicable", "identityProtection": "not_applicable", "evidence": ["o ator é creditado publicamente e nenhuma história de terceiro ficou acessível"]},
        provenance=["public_content", "youtube_public_metadata", "youtube_public_description", "public_metric", "observatory_inference"],
    ),
]

existing_urls = {item.get("url") for item in memory["references"]}
for item in refs:
    if item["url"] in existing_urls:
        raise SystemExit(f"URL duplicada: {item['url']}")
memory["references"].extend(refs)

hyp = next(item for item in memory["hypotheses"] if item["id"] == "hyp-20260830-033")
hyp["previousStatement"] = hyp["statement"]
hyp["statement"] = "Em conteúdo educacional, converter o CTA em uma tarefa que exige aplicar no comentário a unidade recém-ensinada cria continuidade observável entre aula e participação; efeitos sobre prática real, qualidade das respostas, aprendizagem ou comunidade permanecem não medidos."
hyp["status"] = "promoted_to_provisional"
hyp["supportReferenceIds"] = list(dict.fromkeys(hyp.get("supportReferenceIds", []) + ["obs-20260911-131", "obs-20260911-132", "obs-20260911-133"]))
hyp["promotedPatternId"] = "pat-20260911-011"
hyp["consolidatedIntoPatternId"] = "pat-20260911-011"
hyp["promotionReason"] = "A formulação anterior misturava tarefa aplicada, respostas entre pares e efeito comunitário. Três novas referências independentes mostram diretamente uma instrução para produzir frase com a unidade ensinada; somente uma possui pequena evidência pública de execução e feedback. O padrão foi restringido à continuidade estrutural entre aula e CTA."

memory["patterns"].append({
    "id": "pat-20260911-011", "status": "provisional", "stage": "provisional",
    "name": "CTA de comentário convertido em exercício da aula",
    "statement": hyp["statement"], "creativeFamily": "educativo", "objective": "prática e comentário", "segment": "educação e idiomas",
    "mechanism": ["utilidade_pratica", "recompensa", "pertencimento"],
    "conditions": ["conteúdo instrucional identificável", "tarefa exige usar a unidade recém-ensinada", "unidade de resposta delimitada", "CTA vai além de opinião, curtida ou autoavaliação"],
    "supportReferenceIds": ["obs-20260911-131", "obs-20260911-132", "obs-20260911-133"],
    "precursorReferenceIds": ["obs-20260830-075"],
    "comparableSupportCount": 3, "supportingCount": 3, "counterexampleCount": 0, "caseLimitCount": 1,
    "counterexampleReferenceIds": [], "caseLimitReferenceIds": ["obs-20260911-134"], "comparisonLevel": 2,
    "confidence": "medium", "creatorDiversityCount": 3, "sourceDiversityCount": 3, "patternType": "cta",
    "evidence": [
        {"referenceId": "obs-20260911-131", "role": "support", "comparisonLevel": 2, "requiredEvidenceObserved": True, "confidence": "high", "observation": "Descrição pede uma frase com a unidade ensinada após explicação transcrita.", "evidence": "Descrição e transcrição automática integrais.", "limitations": ["zero comentários", "sem audiovisual ou retenção"]},
        {"referenceId": "obs-20260911-132", "role": "support", "comparisonLevel": 2, "requiredEvidenceObserved": True, "confidence": "high", "observation": "Fala pede uma frase com um dos verbos explicados e oferece ajuda.", "evidence": "Transcrição automática integral e descrição.", "limitations": ["comentários e feedback não acessíveis", "sem audiovisual ou retenção"]},
        {"referenceId": "obs-20260911-133", "role": "support", "comparisonLevel": 2, "requiredEvidenceObserved": True, "confidence": "high", "observation": "Descrição pede frase aplicada; comentários mostram uma produção e uma troca explicativa.", "evidence": "Descrição, transcrição automática integral e 14 comentários.", "limitations": ["uma única pequena evidência de execução", "canal grande e comercial"]},
        {"referenceId": "obs-20260911-134", "role": "case_limit", "comparisonLevel": 2, "requiredEvidenceObserved": False, "confidence": "high", "observation": "CTA pede autoavaliação e preferência, sem produção que use a unidade ensinada.", "evidence": "Descrição, transcrição integral e dois comentários.", "limitations": ["não conta como apoio nem contraexemplo"]},
    ],
    "limitations": [
        "O padrão descreve alinhamento estrutural entre conteúdo e CTA, não aprendizagem.",
        "Somente uma referência tem pequena evidência pública de prática e feedback; isso não mede qualidade em escala.",
        "Nenhum apoio possui retenção, experimento, baseline ou conversão.",
        "O precursor antigo permanece contexto porque sua cobertura era secundária e os comentários reais não foram observados.",
        "O caso-limite mostra que comentar nível ou preferência não equivale a aplicar o conteúdo.",
    ],
    "validation": "requires_human_or_experimental_evidence", "taxonomyVersion": "3.0",
})

memory["trainingRuns"].append({
    "id": "run-20260911-supervised-023", "executedAt": NOW, "batchPolicyVersion": "1.1", "requestedBatchSize": 5, "candidatesFound": 23,
    "referenceIds": ["obs-20260911-131", "obs-20260911-132", "obs-20260911-133", "obs-20260911-134", "obs-20260911-135"],
    "targetKnowledgeId": "hyp-20260830-033", "targetReferenceIds": ["obs-20260911-131", "obs-20260911-132", "obs-20260911-133"],
    "falsificationOrBoundaryReferenceIds": ["obs-20260911-134"], "controlledExplorationReferenceIds": ["obs-20260911-135"],
    "discarded": [
        {"url": "https://www.youtube.com/watch?v=QOWqeahtD4o", "reason": "comparável, mas substituído por apoio com transcrição integral"},
        {"url": "https://www.youtube.com/watch?v=CRjg02yGs6g", "reason": "CTA pede opinião sobre dificuldade e formato, não produção aplicada delimitada"},
        {"url": "https://www.youtube.com/watch?v=KTCfoZVyx2c", "reason": "perguntas de prática aparecem, mas o CTA de comentário não ficou observável"},
        {"url": "https://www.youtube.com/watch?v=patl9o3HHlA", "reason": "comentário é canal para dúvidas, não exercício produtivo obrigatório"},
        {"url": "https://www.youtube.com/watch?v=_K8OFhhOWxc", "reason": "mesma fonte do caso-limite selecionado e CTA de autoavaliação"},
        {"url": "https://www.youtube.com/watch?v=SLru-WD2LLs", "reason": "descrição pede frase, mas a fala pede preferência; reservado como teste de consistência entre modalidades"},
        {"url": "https://www.youtube.com/watch?v=0xx4l6xVbiM", "reason": "conteúdo em inglês e comparação com público brasileiro inferior"},
        {"url": "https://www.youtube.com/watch?v=CPf7CvV-uKk", "reason": "português para estrangeiros e cobertura insuficiente após timeout"}
    ],
    "analyzed": 5, "brazilianReferences": 4, "internationalReferences": 0, "unknownOriginReferences": 1,
    "smallOrMediumCreatorReferences": 4, "coverageSummary": {"complete": 0, "partial": 5, "insufficient": 0},
    "audiovisualAcquisition": {"attempted": True, "succeeded": 0, "failure": "endpoints públicos foram consultados; tentativas diretas nos Shorts retornaram formato indisponível e uma legenda da exploração recebeu 429", "effect": "imagem em movimento, áudio ouvido, texto na tela, edição e ritmo ficaram não mensurados"},
    "transcriptCoverage": {"fullAutomatic": 4, "partialAutomatic": 0, "none": 1, "limitation": "transcrições automáticas substituem somente fala e podem errar palavras em inglês"},
    "commentsCoverage": {"fullOrDeclaredZero": 3, "partialSample": 0, "unavailable": 2},
    "baselineCoverage": {"sampledProfiles": 0, "contemporaneousBaselines": 0, "limitation": "métricas absolutas observadas sem baseline funcional"},
    "patternsCreated": ["pat-20260911-011"], "patternsStrengthened": [], "patternsRefined": [],
    "hypothesesCreated": [], "hypothesesStrengthened": ["hyp-20260830-033"], "validatedPatternsCreated": 0, "contradictionsFound": [],
    "caseLimitsFound": ["CTA temático de autoavaliação ou preferência não conta como exercício aplicado"],
    "safetyFindings": ["comentários públicos foram resumidos sem reproduzir usernames", "promessa de feedback foi registrada como não verificada quando comentários não estavam acessíveis"],
    "evidenceGateSummary": {"targetSupportsEligible": 3, "targetSupportsRejected": 0, "boundaryCases": 1, "explorationReferences": 1, "duplicateUrls": 0, "independentCreatorsAddedToPattern": 3, "newHypotheses": 0},
    "outcome": "A hipótese foi restringida ao que a evidência mostra: continuidade estrutural entre aula e tarefa aplicada no comentário. Três apoios independentes sustentam padrão provisório; aprendizagem, qualidade das respostas e comunidade não foram inferidas.",
    "nextTarget": "conteúdo educacional brasileiro curto com audiovisual integral, tarefa aplicada, amostra de respostas e rubrica de feedback; buscar caso funcionalmente semelhante em que respostas revelem erro persistente ou feedback ausente",
    "limitations": ["Nenhum audiovisual ou áudio foi reproduzido.", "Uma referência não teve transcrição.", "Sem retenção, baseline, aprendizagem ou conversão.", "Comentários não são representativos.", "Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references": len(memory["references"]), "patterns": len(memory["patterns"]), "hypotheses": len(memory["hypotheses"]), "runs": len(memory["trainingRuns"])}, ensure_ascii=False))
