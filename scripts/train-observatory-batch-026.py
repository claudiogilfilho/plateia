#!/usr/bin/env python3
import json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "knowledge/observatory/plateia-memory.json"
memory = json.loads(DB.read_text(encoding="utf-8"))

NOW = "2026-09-13T11:11:30.000Z"
OBSERVED = "2026-09-13"
RUN_ID = "run-20260913-supervised-026"
PATTERN_ID = "pat-20260913-013"
TARGET_ID = "hyp-20260824-012"
BATCH_IDS = {f"obs-20260913-{n}" for n in range(146, 151)}

memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]
memory["patterns"] = [p for p in memory["patterns"] if p.get("id") != PATTERN_ID]

hypothesis = next(h for h in memory["hypotheses"] if h["id"] == TARGET_ID)
hypothesis["supportReferenceIds"] = [x for x in hypothesis.get("supportReferenceIds", []) if x not in BATCH_IDS]
hypothesis["status"] = "observed_not_promoted"
hypothesis.pop("promotedPatternId", None)
hypothesis.pop("promotedAt", None)
hypothesis["reasonNotPromoted"] = "Os dois apoios anteriores eram da mesma série e do mesmo criador."

MISSING_AV = [
    "vídeo reproduzido ou auditado quadro a quadro",
    "imagem em movimento efetivamente observada",
    "capa ou outra imagem adquirida",
    "áudio ouvido",
    "texto na tela",
    "edição",
    "ritmo",
    "curva de retenção",
    "impressões e fontes de tráfego",
]


def classification(*, material, presentations, primary, secondary, mix, objectives,
                   advertising, intent, entity, topic, segment, subsegment, audience,
                   awareness, production, scale, replicability, duration, mechanisms,
                   hooks, narrative, proof, cta, confidence, evidence,
                   alternatives=None, missing=None, trend="low"):
    return {
        "taxonomyVersion": "3.0",
        "container": "youtube_video",
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
        "distributionContext": {"organicPaid": "unknown", "trendDependency": trend},
        "confidence": confidence,
        "evidence": evidence,
        "alternativeClassifications": alternatives or [],
        "missingInformation": missing or MISSING_AV,
        "needsHumanReview": True,
    }


