#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-036.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-23T11:11:28.000Z"
OBSERVED = "2026-09-23"
RUN_ID = "run-20260923-supervised-037"
PATTERN_ID = "pat-20260921-015"
BATCH_IDS = {f"obs-20260923-{n}" for n in range(201, 206)}

make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

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
    "mídia paga",
]


def build_ref(*, id, title, creator, identity, url, published, duration,
              accessible, missing, metrics, classification, comparison,
              observations, interpretations, scores, lenses, replicable,
              contingent, role, evidence_level, eligible, claims, source_type,
              consent=None):
    item = make_ref(
        id=id, title=title, creator=creator, identity=identity, url=url,
        published=published, duration=duration, accessible=accessible,
        missing=missing, metrics=metrics, cls=classification,
        comparison=comparison, observations=observations,
        interpretations=interpretations, scores=scores, lenses=lenses,
        replicable=replicable, contingent=contingent, role=role,
        evidence_level=evidence_level, eligible=eligible, claims=claims,
        source_type=source_type, comment_provenance=True,
    )
    item["country"] = "BR"
    item["training"]["provenanceAndConsent"] = consent or {
        "storyOrigin": "conteúdo editorial público do próprio criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhuma história privada identificável de terceiro foi ensinada"],
    }
    item["training"]["notRecommended"] = [
        "copiar pergunta, nome, frase, personagem ou roteiro",
        "expor a identidade de quem enviou uma dúvida sem necessidade e consentimento",
        "tratar comentário, visualização, fama, publicidade ou orçamento como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
        "confundir recorrência estrutural com aprendizagem ou desempenho comprovado",
    ]
    return item


GROUP = "tutorial brasileiro de software ou configuração de interface que parte de dúvida específica atribuída, usa recurso interno e demonstra caminho e resultado na fala"

