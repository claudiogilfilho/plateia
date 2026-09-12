#!/usr/bin/env python3
import json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "knowledge/observatory/plateia-memory.json"
memory = json.loads(DB.read_text(encoding="utf-8"))

NOW = "2026-09-12T12:27:39.000Z"
OBSERVED = "2026-09-12"
BATCH_IDS = {f"obs-20260912-{n}" for n in range(141, 146)}
RUN_ID = "run-20260912-supervised-025"
PATTERN_ID = "pat-20260912-012"
TARGET_ID = "hyp-20260824-007"

memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]
memory["patterns"] = [p for p in memory["patterns"] if p.get("id") != PATTERN_ID]

hypothesis = next(h for h in memory["hypotheses"] if h["id"] == TARGET_ID)
hypothesis["supportReferenceIds"] = [x for x in hypothesis.get("supportReferenceIds", []) if x not in BATCH_IDS]
hypothesis["status"] = "observed_not_promoted"
hypothesis.pop("promotedPatternId", None)
hypothesis.pop("promotedAt", None)
hypothesis["reasonNotPromoted"] = "Dois apoios anteriores eram do mesmo criador e não tinham o payoff reproduzido."

MISSING_AV = [
    "vídeo integral auditado quadro a quadro",
    "imagem em movimento efetivamente observada",
    "áudio ouvido",
    "texto na tela",
    "edição",
    "ritmo",
    "curva de retenção",
    "impressões e fontes de tráfego",
]

def classification(*, container, material, presentations, primary, secondary, mix,
                   objectives, advertising, intent, entity, topic, segment, subsegment,
                   audience, awareness, production, scale, replicability, duration,
                   mechanisms, hooks, narrative, proof, cta, confidence, evidence,
                   alternatives=None, missing=None):
    return {
        "taxonomyVersion": "3.0",
        "container": container,
        "materialFormat": material,
        "presentationFormats": presentations,
        "primaryFamily": primary,
        "secondaryFamilies": secondary,
        "functionalMix": mix,
        "objectives": objectives,
        "advertisingType": advertising,
        "commercialIntent": intent,
        "advertisedEntity": entity,
        "contentTopic": {"label": topic, "iabCode": None},
        "segment": segment,
        "subsegment": subsegment,
        "probableAudience": audience,
        "awarenessStage": awareness,
        "productionLevel": production,
        "creatorScale": scale,
        "replicability": replicability,
        "durationBand": duration,
        "pace": "unknown",
        "mechanisms": mechanisms,
        "hookTypes": hooks,
        "narrativeElements": narrative,
        "proofTypes": proof,
        "ctaTypes": cta,
        "distributionContext": {"organicPaid": "unknown", "trendDependency": "low"},
        "confidence": confidence,
        "evidence": evidence,
        "alternativeClassifications": alternatives or [],
        "missingInformation": missing or MISSING_AV,
        "needsHumanReview": True,
    }

