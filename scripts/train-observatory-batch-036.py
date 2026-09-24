#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-035.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-22T11:53:00.000Z"
OBSERVED = "2026-09-22"
RUN_ID = "run-20260922-supervised-036"
PATTERN_ID = "pat-20260921-015"
BATCH_IDS = {f"obs-20260922-{n}" for n in range(196, 201)}

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


GROUP = "tutorial brasileiro de software de edição que atribui uma dúvida específica à audiência, usa recurso interno e demonstra caminho e resultado na fala"

refs = [
    build_ref(
        id="obs-20260922-196",
        title="Como fazer COLOR MATCH no Final Cut Pro! - Respondendo Inscritos Ep. 5",
        creator="Rai Damasceno", identity="rai-damasceno",
        url="https://www.youtube.com/watch?v=CEl66LU-Tj8",
        published="2023-01-17", duration="PT9M39S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 9 minutos e 39 segundos",
            "transcrição automática integral em português com 235 segmentos e timestamps", "fala por substituição textual",
            "710 visualizações, 32 curtidas e 10 comentários declarados", "amostra integral dos 10 comentários públicos retornados",
            "pergunta atribuída a inscrito na descrição e na fala", "problema de cores diferentes entre duas câmeras e duas soluções internas declaradas",
            "comentário do autor da dúvida dizendo que o vídeo o ajudou e resposta do criador",
        ],
        missing=MISSING_AV + ["termos formais de autorização", "teste independente do color match", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":710,"likesObserved":32,"commentsObserved":10},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":50},{"family":"demonstracao","percentage":35},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="igualar cores de câmeras diferentes no Final Cut Pro",
            segment="software e produção audiovisual", subsegment="cor e pós-produção no Final Cut Pro", audience="editores que trabalham com duas ou mais câmeras",
            awareness="consciente_problema", production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","confianca"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado","depoimento"], cta=["seguir","comentar","clicar"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"curso e comunidade de Final Cut Pro do canal","confidence":"high"},
            evidence=[
                "Entre 0:04 e 0:25, a fala identifica o quadro, atribui a pergunta e delimita diferenças de cor entre duas câmeras.",
                "Entre 0:34 e 0:53, promete duas rotas internas: correspondência automática e ajuste manual.",
                "A transcrição registra o resultado declarado por volta de 4:02; a execução visual não foi observada.",
                "Na amostra integral, o autor da dúvida agradece e afirma que o vídeo o ajudou; isso não é teste controlado.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260922-197","obs-20260922-198"],"confidence":"high"},
        observations=[
            "Pergunta, cenário técnico e duas opções nativas aparecem antes do desenvolvimento.",
            "Há uma inserção comercial entre a promessa e o passo a passo; retenção não foi medida.",
            "O reconhecimento público do autor melhora a procedência, mas não substitui autorização formal nem prova de aprendizagem.",
        ],
        interpretations=[
            "A resposta preserva o caso de uso e oferece alternativa automática e manual, tornando problema e caminho rastreáveis na fala.",
            "Curso, links afiliados, depoimento e métricas são contexto, não causa de confiança ou resultado.",
        ],
        scores={"gancho":89,"clareza":93,"relevancia":92,"desejo":81,"confianca":86,"retencao":"not_assessed","acao":85,"objecoes":87},
        lenses={
            "apressado":"Recebe pergunta, câmeras e problema de cor na abertura.",
            "analitico":"Encontra duas rotas e resultado declarado, mas precisa ver a tela e repetir o teste.",
            "aspiracional":"A consistência entre câmeras representa acabamento profissional.",
            "comunidade":"O autor da pergunta reconhece publicamente a resposta.",
            "cetico":"Desconta inserção comercial, relato individual e ausência de auditoria visual.",
        },
        replicable=["Atribuir a pergunta com consentimento proporcional.","Delimitar equipamento, problema e resultado.","Oferecer rota automática e manual dentro do software."],
        contingent=["O autor da dúvida é identificável no vídeo original.","A inserção comercial antecede parte da entrega.","Color match e resultado visual não foram vistos."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a pergunta específica e sua origem são observáveis em descrição, fala e comentário","requiredModalities":["description","transcript","comments"],"observedModalities":["description","transcript","comments"],"sufficient":True},
            {"claim":"duas rotas internas e o resultado declarado são identificáveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_10_public_comments",
        consent={"storyOrigin":"pergunta de inscrito atribuída no vídeo e reconhecida pelo próprio autor em comentário público","consentStatus":"public_comment_and_explicit_acknowledgment","identityProtection":"nome omitido do princípio transferível","evidence":["o autor agradece publicamente e confirma utilidade; termo formal não foi acessado"]},
    ),
    build_ref(
        id="obs-20260922-197",
        title="HITFILM EXPRESS 15: Como Fazer TRANSIÇÃO no Hitfilm (Respondendo INSCRITOS)",
        creator="Hitfilm Brasil - Edição de Vídeos", identity="hitfilm-brasil",
        url="https://www.youtube.com/watch?v=Z0EGm_CXCT8",
        published="2020-10-28", duration="PT7M11S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 7 minutos e 11 segundos",
            "transcrição automática integral em português com 159 segmentos e timestamps, com ruído lexical", "fala por substituição textual",
            "346 visualizações, 15 curtidas e 3 comentários declarados", "amostra integral dos 3 comentários públicos retornados",
            "dúvida de inscrito sobre transições atribuída na fala", "transições prontas e parâmetros internos do HitFilm nomeados na transcrição",
        ],
        missing=MISSING_AV + ["pergunta original ou identidade verificável do inscrito", "consentimento verificável", "teste independente da transição", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":346,"likesObserved":15,"commentsObserved":3},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"demonstracao","percentage":30},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","seguidores","lead"], topic="uso de transições prontas no HitFilm Express 15",
            segment="software e produção audiovisual", subsegment="edição de vídeo no HitFilm", audience="editores iniciantes que usam uma alternativa gratuita",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","alivio"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["seguir","comentar","cadastrar"],
            advertising="geracao_de_leads", intent="explicita", entity={"kind":"servico","name":"curso gratuito HitFilm Start","confidence":"high"},
            evidence=[
                "Entre 0:07 e 0:34, a fala diz responder à dúvida de um inscrito e formula como fazer transições no HitFilm.",
                "A partir de 1:08, a transcrição registra transições prontas, categorias e ajustes internos.",
                "A transcrição é integral, mas contém trocas lexicais recorrentes; nenhuma imagem de tela foi adquirida.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260922-196","obs-20260922-198"],"confidence":"high"},
        observations=[
            "A origem comunitária, o objeto da dúvida e o recurso interno são reconhecíveis apesar do ruído de transcrição.",
            "Descrição promove curso gratuito; isso é contexto comercial, não prova de aprendizagem.",
            "Três comentários foram lidos e dois agradecem a ajuda; nenhum demonstra execução da técnica.",
        ],
        interpretations=[
            "A pergunta funciona como recorte editorial para uma unidade ensinável do software.",
            "A ausência da pergunta original limita consentimento e rastreabilidade da procedência.",
        ],
        scores={"gancho":86,"clareza":84,"relevancia":89,"desejo":76,"confianca":72,"retencao":"not_assessed","acao":84,"objecoes":74},
        lenses={
            "apressado":"Reconhece inscrito, transição e software cedo.",
            "analitico":"Encontra categorias e ajustes, mas precisa da tela por causa do ruído textual.",
            "aspiracional":"A ferramenta gratuita reduz barreira de entrada.",
            "comunidade":"A aula é apresentada como resposta a inscrito.",
            "cetico":"Exige pergunta original, visual e execução própria.",
        },
        replicable=["Converter uma dúvida específica em unidade curta de software.","Nomear o caminho interno antes dos ajustes.","Manter oferta separada da evidência do tutorial."],
        contingent=["Transcrição automática particularmente ruidosa.","Pergunta e consentimento originais não foram acessados.","Resultado visual não foi observado."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala atribui uma dúvida específica a inscrito","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"recursos internos, passos e resultado declarado são reconstruíveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_but_noisy_automatic_transcript_and_3_public_comments",
        consent={"storyOrigin":"dúvida de inscrito atribuída pelo criador sem pergunta original acessível","consentStatus":"creator_attribution_but_reuse_consent_not_audited","identityProtection":"identidade do inscrito não reproduzida","evidence":["título e fala declaram resposta a inscrito; origem primária e autorização não foram acessadas"]},
    ),
    build_ref(
        id="obs-20260922-198",
        title="COMO CRIAR EFEITO ANTES E DEPOIS - Respondendo aluno",
        creator="Erick Gouma", identity="erick-gouma",
        url="https://www.youtube.com/watch?v=G0xIRJiKZbo",
        published="2022-01-17", duration="PT11M44S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 11 minutos e 44 segundos",
            "transcrição automática integral em português com 263 segmentos e timestamps", "fala por substituição textual",
            "4.089 visualizações, 237 curtidas e 8 comentários declarados", "amostra integral dos 8 comentários públicos retornados",
            "pergunta de aluno citada na abertura", "efeitos e controles internos do Adobe Premiere nomeados", "duas formas de execução e resultado declarados",
        ],
        missing=MISSING_AV + ["consentimento verificável do aluno", "pergunta original fora da citação do criador", "teste independente do efeito", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":4089,"likesObserved":237,"commentsObserved":8},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":50},{"family":"demonstracao","percentage":35},{"family":"comunidade","percentage":15}],
            objectives=["educar","confianca","lead","comentario"], topic="efeito de antes e depois no Adobe Premiere",
            segment="software e produção audiovisual", subsegment="efeitos e transições no Adobe Premiere", audience="editores que querem comparar tratamento de cor",
            awareness="consciente_problema", production="simple", scale="large", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","autoridade","reciprocidade"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["seguir","comentar","clicar","comprar"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"curso de Adobe Premiere e After Effects","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:25, a fala identifica a pergunta de aluno e delimita o efeito de antes e depois dentro do Premiere.",
                "Entre 0:28 e 1:24, registra duplicação de camada e primeiro caminho; depois apresenta efeitos de wipe e máscara.",
                "Entre 9:35 e 10:15, a fala declara as formas de construir o efeito e encaminha a conclusão.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260922-196","obs-20260922-197"],"confidence":"high"},
        observations=[
            "A pergunta é citada literalmente pelo criador e imediatamente transformada em tarefa dentro do Premiere.",
            "A transcrição preserva duas rotas com efeitos internos; o antes/depois não foi visualmente confirmado.",
            "Oito comentários foram lidos; perguntas posteriores ampliam o caso, mas não medem aprendizagem.",
        ],
        interpretations=[
            "Citar a dúvida e oferecer duas rotas torna o vínculo entre problema e solução rastreável.",
            "Curso, canal grande e elogios não comprovam eficácia, confiança ou retenção.",
        ],
        scores={"gancho":91,"clareza":94,"relevancia":92,"desejo":82,"confianca":82,"retencao":"not_assessed","acao":86,"objecoes":86},
        lenses={
            "apressado":"Recebe pergunta e resultado nos primeiros segundos.",
            "analitico":"Reconstrói duplicação, wipe, máscara e duas rotas, mas precisa ver o resultado.",
            "aspiracional":"O antes/depois ajuda a apresentar acabamento de cor.",
            "comunidade":"Uma dúvida de suporte vira aula pública.",
            "cetico":"Exige consentimento do aluno e reprodução visual independente.",
        },
        replicable=["Citar somente o necessário da dúvida e proteger identidade.","Traduzir a pergunta em tarefa dentro do software.","Oferecer mais de uma rota quando houver trade-off real."],
        contingent=["A pergunta teria vindo de ambiente de suporte de curso.","Consentimento do aluno não foi auditado.","A execução visual não foi observada."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala cita uma dúvida específica de aluno e o software-alvo","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"duas rotas, recursos internos e resultado declarado são observáveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_8_public_comments",
        consent={"storyOrigin":"pergunta atribuída a aluno de curso e citada publicamente pelo criador","consentStatus":"support_question_but_reuse_consent_not_audited","identityProtection":"nome do aluno omitido desta ficha","evidence":["a fala cita a pergunta; o canal de suporte e a autorização não foram acessados"]},
    ),
    build_ref(
        id="obs-20260922-199",
        title="Efeito de ANTES x DEPOIS, como fazer? - adobe premiere (respondendo pergunta de inscritos)",
        creator="Renan Pasqua", identity="renan-pasqua",
        url="https://www.youtube.com/watch?v=tACjCLDZp-0",
        published="2022-02-14", duration="PT1M",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 1 minuto",
            "transcrição automática integral em português com 26 segmentos e timestamps", "fala por substituição textual",
            "2.265 visualizações, 110 curtidas e 12 comentários declarados", "amostra integral dos 12 comentários públicos retornados",
            "efeito interno Crop, duplicação de faixa e keyframes descritos na fala", "descrição geral da série como respostas a perguntas recebidas",
        ],
        missing=MISSING_AV + ["pergunta individual reproduzida ou atribuída", "autor ou origem específica da dúvida", "consentimento verificável", "teste independente do efeito", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":2265,"likesObserved":110,"commentsObserved":12},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"demonstracao","percentage":35},{"family":"comunidade","percentage":10}],
            objectives=["educar","comentario","seguidores","confianca"], topic="efeito de antes e depois no Adobe Premiere",
            segment="software e produção audiovisual", subsegment="efeitos curtos no Adobe Premiere", audience="editores que querem mostrar comparação de cor",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="31_to_60s",
            mechanisms=["utilidade_pratica","aproximacao","alivio"], hooks=["problema","promessa"],
            narrative=["problema","progressao","prova","conclusao","cta"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","seguir"],
            evidence=[
                "Entre 0:00 e 0:22, a fala anuncia o efeito e registra duplicação de faixa, Alt/Option e coloração.",
                "Até 0:51, descreve Crop, keyframes e animação; depois convida novas dúvidas para vídeos futuros.",
                "A descrição diz genericamente que a série responde perguntas recebidas, mas não identifica a pergunta que originou esta publicação.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260922-196","obs-20260922-197","obs-20260922-198"],"confidence":"high"},
        observations=[
            "O vídeo ensina recurso interno, passos e resultado declarado em formato curto.",
            "Título e descrição alegam responder perguntas, mas nenhuma dúvida individual, autor ou situação original ficou observável.",
            "Um comentário diz não ter conseguido executar; outros apontam ausência do efeito ou pedem variação. Isso mapeia objeções, não prova falha geral.",
        ],
        interpretations=[
            "A série comunitária não basta para o mecanismo-alvo quando a procedência da pergunta específica desaparece.",
            "É caso-limite, não contraexemplo de eficácia ou clareza.",
        ],
        scores={"gancho":87,"clareza":86,"relevancia":83,"desejo":78,"confianca":69,"retencao":"not_assessed","acao":84,"objecoes":73},
        lenses={
            "apressado":"Recebe efeito e passos rapidamente.",
            "analitico":"Reconstrói o procedimento, mas não a origem da dúvida nem o resultado visual.",
            "aspiracional":"A varredura promete comparação elegante.",
            "comunidade":"O convite a novas perguntas é observável; a pergunta original não.",
            "cetico":"Valoriza comentários de dificuldade sem tratá-los como prova causal.",
        },
        replicable=["Distinguir convite comunitário de procedência da pauta.","Ensinar recurso e passos sem alegar pergunta específica não documentada.","Registrar objeções posteriores para uma nova versão."],
        contingent=["A descrição da série é genérica.","Comentários indicam dificuldades individuais sem representatividade.","O resultado visual não foi observado."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"recurso interno, passos e resultado declarado aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a publicação preserva uma dúvida individual e atribuída","requiredModalities":["description","transcript","comments"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_12_public_comments",
        consent={"storyOrigin":"série declarada como respostas a perguntas, sem origem individual desta pauta acessível","consentStatus":"not_measurable","identityProtection":"nenhuma identidade de terceiro reproduzida","evidence":["descrição geral da série e convite a novas dúvidas; pergunta original ausente"]},
    ),
    build_ref(
        id="obs-20260922-200",
        title="DUOLINGO ANIME: O Teste Final (Ep. 2 Dublado) | O Botão de Cancelar",
        creator="Duolingo Brasil", identity="duolingo-brasil",
        url="https://www.youtube.com/watch?v=KWee85O5VEc",
        published="2026-02-10", duration="PT2M18S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 2 minutos e 18 segundos",
            "legenda humana oficial em português do Brasil com 28 segmentos e timestamps, retornada somente até cerca de 1 minuto e 21 segundos", "fala por substituição textual parcial",
            "388.485 visualizações, 17.362 curtidas e 600 comentários declarados", "amostra pública limitada de 30 comentários",
            "recapitulação, botão de cancelar, avaliação de personagem e abertura do próximo teste presentes na legenda parcial",
        ],
        missing=MISSING_AV + ["legenda ou transcrição do trecho final de aproximadamente 57 segundos", "desfecho audiovisual integral", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":388485,"likesObserved":17362,"commentsObserved":600},
        classification=cls(
            presentations=["animacao","narracao_imagens","institucional"], primary="storytelling",
            secondary=["entretenimento","institucional"],
            mix=[{"family":"storytelling","percentage":50},{"family":"entretenimento","percentage":30},{"family":"institucional","percentage":20}],
            objectives=["marca","visualizacao","compartilhamento","retencao"], topic="segundo episódio de ficção animada sobre teste beta no Duolingo",
            segment="educação de idiomas e entretenimento de marca", subsegment="anime institucional seriado", audience="usuários do Duolingo e fãs de animação",
            awareness="consciente_produto", production="complex", scale="large", replicability="low", duration="over_60s",
            mechanisms=["curiosidade","tensao","pertencimento","antecipacao"], hooks=["narrativo","conflito"],
            narrative=["continuidade_serial","situacao","conflito","virada","risco"], proof=["nenhuma"], cta=["clicar","seguir","proxima_parte"],
            advertising="conteudo_de_marca", intent="explicita", entity={"kind":"marca","name":"Duolingo","confidence":"high"},
            evidence=[
                "A descrição identifica o segundo episódio e promove o curso de japonês.",
                "Entre 0:00 e 0:14, a legenda oficial recapitula o episódio anterior e apresenta a alternativa de cancelar a lição.",
                "Até 1:21, registra consequência, avaliação e abertura do próximo teste; a cobertura textual não alcança o final de 2:18.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de storytelling animado de marca, fora do grupo-alvo de tutoriais de software","referenceIds":[],"confidence":"high"},
        observations=[
            "A legenda oficial parcial permite reconstruir recapitulação, regra e progressão inicial.",
            "Nenhum quadro ou áudio foi adquirido e o trecho final permanece ausente.",
            "Comentários amostrados citam falas e momentos visuais, mas não substituem observação audiovisual.",
        ],
        interpretations=[
            "A recapitulação serial por consequência merece exploração futura, sem gerar hipótese neste lote.",
            "Marca, escala e fandom não provam retenção, compreensão ou conversão.",
        ],
        scores={"gancho":90,"clareza":85,"relevancia":82,"desejo":84,"confianca":72,"retencao":"not_assessed","acao":68,"objecoes":61},
        lenses={
            "apressado":"Recebe recapitulação e novo conflito na legenda inicial.",
            "analitico":"Entende a regra parcial, mas não possui o trecho final nem o visual.",
            "aspiracional":"A lição é convertida em desafio ficcional.",
            "comunidade":"Comentários mostram reconhecimento de personagens, sem representatividade.",
            "cetico":"Desconta campanha de marca, cobertura parcial e ausência de cenas.",
        },
        replicable=["Recapitular somente a consequência necessária ao novo episódio.","Converter regra de produto em conflito abstrato.","Não copiar personagens, falas ou propriedade intelectual."],
        contingent=["Anime e personagens da marca não são diretamente replicáveis.","A legenda oficial ficou temporalmente parcial.","Nenhuma cena, voz ou montagem foi observada."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"descrição e legenda parcial estabelecem posição serial, regra e progressão inicial","requiredModalities":["description","captions"],"observedModalities":["description","captions"],"sufficient":True},
            {"claim":"o arco e o desfecho completos foram observados","requiredModalities":["video","captions"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_partial_official_human_ptbr_captions_and_30_of_600_public_comments",
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 036")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260922-196","obs-20260922-197","obs-20260922-198"]
new_case = "obs-20260922-199"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 6
pattern["supportingCount"] = 6
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["conditions"] = [
    "dúvida específica com procedência explicitamente registrada",
    "problema funcional delimitado antes do passo a passo",
    "recurso padrão ou interno ao software nomeado",
    "procedimento e resultado identificáveis em evidência direta",
    "identidade e consentimento tratados proporcionalmente",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260922-196","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta sobre color match, cenário técnico, duas rotas internas e resultado declarado aparecem em descrição e fala; o autor reconhece a resposta em comentário.","evidence":"Metadados, descrição integral, transcrição automática integral e dez comentários.","limitations":["sem audiovisual, teste independente ou termo formal de autorização"]},
    {"referenceId":"obs-20260922-197","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Dúvida de inscrito sobre transições é convertida em categorias e ajustes internos do HitFilm.","evidence":"Metadados, descrição integral, transcrição automática integral e três comentários.","limitations":["transcrição ruidosa; pergunta original e consentimento ausentes"]},
    {"referenceId":"obs-20260922-198","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta de aluno é citada e respondida com duas rotas e recursos internos do Premiere.","evidence":"Metadados, descrição integral, transcrição automática integral e oito comentários.","limitations":["sem audiovisual, consentimento auditado ou teste de execução"]},
    {"referenceId":"obs-20260922-199","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"O tutorial entrega recurso e passos, mas apenas a série, não a pauta individual, é atribuída a perguntas da audiência.","evidence":"Metadados, descrição integral, transcrição automática integral e doze comentários.","limitations":["não é contraexemplo de desempenho"]},
])
pattern["limitations"] = [
    "Seis apoios formais vêm de seis criadores e fontes; demonstram recorrência estrutural, não eficácia.",
    "Os três novos apoios expandem o padrão do Excel para Final Cut, HitFilm e Adobe Premiere, mas todos são tutoriais de edição publicados entre 2020 e 2023.",
    "Nenhum audiovisual, ritmo, retenção, baseline, execução pelo espectador ou teste de compreensão foi adquirido.",
    "Atribuição pelo criador não substitui acesso à pergunta original ou consentimento formal; um apoio possui reconhecimento público do autor.",
    "O segundo caso-limite mostra que uma série de respostas e um tutorial completo não preservam necessariamente a procedência da pauta individual.",
    "Transcrições automáticas podem conter erros, especialmente no apoio de HitFilm, e não autorizam copiar frases ou perguntas.",
    "Ofertas, links afiliados, popularidade, escala e comentários são contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("Ln9xIVUQrrc", "pergunta atribuída, porém a solução depende de serviço externo e não atende com clareza ao recurso interno do padrão"),
        ("CQacAGmLaaU", "mesmo criador de apoio selecionado e formato mais longo; não acrescenta independência"),
        ("-OPubC3P_Hc", "mesmo criador de outro apoio e redundante após três fontes independentes"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 355,
    "referenceIds": [f"obs-20260922-{n}" for n in range(196, 201)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260922-200"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["educativo","demonstracao","comunidade","storytelling","entretenimento","institucional"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"cinco downloads de mídia ficaram presos em timeout da página do YouTube; cinco tentativas diretas de capa expiraram após 25 segundos","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":4,"partialHumanOrCreatorProvided":1,"partialAutomatic":0,"none":0,"limitation":"quatro transcrições automáticas substituem somente a fala; a legenda humana oficial da exploração cobre 28 segmentos até cerca de 1:21 de um vídeo de 2:18"},
    "commentsCoverage": {"countsOnly":0,"sampledReferences":5,"sampledComments":63,"limitation":"a exploração foi limitada a 30 de 600 comentários; amostras públicas não são representativas nem teste de compreensão"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"datas, canais, softwares, durações e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["uma série declarada como resposta a inscritos não preserva procedência quando a pergunta individual e sua situação não aparecem"],
    "safetyFindings": [
        "nomes de quem enviou perguntas foram omitidos quando desnecessários ao princípio",
        "atribuição do criador e reconhecimento público não foram confundidos com consentimento formal",
        "ofertas, links afiliados, marca, escala e comentários permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, edição, ritmo, retenção, frase ou roteiro foi inventado",
        "a legenda parcial do anime não foi tratada como cobertura do arco completo",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes expandem o padrão de Excel para Final Cut, HitFilm e Premiere. O padrão passa de três para seis apoios e de um para dois casos-limite; permanece provisório e não demonstra aprendizagem, retenção, participação ou desempenho.",
    "nextTarget": "tutorial brasileiro recente e curto de software fora de planilhas e edição, de criador pequeno ou médio, com audiovisual integral, pergunta anonimizada ou consentida e teste de execução ou compreensão; procurar também caso em que a resposta exija ferramenta externa paga",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "Quatro transcrições são automáticas; uma delas é ruidosa e a legenda humana da exploração ficou parcial.",
        "Foram amostrados 63 comentários; a amostra não é representativa.",
        "Os três apoios novos são antigos e restritos a software de edição.",
        "Não houve baseline, retenção, replay, teste de execução, compreensão ou causalidade.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