refs = [
    build_ref(
        id="obs-20260923-201",
        title="PERGUNTAS #01 | Respondendo dúvidas dos inscritos!",
        creator="PPTRETA", identity="pptreta",
        url="https://www.youtube.com/watch?v=obTMWZHombM",
        published="2020-06-25", duration="PT7M45S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 7 minutos e 45 segundos",
            "transcrição automática integral em português com 149 segmentos e timestamps", "fala por substituição textual",
            "1.127 visualizações e 62 curtidas observadas", "amostra integral dos 2 comentários públicos retornados",
            "pergunta específica sobre fonte padrão atribuída a inscrito", "rotas nativas Design, Fontes, Slide Mestre e caixa de texto padrão nomeadas",
            "comentário do autor da dúvida agradecendo a resposta",
        ],
        missing=MISSING_AV + ["contagem pública total de comentários", "termo formal de autorização", "teste contemporâneo no PowerPoint", "teste de compreensão"],
        metrics={"viewsObserved":1127,"likesObserved":62,"commentsObserved":"not_measured"},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":50},{"family":"demonstracao","percentage":35},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="alterar a fonte padrão no PowerPoint",
            segment="software e produtividade", subsegment="design de apresentações no PowerPoint", audience="usuários que querem padronizar apresentações",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","confianca"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado","depoimento"], cta=["comentar","seguir"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"produtos e serviços do canal","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:30, a fala apresenta o quadro, atribui a pergunta e delimita a fonte padrão no PowerPoint.",
                "Entre 1:02 e 4:07, a transcrição registra Design, Fontes, Slide Mestre e caixa de texto padrão como rotas internas.",
                "Um dos dois comentários retornados é do autor da dúvida e agradece a resposta; isso não é teste controlado.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260923-202","obs-20260923-203"],"confidence":"high"},
        observations=[
            "Pergunta, objeto, software e rotas internas são rastreáveis na fala.",
            "A confirmação pública do autor melhora a procedência, sem provar aprendizagem ou autorização formal.",
            "A interface de 2020 não foi revalidada em versão contemporânea.",
        ],
        interpretations=[
            "Uma dúvida específica pode organizar alternativas internas sem exigir ferramenta externa.",
            "Ofertas e métricas são contexto e não explicam utilidade, confiança ou desempenho.",
        ],
        scores={"gancho":87,"clareza":93,"relevancia":92,"desejo":79,"confianca":84,"retencao":"not_assessed","acao":82,"objecoes":86},
        lenses={
            "apressado":"Recebe pergunta e software na abertura.",
            "analitico":"Encontra três rotas internas, mas precisa ver a tela e testar a versão atual.",
            "aspiracional":"Padronização promete apresentações mais consistentes.",
            "comunidade":"O autor da dúvida agradece publicamente.",
            "cetico":"Desconta UI antiga, oferta e ausência de execução audiovisual.",
        },
        replicable=["Atribuir a dúvida sem expor identidade desnecessária.","Delimitar objeto e software antes dos passos.","Apresentar alternativas internas e seus usos."],
        contingent=["Interface publicada em 2020.","Resultado visual não observado.","Consentimento formal não auditado."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a pauta parte de dúvida específica atribuída e reconhecida publicamente","requiredModalities":["transcript","comments"],"observedModalities":["transcript","comments"],"sufficient":True},
            {"claim":"rotas internas, passos e resultado declarado são identificáveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_2_public_comments",
        consent={"storyOrigin":"pergunta de inscrito atribuída na fala e reconhecida pelo próprio autor em comentário público","consentStatus":"public_acknowledgment_but_formal_reuse_consent_not_audited","identityProtection":"nome omitido do princípio transferível","evidence":["o autor agradece publicamente; termo formal não foi acessado"]},
    ),
    build_ref(
        id="obs-20260923-202",
        title="CENTRAL MULTIMÍDIA ADAK - Dúvidas dos inscritos, Como configurar a para aparecer a logo",
        creator="CANAL DO MANOBIZA TECH", identity="canal-do-manobiza-tech",
        url="https://www.youtube.com/watch?v=pLFYw7G2qpw",
        published="2023-04-27", duration="PT5M29S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 5 minutos e 29 segundos",
            "transcrição automática integral em português com 129 segmentos e timestamps", "fala por substituição textual",
            "201.309 visualizações e 4.941 curtidas observadas", "amostra pública de 20 comentários de topo",
            "comentário específico atribuído na fala", "problema de reinicialização e logo delimitado", "caminho interno Configurações, suspensão e não desligar nomeado",
        ],
        missing=MISSING_AV + ["contagem pública total de comentários", "consentimento formal do comentarista", "confirmação visual da reinicialização e da logo", "teste independente"],
        metrics={"viewsObserved":201309,"likesObserved":4941,"commentsObserved":"not_measured"},
        classification=cls(
            presentations=["tutorial","demonstracao","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":45},{"family":"demonstracao","percentage":40},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="configurar reinicialização e exibição da logo em central multimídia Android",
            segment="tecnologia automotiva", subsegment="configuração de central multimídia", audience="proprietários de central multimídia que não veem a logo ao ligar",
            awareness="consciente_problema", production="simple", scale="large", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","alivio"], hooks=["pergunta","problema"],
            narrative=["problema","mecanismo","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","seguir","clicar"],
            advertising="publicidade_nativa", intent="explicita", entity={"kind":"produto","name":"centrais multimídia e acessórios divulgados pelo canal","confidence":"high"},
            evidence=[
                "Entre 0:03 e 0:43, a fala atribui o comentário e explica que a unidade retoma o estado anterior em vez de reiniciar.",
                "Entre 1:00 e 1:38, descreve o mecanismo de suspensão; entre 2:11 e 3:06, registra Configurações, suspensão e não desligar.",
                "Entre 3:13 e 3:16, declara reinicialização e logo; o resultado visual não foi observado.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260923-201","obs-20260923-203"],"confidence":"high"},
        observations=[
            "A dúvida atribuída é convertida em diagnóstico do estado de suspensão antes do ajuste.",
            "O caminho de configuração e o resultado declarado são reconstruíveis na transcrição.",
            "Comentários trazem agradecimento e novas dúvidas; nenhum é teste representativo de execução.",
        ],
        interpretations=[
            "O padrão aparece também em interface embarcada, não apenas em software de desktop.",
            "Afiliados, merchandising e escala são contexto, não causa da entrega.",
        ],
        scores={"gancho":89,"clareza":94,"relevancia":94,"desejo":82,"confianca":80,"retencao":"not_assessed","acao":84,"objecoes":87},
        lenses={
            "apressado":"Reconhece problema e comportamento da central cedo.",
            "analitico":"Recebe mecanismo e caminho, mas precisa confirmar o modelo e a tela.",
            "aspiracional":"A logo na inicialização sinaliza personalização do equipamento.",
            "comunidade":"Um comentário público vira resposta técnica.",
            "cetico":"Exige compatibilidade do modelo, visual e teste próprio.",
        },
        replicable=["Transformar a dúvida em diagnóstico antes dos cliques.","Nomear estado atual, ajuste e resultado.","Separar merchandising da evidência técnica."],
        contingent=["Compatibilidade pode variar por modelo e firmware.","Identidade pública foi omitida desta ficha.","Resultado visual não observado."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala atribui comentário específico e delimita o problema funcional","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"mecanismo, caminho interno e resultado declarado aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_20_public_comments",
        consent={"storyOrigin":"comentário público atribuído pelo criador","consentStatus":"creator_attribution_but_formal_reuse_consent_not_audited","identityProtection":"identidade omitida do princípio e da ficha analítica","evidence":["a fala identifica a origem pública; autorização formal não foi acessada"]},
    ),
    build_ref(
        id="obs-20260923-203",
        title="Canva: Como excluir conta Canva (respondendo dúvida do inscrito)",
        creator="Edenia Borges | Pinterest para Negócios", identity="edenia-borges-pinterest-para-negocios",
        url="https://www.youtube.com/watch?v=b61O87VpeqQ",
        published="2020-01-17", duration="PT8M28S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 8 minutos e 28 segundos",
            "transcrição automática integral em português com 191 segmentos e timestamps", "fala por substituição textual",
            "14.489 visualizações e 237 curtidas observadas", "amostra pública de 13 comentários de topo",
            "dúvida específica atribuída sobre excluir ou desativar conta", "rotas internas Ajuda, Configurações e contato com suporte nomeadas", "risco de perda dos designs advertido",
        ],
        missing=MISSING_AV + ["contagem pública total de comentários", "consentimento formal do inscrito", "validação da interface atual do Canva", "teste de execução ou compreensão"],
        metrics={"viewsObserved":14489,"likesObserved":237,"commentsObserved":"not_measured"},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":50},{"family":"demonstracao","percentage":35},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="excluir ou desativar uma conta no Canva",
            segment="software e produtividade", subsegment="gestão de conta no Canva", audience="usuários que querem encerrar a conta ou não encontram a opção",
            awareness="consciente_problema", production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","vigilancia"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","risco","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","seguir","clicar"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"cursos e materiais da criadora","confidence":"high"},
            evidence=[
                "Entre 0:06 e 0:43, a fala explica que a série responde perguntas; entre 1:31 e 2:09, atribui a dúvida sobre apagar ou desativar a conta.",
                "Entre 2:30 e 5:18, a transcrição registra Ajuda, Configurações, desativação e aviso de perda irreversível dos designs.",
                "Entre 5:20 e 7:15, oferece contato com suporte e captura de tela como segunda rota quando o botão não aparece.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260923-201","obs-20260923-202"],"confidence":"high"},
        observations=[
            "A pergunta preserva uma exceção real: ausência do botão ou do email esperado.",
            "A transcrição liga duas rotas nativas a um alerta de irreversibilidade.",
            "Comentários relatam gratidão e novos casos, sem constituir teste de execução.",
        ],
        interpretations=[
            "Responder a exceção junto do caminho padrão torna objeção e contingência rastreáveis.",
            "A idade da publicação impede assumir que o caminho continua funcional hoje.",
        ],
        scores={"gancho":86,"clareza":92,"relevancia":93,"desejo":77,"confianca":81,"retencao":"not_assessed","acao":83,"objecoes":92},
        lenses={
            "apressado":"Recebe problema e risco de apagar a conta.",
            "analitico":"Encontra caminho padrão e contingência, mas deve verificar a UI atual.",
            "aspiracional":"A solução promete encerrar uma pendência de conta.",
            "comunidade":"A série transforma perguntas em tutoriais.",
            "cetico":"Valoriza o alerta e exige revalidação contemporânea.",
        },
        replicable=["Formular a dúvida com sua exceção funcional.","Explicar caminho padrão e rota de suporte.","Avisar perdas irreversíveis antes da ação."],
        contingent=["Interface publicada em 2020.","Oferta comercial presente.","Resultado visual não observado."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a dúvida específica, sua exceção e sua origem são observáveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"rotas internas, risco e resultado declarado são identificáveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_13_public_comments",
        consent={"storyOrigin":"pergunta de inscrito atribuída na fala","consentStatus":"creator_attribution_but_formal_reuse_consent_not_audited","identityProtection":"nome omitido do princípio e da ficha analítica","evidence":["a fala atribui a pergunta; autorização formal não foi acessada"]},
    ),
    build_ref(
        id="obs-20260923-204",
        title="Respondendo dúvida de seguidor: como fazer silhueta no Canva 🎨",
        creator="Demétrio Jessé", identity="demetrio-jesse",
        url="https://www.youtube.com/watch?v=1Jv8S586jtE",
        published="2025-08-22", duration="PT1M24S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 1 minuto e 24 segundos",
            "transcrição automática integral em português com 35 segmentos e timestamps", "fala por substituição textual",
            "1.633 visualizações e 48 curtidas observadas", "amostra integral dos 2 comentários públicos retornados",
            "dúvida de seguidor atribuída", "passos nativos do Canva descritos", "dependência do aplicativo externo Image Blender explicitada para concluir o efeito desfocado",
        ],
        missing=MISSING_AV + ["contagem pública total de comentários", "consentimento formal do seguidor", "execução visual no Canva e no aplicativo externo", "informação de preço ou disponibilidade atual do aplicativo"],
        metrics={"viewsObserved":1633,"likesObserved":48,"commentsObserved":"not_measured"},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":45},{"family":"demonstracao","percentage":40},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="criar silhueta e efeito desfocado a partir de foto no Canva",
            segment="software e design", subsegment="efeitos de imagem no Canva com aplicativo complementar", audience="usuários do Canva que querem reproduzir efeito visual de outro vídeo",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","alivio"], hooks=["pergunta","promessa"],
            narrative=["problema","progressao","prova","conclusao","cta"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","seguir"],
            evidence=[
                "Entre 0:00 e 0:17, a fala atribui a dúvida a um seguidor de vídeo anterior.",
                "Entre 0:17 e 1:01, registra remover fundo, tornar a silhueta branca, baixar com transparência e recompor no Canva.",
                "Entre 1:01 e 1:08, exige o aplicativo externo Image Blender para o desfoque; depois retorna ao Canva.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260923-201","obs-20260923-202","obs-20260923-203"],"confidence":"high"},
        observations=[
            "Origem, problema e parte dos passos no Canva são rastreáveis.",
            "O resultado prometido não é totalmente obtido com recurso interno: a fala exige Image Blender.",
            "Dois comentários agradecem a ajuda, sem provar reprodução do resultado.",
        ],
        interpretations=[
            "É caso-limite do padrão nativo, não contraexemplo de eficácia do tutorial.",
            "Dependência externa precisa aparecer como condição da solução, não como se fosse nativa.",
        ],
        scores={"gancho":90,"clareza":91,"relevancia":89,"desejo":83,"confianca":76,"retencao":"not_assessed","acao":82,"objecoes":73},
        lenses={
            "apressado":"Recebe dúvida e efeito desejado imediatamente.",
            "analitico":"Reconstrói os passos, mas encontra dependência fora do Canva.",
            "aspiracional":"O efeito promete acabamento visual reutilizável.",
            "comunidade":"A pauta responde a uma dúvida de vídeo anterior.",
            "cetico":"Exige disclosure do aplicativo, custo, disponibilidade e resultado visual.",
        },
        replicable=["Explicitar cedo qualquer dependência externa.","Separar etapas nativas das realizadas em outro aplicativo.","Não omitir custo, disponibilidade ou compatibilidade quando conhecidos."],
        contingent=["Resultado completo depende de outro aplicativo.","Preço e disponibilidade não foram medidos.","Execução visual não observada."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"dúvida, passos e resultado declarado são reconstruíveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o resultado completo é obtido somente com recurso interno do Canva","requiredModalities":["transcript"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_2_public_comments",
        consent={"storyOrigin":"dúvida de seguidor atribuída sem identidade reproduzida","consentStatus":"creator_attribution_but_formal_reuse_consent_not_audited","identityProtection":"identidade do seguidor não reproduzida","evidence":["a fala atribui a pauta; pergunta original e autorização não foram acessadas"]},
    ),
    build_ref(
        id="obs-20260923-205",
        title="DUOLINGO & BRAWL STARS",
        creator="Duolingo Brasil 🇧🇷", identity="duolingo-brasil",
        url="https://www.youtube.com/watch?v=qF3_dV0cFTs",
        published="2026-09-17", duration="PT40S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 40 segundos",
            "transcrição automática parcial em inglês com 5 segmentos até cerca de 28,9 segundos", "fala por substituição textual parcial",
            "514.774 visualizações e 6.563 curtidas observadas", "amostra pública de 20 comentários de topo",
            "descrição da campanha com modo chefe entre 19 de setembro e 1º de outubro de 2026", "missão de sete dias no Duolingo entre 19 e 30 de setembro de 2026 e recompensas por marcos",
        ],
        missing=MISSING_AV + ["transcrição ou legenda do trecho final de cerca de 11 segundos", "contagem pública total de comentários", "mecânica audiovisual integral", "baseline de campanha", "métricas de participação e conversão"],
        metrics={"viewsObserved":514774,"likesObserved":6563,"commentsObserved":"not_measured"},
        classification=cls(
            material="video_curto", presentations=["institucional","narracao_imagens","animacao"], primary="institucional",
            secondary=["entretenimento","comunidade"],
            mix=[{"family":"institucional","percentage":40},{"family":"entretenimento","percentage":35},{"family":"comunidade","percentage":25}],
            objectives=["marca","comunidade","visualizacao","trafego"], topic="colaboração entre Duolingo e Brawl Stars com metas e recompensas cruzadas",
            segment="educação de idiomas e jogos", subsegment="campanha institucional gamificada", audience="usuários do Duolingo e jogadores de Brawl Stars",
            awareness="consciente_produto", production="complex", scale="large", replicability="low", duration="31_to_60s",
            mechanisms=["curiosidade","pertencimento","urgencia","recompensa"], hooks=["novidade","narrativo"],
            narrative=["situacao","conflito","progressao","payoff","cta"], proof=["nenhuma"], cta=["experimentar","clicar","seguir"],
            advertising="conteudo_de_marca", intent="explicita", entity={"kind":"marca","name":"Duolingo e Brawl Stars","confidence":"high"},
            evidence=[
                "A descrição pública estabelece datas, modo chefe, perguntas de idioma, metas comunitárias e recompensas.",
                "A transcrição automática retorna somente cinco segmentos até 28,9 segundos de um vídeo de 40 segundos.",
                "Um comentário individual critica excesso de estímulo para uma criança; não é evidência de efeito geral.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de campanha institucional gamificada, fora do grupo-alvo de tutoriais de interface","referenceIds":[],"confidence":"high"},
        observations=[
            "A descrição liga ações em duas plataformas a metas e recompensas datadas.",
            "A transcrição parcial contém uma pergunta em francês, resposta, piada e sons indicados, mas não cobre todo o vídeo.",
            "Comentários amostrados refletem fandom e uma objeção individual de sobrecarga visual; não são representativos.",
        ],
        interpretations=[
            "A colaboração oferece exploração futura de metas cruzadas, sem gerar hipótese neste lote.",
            "Marcas, escala, fandom e métricas não demonstram participação, retenção ou conversão.",
        ],
        scores={"gancho":88,"clareza":78,"relevancia":82,"desejo":85,"confianca":69,"retencao":"not_assessed","acao":86,"objecoes":62},
        lenses={
            "apressado":"A descrição informa campanha e janela temporal.",
            "analitico":"Entende regras textuais, mas não possui mídia nem transcrição integral.",
            "aspiracional":"Recompensas conectam prática e jogo.",
            "comunidade":"Metas coletivas coordenam duas bases de fãs.",
            "cetico":"Desconta escala, fandom e cobertura audiovisual ausente.",
        },
        replicable=["Definir janelas e marcos de participação.","Separar recompensas individuais de metas comunitárias.","Não copiar personagens, frases ou propriedade intelectual."],
        contingent=["Colaboração entre marcas e produção complexa.","Transcrição temporalmente parcial.","Audiovisual e resposta comportamental não observados."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"a descrição documenta regras, datas, metas e recompensas da campanha","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
            {"claim":"estrutura audiovisual, ritmo e arco completo foram observados","requiredModalities":["video","audio","captions"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_partial_automatic_transcript_and_20_public_comments",
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 037")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260923-201","obs-20260923-202","obs-20260923-203"]
new_case = "obs-20260923-204"
pattern["statement"] = "Em tutoriais de software ou configuração de interface, explicitar uma dúvida atribuída a um usuário, localizar o recurso interno que a resolve e demonstrar passos e resultado torna problema, caminho e resposta rastreáveis; efeitos sobre aprendizagem, retenção e participação não foram medidos."
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 9
pattern["supportingCount"] = 9
pattern["caseLimitCount"] = 3
pattern["creatorDiversityCount"] = 9
pattern["sourceDiversityCount"] = 9
pattern["conditions"] = [
    "dúvida específica com procedência explicitamente registrada",
    "problema funcional delimitado antes do passo a passo",
    "recurso padrão ou interno à interface nomeado",
    "procedimento e resultado identificáveis em evidência direta",
    "dependência externa declarada como condição, não tratada como solução nativa",
    "identidade e consentimento tratados proporcionalmente",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260923-201","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta sobre fonte padrão, origem, três rotas internas e resultado declarado aparecem na fala; o autor agradece em comentário.","evidence":"Metadados, descrição integral, transcrição automática integral e dois comentários.","limitations":["sem audiovisual, teste contemporâneo ou termo formal de autorização"]},
    {"referenceId":"obs-20260923-202","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Comentário sobre inicialização é convertido em diagnóstico, caminho interno e resultado declarado em central multimídia.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários.","limitations":["sem audiovisual, compatibilidade auditada ou teste independente"]},
    {"referenceId":"obs-20260923-203","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta sobre excluir conta é respondida com caminho interno, alerta de irreversibilidade e rota de suporte.","evidence":"Metadados, descrição integral, transcrição automática integral e treze comentários.","limitations":["interface de 2020 sem revalidação; sem audiovisual ou teste de execução"]},
    {"referenceId":"obs-20260923-204","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"O tutorial atribui a dúvida e usa Canva, mas o resultado completo depende explicitamente do aplicativo externo Image Blender.","evidence":"Metadados, descrição integral, transcrição automática integral e dois comentários.","limitations":["não é contraexemplo de eficácia; custo e disponibilidade do aplicativo não medidos"]},
])
pattern["limitations"] = [
    "Nove apoios formais vêm de nove criadores e fontes; demonstram recorrência estrutural, não eficácia.",
    "Os três novos apoios ampliam o padrão para PowerPoint, gestão de conta no Canva e configuração Android embarcada, mas dois foram publicados em 2020 e um em 2023.",
    "Nenhum audiovisual, ritmo, retenção, baseline, execução pelo espectador ou teste de compreensão foi adquirido.",
    "Atribuição pelo criador e reconhecimento público não substituem consentimento formal.",
    "O terceiro caso-limite mostra que passos internos parciais não tornam nativa uma solução cujo resultado completo exige aplicativo externo.",
    "Transcrições automáticas podem conter erros e não autorizam copiar frases ou perguntas.",
    "Ofertas, links afiliados, popularidade, escala e comentários são contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url":"https://www.youtube.com/watch?v=gE8QuCJC-3k","reason":"pergunta atribuída, porém a solução combina PowerPoint e OBS; redundante com o caso-limite de dependência externa"},
    {"url":"https://www.youtube.com/watch?v=GHozZrPVk0I","reason":"mesmo criador de um caso já selecionado e publicação com múltiplas perguntas, menos comparável ao recorte funcional único"},
    {"url":"https://www.youtube.com/watch?v=JS6QO6lH_eI","reason":"mesmo criador do apoio de PowerPoint e redundante após três fontes independentes"},
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 94,
    "referenceIds": [f"obs-20260923-{n}" for n in range(201, 206)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260923-205"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["educativo","demonstracao","comunidade","institucional","entretenimento","storytelling"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads de vídeo e consultas do player expiraram ou não expuseram stream utilizável; cinco solicitações diretas de capa retornaram HTML de 195 bytes, não imagem","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":4,"partialHumanOrCreatorProvided":0,"partialAutomatic":1,"none":0,"limitation":"quatro transcrições automáticas substituem somente a fala; a exploração institucional retorna cinco segmentos até 28,9 segundos de um vídeo de 40 segundos"},
    "commentsCoverage": {"countsOnly":0,"sampledReferences":5,"sampledComments":57,"limitation":"amostras públicas de comentários não são representativas nem teste de compreensão ou execução"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"datas, interfaces, segmentos, durações e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["uma solução deixa de ser nativa quando o resultado completo depende de aplicativo externo, mesmo que parte dos passos ocorra no software principal"],
    "safetyFindings": [
        "identidades de quem enviou perguntas foram omitidas quando desnecessárias ao princípio",
        "atribuição pública e agradecimento não foram confundidos com consentimento formal",
        "ofertas, afiliados, marca, escala e comentários permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, edição, ritmo, retenção, frase ou roteiro foi inventado",
        "a transcrição parcial da exploração não foi tratada como cobertura do vídeo completo",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes ampliam o padrão de tutoriais nativos para PowerPoint, Canva e configuração Android embarcada. O padrão passa de seis para nove apoios e de dois para três casos-limite; permanece provisório e não demonstra aprendizagem, retenção, participação ou desempenho.",
    "nextTarget": "tutorial brasileiro recente e curto de software ou interface, de criador pequeno ou médio, com audiovisual integral, pergunta anonimizada ou consentida e teste de execução ou compreensão; procurar também título que prometa recurso nativo mas exija ferramenta externa paga ou falhe por mudança de interface",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "Quatro transcrições são automáticas integrais e uma automática ficou parcial.",
        "Foram amostrados 57 comentários; a amostra não é representativa.",
        "Dois dos três apoios novos foram publicados em 2020 e não tiveram a interface atual revalidada.",
        "Não houve baseline, retenção, replay, teste de execução, compreensão ou causalidade.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