def make_ref(*, id, title, creator, identity, url, published, duration, accessible,
             missing, metrics, cls, comparison, observations, interpretations,
             scores, lenses, replicable, limitations, role, evidence_level,
             eligible, claims, source_type, source_evidence=None):
    return {
        "id": id,
        "title": title,
        "creator": creator,
        "creatorIdentity": identity,
        "sourceIdentity": identity,
        "country": "BR",
        "url": url,
        "sourceEvidence": source_evidence or [url],
        "publishedAt": published,
        "duration": duration,
        "createdAt": NOW,
        "coverage": {"level": "partial", "accessible": accessible, "missing": missing},
        "publicMetrics": {**metrics, "observedAt": OBSERVED, "sourceType": source_type, "causality": "not_inferred"},
        "classification": cls,
        "comparison": comparison,
        "observations": observations,
        "interpretations": interpretations,
        "scores": scores,
        "fiveLenses": lenses,
        "hypotheses": [],
        "replicable": replicable,
        "limitations": limitations,
        "provenance": [
            "public_content", "youtube_public_metadata", "public_search",
            "youtube_automatic_transcript", "youtube_public_comments",
            "public_metric", "observatory_inference",
        ],
        "training": {
            "evidencePolicyVersion": "1.1",
            "evidenceRole": role,
            "evidenceLevel": evidence_level,
            "requiredEvidenceObserved": eligible,
            "supportEligible": eligible,
            "claimCoverage": claims,
            "provenanceAndConsent": {
                "storyOrigin": "not_applicable",
                "consentStatus": "not_applicable",
                "identityProtection": "not_applicable",
                "evidence": ["esquete ficcional ou conteúdo instrucional; nenhum relato de terceiro foi ensinado"],
            },
            "replicable": replicable,
            "contingent": limitations,
            "notRecommended": [
                "copiar frases, personagens ou roteiro",
                "confundir uma reversão isolada com escalada narrativa",
                "inferir vídeo, áudio, texto na tela, edição, ritmo ou retenção",
                "atribuir alcance ao mecanismo sem experimento ou baseline funcional",
            ],
            "hypotheses": [],
        },
        "viralAssessment": {
            "status": "indeterminate",
            "observedSignal": metrics.get("viewsObserved", "not_assessed"),
            "missingForRelativeAssessment": [
                "coorte funcional contemporânea homogênea", "retenção", "impressões",
                "fontes de tráfego", "mídia paga",
            ],
            "confounders": ["tamanho do canal", "idade do vídeo", "tema", "distribuição"],
            "causalClaimAllowed": False,
        },
    }

