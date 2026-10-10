#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-039.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-28T11:35:00.000Z"
OBSERVED = "2026-09-28"
RUN_ID = "run-20260928-supervised-040"
PATTERN_ID = "pat-20260823-003"
BATCH_IDS = {f"obs-20260928-{n}" for n in range(216, 221)}

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
              contingent, role, evidence_level, eligible, claims, source_type):
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
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "conteúdo editorial público do próprio canal",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado identificável de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frase, personagem, promessa, produto ou roteiro",
        "tratar prazo fixo, mentalidade, autoridade percebida ou comentário como prova de resultado financeiro",
        "prescrever estratégia financeira individual sem renda, dívida, juros, risco e capacidade de pagamento",
        "tratar visualizações, fama, escala, produção ou venda de material como causa de desempenho",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
    ]
    return item


GROUP = "educação financeira brasileira para iniciantes que nomeia desorganização ou falta de clareza e oferece um caminho finito e executável"

refs = [
    build_ref(
        id="obs-20260928-216",
        title="Como organizar a VIDA FINANCEIRA do zero",
        creator="Gabi Teixeira", identity="gabi-teixeira",
        url="https://www.youtube.com/watch?v=dzmjIW_jBNA",
        published="2025-07-10", duration="PT10M58S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 10 minutos e 58 segundos",
            "transcrição automática integral em português com 259 segmentos e timestamps", "fala por substituição textual",
            "64.129 visualizações, 3.299 curtidas e 73 comentários públicos indicados", "amostra pública de 20 comentários",
            "problema de desorganização ou endividamento explicitado na abertura",
            "três passos falados: levantar saídas, categorizar e somar, depois cortar, centralizar e repetir",
            "oferta de planner próprio e links comerciais na descrição",
        ],
        missing=MISSING_AV + ["baseline comparável", "teste de compreensão", "resultado financeiro dos espectadores", "disclosure detalhado dos links comerciais"],
        metrics={"viewsObserved":64129,"likesObserved":3299,"commentsObserved":73},
        classification=cls(
            material="video_longo", presentations=["camera_direta","tutorial"], primary="educativo",
            secondary=["explicativo","oferta_direta"],
            mix=[{"family":"educativo","percentage":55},{"family":"explicativo","percentage":30},{"family":"oferta_direta","percentage":15}],
            objectives=["educar","consciencia_problema","apresentar_solucao","trafego"],
            topic="organização financeira do zero", segment="finanças pessoais", subsegment="controle de gastos para iniciantes",
            audience="adultos desorganizados, endividados ou sem clareza sobre gastos", awareness="consciente_problema",
            production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["aproximacao","alivio","confianca"], hooks=["problema","numero","promessa"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","tratamento_objecao"],
            cta=["clicar","outro_conteudo"], advertising="oferta_direta", intent="explicita",
            entity={"kind":"produto","name":"Combo Vida em Ordem","confidence":"high"},
            evidence=[
                "A fala promete três passos e os executa em sequência verificável.",
                "O caminho parte de extratos e faturas, passa por categorias e termina em cortes e repetição mensal.",
                "Vinte comentários foram amostrados; relatos de utilidade ou dificuldade não medem resultado financeiro.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20260928-217","obs-20260928-218"],"confidence":"high"},
        observations=[
            "A abertura nomeia falta de direção, cartão no limite, dívidas e ausência de sobra antes de oferecer três passos.",
            "Cada passo produz uma tarefa observável na fala, do levantamento ao compromisso de repetir no mês seguinte.",
            "A oferta do planner vem depois do método; sua utilidade comercial e conversão não foram medidas.",
        ],
        interpretations=[
            "Problema concreto e sequência finita tornam o caminho rastreável para iniciantes.",
            "Produto próprio, métricas e comentários são contexto, não prova de aprendizagem ou eficácia.",
        ],
        scores={"gancho":91,"clareza":95,"relevancia":93,"desejo":77,"confianca":80,"retencao":"not_assessed","acao":92,"objecoes":82},
        lenses={
            "apressado":"Entende cedo o problema e a promessa de três passos.",
            "analitico":"Encontra tarefas concretas, mas não resultado ou adequação individual.",
            "aspiracional":"Visualiza controle e decisões mais conscientes.",
            "comunidade":"Comentários trazem relatos e dúvidas sem representatividade.",
            "cetico":"Separa o método da venda do planner e exige prova de resultado.",
        },
        replicable=["Nomear o problema financeiro antes da explicação.","Anunciar uma sequência curta e executar cada etapa.","Transformar cada passo em tarefa verificável."],
        contingent=["A adequação financeira individual não foi testada.","A oferta de produto e links comerciais exige transparência.","Audiovisual, ritmo, retenção e resultado permaneceram não mensurados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"problema concreto e caminho organizado em três passos aparecem publicamente","requiredModalities":["metadata","description","transcript"],"observedModalities":["metadata","description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
    build_ref(
        id="obs-20260928-217",
        title="Organizar Suas Finanças é FÁCIL, Na Verdade (Guia Completo para Iniciantes)",
        creator="Larissa Quintanilha", identity="larissa-quintanilha",
        url="https://www.youtube.com/watch?v=FfJRuxVqqvQ",
        published="2025-08-31", duration="PT27M37S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 27 minutos e 37 segundos",
            "transcrição automática integral em português com 817 segmentos e timestamps", "fala por substituição textual",
            "66.951 visualizações, 3.088 curtidas e 40 comentários públicos indicados", "amostra pública de 20 comentários",
            "problema de contas, gasto e falta de sobra explicitado",
            "quatro blocos falados: raio X, metas, organização cotidiana e mentalidade",
            "oferta de planner próprio no comentário fixado e na fala",
        ],
        missing=MISSING_AV + ["baseline comparável", "teste de compreensão", "resultado financeiro dos espectadores", "adequação individual das recomendações"],
        metrics={"viewsObserved":66951,"likesObserved":3088,"commentsObserved":40},
        classification=cls(
            material="video_longo", presentations=["camera_direta","tutorial"], primary="educativo",
            secondary=["explicativo","inspiracao"],
            mix=[{"family":"educativo","percentage":55},{"family":"explicativo","percentage":30},{"family":"inspiracao","percentage":15}],
            objectives=["educar","consciencia_problema","apresentar_solucao","trafego"],
            topic="guia completo de organização financeira", segment="finanças pessoais", subsegment="planejamento para iniciantes",
            audience="adultos iniciantes que perdem controle das contas e metas", awareness="consciente_problema",
            production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["aproximacao","alivio","desejo","confianca"], hooks=["problema","promessa","identificacao"],
            narrative=["situacao","problema","progressao","mecanismo","cta"], proof=["mecanismo_explicado","tratamento_objecao"],
            cta=["clicar","seguir"], advertising="oferta_direta", intent="explicita",
            entity={"kind":"produto","name":"Planner Your Success","confidence":"high"},
            evidence=[
                "A fala parte do descontrole mensal e declara um guia para iniciantes.",
                "Raio X, metas, rotina e mentalidade formam quatro blocos ordenados com exemplos.",
                "Um comentário questiona a venda do planner; isso registra objeção, não invalida o método.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260928-216","obs-20260928-218"],"confidence":"high"},
        observations=[
            "O vídeo nomeia a sensação de descontrole e reconstrói o caminho por quatro blocos falados.",
            "Exemplos ligam gastos, causas, metas e ajustes, mas algumas recomendações exigem adequação ao perfil.",
            "A extensão de 27 minutos reduz comparabilidade de duração sem impedir a comparação funcional.",
        ],
        interpretations=[
            "Um mapa explícito sustenta rastreabilidade mesmo em conteúdo longo.",
            "Experiência pessoal e produto próprio não substituem teste de compreensão ou resultado.",
        ],
        scores={"gancho":89,"clareza":92,"relevancia":91,"desejo":79,"confianca":76,"retencao":"not_assessed","acao":88,"objecoes":75},
        lenses={
            "apressado":"Entende o problema e a promessa, mas enfrenta uma entrega longa.",
            "analitico":"Encontra mapa e exemplos; pede adequação das recomendações ao perfil.",
            "aspiracional":"Vê metas e controle de longo prazo.",
            "comunidade":"Comentários incluem identificação, elogios e objeção comercial.",
            "cetico":"Questiona universalização e a venda do planner sem prova de eficácia.",
        },
        replicable=["Abrir com uma situação cotidiana reconhecível.","Organizar um guia longo em blocos nomeados.","Vincular exemplos a causas e próximos passos."],
        contingent=["Duração e produto próprio alteram a experiência.","Recomendações financeiras exigem adequação individual.","Audiovisual, ritmo, retenção e resultado permaneceram não mensurados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"problema de descontrole e caminho organizado em quatro blocos aparecem na fala","requiredModalities":["metadata","transcript"],"observedModalities":["metadata","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
    build_ref(
        id="obs-20260928-218",
        title="Como fazer Controle Financeiro Pessoal no Caderno?",
        creator="Ju Oliveira Finanças", identity="ju-oliveira-financas",
        url="https://www.youtube.com/watch?v=vSalOkoX9G8",
        published="2022-07-05", duration="PT5M5S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 5 minutos e 5 segundos",
            "transcrição automática integral em português com 91 segmentos e timestamps", "fala por substituição textual",
            "174.942 visualizações, 8.218 curtidas e 221 comentários públicos indicados", "amostra pública de 20 comentários",
            "procedimento falado de controle em caderno com receitas, despesas fixas, despesas variáveis, reserva e movimentações",
            "links afiliados de livros na descrição",
        ],
        missing=MISSING_AV + ["execução visual do caderno", "legibilidade do modelo", "baseline comparável", "teste de execução", "resultado financeiro dos espectadores"],
        metrics={"viewsObserved":174942,"likesObserved":8218,"commentsObserved":221},
        classification=cls(
            material="video_longo", presentations=["tutorial","demonstracao"], primary="educativo",
            secondary=["demonstracao","explicativo"],
            mix=[{"family":"educativo","percentage":50},{"family":"demonstracao","percentage":30},{"family":"explicativo","percentage":20}],
            objectives=["educar","apresentar_solucao","salvamento","seguidores"],
            topic="controle financeiro manual no caderno", segment="finanças pessoais", subsegment="registro de orçamento para iniciantes",
            audience="pessoas que preferem papel a planilha ou aplicativo", awareness="consciente_solucao",
            production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["aproximacao","alivio","confianca"], hooks=["pergunta","problema"],
            narrative=["problema","mecanismo","progressao","conclusao"], proof=["mecanismo_explicado"],
            cta=["seguir"], advertising="publicidade_nativa", intent="implicita",
            entity={"kind":"produto","name":"livros afiliados na descrição","confidence":"high"},
            evidence=[
                "A fala apresenta um método para quem não gosta de planilhas ou aplicativos.",
                "Receitas, categorias de despesas, reserva e movimentações são preenchidas em ordem verbal.",
                "A demonstração visual e a legibilidade não puderam ser confirmadas.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260928-216","obs-20260928-217"],"confidence":"high"},
        observations=[
            "A objeção a planilhas e aplicativos é convertida em caminho manual de baixa barreira.",
            "O procedimento falado organiza entradas, saídas, reserva e saldo.",
            "Comentários descrevem adoção e facilidade, mas não constituem teste representativo de execução.",
        ],
        interpretations=[
            "Uma alternativa de baixo custo pode tornar o caminho mais executável para o público que prefere papel.",
            "Sem a imagem, não se ensina layout, legibilidade ou resultado visual.",
        ],
        scores={"gancho":84,"clareza":91,"relevancia":88,"desejo":66,"confianca":75,"retencao":"not_assessed","acao":88,"objecoes":80},
        lenses={
            "apressado":"Entende a solução manual rapidamente.",
            "analitico":"Recebe categorias e cálculo, mas não vê o modelo.",
            "aspiracional":"Visualiza controle simples e acessível.",
            "comunidade":"Comentários relatam preferência por caderno e intenção de uso.",
            "cetico":"Não confunde relatos com resultado e pede a execução visual.",
        },
        replicable=["Começar por uma objeção concreta à ferramenta comum.","Oferecer alternativa barata e acessível.","Ordenar os campos antes de calcular o saldo."],
        contingent=["A execução visual não foi observada.","Links afiliados são contexto comercial.","Retenção, adesão e resultado financeiro não foram medidos."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"problema de ferramenta e caminho manual organizado aparecem na fala","requiredModalities":["metadata","description","transcript"],"observedModalities":["metadata","description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
    build_ref(
        id="obs-20260928-219",
        title="90 DIAS SEM DÍVIDAS Plano Passo a Passo – Napoleon Hill",
        creator="Segredos de Napoleon Hill", identity="segredos-de-napoleon-hill",
        url="https://www.youtube.com/watch?v=OUeMneVcI9o",
        published="2025-06-13", duration="PT23M31S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 23 minutos e 31 segundos",
            "transcrição automática integral em português com 518 segmentos e timestamps", "fala por substituição textual",
            "1.358 visualizações, 55 curtidas e 9 comentários públicos", "todos os 9 comentários públicos amostrados",
            "cinco princípios falados: diagnóstico, cortes, renda extra, foco em uma dívida e missão pessoal",
            "promessa reiterada de eliminação das dívidas em 90 dias", "atribuições a Napoleon Hill sem obra, página ou fonte identificada",
        ],
        missing=MISSING_AV + ["autor ou especialista financeiro identificável", "fonte primária das atribuições", "baseline de renda, dívida e juros", "teste de resultado em 90 dias", "adequação individual"],
        metrics={"viewsObserved":1358,"likesObserved":55,"commentsObserved":9},
        classification=cls(
            material="video_longo", presentations=["narracao_imagens","comentario"], primary="inspiracao",
            secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"inspiracao","percentage":45},{"family":"educativo","percentage":35},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["consciencia_problema","educar","comentario","seguidores"],
            topic="eliminação de dívidas em 90 dias", segment="finanças pessoais", subsegment="dívidas e motivação financeira",
            audience="pessoas endividadas buscando plano e motivação", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["aversao_perda","urgencia","desejo","medo"], hooks=["urgencia","promessa","autoridade"],
            narrative=["problema","progressao","promessa","cta"], proof=["autoridade_percebida","alegacao_sem_prova"],
            cta=["comentar","seguir","compartilhar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"medium"},
            evidence=[
                "A fala oferece cinco passos e calcula um exemplo, mas mantém prazo fixo para situações distintas.",
                "O método é chamado de testado e universal sem baseline, coorte ou evidência de resultado.",
                "Os nove comentários são declarações de intenção; nenhum comprova quitação em 90 dias.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260928-216","obs-20260928-217","obs-20260928-218"],"confidence":"high"},
        observations=[
            "Problema e caminho finito estão presentes, mas o prazo de 90 dias independe da relação entre dívida, juros, renda e despesas.",
            "A fala promete funcionamento e atribui princípios a Napoleon Hill sem fonte rastreável.",
            "Comentários repetem a declaração proposta pelo CTA, sem evidência posterior de resultado.",
        ],
        interpretations=[
            "É caso-limite: organização existe, porém universalidade, autoridade não rastreada e prazo rígido elevam o ônus de prova.",
            "Não é contraexemplo de eficácia, porque não há resultado comparável nem teste de 90 dias.",
        ],
        scores={"gancho":96,"clareza":84,"relevancia":90,"desejo":88,"confianca":34,"retencao":"not_assessed","acao":85,"objecoes":32},
        lenses={
            "apressado":"Entende prazo e promessa imediatamente.",
            "analitico":"Questiona viabilidade, atribuição e ausência de baseline.",
            "aspiracional":"É atraído pela liberdade total em 90 dias.",
            "comunidade":"Vê declarações públicas induzidas pelo CTA, não resultados.",
            "cetico":"Rejeita universalidade e autoridade sem fonte.",
        },
        replicable=["Estruturar diagnóstico, cortes e priorização.","Recapitular o plano em lista finita.","Transformar intenção em tarefa imediata."],
        contingent=["Prazo de 90 dias não é proporcional ao baseline.","Atribuições e eficácia não têm fonte rastreável.","Audiovisual, retenção, execução e resultado não foram medidos."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"problema e caminho organizado em cinco passos aparecem na fala","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"o plano elimina dívidas em 90 dias independentemente do caso","requiredModalities":["baseline","intervention","outcome","comparison"],"observedModalities":[],"sufficient":False},
            {"claim":"as atribuições a Napoleon Hill estão documentadas","requiredModalities":["primary_source"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_9_public_comments",
    ),
    build_ref(
        id="obs-20260928-220",
        title="Minuto Ciência - Como extrair DNA do morango (Episódio 10)",
        creator="AgDC - IBB", identity="agdc-ibb",
        url="https://www.youtube.com/watch?v=1w5u0XIGydI",
        published="2019-05-21", duration="PT2M58S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 2 minutos e 58 segundos",
            "transcrição automática integral em português com 61 segmentos e timestamps", "fala por substituição textual",
            "106.653 visualizações, 3.641 curtidas e 112 comentários públicos indicados", "amostra pública de 20 comentários",
            "materiais e etapas falados: morango, água, detergente, sal, filtragem e álcool",
            "mecanismo de cada etapa explicado na descrição e autoria institucional identificada",
        ],
        missing=MISSING_AV + ["execução visual do procedimento", "resultado visual dos fios", "aviso de segurança sobre álcool e produtos de limpeza", "teste de compreensão", "revisão contemporânea do protocolo"],
        metrics={"viewsObserved":106653,"likesObserved":3641,"commentsObserved":112},
        classification=cls(
            material="video_curto", presentations=["demonstracao","dialogo","institucional"], primary="demonstracao",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":35},{"family":"curiosidade","percentage":15}],
            objectives=["educar","visualizacao","salvamento","compartilhamento"],
            topic="extração caseira de DNA do morango", segment="educação científica", subsegment="biologia experimental",
            audience="estudantes, professores e famílias interessadas em experimento de DNA", awareness="consciente_solucao",
            production="intermediate", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","surpresa","recompensa","confianca"], hooks=["pergunta","demonstracao_antecipada","resultado_antecipado"],
            narrative=["promessa","progressao","payoff","cta"], proof=["fonte","mecanismo_explicado","autoridade_demonstrada"],
            cta=["comentar","seguir"], advertising="institucional", intent="implicita",
            entity={"kind":"marca","name":"Instituto de Biociências de Botucatu","confidence":"high"},
            evidence=[
                "A fala lista materiais, passos e resultado declarado.",
                "A descrição explica ruptura de membrana, neutralização e precipitação.",
                "Um comentário pede mecanismo; a descrição o oferece, mas não houve teste de compreensão.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de demonstração científica doméstica","referenceIds":[],"confidence":"low"},
        observations=[
            "Procedimento e mecanismo estão rastreáveis em fala e descrição.",
            "O resultado visual e a execução não foram observados, portanto a demonstração não é ensinada como audiovisual confirmado.",
            "A publicação não apresenta aviso de segurança acessível para álcool e detergente.",
        ],
        interpretations=[
            "A exploração mostra alinhamento entre procedimento falado e explicação escrita, sem provar compreensão ou segurança operacional.",
            "Uma única referência não gera hipótese nova.",
        ],
        scores={"gancho":87,"clareza":92,"relevancia":89,"desejo":72,"confianca":83,"retencao":"not_assessed","acao":76,"objecoes":70},
        lenses={
            "apressado":"Recebe experimento e resultado prometido cedo.",
            "analitico":"Encontra mecanismo na descrição, mas não a execução visual.",
            "aspiracional":"Visualiza uma atividade científica acessível.",
            "comunidade":"Comentários relatam uso em aula sem teste representativo.",
            "cetico":"Exige confirmação visual e orientação de segurança.",
        },
        replicable=["Listar materiais e passos na fala.","Usar a descrição para explicar o mecanismo.","Vincular resultado declarado a um conceito científico."],
        contingent=["Execução e resultado visuais não foram confirmados.","Segurança operacional não foi documentada.","Popularidade e uso relatado em aula não provam compreensão."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"materiais, passos e mecanismo aparecem na fala e descrição","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"a execução e o resultado visual funcionam como demonstrados","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
            {"claim":"o procedimento é seguro para execução sem supervisão","requiredModalities":["safety_guidance","expert_review"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 040")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260928-216", "obs-20260928-217", "obs-20260928-218"]
new_case = "obs-20260928-219"
pattern["statement"] = "Em educação financeira para iniciantes, nomear um problema concreto e organizar a resposta em etapas finitas torna problema, caminho e próxima ação identificáveis; prazos fixos ou promessas universais sem renda, dívida, juros e viabilidade elevam o ônus de prova, e efeitos sobre compreensão, relevância e resultado permanecem não medidos."
pattern["name"] = pattern["statement"]
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 11
pattern["supportingCount"] = 11
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 11
pattern["sourceDiversityCount"] = 11
pattern["conditions"] = [
    "conteúdo educativo de finanças pessoais para iniciantes",
    "problema financeiro concreto identificado",
    "caminho organizado em etapas finitas",
    "ações executáveis compatíveis com o escopo declarado",
    "promessas proporcionais ao baseline e sem universalidade não demonstrada",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260928-216","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Desorganização, dívida e ausência de sobra antecedem três passos executáveis de levantamento, categorização e faxina.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários amostrados.","limitations":["sem audiovisual, teste de compreensão ou resultado financeiro"]},
    {"referenceId":"obs-20260928-217","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"O descontrole mensal é reorganizado em raio X, metas, rotina e mentalidade, com exemplos falados.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários amostrados.","limitations":["duração longa, produto próprio e recomendações sem adequação individual testada"]},
    {"referenceId":"obs-20260928-218","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"A objeção a planilhas é resolvida por um caminho manual de receitas, despesas, reserva, movimentos e saldo.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários amostrados.","limitations":["sem execução visual, teste de uso ou resultado"]},
    {"referenceId":"obs-20260928-219","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Há problema e cinco passos, mas prazo fixo de 90 dias, universalidade e autoridade sem fonte excedem a evidência acessível.","evidence":"Metadados, descrição integral, transcrição automática integral e nove comentários.","limitations":["não conta como apoio nem como contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Onze apoios vêm de onze criadores e onze fontes; demonstram recorrência estrutural, não compreensão, relevância percebida ou resultado financeiro.",
    "Nenhuma referência oferece retenção, teste de compreensão, baseline individual ou experimento causal.",
    "Comentários, métricas, fama, escala e venda de material permanecem contexto não causal.",
    "O novo caso-limite reforça que sequência organizada não compensa prazo universal e autoridade não rastreada.",
    "Conselhos financeiros exigem adequação a renda, despesas, dívida, juros, risco e capacidade de pagamento.",
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 49,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260928-220"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=xIIa3A3kY-k","reason":"mesma criadora de um apoio selecionado; a diversidade de fontes teve prioridade"},
        {"url":"https://www.youtube.com/watch?v=in0XbfQEm2A","reason":"criador de grande escala; três apoios de produção mais acessível foram priorizados"},
        {"url":"https://www.youtube.com/watch?v=rilMuvFaIEQ","reason":"título agressivo, porém caso-limite menos nítido que a promessa fixa de 90 dias selecionada"},
        {"url":"https://www.youtube.com/watch?v=D9HDgpvY5-Y","reason":"URL já presente na memória"},
        {"url":"https://www.youtube.com/watch?v=BTPmIFV1q0U","reason":"publicação indisponível na verificação de cobertura"},
        {"url":"https://www.youtube.com/watch?v=FCRJcWRj5Xg","reason":"publicação indisponível na verificação de cobertura"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 5,
    "replicableReferences": 5,
    "creativeFamiliesObserved": ["educativo","explicativo","oferta_direta","inspiracao","demonstracao","autoridade_opiniao","curiosidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "para as cinco URLs, as amostras de vídeo falharam como dados inválidos e as capas retornaram HTML de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":5,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":0,
        "limitation":"transcrições automáticas substituem somente a fala; não sustentam cenas, voz, texto na tela ou ritmo",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":5,
        "sampledComments":89,
        "zeroReturnedReferences":0,
        "limitation":"comentários públicos não são amostra representativa nem teste de compreensão, execução ou resultado financeiro",
    },
    "baselineCoverage": {
        "sampledProfiles":0,
        "contemporaneousBaselines":0,
        "limitation":"datas, durações, escalas e ofertas diferentes impedem benchmark causal de desempenho",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["um caminho organizado não sustenta prazo universal quando renda, dívida, juros, despesas e capacidade de pagamento não são medidos"],
    "safetyFindings": [
        "nenhuma recomendação financeira foi tratada como adequada a todo perfil",
        "prazo, mentalidade, comentários, autoridade percebida e métricas não foram tratados como prova de resultado",
        "o experimento científico não foi ensinado como execução visual confirmada ou procedimento seguro sem supervisão",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes elevam de oito para onze os apoios do padrão de educação financeira para iniciantes. Um caso-limite mostra que um plano em etapas não torna proporcional uma promessa de quitação em 90 dias. O padrão permanece provisório.",
    "nextTarget": "explicador financeiro brasileiro recente e curto, de criador pequeno ou médio, com audiovisual integral, caminho finito, premissas de renda, dívida e juros visíveis e teste de execução ou compreensão; buscar também um caso em que os passos contradigam o próprio baseline",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "As cinco transcrições são automáticas integrais.",
        "Foram amostrados 89 comentários; a amostra não é representativa.",
        "Não houve baseline contemporâneo, retenção, teste de compreensão, adequação financeira individual ou causalidade.",
        "O resultado do experimento científico e sua segurança operacional não foram confirmados visualmente.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