def make_ref(*, id, title, creator, identity, url, published, duration, accessible,
             missing, metrics, cls, comparison, observations, interpretations,
             scores, lenses, replicable, contingent, role, evidence_level,
             eligible, claims, source_type, comment_provenance=True):
    provenance = [
        "public_content", "youtube_public_metadata", "public_search",
        "youtube_automatic_transcript", "public_metric", "observatory_inference",
    ]
    if comment_provenance:
        provenance.append("youtube_public_comments")
    return {
        "id": id,
        "title": title,
        "creator": creator,
        "creatorIdentity": identity,
        "sourceIdentity": identity,
        "country": "BR",
        "url": url,
        "sourceEvidence": [url],
        "publishedAt": published,
        "duration": duration,
        "createdAt": NOW,
        "coverage": {"level": "partial", "accessible": accessible, "missing": missing},
        "publicMetrics": {
            **metrics,
            "observedAt": OBSERVED,
            "sourceType": source_type,
            "causality": "not_inferred",
        },
        "classification": cls,
        "comparison": comparison,
        "observations": observations,
        "interpretations": interpretations,
        "scores": scores,
        "fiveLenses": lenses,
        "hypotheses": [],
        "replicable": replicable,
        "limitations": contingent,
        "provenance": provenance,
        "training": {
            "evidencePolicyVersion": "1.1",
            "evidenceRole": role,
            "evidenceLevel": evidence_level,
            "requiredEvidenceObserved": eligible,
            "supportEligible": eligible,
            "claimCoverage": claims,
            "provenanceAndConsent": {
                "storyOrigin": "creator-authored gameplay or documented own project",
                "consentStatus": "not_applicable",
                "identityProtection": "not_applicable",
                "evidence": ["nenhum relato privado de terceiro foi ensinado"],
            },
            "replicable": replicable,
            "contingent": contingent,
            "notRecommended": [
                "copiar frases, personagens, mundo de jogo ou roteiro",
                "tratar numeração de episódio como prova de compreensão ou retenção",
                "inferir cenas, áudio, texto na tela, montagem, ritmo ou retenção",
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
        id="obs-20260913-146",
        title="Construindo uma casa do zero em 100 dias – Episódio 9: Novo janelão XXL",
        creator="Construindo no Paraíso", identity="construindo-no-paraiso",
        url="https://www.youtube.com/watch?v=EWNQZjWOH2U",
        published="2026-04-01", duration="PT56M10S",
        accessible=[
            "título", "criador", "descrição integral com capítulos", "data exata", "duração",
            "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "129 visualizações", "2 curtidas",
            "meta global de reformar uma casa em 100 dias", "posição no episódio 9",
            "recapitulação do estado inicial e objetivo específico de portas e janelão",
        ],
        missing=MISSING_AV + ["comentários públicos ou contagem de comentários"],
        metrics={"viewsObserved": "129", "likesObserved": "2", "commentsObserved": "not_assessed"},
        cls=classification(
            material="video_longo", presentations=["transformacao", "bastidores", "tutorial"],
            primary="transformacao", secondary=["storytelling", "demonstracao"],
            mix=[{"family":"transformacao","percentage":45},{"family":"storytelling","percentage":35},{"family":"demonstracao","percentage":20}],
            objectives=["visualizacao","retencao","comunidade","educar"], advertising="parceria_com_criador",
            intent="implicita", entity={"kind":"servico","name":"Renoves","confidence":"medium"},
            topic="reforma seriada de casa abandonada", segment="casa, construção e DIY",
            subsegment="reforma em desafio de 100 dias", audience="adultos interessados em reforma, arquitetura e DIY",
            awareness="consciente_solucao", production="intermediate", scale="small", replicability="medium",
            duration="over_60s", mechanisms=["curiosidade","recompensa","admiracao"],
            hooks=["transformacao","pergunta","numero"], narrative=["situacao","problema","continuidade_serial","progressao","transformacao"],
            proof=["alegacao_sem_prova"], cta=["seguir","comentar","conversar"], confidence="high",
            evidence=[
                "O título informa desafio de 100 dias, episódio 9 e entrega local do janelão.",
                "Entre 00:33 e 01:03, a transcrição recapitula ruína, projeto, meta e inexperiência.",
                "Entre 01:39 e 01:45, a fala abre a tarefa local: janela grande e portas.",
            ],
        ),
        comparison={"level":2,"group":"storytelling seriado de desafio com meta, posição, recapitulação e complicação","referenceIds":["obs-20260913-147","obs-20260913-148"],"confidence":"medium"},
        observations=[
            "O pacote título mais abertura identifica meta global, posição serial e transformação local.",
            "A recapitulação verbal reconstrói o ponto de partida antes da tarefa do episódio.",
            "A integração comercial aparece depois da orientação inicial e é contexto, não prova causal.",
        ],
        interpretations=[
            "A orientação pode permitir entrada no episódio sem exigir conhecimento de capítulos anteriores.",
            "A diversidade de segmento amplia recorrência estrutural, mas reduz comparabilidade de desempenho.",
        ],
        scores={"gancho":86,"clareza":92,"relevancia":84,"desejo":85,"confianca":77,"retencao":"not_assessed","acao":76,"objecoes":70},
        lenses={
            "apressado":"Título e abertura delimitam meta, episódio e obra local.",
            "analitico":"Recebe objetivo e contexto, mas não teve execução visual auditada.",
            "aspiracional":"A passagem de ruína a casa oferece transformação declarada.",
            "comunidade":"A série e o convite a acompanhar dias criam continuidade possível, sem comentários observados.",
            "cetico":"Desconta parceria, tradução automática e ausência de vídeo reproduzido.",
        },
        replicable=["Nomear meta finita e posição serial no título.","Recapitular ponto de partida em uma frase curta.","Abrir uma tarefa local que avance a meta global."],
        contingent=["Sem audiovisual, áudio ouvido, texto na tela, edição, ritmo ou retenção.","A reforma física e a parceria elevam custo material.","Comentários e baseline contemporâneo não foram obtidos."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"meta global e posição serial aparecem cedo","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"a abertura recapitula contexto e abre complicação específica","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_after_public_search",
        comment_provenance=False,
    ),
    make_ref(
        id="obs-20260913-147",
        title="NO LIMITE — A Vila Precisa de Proteção! | Minecraft Hardcore Relaxante #03",
        creator="eDuBom", identity="edubom",
        url="https://www.youtube.com/watch?v=FImFjzVFCnc",
        published="2026-07-06", duration="PT3H32M38S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "1.029 visualizações", "55 curtidas",
            "7 comentários declarados", "amostra pública de 4 comentários",
            "posição no episódio 3 e dia 33 de 100", "recapitulação das duas lives anteriores",
            "missão local de proteger a vila",
        ],
        missing=MISSING_AV + ["três comentários não adquiridos"],
        metrics={"viewsObserved":"1.029","likesObserved":"55","commentsObserved":"7 declarados; 4 extraídos como amostra"},
        cls=classification(
            material="video_longo", presentations=["narracao_imagens", "bastidores", "camera_direta"],
            primary="storytelling", secondary=["entretenimento", "comunidade"],
            mix=[{"family":"storytelling","percentage":50},{"family":"entretenimento","percentage":30},{"family":"comunidade","percentage":20}],
            objectives=["visualizacao","retencao","comunidade","comentario"], advertising="publicidade_nativa",
            intent="implicita", entity={"kind":"produto","name":"Galley, LivePix e membros","confidence":"high"},
            topic="Minecraft Hardcore relaxante em série de 100 dias", segment="games e entretenimento",
            subsegment="longplay Minecraft Hardcore", audience="jogadores brasileiros que buscam longplay calmo e progressão serial",
            awareness="consciente_produto", production="simple", scale="small", replicability="high",
            duration="over_60s", mechanisms=["curiosidade","pertencimento","recompensa","tensao"],
            hooks=["narrativo","risco","promessa"], narrative=["situacao","problema","risco","progressao","continuidade_serial"],
            proof=["alegacao_sem_prova"], cta=["comentar","seguir","comprar"], confidence="high",
            evidence=[
                "A descrição localiza dia 33, meta de 100 dias e risco de morte permanente.",
                "Entre 00:34 e 00:54, a transcrição recapitula as duas lives anteriores.",
                "Entre 00:54 e 01:17, a fala define proteger a vila como missão do episódio.",
            ],
        ),
        comparison={"level":2,"group":"storytelling seriado de desafio com meta, posição, recapitulação e complicação","referenceIds":["obs-20260913-146","obs-20260913-148"],"confidence":"high"},
        observations=[
            "Descrição e fala combinam meta de 100 dias, dia 33, retrospecto e missão atual.",
            "A abertura verbal também lembra a regra sem segunda chance.",
            "Quatro comentários amostrados sinalizam acompanhamento da série, sem representar toda a recepção.",
        ],
        interpretations=[
            "Recapitulação e missão local tornam a continuidade compreensível na fala.",
            "A duração de mais de três horas impede comparar desempenho com episódios editados.",
        ],
        scores={"gancho":83,"clareza":91,"relevancia":86,"desejo":82,"confianca":82,"retencao":"not_assessed","acao":78,"objecoes":79},
        lenses={
            "apressado":"Entende série, risco e missão no primeiro minuto falado.",
            "analitico":"Recebe histórico e regra, mas não viu a execução do jogo.",
            "aspiracional":"A construção progressiva do refúgio fornece avanço declarado.",
            "comunidade":"Saudação e comentários amostrados indicam continuidade, não eficácia.",
            "cetico":"A longplay e a live têm contexto de consumo distinto de vídeo editado.",
        },
        replicable=["Localizar episódio e posição global antes da missão.","Recapitular somente marcos relevantes.","Relacionar a missão local à regra permanente da série."],
        contingent=["Sem audiovisual, áudio ouvido, texto na tela, edição, ritmo ou retenção.","Longplay de mais de três horas tem contexto específico.","Amostra de comentários pequena e não representativa."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"meta global e posição serial aparecem cedo","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"a abertura recapitula e abre missão específica","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_and_public_comment_sample_after_public_search",
    ),
    make_ref(
        id="obs-20260913-148",
        title="FINALMENTE TERMINAMOS A NOSSA CASA NO 100 DIAS EM 1 BLOCO NO MINECRAFT - EP. 3",
        creator="MV Games", identity="mv-games",
        url="https://www.youtube.com/watch?v=qc8SCgY0dlc",
        published="2023-05-29", duration="PT41M08S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "41 visualizações", "5 curtidas",
            "meta de 100 dias em um bloco", "posição no episódio 3 e dia 20",
            "recapitulação do episódio anterior", "problema local de proteger os animais",
        ],
        missing=MISSING_AV + ["comentários públicos ou contagem de comentários"],
        metrics={"viewsObserved":"41","likesObserved":"5","commentsObserved":"not_assessed"},
        cls=classification(
            material="video_longo", presentations=["narracao_imagens", "demonstracao"],
            primary="storytelling", secondary=["entretenimento", "demonstracao"],
            mix=[{"family":"storytelling","percentage":55},{"family":"entretenimento","percentage":25},{"family":"demonstracao","percentage":20}],
            objectives=["visualizacao","retencao","comunidade"], advertising="editorial_organico",
            intent="ausente", entity={"kind":"nenhuma","name":"","confidence":"high"},
            topic="Minecraft em um bloco durante 100 dias", segment="games e entretenimento",
            subsegment="desafio Minecraft One Block", audience="jogadores brasileiros interessados em sobrevivência e construção serial",
            awareness="consciente_produto", production="simple", scale="small", replicability="high",
            duration="over_60s", mechanisms=["curiosidade","tensao","recompensa","pertencimento"],
            hooks=["resultado_antecipado","numero","narrativo"], narrative=["situacao","problema","risco","progressao","continuidade_serial"],
            proof=["alegacao_sem_prova"], cta=["outro_conteudo"], confidence="high",
            evidence=[
                "O título declara a meta de 100 dias, episódio 3 e resultado da casa.",
                "Entre 00:04 e 00:28, a fala recapitula a evolução e remete ao episódio anterior.",
                "Entre 00:50 e 01:50, a fala localiza o dia 20 e abre o risco aos animais como tarefa.",
            ],
        ),
        comparison={"level":1,"group":"storytelling seriado de desafio Minecraft com meta, posição, recapitulação e complicação","referenceIds":["obs-20260913-147"],"confidence":"high"},
        observations=[
            "Título e abertura fornecem meta global, posição serial, retrospecto e obstáculo local.",
            "A perda anterior de um cachorro torna a proteção dos animais uma consequência concreta declarada.",
            "O convite a ver o episódio anterior não substitui a recapitulação, que ainda ocorre na fala.",
        ],
        interpretations=[
            "Este é o apoio novo mais comparável porque compartilha jogo, desafio, série e mecanismo com o episódio de eDuBom.",
            "O baixo alcance absoluto não é contraevidência sem impressões ou baseline do canal.",
        ],
        scores={"gancho":86,"clareza":90,"relevancia":84,"desejo":81,"confianca":79,"retencao":"not_assessed","acao":62,"objecoes":76},
        lenses={
            "apressado":"Dia, meta e problema ficam identificáveis antes de um minuto.",
            "analitico":"Entende o estado e a tarefa, mas não viu a construção ou o payoff.",
            "aspiracional":"A casa concluída é prometida no título, sem prova visual auditada.",
            "comunidade":"A referência ao episódio anterior favorece continuidade, sem comentários acessíveis.",
            "cetico":"Não trata 41 visualizações como falha do mecanismo sem denominador.",
        },
        replicable=["Combinar meta global, dia atual e risco local.","Recapitular o progresso sem exigir retorno ao capítulo anterior.","Fazer a complicação local derivar de uma perda ou limite já declarado."],
        contingent=["Sem audiovisual, áudio ouvido, texto na tela, edição, ritmo ou retenção.","Transcrição automática contém erros lexicais.","Sem comentários, impressões ou baseline contemporâneo."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"meta global e posição serial aparecem cedo","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"a abertura recapitula e abre complicação específica","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_after_public_search",
        comment_provenance=False,
    ),
    make_ref(
        id="obs-20260913-149",
        title="O ARK NÃO QUER QUE EU SOBREVIVA! - ARK: THE ISLAND #04",
        creator="PaulloArk", identity="paulloark",
        url="https://www.youtube.com/watch?v=1zLXAcK-4go",
        published="2026-08-25", duration="PT20M18S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "20 visualizações", "posição no episódio 4",
            "continuidade imediata após calor extremo", "complicação de recursos insuficientes",
        ],
        missing=MISSING_AV + ["curtidas", "comentários públicos ou contagem de comentários", "meta global finita", "posição de progresso dentro de uma meta global"],
        metrics={"viewsObserved":"20","likesObserved":"not_assessed","commentsObserved":"not_assessed"},
        cls=classification(
            material="video_longo", presentations=["narracao_imagens", "demonstracao"],
            primary="storytelling", secondary=["entretenimento", "demonstracao"],
            mix=[{"family":"storytelling","percentage":55},{"family":"entretenimento","percentage":30},{"family":"demonstracao","percentage":15}],
            objectives=["visualizacao","retencao"], advertising="editorial_organico",
            intent="ausente", entity={"kind":"nenhuma","name":"","confidence":"high"},
            topic="sobrevivência seriada em ARK", segment="games e entretenimento",
            subsegment="gameplay narrado de ARK", audience="jogadores brasileiros interessados em sobrevivência e progressão",
            awareness="consciente_produto", production="simple", scale="small", replicability="high",
            duration="over_60s", mechanisms=["tensao","curiosidade","recompensa"],
            hooks=["narrativo","risco"], narrative=["situacao","problema","tentativa","progressao","continuidade_serial"],
            proof=["alegacao_sem_prova"], cta=[], confidence="high",
            evidence=[
                "O título localiza o episódio 4, mas não declara meta global finita.",
                "A fala abre após recuperação do calor e encontra falta de três lingotes.",
                "Até 02:24, a transcrição avança tarefas sem recapitulação explícita de meta global ou posição de progresso.",
            ],
        ),
        comparison={"level":1,"group":"caso-limite de storytelling seriado de sobrevivência com continuidade e complicação, sem meta global finita","referenceIds":["obs-20260913-147","obs-20260913-148"],"confidence":"high"},
        observations=[
            "Há continuidade serial, risco e obstáculo local diretamente na abertura.",
            "Não foi observada meta global finita nem posição atual dentro dela.",
            "O caso separa recapitulação orientadora de simples retomada da ação.",
        ],
        interpretations=[
            "Continuidade e complicação isoladas não satisfazem o padrão completo.",
            "Vinte visualizações não configuram contraexemplo de desempenho sem baseline ou impressões.",
        ],
        scores={"gancho":78,"clareza":82,"relevancia":80,"desejo":76,"confianca":78,"retencao":"not_assessed","acao":"not_assessed","objecoes":67},
        lenses={
            "apressado":"Reconhece perigo e tarefa, mas não recebe a meta ampla.",
            "analitico":"Vê progressão de recursos na fala, sem mapa da série.",
            "aspiracional":"Há sobrevivência e evolução declaradas, sem transformação final definida.",
            "comunidade":"A numeração permite reconhecer continuidade, sem comentários acessíveis.",
            "cetico":"Classifica como limite estrutural, não como fracasso causal.",
        },
        replicable=["Abrir pela consequência imediata do capítulo anterior.","Usar um recurso faltante como complicação concreta."],
        contingent=["Sem meta global finita ou posição de progresso observável.","Sem audiovisual, áudio ouvido, texto na tela, edição, ritmo ou retenção.","Sem comentários, curtidas, impressões ou baseline."],
        role="falsification_or_boundary", evidence_level=1, eligible=False,
        claims=[
            {"claim":"há continuidade serial e complicação específica","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"há meta global finita e posição atual","requiredModalities":["title","description","transcript","finite_goal_statement"],"observedModalities":["title","description","transcript"],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_after_public_search",
        comment_provenance=False,
    ),
    make_ref(
        id="obs-20260913-150",
        title="Como falamos \"estragar\" em inglês",
        creator="English by Dr Cooper", identity="english-by-dr-cooper",
        url="https://www.youtube.com/watch?v=Q1LTIqunioY",
        published="2020-03-26", duration="PT1M",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral com timestamps, porém ruidosa e de baixa confiabilidade",
            "10.102 visualizações", "1.009 curtidas", "72 comentários declarados",
            "amostra pública de 50 comentários", "descrição com tarefa de escrever frases e promessa de correção",
            "três respostas de alunos aplicando o verbo na amostra",
        ],
        missing=MISSING_AV + ["fala integral confiável por substituição textual", "respostas corretivas do criador na amostra de comentários"],
        metrics={"viewsObserved":"10.102","likesObserved":"1.009","commentsObserved":"72 declarados; 50 extraídos como amostra"},
        cls=classification(
            material="video_curto", presentations=["camera_direta", "dramatizacao", "tutorial"],
            primary="educativo", secondary=["humor", "comunidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"humor","percentage":30},{"family":"comunidade","percentage":15}],
            objectives=["educar","comentario","comunidade","lead"], advertising="geracao_de_leads",
            intent="explicita", entity={"kind":"servico","name":"English by Dr Cooper","confidence":"high"},
            topic="uso do verbo inglês ruin", segment="educação e idiomas",
            subsegment="vocabulário inglês para brasileiros", audience="brasileiros aprendendo inglês",
            awareness="consciente_solucao", production="simple", scale="medium", replicability="high",
            duration="31_to_60s", mechanisms=["humor","recompensa","pertencimento"],
            hooks=["problema","verbal"], narrative=["mecanismo","progressao","cta"],
            proof=["prova_social"], cta=["comentar","clicar"], confidence="medium",
            evidence=[
                "A descrição pede frases nos comentários e promete correção posterior.",
                "A amostra contém três aplicações do verbo e perguntas de uso.",
                "Nenhuma resposta corretiva do criador apareceu na amostra adquirida.",
            ],
            alternatives=["humor como família principal"],
            missing=MISSING_AV + ["fala integral confiável", "feedback corretivo observado"],
        ),
        comparison={"level":3,"group":"exploração educacional de tarefa aplicada em comentários","referenceIds":["obs-20260911-131","obs-20260911-132","obs-20260911-133"],"confidence":"medium"},
        observations=[
            "A descrição converte o CTA em produção de frases com o verbo ensinado.",
            "Três comentários amostrados aplicam a unidade; outros perguntam por alternativas semânticas.",
            "A promessa de correção não foi confirmada na amostra de 50 comentários.",
        ],
        interpretations=[
            "A tarefa pode gerar aplicação observável sem garantir feedback ou aprendizagem.",
            "Humor e elogios são recepção declarada, não prova de memória, compreensão ou desempenho.",
        ],
        scores={"gancho":76,"clareza":82,"relevancia":86,"desejo":78,"confianca":75,"retencao":"not_assessed","acao":88,"objecoes":74},
        lenses={
            "apressado":"Título e duração delimitam uma unidade pequena.",
            "analitico":"Encontra exemplos e aplicações, mas quer correção observável.",
            "aspiracional":"A aplicação imediata torna o vocabulário utilizável.",
            "comunidade":"Há respostas de alunos, mas não retorno corretivo amostrado.",
            "cetico":"Não trata elogios nem promessa de correção como aprendizagem comprovada.",
        },
        replicable=["Pedir uma produção que use exatamente a unidade ensinada.","Amostrar respostas separadamente de elogios.","Se prometer correção, tornar o feedback rastreável e específico."],
        contingent=["Exploração de outra família; não sustenta o padrão de storytelling seriado.","Transcrição automática é ruidosa e não suporta reconstrução fina da fala.","Sem audiovisual, áudio ouvido, texto na tela, edição, ritmo ou retenção.","Amostra de 50 comentários não contém correção observável."],
        role="controlled_exploration", evidence_level=3, eligible=False,
        claims=[
            {"claim":"o CTA pede aplicação da unidade","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
            {"claim":"alunos aplicaram a unidade","requiredModalities":["comment_sample"],"observedModalities":["comment_sample"],"sufficient":True},
            {"claim":"o criador corrigiu as respostas","requiredModalities":["comment_sample","creator_reply"],"observedModalities":["comment_sample"],"sufficient":False},
            {"claim":"houve aprendizagem","requiredModalities":["learning_measure"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_noisy_full_automatic_transcript_and_public_comment_sample_after_public_search",
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
for item in refs:
    if item["url"] in existing_urls:
        raise SystemExit(f"URL duplicada: {item['url']}")
    existing_urls.add(item["url"])
memory["references"].extend(refs)

new_supports = ["obs-20260913-146", "obs-20260913-147", "obs-20260913-148"]
hypothesis["supportReferenceIds"].extend(new_supports)
hypothesis["status"] = "promoted_to_provisional"
hypothesis["promotedPatternId"] = PATTERN_ID
hypothesis["promotedAt"] = NOW
hypothesis.pop("reasonNotPromoted", None)

memory["patterns"].append({
    "id": PATTERN_ID,
    "status": "provisional",
    "stage": "provisional",
    "name": "Recapitulação orientadora antes da complicação serial",
    "statement": "Em storytelling seriado de desafio, declarar a meta global e a posição atual, recapitular apenas o estado necessário e então abrir uma complicação específica torna orientação e progressão reconhecíveis na fala ou no pacote título-abertura; efeitos sobre retenção, entrada de novos espectadores ou desempenho permanecem não medidos.",
    "creativeFamily": "storytelling",
    "objective": "orientação serial e compreensão da progressão",
    "segment": "séries de desafio em viagem, games e transformação",
    "mechanism": ["curiosidade", "recompensa", "pertencimento", "tensao"],
    "conditions": [
        "meta global finita ou explicitamente delimitada",
        "posição atual identificável por dia, episódio ou progresso",
        "recapitulação do estado anterior suficiente para orientar",
        "complicação ou missão local ligada ao avanço da meta",
        "sequência observável em título, descrição ou transcrição",
    ],
    "supportReferenceIds": new_supports,
    "precursorReferenceIds": ["obs-20260824-035", "obs-20260825-050"],
    "comparableSupportCount": 3,
    "supportingCount": 3,
    "counterexampleCount": 0,
    "caseLimitCount": 1,
    "counterexampleReferenceIds": [],
    "caseLimitReferenceIds": ["obs-20260913-149"],
    "comparisonLevel": 2,
    "confidence": "medium",
    "creatorDiversityCount": 3,
    "sourceDiversityCount": 3,
    "patternType": "compreensao",
    "evidence": [
        {"referenceId":"obs-20260913-146","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Título e abertura conectam desafio de 100 dias, episódio 9, estado da ruína e tarefa de portas e janelão.","evidence":"Metadados, descrição com capítulos e transcrição automática integral.","limitations":["sem audiovisual ou retenção","segmento de reforma"]},
        {"referenceId":"obs-20260913-147","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Descrição e fala localizam dia 33, episódio 3, duas etapas anteriores e missão de proteger a vila.","evidence":"Metadados, transcrição automática integral e amostra de quatro comentários.","limitations":["longplay de mais de três horas","sem audiovisual ou retenção"]},
        {"referenceId":"obs-20260913-148","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Título e abertura combinam 100 dias, episódio 3, dia 20, progresso anterior e risco aos animais.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["sem audiovisual ou retenção","sem comentários"]},
        {"referenceId":"obs-20260913-149","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"A retomada serial abre com consequência e recurso faltante, mas sem meta global finita nem posição de progresso.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["não conta como apoio nem contraexemplo"]},
    ],
    "limitations": [
        "Os três apoios independentes demonstram recorrência estrutural, não eficácia.",
        "Nenhum vídeo, áudio, capa, texto na tela, ritmo, montagem ou curva de retenção foi auditado.",
        "Os apoios abrangem games e reforma e variam de 41 minutos a mais de três horas; não formam benchmark numérico.",
        "Os dois precursores do mesmo criador permanecem contexto e não contam para independência.",
        "O caso-limite separa retomada da ação de orientação por meta e posição.",
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
    "candidatesFound": 72,
    "referenceIds": ["obs-20260913-146","obs-20260913-147","obs-20260913-148","obs-20260913-149","obs-20260913-150"],
    "targetKnowledgeId": TARGET_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": ["obs-20260913-149"],
    "controlledExplorationReferenceIds": ["obs-20260913-150"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=hiGpqjdisK4","reason":"dublagem/adaptação de obra de terceiro; autoria e fonte reduziriam independência do apoio"},
        {"url":"https://www.youtube.com/watch?v=O0SYl9dvyL8","reason":"mesmo criador de apoio selecionado e sem transcrição adquirida; redundante"},
        {"url":"https://www.youtube.com/watch?v=_JBNTXeQFqk","reason":"mesmo criador de apoio selecionado; diversidade inferior"},
        {"url":"https://www.youtube.com/watch?v=B-70DkGkxlI","reason":"dublagem de série estrangeira e mesma fonte de outro candidato"},
        {"url":"https://www.youtube.com/watch?v=80TyhLlMaX8","reason":"dublagem de série estrangeira e mesma fonte de outro candidato"},
        {"url":"https://www.youtube.com/watch?v=SM3tgP3eOLo","reason":"produção televisiva complexa e episódio não orientado por posição serial comparável"},
        {"url":"https://www.youtube.com/watch?v=lBNvX5-Eos0","reason":"produção televisiva complexa, baixa replicabilidade e formato de episódio integral"},
        {"url":"https://www.youtube.com/watch?v=J6ivwIndleQ","reason":"recap televisivo internacional e produção não replicável para o lote"},
        {"url":"https://www.youtube.com/watch?v=8jC3G2dFOKc","reason":"timelapse internacional; prioridade brasileira e menor comparabilidade de fala"},
        {"url":"https://www.youtube.com/watch?v=QF5YpZI1wnk","reason":"criador internacional de grande escala e sem posição serial no título"},
        {"url":"https://www.youtube.com/watch?v=POoMk4pvqvo","reason":"educativo recente sem histórico de comentários suficiente; exploração escolhida tinha aplicações públicas"},
        {"url":"https://www.youtube.com/watch?v=ZwwLcjoMlhg","reason":"aula longa; exploração escolhida oferecia tarefa aplicada e amostra de respostas"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 5,
    "replicableReferences": 5,
    "creativeFamiliesObserved": ["storytelling","transformacao","demonstracao","entretenimento","educativo","humor","comunidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads de vídeo e áudio e aquisição de capas expiraram por timeout; o player público também não foi usado como substituto de pesquisa","effect":"imagem em movimento, áudio ouvido, texto na tela, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullAutomatic":4,"fullAutomaticLowConfidence":1,"partialAutomatic":0,"none":0,"limitation":"transcrições automáticas substituem apenas fala e podem conter erros; a exploração tem reconhecimento multilíngue ruidoso"},
    "commentsCoverage": {"partialSample":2,"unavailable":3,"limitation":"amostras públicas não são representativas nem equivalem a retenção ou aprendizagem"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"idades, durações, segmentos e escalas heterogêneos impedem benchmark de desempenho"},
    "patternsCreated": [PATTERN_ID],
    "patternsStrengthened": [],
    "patternsRefined": [],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [TARGET_ID],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["continuidade serial e complicação local não substituem meta global finita e posição atual"],
    "safetyFindings": ["comentários públicos foram resumidos sem usernames","nenhum relato privado de terceiro ou alegação sensível foi ensinado"],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três fontes brasileiras independentes sustentam recorrência estrutural de meta, posição, recapitulação e complicação em storytelling seriado de desafio. O padrão é provisório; entrada de novos espectadores, retenção e desempenho não foram medidos.",
    "nextTarget": "storytelling seriado brasileiro curto com audiovisual integral e coorte contemporânea, incluindo um episódio cuja recapitulação seja longa ou confusa e um teste de compreensão entre novos e recorrentes",
    "limitations": ["Nenhum audiovisual, áudio ou capa foi adquirido.","Uma transcrição automática teve baixa confiabilidade.","Sem retenção, teste de compreensão ou baseline homogêneo.","Comentários são ausentes ou amostrais.","Nenhum resultado autoriza causalidade ou validação."],
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