refs = [
    make_ref(
        id="obs-20260912-141", title="Atendimento Sincero", creator="Comédia S.A",
        identity="comedia-sa", url="https://www.youtube.com/watch?v=a5bKQ6WW4MA",
        published="2025-07-16", duration="PT14S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral com timestamps até 00:14.880",
            "fala por substituição textual", "352 visualizações", "2 curtidas",
            "zero comentários declarado",
        ],
        missing=MISSING_AV,
        metrics={"viewsObserved":"352", "likesObserved":"2", "commentsObserved":"zero declarado"},
        cls=classification(
            container="youtube_video", material="video_curto", presentations=["esquete", "dialogo"],
            primary="humor", secondary=["identificacao", "storytelling"],
            mix=[{"family":"humor","percentage":60},{"family":"identificacao","percentage":25},{"family":"storytelling","percentage":15}],
            objectives=["visualizacao","compartilhamento","identificacao"], advertising="editorial_organico",
            intent="ausente", entity={"kind":"nenhuma","name":"","confidence":"high"},
            topic="atendimento de crédito e nome negativado", segment="entretenimento e comédia",
            subsegment="humor de atendimento", audience="adultos brasileiros familiarizados com crediário",
            awareness="consciente_problema", production="simple", scale="unknown", replicability="high",
            duration="up_to_15s", mechanisms=["identificacao","surpresa","humor"],
            hooks=["problema","verbal"], narrative=["situacao","problema","escalada","payoff"],
            proof=[], cta=[], confidence="high",
            evidence=[
                "A transcrição abre com pedido cotidiano de crediário e introduz a restrição de nome sujo.",
                "A resposta abandona o serviço esperado e escala para café e desejo de boa sorte.",
            ],
        ),
        comparison={"level":1,"group":"esquete curta de tensão cotidiana com consequência absurda","referenceIds":["obs-20260912-142","obs-20260912-143"],"confidence":"high"},
        observations=[
            "O conflito cotidiano é formulado em duas perguntas antes da resposta desviada.",
            "A consequência absurda permanece semanticamente ligada à impossibilidade de crédito.",
        ],
        interpretations=[
            "A fala torna situação, obstáculo e desvio identificáveis em poucos enunciados.",
            "Não há evidência para atribuir riso, retenção ou desempenho à estrutura.",
        ],
        scores={"gancho":88,"clareza":91,"relevancia":86,"desejo":"not_assessed","confianca":80,"retencao":"not_assessed","acao":"not_assessed","objecoes":78},
        lenses={
            "apressado":"Entende crediário, obstáculo e desvio pela fala transcrita.",
            "analitico":"A lógica interna fecha, mas a encenação não foi vista.",
            "aspiracional":"Não há transformação aspiracional mensurável.",
            "comunidade":"O problema financeiro pode gerar identificação, sem comentários observados.",
            "cetico":"Não pode atribuir eficácia ao texto sem teste de audiência.",
        },
        replicable=["Partir de uma regra de atendimento reconhecível.","Escalar para uma resposta impossível, mas ligada ao obstáculo.","Fechar o desvio sem exigir contexto externo."],
        limitations=["Sem audiovisual, áudio ouvido, edição, ritmo ou retenção.","Zero comentários não mede recepção sem impressões.","A transcrição automática não revela atuação."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"há tensão cotidiana identificável","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a tensão escala para consequência absurda ligada ao problema","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_and_declared_zero_comments_after_public_search",
    ),
    make_ref(
        id="obs-20260912-142", title="BOM DIA PRA QUEM? | EMBRULHA PRA VIAGEM",
        creator="Embrulha Pra Viagem", identity="embrulha-pra-viagem",
        url="https://www.youtube.com/watch?v=JrFV9bq3ht8", published="2017-01-31", duration="PT4M39S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral com timestamps até 00:04:40.560",
            "fala por substituição textual", "1.299.580 visualizações", "59.708 curtidas",
            "cerca de 1.700 comentários declarados", "amostra pública de 50 comentários",
        ],
        missing=MISSING_AV,
        metrics={"viewsObserved":"1.299.580","likesObserved":"59.708","commentsObserved":"cerca de 1.700; 50 extraídos como amostra"},
        cls=classification(
            container="youtube_video", material="video_curto", presentations=["esquete","dialogo","dramatizacao"],
            primary="humor", secondary=["storytelling","identificacao"],
            mix=[{"family":"humor","percentage":55},{"family":"storytelling","percentage":30},{"family":"identificacao","percentage":15}],
            objectives=["visualizacao","compartilhamento","identificacao"], advertising="editorial_organico",
            intent="ausente", entity={"kind":"nenhuma","name":"","confidence":"high"},
            topic="cumprimento, pressa e burocracia em portaria", segment="entretenimento e comédia",
            subsegment="humor de convivência", audience="adultos brasileiros familiarizados com condomínios",
            awareness="consciente_problema", production="intermediate", scale="large", replicability="medium",
            duration="over_60s", mechanisms=["identificacao","tensao","surpresa","humor"],
            hooks=["conflito","verbal"], narrative=["situacao","problema","escalada","progressao","payoff"],
            proof=[], cta=["seguir"], confidence="high",
            evidence=[
                "A transcrição começa com a moradora apressada que não cumprimenta o porteiro.",
                "A negativa de abrir o portão escala para exigência de documento, polícia, superior e advogado, preservando o motivo do cumprimento.",
            ],
        ),
        comparison={"level":2,"group":"esquete de tensão cotidiana com escalada absurda verbal","referenceIds":["obs-20260912-141","obs-20260912-143"],"confidence":"high"},
        observations=[
            "Um descuido social simples vira impedimento de acesso e sucessivas autoridades na transcrição.",
            "A repetição de cumprimentos mantém a variável inicial ativa durante a escalada.",
            "Comentários amostrados discutem a regra de educação e citam falas, mas não medem recepção representativa.",
        ],
        interpretations=[
            "A escalada ganha coerência porque cada complicação deriva do conflito inicial.",
            "Popularidade e comentários não demonstram que a estrutura causou desempenho.",
        ],
        scores={"gancho":84,"clareza":88,"relevancia":85,"desejo":"not_assessed","confianca":82,"retencao":"not_assessed","acao":55,"objecoes":76},
        lenses={
            "apressado":"Reconhece pressa e conflito social cedo pela fala.",
            "analitico":"A cadeia causal verbal é clara; a montagem permanece não avaliada.",
            "aspiracional":"Não há transformação aspiracional central.",
            "comunidade":"Comentários discutem educação e repetem a premissa.",
            "cetico":"A amostra de comentários e o alcance antigo não isolam o mecanismo.",
        },
        replicable=["Manter a causa inicial ativa em cada nova complicação.","Escalar por agentes sucessivos que repetem a mesma regra.","Fazer o absurdo aumentar sem trocar de conflito."],
        limitations=["Sem audiovisual, áudio ouvido, edição, ritmo ou retenção.","Comentários são amostra não representativa.","Produção e elenco reduzem replicabilidade material."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"há tensão cotidiana identificável","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a tensão escala por complicações absurdas encadeadas","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_and_public_comment_sample_after_public_search",
    ),
    make_ref(
        id="obs-20260912-143", title="QUE REMÉDIO?", creator="Vetor Humor",
        identity="vetor-humor", url="https://www.youtube.com/watch?v=n9iTaU498d4",
        published="2013-03-08", duration="PT2M48S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral com timestamps até 00:02:48.560",
            "fala por substituição textual", "11.905.382 visualizações", "367.151 curtidas",
            "cerca de 9.600 comentários declarados", "amostra pública de 50 comentários",
        ],
        missing=MISSING_AV,
        metrics={"viewsObserved":"11.905.382","likesObserved":"367.151","commentsObserved":"cerca de 9.600; 50 extraídos como amostra"},
        cls=classification(
            container="youtube_video", material="video_curto", presentations=["esquete","dialogo","dramatizacao"],
            primary="humor", secondary=["storytelling","curiosidade"],
            mix=[{"family":"humor","percentage":60},{"family":"storytelling","percentage":25},{"family":"curiosidade","percentage":15}],
            objectives=["visualizacao","compartilhamento","retencao"], advertising="editorial_organico",
            intent="ausente", entity={"kind":"nenhuma","name":"","confidence":"high"},
            topic="esquecimento em atendimento de farmácia", segment="entretenimento e comédia",
            subsegment="humor de atendimento", audience="adultos brasileiros consumidores de esquetes",
            awareness="inconsciente", production="intermediate", scale="large", replicability="medium",
            duration="over_60s", mechanisms=["curiosidade","surpresa","humor"],
            hooks=["problema","verbal"], narrative=["situacao","problema","escalada","loop","payoff"],
            proof=[], cta=["seguir"], confidence="high",
            evidence=[
                "A transcrição começa com um cliente que não lembra o nome do remédio.",
                "O esquecimento se repete em preço, pagamento e finalidade até o personagem perguntar quem é o atendente.",
            ],
        ),
        comparison={"level":2,"group":"esquete de atendimento cotidiano com escalada absurda verbal","referenceIds":["obs-20260912-141","obs-20260912-142"],"confidence":"high"},
        observations=[
            "A mesma lacuna de memória é reaplicada a etapas sucessivas da compra.",
            "O encerramento amplia a falha inicial para o reconhecimento do interlocutor.",
            "Comentários amostrados citam o diálogo e longevidade do vídeo, sem explicar causalidade.",
        ],
        interpretations=[
            "Repetição com aumento de consequência produz progressão verbal observável.",
            "O alcance acumulado em treze anos não é comparável a lançamentos recentes.",
        ],
        scores={"gancho":82,"clareza":86,"relevancia":80,"desejo":"not_assessed","confianca":79,"retencao":"not_assessed","acao":58,"objecoes":72},
        lenses={
            "apressado":"Entende rapidamente o problema de memória pela fala.",
            "analitico":"A regra da repetição é consistente, mas a encenação não foi auditada.",
            "aspiracional":"Não há desejo aspiracional mensurável.",
            "comunidade":"Comentários citam falas, sem amostra representativa.",
            "cetico":"Métricas antigas e escala não autorizam inferência causal.",
        },
        replicable=["Escolher uma única falha cotidiana como regra da cena.","Reaplicar a regra a etapas sucessivas.","Aumentar a consequência no fechamento sem abandonar a premissa."],
        limitations=["Sem audiovisual, áudio ouvido, edição, ritmo ou retenção.","Transcrição automática contém ruído lexical.","Métricas acumuladas por treze anos não formam baseline contemporâneo."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"há tensão cotidiana identificável","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a tensão escala por repetição e aumento de consequência","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_and_public_comment_sample_after_public_search",
    ),
    make_ref(
        id="obs-20260912-144", title="Perda Certa", creator="Comédia S.A",
        identity="comedia-sa", url="https://www.youtube.com/watch?v=7lFoo4FUtmM",
        published="2025-07-26", duration="PT14S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral com timestamps até 00:00:15.400",
            "fala por substituição textual", "9 visualizações", "zero comentários declarado",
        ],
        missing=MISSING_AV,
        metrics={"viewsObserved":"9","likesObserved":"not_assessed","commentsObserved":"zero declarado"},
        cls=classification(
            container="youtube_video", material="video_curto", presentations=["esquete","dialogo"],
            primary="humor", secondary=["curiosidade","identificacao"],
            mix=[{"family":"humor","percentage":60},{"family":"curiosidade","percentage":25},{"family":"identificacao","percentage":15}],
            objectives=["visualizacao","compartilhamento"], advertising="editorial_organico",
            intent="ausente", entity={"kind":"nenhuma","name":"","confidence":"high"},
            topic="aposta de alto risco e cassino", segment="entretenimento e comédia",
            subsegment="humor financeiro", audience="adultos brasileiros familiarizados com apostas",
            awareness="consciente_problema", production="simple", scale="unknown", replicability="high",
            duration="up_to_15s", mechanisms=["curiosidade","surpresa","humor"],
            hooks=["pergunta","verbal"], narrative=["situacao","virada","payoff"],
            proof=[], cta=[], confidence="high",
            evidence=[
                "A transcrição contrasta investimento de alto risco com uma aposta pequena no cassino.",
                "Há uma revelação única; não aparece cadeia de consequências crescentes.",
            ],
        ),
        comparison={"level":1,"group":"caso-limite de esquete curta com tensão cotidiana e reversão única","referenceIds":["obs-20260912-141"],"confidence":"high"},
        observations=["A fala apresenta expectativa financeira e a inverte numa única resposta.","Não há escalada progressiva observável na transcrição."],
        interpretations=["Surpresa isolada é mecanismo diferente de escalada.","Nove visualizações sem impressões ou baseline não configuram contraexemplo de desempenho."],
        scores={"gancho":81,"clareza":89,"relevancia":78,"desejo":"not_assessed","confianca":77,"retencao":"not_assessed","acao":"not_assessed","objecoes":74},
        lenses={
            "apressado":"Entende expectativa e reversão em duas falas.",
            "analitico":"O desvio é claro, mas não testa progressão.",
            "aspiracional":"Não há transformação aspiracional observável.",
            "comunidade":"Tema pode ser reconhecível, sem comentários públicos.",
            "cetico":"Baixo alcance isolado não mede eficácia da estrutura.",
        },
        replicable=["Distinguir reversão de expectativa de escalada narrativa.","Usar contraste curto quando uma única revelação basta."],
        limitations=["Não conta como apoio nem contraexemplo.","Sem audiovisual, áudio ouvido, edição, ritmo ou retenção.","Sem baseline ou impressões."],
        role="falsification_or_boundary", evidence_level=1, eligible=False,
        claims=[
            {"claim":"há tensão cotidiana identificável","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"há escalada de consequências","requiredModalities":["transcript","escalation_chain"],"observedModalities":["transcript"],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_and_declared_zero_comments_after_public_search",
    ),
    make_ref(
        id="obs-20260912-145", title="How often: a expressão que todo aluno de inglês precisa saber",
        creator="Fluency Academy", identity="fluency-academy",
        url="https://www.youtube.com/watch?v=v7wpvS24Ek0", published="2020-12-28", duration="PT2M16S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "8.520 visualizações", "42 comentários declarados",
            "descrição indexada com pedido de frase e promessa de correção",
            "artigo oficial com regra, exemplos e respostas de frequência",
        ],
        missing=MISSING_AV + ["transcrição ou legenda adquirida", "fala integral por substituição textual", "conteúdo dos comentários", "feedback corretivo prometido"],
        metrics={"viewsObserved":"8.520","likesObserved":"not_assessed","commentsObserved":"42 declarados; conteúdo indisponível"},
        cls=classification(
            container="youtube_video", material="video_curto", presentations=["tutorial","camera_direta"],
            primary="educativo", secondary=["explicativo","comunidade"],
            mix=[{"family":"educativo","percentage":60},{"family":"explicativo","percentage":25},{"family":"comunidade","percentage":15}],
            objectives=["educar","comentario","lead"], advertising="geracao_de_leads",
            intent="explicita", entity={"kind":"servico","name":"Fluency Academy","confidence":"high"},
            topic="perguntas e respostas com how often", segment="educação e idiomas",
            subsegment="gramática e frequência em inglês", audience="brasileiros aprendendo inglês",
            awareness="consciente_solucao", production="simple", scale="large", replicability="high",
            duration="over_60s", mechanisms=["curiosidade","recompensa","pertencimento"],
            hooks=["textual","promessa"], narrative=["problema","mecanismo","progressao","cta"],
            proof=["mecanismo_explicado"], cta=["comentar","seguir","clicar"], confidence="medium",
            evidence=[
                "A página e o artigo oficiais identificam a regra e exemplos de how often.",
                "O trecho indexado da descrição pede uma frase no futuro e promete conferir, mas os comentários não foram adquiridos.",
            ],
            alternatives=["explicativo como família principal"],
            missing=MISSING_AV + ["transcrição ou legenda adquirida", "conteúdo dos comentários", "feedback corretivo"],
        ),
        comparison={"level":4,"group":"exploração educacional de tarefa com promessa de correção não auditada","referenceIds":["obs-20260911-133"],"confidence":"low"},
        observations=[
            "A fonte oficial ensina a estrutura de pergunta e respostas de frequência.",
            "A descrição indexada pede uma frase e promete conferência, mas não foi possível observar resposta ou correção.",
        ],
        interpretations=["Prometer correção é diferente de feedback corretivo observável.","A referência não acrescenta apoio ao padrão de humor nem prova aprendizagem."],
        scores={"gancho":77,"clareza":88,"relevancia":84,"desejo":72,"confianca":81,"retencao":"not_assessed","acao":80,"objecoes":74},
        lenses={
            "apressado":"O título delimita a expressão e o benefício.",
            "analitico":"A regra está no artigo oficial; falta correspondência integral com o vídeo.",
            "aspiracional":"Pode imaginar uso mais fluente de perguntas de frequência.",
            "comunidade":"Existe promessa de correção, sem feedback público observado.",
            "cetico":"Não aceita promessa de correção como correção realizada.",
        },
        replicable=["Pedir uma frase que aplique a unidade ensinada.","Se prometer correção, tornar o feedback observável e específico.","Separar CTA pedagógico de oferta comercial."],
        limitations=["Sem transcrição adquirida ou audiovisual.","Comentários e feedback corretivo indisponíveis.","Artigo oficial sustenta o conteúdo conceitual, não a execução audiovisual."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a regra e exemplos estão disponíveis","requiredModalities":["official_text"],"observedModalities":["official_text"],"sufficient":True},
            {"claim":"a descrição pede produção e promete correção","requiredModalities":["indexed_description"],"observedModalities":["indexed_description"],"sufficient":True},
            {"claim":"o feedback corretivo aconteceu","requiredModalities":["comments"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_indexed_description_and_official_companion_article_after_public_search",
        source_evidence=[
            "https://www.youtube.com/watch?v=v7wpvS24Ek0",
            "https://fluency.io/br/blog/how-often/",
        ],
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
for item in refs:
    if item["url"] in existing_urls:
        raise SystemExit(f"URL duplicada: {item['url']}")
    existing_urls.add(item["url"])
memory["references"].extend(refs)

new_supports = ["obs-20260912-141", "obs-20260912-142", "obs-20260912-143"]
hypothesis["supportReferenceIds"].extend(new_supports)
hypothesis["status"] = "promoted_to_provisional"
hypothesis["promotedPatternId"] = PATTERN_ID
hypothesis["promotedAt"] = NOW
hypothesis.pop("reasonNotPromoted", None)

memory["patterns"].append({
    "id": PATTERN_ID,
    "status": "provisional",
    "stage": "provisional",
    "name": "Tensão cotidiana escalada por consequência absurda",
    "statement": "Em esquetes de humor, partir de uma tensão cotidiana identificável e escalar consequências que continuam ligadas à mesma regra torna premissa, desvio e progressão reconhecíveis na fala; efeitos sobre riso, retenção, compartilhamento ou desempenho permanecem não medidos.",
    "creativeFamily": "humor",
    "objective": "compreensão da premissa e progressão cômica",
    "segment": "esquetes brasileiras de situação cotidiana",
    "mechanism": ["identificacao", "surpresa", "humor"],
    "conditions": [
        "tensão cotidiana identificável",
        "consequência absurda semanticamente ligada à tensão inicial",
        "ao menos um aumento de consequência ou reaplicação da regra",
        "progressão observável em fala ou audiovisual",
    ],
    "supportReferenceIds": new_supports,
    "precursorReferenceIds": ["obs-20260824-026", "obs-20260824-027"],
    "comparableSupportCount": 3,
    "supportingCount": 3,
    "counterexampleCount": 0,
    "caseLimitCount": 1,
    "counterexampleReferenceIds": [],
    "caseLimitReferenceIds": ["obs-20260912-144"],
    "comparisonLevel": 2,
    "confidence": "medium",
    "creatorDiversityCount": 3,
    "sourceDiversityCount": 3,
    "patternType": "retencao",
    "evidence": [
        {"referenceId":"obs-20260912-141","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pedido cotidiano de crédito encontra obstáculo e escala para uma resposta de atendimento impossível, ligada ao problema.","evidence":"Descrição, metadados e transcrição automática integral.","limitations":["sem audiovisual ou retenção"]},
        {"referenceId":"obs-20260912-142","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Falta de cumprimento escala de portaria para documento, polícia e advogado, mantendo a mesma regra verbal.","evidence":"Descrição, transcrição automática integral e amostra de 50 comentários.","limitations":["produção intermediária","comentários não representativos","sem audiovisual ou retenção"]},
        {"referenceId":"obs-20260912-143","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Esquecimento em farmácia é reaplicado a preço, pagamento, finalidade e reconhecimento do atendente.","evidence":"Transcrição automática integral e amostra de 50 comentários.","limitations":["transcrição ruidosa","vídeo antigo","sem audiovisual ou retenção"]},
        {"referenceId":"obs-20260912-144","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"Uma expectativa financeira recebe uma única reversão, sem aumento de consequências.","evidence":"Descrição, metadados e transcrição automática integral.","limitations":["não conta como apoio nem contraexemplo"]},
    ],
    "limitations": [
        "Os três apoios independentes demonstram recorrência estrutural na fala, não eficácia.",
        "Nenhum audiovisual, ritmo, montagem ou retenção foi auditado.",
        "Os apoios variam de 14 segundos a 4 minutos e 39 segundos; a comparação é de nível 1 ou 2, não benchmark numérico.",
        "Dois precursores antigos permanecem contexto porque eram do mesmo criador e sem payoff reproduzido.",
        "O caso-limite separa reversão única de escalada narrativa.",
        "Validação exige revisão humana ou evidência experimental apropriada.",
    ],
    "validation": "requires_human_or_experimental_evidence",
    "taxonomyVersion": "3.0",
})

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 16,
    "referenceIds": ["obs-20260912-141","obs-20260912-142","obs-20260912-143","obs-20260912-144","obs-20260912-145"],
    "targetKnowledgeId": TARGET_ID,
    "targetReferenceIds": ["obs-20260912-141","obs-20260912-142","obs-20260912-143"],
    "falsificationOrBoundaryReferenceIds": ["obs-20260912-144"],
    "controlledExplorationReferenceIds": ["obs-20260912-145"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=VNWNwYRk_Bo","reason":"transcrição integral disponível, mas compilação de oito minutos com múltiplas situações reduz comparabilidade com uma premissa escalada"},
        {"url":"https://www.youtube.com/watch?v=blDNJbf_rwo","reason":"esquete longa com integração comercial e múltiplos núcleos; comparabilidade e replicabilidade inferiores"},
        {"url":"https://www.youtube.com/watch?v=TozVopOCaZg","reason":"vídeo longo com muitas situações familiares; alvo não fica concentrado em uma regra"},
        {"url":"https://www.youtube.com/watch?v=9bWjJVBJCYo","reason":"mesmo criador de apoio selecionado e cobertura redundante"},
        {"url":"https://www.youtube.com/watch?v=ZXFf1YjIrM8","reason":"mesmo criador e reversão única, sem ganho além do caso-limite escolhido"},
        {"url":"https://www.youtube.com/watch?v=ASsUkhSN2sY","reason":"montagem de quatro falas de bar; sem progressão causal única na transcrição"},
        {"url":"https://www.youtube.com/watch?v=j-y59n8nfU4","reason":"mesmo criador e punchline única, redundante com o caso-limite"},
        {"url":"https://www.youtube.com/watch?v=DeRqO5TwGRA","reason":"sem transcrição adquirida e produção complexa recente"},
        {"url":"https://www.youtube.com/watch?v=8QVCOrh8KMA","reason":"sem transcrição adquirida e duração maior; descrição não substitui progressão observável"},
        {"url":"https://www.youtube.com/watch?v=jEFRii6aJT4","reason":"transcrição ruidosa e payoff insuficientemente reconstruível"},
        {"url":"https://www.youtube.com/watch?v=hNjhCtft6Ug","reason":"lista de situações do SUS, não uma única tensão escalada; evitado também como ensino sobre serviço de saúde"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 2,
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads diretos retornaram timeout e ausência de formato disponível; aquisição de capas também falhou","effect":"imagem em movimento, áudio ouvido, texto na tela, edição e ritmo ficaram não mensurados"},
    "transcriptCoverage": {"fullAutomatic":4,"partialAutomatic":0,"none":1,"limitation":"transcrições automáticas substituem apenas fala e podem conter erros; a exploração usa texto oficial e descrição indexada"},
    "commentsCoverage": {"fullOrDeclaredZero":2,"partialSample":2,"unavailable":1},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"idades, escalas e durações heterogêneas impedem benchmark de desempenho"},
    "patternsCreated": [PATTERN_ID],
    "patternsStrengthened": [],
    "patternsRefined": [],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [TARGET_ID],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["reversão única não equivale a escalada de consequências"],
    "safetyFindings": ["comentários públicos foram resumidos sem usernames","conteúdo de saúde foi descartado para não ensinar caricatura como informação médica"],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três esquetes de criadores independentes sustentam recorrência estrutural de tensão cotidiana com consequências escaladas na fala. O padrão é provisório; riso, retenção e desempenho não foram medidos.",
    "nextTarget": "esquete brasileira curta com audiovisual integral e uma coorte funcional contemporânea, incluindo caso em que a escalada abandone a premissa ou prejudique a clareza",
    "limitations": ["Nenhum audiovisual ou áudio foi reproduzido.","Uma referência não teve transcrição adquirida.","Sem retenção, teste de compreensão ou baseline homogêneo.","Comentários são ausentes ou amostrais.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "references": len(memory["references"]),
    "patterns": len(memory["patterns"]),
    "hypotheses": len(memory["hypotheses"]),
    "runs": len(memory["trainingRuns"]),
    "newPattern": PATTERN_ID,
}, ensure_ascii=False))
