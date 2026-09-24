#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Rebuild the last approved checkpoint and reuse its schema helpers.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-033.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-20T11:16:12.000Z"
OBSERVED = "2026-09-20"
RUN_ID = "run-20260920-supervised-034"
PATTERN_ID = "pat-20260913-013"
BATCH_IDS = {f"obs-20260920-{n}" for n in range(186, 191)}

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
        "copiar frases, personagens, desafios, episódios ou roteiro",
        "tratar posição na série, fama, métricas, publicidade ou orçamento como prova causal",
        "inferir cena, áudio, texto na tela, atuação, edição, ritmo ou retenção sem mídia reproduzida",
        "confundir recapitulação estrutural com compreensão ou desempenho comprovados",
    ]
    return item


refs = [
    build_ref(
        id="obs-20260920-186",
        title="DESAFIO 30 DIAS SPINS MICRO: Episódio 2",
        creator="Spins Brasil Poker", identity="spins-brasil-poker",
        url="https://www.youtube.com/watch?v=MUTaGV4YykI",
        published="2025-09-29", duration="PT7M41S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 7 minutos e 41 segundos",
            "transcrição automática integral em português com 174 segmentos e timestamps", "fala por substituição textual",
            "352 visualizações, 21 curtidas e 3 comentários declarados", "amostra integral dos 3 comentários públicos retornados",
            "meta de 30 dias, posição de segundo episódio, saldo inicial e objetivo final declarados na fala",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "resultado final do desafio", "auditoria das transações e vínculos afiliados"],
        metrics={"viewsObserved":352,"likesObserved":21,"commentsObserved":3},
        classification=cls(
            presentations=["camera_direta","tela_gravada","desafio"], primary="storytelling",
            secondary=["educativo","demonstracao"],
            mix=[{"family":"storytelling","percentage":50},{"family":"educativo","percentage":30},{"family":"demonstracao","percentage":20}],
            objectives=["visualizacao","educar","comunidade","lead"], topic="desafio de 30 dias jogando torneios de poker de baixo valor",
            segment="poker e entretenimento", subsegment="desafio serial documentado", audience="jogadores iniciantes interessados em acompanhar banca e volume",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["antecipacao","tensao","utilidade_pratica","pertencimento"], hooks=["numero","narrativo","promessa"],
            narrative=["situacao","promessa","progressao","risco","continuidade_serial","cta"], proof=["evidencia_documental","mecanismo_explicado"], cta=["seguir","comentar","clicar","proxima_parte"],
            advertising="conteudo_de_marca", intent="explicita", entity={"kind":"servico","name":"ChampionPoker, Profit Deals e PokerTracker","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:24, a fala apresenta a continuação do desafio visto no episódio anterior e a tarefa de depositar a banca inicial.",
                "Entre 0:20 e 0:38, recapitula a expectativa de 2.500 jogos de €2 e um resultado próximo de um salário mínimo em 30 dias.",
                "Entre 5:31 e 6:53, declara depósito concluído, banca de €207, alvo de €437 e acompanhamento por banco de dados.",
            ],
        ),
        comparison={"level":2,"group":"desafio serial brasileiro com meta finita, posição atual, estado anterior e complicação local declarados","referenceIds":["obs-20260920-187","obs-20260920-188"],"confidence":"high"},
        observations=[
            "Título, descrição e fala tornam reconhecíveis a meta global, o segundo episódio, o estado inicial da banca e a tarefa específica de fazer o depósito.",
            "O saldo e o alvo são declarações do criador; não houve auditoria documental independente nem observação da tela.",
            "Um dos três comentários questiona a configuração do desafio e recebe resposta do criador; isso mapeia objeção, não mede compreensão.",
        ],
        interpretations=[
            "A recapitulação mínima conecta episódio anterior, posição presente e tarefa sem depender de cenas não observadas.",
            "Links afiliados, saldo declarado e métricas são contexto comercial, não prova de eficácia, lucro ou retenção.",
        ],
        scores={"gancho":88,"clareza":92,"relevancia":86,"desejo":78,"confianca":72,"retencao":"not_assessed","acao":84,"objecoes":76},
        lenses={
            "apressado":"Reconhece desafio, duração e episódio no título.",
            "analitico":"Reconstrói banca, alvo, período e método declarado, mas exige auditoria financeira.",
            "aspiracional":"A progressão é mensurável, embora o resultado permaneça futuro e incerto.",
            "comunidade":"Comentários permitem discutir regras; três respostas não representam a audiência.",
            "cetico":"Desconta afiliados, promessa econômica e ausência de resultado final.",
        },
        replicable=["Reafirmar meta global e posição em uma frase.","Retomar somente o estado necessário para a tarefa atual.","Definir marco mensurável para o próximo episódio sem copiar números ou roteiro."],
        contingent=["Poker envolve risco financeiro e variância.","Valores, sala e afiliados são contingentes ao criador.","O resultado final e a tela não foram observados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"a fala conecta meta de 30 dias, posição de episódio, estado inicial e tarefa atual","requiredModalities":["title","description","transcript"],"observedModalities":["title","description","transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_3_public_comments",
    ),
    build_ref(
        id="obs-20260920-187",
        title="100 DIAS NO MINECRAFT EPISÓDIO 8. A CONSTRUÇÃO PARTE 1.",
        creator="GamerProX79", identity="gamerprox79",
        url="https://www.youtube.com/watch?v=_uE__ezAwEo",
        published="2026-09-10", duration="PT13M27S",
        accessible=[
            "título", "criador", "descrição pública curta", "data exata", "duração de 13 minutos e 27 segundos",
            "transcrição automática integral em português com 201 segmentos e timestamps", "fala por substituição textual",
            "47 visualizações, 6 curtidas e 5 comentários declarados", "amostra integral dos 5 comentários públicos retornados",
            "meta de 100 dias, episódio 8, estado das árvores, tarefa da casa e prazo do episódio final declarados",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "estado visual da construção", "resultado do episódio final"],
        metrics={"viewsObserved":47,"likesObserved":6,"commentsObserved":5},
        classification=cls(
            presentations=["desafio","tela_gravada","comentario"], primary="storytelling",
            secondary=["entretenimento","comunidade"],
            mix=[{"family":"storytelling","percentage":55},{"family":"entretenimento","percentage":35},{"family":"comunidade","percentage":10}],
            objectives=["visualizacao","retencao","comunidade","seguidores"], topic="cem dias de sobrevivência e construção no Minecraft",
            segment="games", subsegment="série de desafio em Minecraft", audience="jogadores que acompanham progressão serial",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["antecipacao","tensao","pertencimento","recompensa"], hooks=["numero","narrativo","problema"],
            narrative=["situacao","progressao","problema","tentativa","continuidade_serial","cta"], proof=["demonstracao"], cta=["seguir","proxima_parte"],
            evidence=[
                "Entre 0:00 e 0:21, a fala identifica o episódio 8, a posição penúltima, a casa planejada e o estado das árvores.",
                "Entre 0:31 e 0:39, declara que a construção não terminará no episódio atual.",
                "Entre 12:55 e 13:19, recapitula o pouco avanço e abre a obrigação de terminar a estrutura no episódio final.",
            ],
        ),
        comparison={"level":2,"group":"desafio serial brasileiro com meta finita, posição atual, estado anterior e complicação local declarados","referenceIds":["obs-20260920-186","obs-20260920-188"],"confidence":"high"},
        observations=[
            "O título dá meta e posição; a abertura transcrita retoma a casa planejada e o recurso que voltou a existir antes da tarefa.",
            "A fala encerra com avanço incompleto e exigência para o episódio final; execução e aparência da construção não foram vistas.",
        ],
        interpretations=[
            "A recapitulação usa somente estado útil à missão e mantém a posição dentro da temporada reconhecível.",
            "Poucas visualizações não refutam a estrutura; tampouco provam retenção ou clareza para novos espectadores.",
        ],
        scores={"gancho":86,"clareza":90,"relevancia":84,"desejo":76,"confianca":68,"retencao":"not_assessed","acao":78,"objecoes":66},
        lenses={
            "apressado":"Recebe meta, episódio e tarefa no título e na abertura.",
            "analitico":"Entende dependência de recursos e prazo, mas não observa a construção.",
            "aspiracional":"A proximidade do final dá marco concreto de progresso.",
            "comunidade":"Cinco comentários incluem relato de bug; não medem compreensão narrativa.",
            "cetico":"Não converte série, prazo ou métricas em prova de retenção.",
        },
        replicable=["Declarar posição dentro da série.","Recapitular apenas recurso ou decisão necessária à missão.","Encerrar com complicação específica para o próximo capítulo."],
        contingent=["A clareza depende de conhecimento básico do jogo.","Transcrição automática contém ruído.","O estado visual não foi confirmado."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"título e fala conectam meta de 100 dias, episódio 8, estado anterior e missão de construção","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_short_description_full_automatic_transcript_and_5_public_comments",
    ),
    build_ref(
        id="obs-20260920-188",
        title="EPISÓDIO 02 - MILIONÁRIOS EM 100 DIAS BY LINK SCHOOL OF BUSINESS",
        creator="Link School Of Business", identity="link-school-of-business",
        url="https://www.youtube.com/watch?v=nHth71RX4ds",
        published="2026-03-25", duration="PT15M27S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 15 minutos e 27 segundos",
            "transcrição automática integral em português com 451 segmentos e timestamps", "fala por substituição textual",
            "14.097 visualizações, 801 curtidas e 28 comentários declarados", "amostra integral dos 28 comentários públicos retornados",
            "recapitulação do primeiro episódio, posição de segunda semana, missão de validar problema e complicação da feira declaradas",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "auditoria independente dos negócios e resultados", "termos de participação dos alunos"],
        metrics={"viewsObserved":14097,"likesObserved":801,"commentsObserved":28},
        classification=cls(
            presentations=["institucional","reportagem","desafio"], primary="storytelling",
            secondary=["institucional","educativo"],
            mix=[{"family":"storytelling","percentage":45},{"family":"institucional","percentage":35},{"family":"educativo","percentage":20}],
            objectives=["marca","educar","visualizacao","comunidade"], topic="programa de cem dias para desenvolvimento de startups",
            segment="educação e empreendedorismo", subsegment="série institucional de desafio empreendedor", audience="aspirantes a empreendedores e interessados na escola",
            production="complex", scale="medium", replicability="medium", duration="over_60s",
            mechanisms=["antecipacao","tensao","autoridade","pertencimento"], hooks=["narrativo","problema","conflito"],
            narrative=["situacao","problema","progressao","prova","risco","continuidade_serial","cta"], proof=["depoimento","evidencia_documental","autoridade_demonstrada"], cta=["seguir","compartilhar","proxima_parte"],
            advertising="institucional", intent="explicita", entity={"kind":"marca","name":"Link School of Business","confidence":"high"},
            evidence=[
                "A descrição recapitula a semana inicial e antecipa validação de problema, pessoas e solução no segundo episódio.",
                "Entre 0:34 e 1:24, a fala marca a segunda semana e a missão de encontrar clareza de problema, proposta e oferta.",
                "Entre 2:55 e 3:12, apresenta a feira como prova local; o restante acompanha mudanças declaradas e abre a semana de pitch.",
            ],
        ),
        comparison={"level":2,"group":"desafio serial brasileiro com meta finita, posição atual, estado anterior e complicação local declarados","referenceIds":["obs-20260920-186","obs-20260920-187"],"confidence":"high"},
        observations=[
            "Descrição e fala conectam episódio anterior, segunda semana, hipótese em teste e feira de startups.",
            "Alguns participantes narram pivôs e descarte de problemas; resultados e consentimentos não foram auditados fora da produção pública.",
            "Comentários pedem continuação e criticam música; sem áudio ouvido, isso não autoriza avaliação de ritmo ou trilha.",
        ],
        interpretations=[
            "A recapitulação transforma um elenco amplo em problema comum e missão local reconhecível.",
            "Marca, produção e popularidade são contexto institucional, não prova de aprendizagem, retenção ou sucesso empresarial.",
        ],
        scores={"gancho":89,"clareza":92,"relevancia":85,"desejo":83,"confianca":74,"retencao":"not_assessed","acao":82,"objecoes":72},
        lenses={
            "apressado":"Reconhece episódio, prazo e teste de mercado.",
            "analitico":"Vê problema, feira e pivôs declarados, mas precisa de dados externos para resultados.",
            "aspiracional":"A série oferece avanço e risco de eliminação visíveis na fala.",
            "comunidade":"Comentários acompanham a saga, sem representar toda a audiência.",
            "cetico":"Desconta autopromoção institucional e ausência de auditoria dos negócios.",
        },
        replicable=["Retomar estado anterior em uma frase editorial.","Nomear posição temporal e teste concreto do capítulo.","Abrir risco futuro sem copiar participantes ou conflitos."],
        contingent=["Produção e acesso institucional são difíceis de replicar integralmente.","Resultados pertencem à narrativa da própria escola.","Participação pública não equivale a auditoria de consentimento."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"descrição e fala conectam primeiro episódio, segunda semana, estado do problema e feira como complicação específica","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_28_public_comments",
        consent={"storyOrigin":"produção institucional pública com participantes identificáveis","consentStatus":"public_editorial_participation_but_release_not_audited","identityProtection":"not_applicable","evidence":["participação é pública na produção oficial; termos de imagem e consentimento não foram acessados"]},
    ),
    build_ref(
        id="obs-20260920-189",
        title="Episódio 2 - Atravessando os rios - 12 dias para vencer o desafio de Makunaíma",
        creator="Health For Plants", identity="health-for-plants",
        url="https://www.youtube.com/watch?v=J_cWPnSg-5U",
        published="2025-08-26", duration="PT18M27S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 18 minutos e 27 segundos",
            "transcrição automática integral em português com 420 segmentos e timestamps", "fala por substituição textual",
            "2.920 visualizações, 549 curtidas e 82 comentários declarados", "amostra pública limitada de 30 comentários",
            "meta de 12 dias, posição de episódio e segundo dia, travessia de dois rios e acampamento declarados",
        ],
        missing=MISSING_AV + ["recapitulação explícita do estado do episódio ou dia anterior", "baseline funcional contemporâneo", "auditoria da expedição e da promoção de saúde"],
        metrics={"viewsObserved":2920,"likesObserved":549,"commentsObserved":82},
        classification=cls(
            presentations=["desafio","reportagem","depoimento"], primary="storytelling",
            secondary=["curiosidade","educativo"],
            mix=[{"family":"storytelling","percentage":60},{"family":"curiosidade","percentage":25},{"family":"educativo","percentage":15}],
            objectives=["visualizacao","comunidade","marca","educar"], topic="expedição de doze dias ao Monte Roraima",
            segment="aventura e natureza", subsegment="diário serial de expedição", audience="público interessado em trekking, natureza e no criador",
            production="intermediate", scale="large", replicability="medium", duration="over_60s",
            mechanisms=["curiosidade","tensao","admiracao","pertencimento"], hooks=["narrativo","risco","numero"],
            narrative=["situacao","risco","progressao","tentativa","continuidade_serial","cta"], proof=["depoimento"], cta=["clicar","seguir"],
            advertising="geracao_de_leads", intent="explicita", entity={"kind":"servico","name":"Clube da Planta e Autor da Própria Saúde","confidence":"high"},
            evidence=[
                "O título declara episódio 2, desafio de 12 dias e travessia dos rios.",
                "Entre 1:28 e 1:41, a fala situa o segundo dia e a saída da pousada, sem reconstruir o que ocorreu antes.",
                "Entre 4:13 e 4:29, define a missão de atravessar dois rios e montar acampamento.",
            ],
        ),
        comparison={"level":2,"group":"desafio serial brasileiro com meta finita e missão local, mas sem recapitulação explícita do estado anterior","referenceIds":["obs-20260920-186","obs-20260920-187","obs-20260920-188"],"confidence":"high"},
        observations=[
            "Meta, episódio, dia atual e missão são reconhecíveis no título e na fala.",
            "A abertura pula diretamente da saída da pousada para o deslocamento; não reconstrói o estado ou resultado do capítulo anterior.",
            "A ausência de recapitulação delimita o mecanismo-alvo, mas não demonstra confusão ou pior retenção.",
        ],
        interpretations=[
            "Meta, posição e tarefa local não substituem uma recapitulação do estado anterior quando a continuidade é parte do padrão.",
            "O material é caso-limite estrutural, não contraexemplo de desempenho.",
        ],
        scores={"gancho":88,"clareza":84,"relevancia":82,"desejo":80,"confianca":66,"retencao":"not_assessed","acao":72,"objecoes":60},
        lenses={
            "apressado":"Recebe duração do desafio, episódio e travessia no título.",
            "analitico":"Encontra dia e missão, mas não o estado anterior.",
            "aspiracional":"A progressão geográfica oferece conquista futura.",
            "comunidade":"Trinta comentários foram amostrados; não medem orientação narrativa.",
            "cetico":"Não chama ausência de recap de falha sem teste com espectadores.",
        },
        replicable=["Distinguir posição cronológica de recapitulação funcional.","Nomear missão local e risco concreto.","Não presumir desorientação sem evidência."],
        contingent=["O título já entrega contexto relevante.","A expedição tem produção e risco físico próprios.","A descrição promove serviço adjacente de saúde."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"título e fala declaram meta, posição e missão local","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"a abertura recapitula o estado do episódio anterior","requiredModalities":["transcript","description"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_30_of_82_public_comments",
    ),
    build_ref(
        id="obs-20260920-190",
        title="Você NEM IMAGINA TUDO que TEM na NOTA de REAL!",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=xvJsVsiQzb0",
        published="2026-09-12", duration="PT26M32S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 26 minutos e 32 segundos",
            "transcrição automática integral em português com 722 segmentos e timestamps", "fala por substituição textual",
            "2.256.637 visualizações, 43.076 curtidas e 1.200 comentários declarados", "amostra pública limitada de 30 comentários",
            "perguntas sobre animais, efígie e autenticidade, além de explicações verbais de microscopia e mecanismos de segurança",
        ],
        missing=MISSING_AV + ["confirmação visual dos microtextos, relevos, hologramas, marca-d'água e luz ultravioleta", "baseline funcional contemporâneo", "verificação externa de todas as afirmações históricas e legais"],
        metrics={"viewsObserved":2256637,"likesObserved":43076,"commentsObserved":1200},
        classification=cls(
            presentations=["camera_direta","demonstracao","reportagem"], primary="educativo",
            secondary=["demonstracao","curiosidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"demonstracao","percentage":25},{"family":"curiosidade","percentage":20}],
            objectives=["educar","visualizacao","compartilhamento","marca"], topic="história, design e mecanismos de segurança das cédulas brasileiras",
            segment="divulgação científica e cultural", subsegment="análise de objeto cotidiano", audience="público geral curioso sobre dinheiro brasileiro",
            production="complex", scale="large", replicability="medium", duration="over_60s",
            mechanisms=["curiosidade","surpresa","utilidade_pratica","autoridade"], hooks=["pergunta","promessa"],
            narrative=["promessa","progressao","mecanismo","prova","conclusao"], proof=["demonstracao","mecanismo_explicado","fonte"], cta=["outro_conteudo","seguir"],
            advertising="conteudo_de_marca", intent="implicita", entity={"kind":"marca","name":"Manual do Mundo","confidence":"high"},
            evidence=[
                "A descrição formula perguntas sobre animais, efígie e autenticidade e promete microscópio e luz ultravioleta.",
                "Entre 0:27 e 0:37, a fala promete um raio-X das cédulas com microscópio.",
                "Entre 12:33 e 24:31, a fala descreve assinaturas, papel, marca-d'água, fio, microtextos, relevo e luz negra; os efeitos visuais não foram vistos.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de explicador demonstrativo sobre objeto cotidiano, fora do grupo-alvo de storytelling serial","referenceIds":[],"confidence":"high"},
        observations=[
            "Perguntas, percurso explicativo e mecanismos aparecem em descrição e fala transcrita.",
            "A transcrição afirma observações feitas ao microscópio e sob luz negra, mas nenhum detalhe visual foi confirmado.",
            "Comentários amostrados contêm dúvidas e correções alegadas; não substituem fontes ou auditoria visual.",
        ],
        interpretations=[
            "A combinação de perguntas concretas e análise de objeto cotidiano merece exploração futura, sem gerar hipótese neste lote.",
            "Popularidade e escala de produção não provam precisão, compreensão ou retenção.",
        ],
        scores={"gancho":91,"clareza":93,"relevancia":88,"desejo":86,"confianca":78,"retencao":"not_assessed","acao":76,"objecoes":74},
        lenses={
            "apressado":"Reconhece imediatamente o objeto e a promessa de descoberta.",
            "analitico":"Reconstrói mecanismos pela fala, mas precisa ver imagens e checar fontes.",
            "aspiracional":"Promete perceber detalhes antes invisíveis no cotidiano.",
            "comunidade":"Comentários apontam dúvidas e possíveis omissões, sem representatividade.",
            "cetico":"Não aceita descrição de imagem como confirmação visual.",
        },
        replicable=["Começar por perguntas concretas sobre um objeto familiar.","Organizar investigação por camadas observáveis.","Separar explicação verbal de prova visual e fonte externa."],
        contingent=["Microscópio, luz UV e equipe elevam a produção.","Alegações históricas e legais exigem fontes.","A demonstração visual não foi adquirida."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"descrição e fala delimitam perguntas e mecanismos de segurança","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"microtextos, relevos e efeitos de luz foram visualmente demonstrados","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_30_of_1200_public_comments",
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 034")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260920-186", "obs-20260920-187", "obs-20260920-188"]
new_case = "obs-20260920-189"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 6
pattern["supportingCount"] = 6
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260920-186","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Meta de 30 dias, episódio 2, estado da banca e tarefa de depósito são conectados na abertura e no desenvolvimento.","evidence":"Metadados, descrição integral, transcrição automática integral e três comentários.","limitations":["sem audiovisual, auditoria financeira, resultado final ou retenção","conteúdo afiliado"]},
    {"referenceId":"obs-20260920-187","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Meta de 100 dias, episódio 8, estado de recursos e missão da casa aparecem antes do avanço incompleto e do prazo final.","evidence":"Metadados, descrição curta, transcrição automática integral e cinco comentários.","limitations":["sem audiovisual, estado visual ou retenção"]},
    {"referenceId":"obs-20260920-188","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Descrição e fala recapitularam a primeira semana, situaram a segunda e abriram o teste específico da feira.","evidence":"Metadados, descrição integral, transcrição automática integral e 28 comentários.","limitations":["produção institucional","sem audiovisual, auditoria de resultados ou retenção"]},
    {"referenceId":"obs-20260920-189","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Há meta, episódio, dia e missão local, mas nenhuma recapitulação explícita do estado anterior.","evidence":"Metadados, descrição integral, transcrição automática integral e 30 de 82 comentários.","limitations":["não é contraexemplo de desempenho","sem teste de orientação"]},
])
pattern["limitations"] = [
    "Seis apoios formais vêm de seis criadores e fontes; demonstram recorrência estrutural, não eficácia.",
    "Os três novos apoios possuem transcrição integral, mas nenhum audiovisual, ritmo, retenção, baseline ou teste de compreensão.",
    "O segundo caso-limite mostra que meta, posição e missão local não substituem recapitulação explícita do estado anterior.",
    "Recapitulação curta pode orientar, mas não foi comparada com recapitulação longa, confusa ou ausente em teste controlado.",
    "Transcrições automáticas podem conter erros e não autorizam copiar a fala.",
    "Popularidade, escala, orçamento, publicidade e comentários permanecem contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("g3og0KFzadA", "episódio serial acessível, mas menor comparabilidade com meta global finita e redundante com apoios mais claros"),
        ("9dLnl3CCrqs", "transcrição desativada e cobertura insuficiente para reconstruir recapitulação"),
        ("zprM6DP02W0", "vídeo de rotina seriada sem meta global finita claramente observável"),
        ("YhfXYdu2a-U", "resultado de busca não correspondia de modo confiável ao mecanismo-alvo"),
        ("YzFGVZyAXKo", "posição serial e recapitulação insuficientes na cobertura adquirida"),
        ("UOAoaad5oUk", "funcionalmente menos comparável e sem ganho informativo sobre o limite do padrão"),
        ("Lxe4FAI-g6s", "candidato redundante após seleção dos três apoios independentes"),
        ("EWNQZjWOH2U", "já presente na memória"),
        ("FImFjzVFCnc", "já presente na memória"),
        ("qc8SCgY0dlc", "já presente na memória"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 112,
    "referenceIds": [f"obs-20260920-{n}" for n in range(186, 191)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260920-190"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["storytelling","educativo","demonstracao","comunidade","entretenimento","institucional","curiosidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"os cinco downloads de vídeo expiraram após 70 segundos; tentativas de capa terminaram sem arquivo por timeout ou resposta 502","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":5,"partialAutomatic":0,"none":0,"limitation":"transcrições automáticas substituem somente a fala e podem conter erros"},
    "commentsCoverage": {"countsOnly":0,"sampledReferences":5,"sampledComments":96,"limitation":"duas amostras foram limitadas a 30 comentários; amostras públicas não são representativas"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"datas, canais, durações, temas e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["meta global, posição atual e missão local não contam como recapitulação quando o estado anterior não é reconstruído"],
    "safetyFindings": [
        "conteúdo de poker foi tratado como narrativa com risco financeiro, nunca como promessa de renda",
        "participação institucional pública não foi confundida com auditoria de consentimento",
        "métricas, afiliados, marca e escala permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, ritmo, retenção, frase ou roteiro foi inventado",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes reforçam a recorrência de meta global, posição atual, estado anterior e complicação específica. O padrão passa de três para seis apoios e de um para dois casos-limite; permanece provisório e não demonstra orientação, retenção, compreensão ou desempenho.",
    "nextTarget": "storytelling serial brasileiro recente e curto de criador pequeno ou médio, com audiovisual integral, recapitulação explícita do estado anterior e teste entre espectadores novos e recorrentes; procurar também recapitulação longa ou confusa e ausência de recap em caso funcionalmente comparável",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "As cinco transcrições são automáticas e substituem somente a fala.",
        "Foram amostrados 96 comentários em cinco publicações; as amostras não são representativas.",
        "Não houve baseline, retenção, replay, teste de orientação ou compreensão.",
        "Uma referência é institucional e outra contém risco financeiro e links afiliados.",
        "Nenhum resultado autoriza causalidade ou validação.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
