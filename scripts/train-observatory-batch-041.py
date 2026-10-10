#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-040.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]
make_ref = ns["make_ref"]

NOW = "2026-09-29T11:17:14.000Z"
OBSERVED = "2026-09-29"
RUN_ID = "run-20260929-supervised-041"
PATTERN_ID = "pat-20260823-003"
BATCH_IDS = {f"obs-20260929-{n}" for n in range(221, 226)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

FINANCE_GROUP = "educação financeira brasileira para iniciantes que converte desorganização ou dívida em um caminho finito, condicionado por renda, despesas, juros e capacidade de pagamento"
MISSING_COMMON = MISSING_AV + [
    "comentários públicos e sua contagem",
    "baseline individual comparável",
    "teste de compreensão ou execução",
    "resultado financeiro dos espectadores",
]

refs = [
    build_ref(
        id="obs-20260929-221",
        title="COMO ORGANIZAR SUAS FINANÇAS DO ZERO EM 2026 | Organização financeira para 2026",
        creator="Ruth Szilagy", identity="ruth-szilagy",
        url="https://www.youtube.com/watch?v=wDxevnvAj0k",
        published="2025-12-02", duration="PT16M9S",
        accessible=[
            "título, criador, categoria e descrição pública integral de 1.871 caracteres",
            "data exata, duração de 16 minutos e 9 segundos, 5.891 visualizações e 479 curtidas públicas",
            "transcrição automática integral em português com 32 blocos temporais; fala acessível somente por substituição textual",
            "etapas faladas: identificar renda líquida ou média variável, listar obrigações mensais e anuais, mapear gastos variáveis e construir orçamento realista",
            "alternativas faladas de controle por aplicativo, caderno, planilha, grupo próprio de mensagens ou inteligência artificial",
            "oferta de consultoria, material e links comerciais na descrição",
        ],
        missing=MISSING_COMMON + ["adequação individual do orçamento", "disclosure completo dos vínculos comerciais"],
        metrics={"viewsObserved":5891,"likesObserved":479,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_longo", presentations=["camera_direta","tutorial"], primary="educativo",
            secondary=["explicativo","oferta_direta"],
            mix=[{"family":"educativo","percentage":55},{"family":"explicativo","percentage":30},{"family":"oferta_direta","percentage":15}],
            objectives=["educar","consciencia_problema","apresentar_solucao","trafego"],
            topic="organização financeira do zero", segment="finanças pessoais", subsegment="orçamento para iniciantes",
            audience="adultos sem clareza sobre renda, obrigações e gastos", awareness="consciente_problema",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["aproximacao","alivio","confianca"], hooks=["problema","promessa","identificacao"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","tratamento_objecao"],
            cta=["outro_conteudo","seguir"], advertising="oferta_direta", intent="explicita",
            entity={"kind":"servico","name":"consultoria e materiais próprios","confidence":"high"},
            evidence=[
                "A fala começa pela incerteza sobre o destino do dinheiro e anuncia um passo a passo do zero.",
                "Renda fixa e variável, obrigações anuais, gastos variáveis e limites semanais aparecem antes da conclusão.",
                "Oferta e métricas são contexto; não medem aprendizagem nem resultado financeiro.",
            ],
        ),
        comparison={"level":1,"group":FINANCE_GROUP,"referenceIds":["obs-20260929-222","obs-20260929-223"],"confidence":"high"},
        observations=[
            "O caminho começa pela renda realmente disponível e diferencia salário fixo de renda variável.",
            "Obrigações mensais e anuais e gastos variáveis são reconstruídos antes de propor limites e prioridades.",
            "Quando despesas excedem a renda, a fala reconhece a necessidade de medidas corretivas separadas, sem demonstrar resultado.",
        ],
        interpretations=[
            "A sequência torna auditável de onde parte o orçamento e quais decisões vêm depois.",
            "A adequação a cada perfil e a eficácia permanecem não medidas.",
        ],
        scores={"gancho":88,"clareza":94,"relevancia":93,"desejo":72,"confianca":80,"retencao":"not_assessed","acao":91,"objecoes":84},
        lenses={
            "apressado":"Entende cedo o problema e o primeiro passo.",
            "analitico":"Encontra renda, obrigações e gastos, mas não vê execução ou resultado.",
            "aspiracional":"Visualiza um orçamento alinhado a prioridades pessoais.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Separa estrutura educativa, oferta comercial e eficácia não demonstrada.",
        },
        replicable=["Começar pela renda realmente disponível.","Separar obrigações mensais, anuais e gastos variáveis.","Só propor limites depois de reconstruir o baseline."],
        contingent=["Consultoria e materiais próprios são contexto comercial.","Adequação individual não foi testada.","Audiovisual, comentários, retenção e resultado não foram medidos."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"problema financeiro e caminho condicionado por renda, obrigações e gastos aparecem publicamente","requiredModalities":["metadata","description","transcript"],"observedModalities":["metadata","description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260929-222",
        title="COMO SAIR DAS DÍVIDAS: 5 passos simples (que funcionam mesmo)",
        creator="Vamos Prosperar", identity="vamos-prosperar",
        url="https://www.youtube.com/watch?v=nl5cgUz8rNo",
        published="2022-02-28", duration="PT14M36S",
        accessible=[
            "título, criador, categoria e descrição pública integral de 1.526 caracteres com capítulos",
            "data exata, duração de 14 minutos e 36 segundos, 8.274 visualizações e cerca de 1,3 mil curtidas públicas",
            "transcrição automática integral em português com 28 blocos temporais; fala acessível somente por substituição textual",
            "cinco passos falados: mapear dívida e juros, calcular capacidade de pagamento, negociar, escolher forma de quitação e monitorar o plano",
            "enquadramento religioso, captação de leads e links comerciais na descrição",
        ],
        missing=MISSING_COMMON + ["fonte da alegação de redução de gastos entre 20% e 40%", "adequação individual das estratégias"],
        metrics={"viewsObserved":8274,"likesObserved":"about_1300","commentsObserved":"not_assessed"},
        classification=cls(
            material="video_longo", presentations=["camera_direta","tutorial"], primary="educativo",
            secondary=["explicativo","inspiracao"],
            mix=[{"family":"educativo","percentage":55},{"family":"explicativo","percentage":30},{"family":"inspiracao","percentage":15}],
            objectives=["educar","consciencia_problema","apresentar_solucao","trafego"],
            topic="saída de dívidas em cinco passos", segment="finanças pessoais", subsegment="negociação e quitação de dívidas",
            audience="adultos endividados buscando um plano de negociação", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["alivio","confianca","aversao_perda"], hooks=["problema","numero","promessa"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","tratamento_objecao"],
            cta=["clicar","seguir"], advertising="oferta_direta", intent="explicita",
            entity={"kind":"servico","name":"materiais e captação do canal","confidence":"high"},
            evidence=[
                "Cada dívida deve ser listada com saldo, parcela e taxa de juros; a capacidade de pagamento é calculada pela diferença entre renda e despesas.",
                "A negociação inclui extensão, desconto à vista, consolidação de juros menores ou priorização da maior taxa.",
                "Enquadramento religioso, oferta e métricas não foram tratados como causa de desempenho.",
            ],
        ),
        comparison={"level":1,"group":FINANCE_GROUP,"referenceIds":["obs-20260929-221","obs-20260929-223"],"confidence":"high"},
        observations=[
            "A sequência liga saldo, parcela e juros à capacidade de pagamento antes da negociação.",
            "A fala explicita que alongar prazo pode aumentar o total pago e que consolidação exige taxa menor.",
            "Monitoramento e ajuste fecham o caminho, mas nenhum resultado individual foi observado.",
        ],
        interpretations=[
            "Tornar juros e capacidade visíveis qualifica o caminho para dívida sem provar que ele funciona para todos.",
            "A alegação numérica sobre redução de gastos permaneceu não auditada.",
        ],
        scores={"gancho":90,"clareza":95,"relevancia":95,"desejo":75,"confianca":82,"retencao":"not_assessed","acao":93,"objecoes":88},
        lenses={
            "apressado":"Recebe cinco passos e a primeira tarefa rapidamente.",
            "analitico":"Encontra saldo, juros, capacidade e trade-offs explícitos.",
            "aspiracional":"Visualiza uma rota de negociação e acompanhamento.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Exige fonte para a alegação percentual e adequação ao caso individual.",
        },
        replicable=["Listar saldo, parcela e taxa antes de aconselhar.","Calcular capacidade de pagamento com renda e despesas.","Explicar trade-offs de cada forma de quitação."],
        contingent=["A redução percentual de gastos não foi verificada.","Estratégias dependem de contrato, taxa e capacidade individual.","Audiovisual, comentários, retenção e resultado não foram medidos."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"caminho de dívida condicionado por saldo, juros, renda, despesas e capacidade aparece na fala","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260929-223",
        title="Como Quitar Dívidas Mesmo Ganhando Pouco (O Plano Definitivo Que Funciona no Brasil)",
        creator="Sem Juros Mentais", identity="sem-juros-mentais",
        url="https://www.youtube.com/watch?v=PAJ3FESfXOY",
        published="2026-01-16", duration="PT8M8S",
        accessible=[
            "título, criador, categoria e descrição pública integral de 610 caracteres",
            "data exata, duração de 8 minutos e 8 segundos, 12 visualizações e 5 curtidas públicas",
            "transcrição automática integral em português com 16 blocos temporais; fala acessível somente por substituição textual",
            "etapas faladas: listar dívida total, juros, parcela e vencimento; escolher avalanche ou bola de neve; abrir margem, negociar e formar reserva mínima",
        ],
        missing=MISSING_COMMON + ["credencial ou fonte técnica identificável", "prova da promessa de plano definitivo", "adequação a necessidades essenciais"],
        metrics={"viewsObserved":12,"likesObserved":5,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_longo", presentations=["comentario","tutorial"], primary="explicativo",
            secondary=["educativo","inspiracao"],
            mix=[{"family":"explicativo","percentage":45},{"family":"educativo","percentage":40},{"family":"inspiracao","percentage":15}],
            objectives=["educar","consciencia_problema","apresentar_solucao","seguidores"],
            topic="quitação de dívidas com baixa renda", segment="finanças pessoais", subsegment="priorização e negociação de dívidas",
            audience="adultos endividados com pouca margem mensal", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["alivio","aversao_perda","confianca"], hooks=["problema","promessa","identificacao"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","alegacao_sem_prova"],
            cta=["seguir","compartilhar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"medium"},
            evidence=[
                "A primeira tarefa exige saldo, juros, parcela e vencimento de cada dívida.",
                "Avalanche e bola de neve são apresentadas como rotas alternativas; a escolha é condicionada à manutenção do plano.",
                "A reserva mínima aparece depois da negociação, mas a promessa definitiva não possui prova acessível.",
            ],
        ),
        comparison={"level":1,"group":FINANCE_GROUP,"referenceIds":["obs-20260929-221","obs-20260929-222"],"confidence":"high"},
        observations=[
            "O plano exige um inventário de dívida antes de escolher a ordem de pagamento.",
            "A fala preserva duas estratégias e reconhece que adesão importa, sem medir adesão ou resultado.",
            "A afirmação de que dívida costuma não decorrer de baixa renda é ampla e não foi sustentada por fonte.",
        ],
        interpretations=[
            "O inventário e a escolha explícita tornam o caminho rastreável.",
            "Promessa definitiva, causalidade sobre renda e eficácia continuam não demonstradas.",
        ],
        scores={"gancho":92,"clareza":91,"relevancia":92,"desejo":80,"confianca":58,"retencao":"not_assessed","acao":90,"objecoes":72},
        lenses={
            "apressado":"Entende a dívida-alvo e recebe uma primeira tarefa.",
            "analitico":"Encontra dados mínimos e duas estratégias, mas pede fontes e adequação.",
            "aspiracional":"Visualiza controle e reserva mesmo com baixa renda.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Questiona a promessa definitiva e generalizações sem fonte.",
        },
        replicable=["Inventariar dívida, juros, parcela e vencimento.","Apresentar alternativas com critério explícito.","Incluir margem e reserva sem prometer universalidade."],
        contingent=["Credenciais e fontes não ficaram identificáveis.","A promessa definitiva excede a evidência acessível.","Audiovisual, comentários, retenção e resultado não foram medidos."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"inventário da dívida, alternativas de priorização e negociação aparecem na fala","requiredModalities":["metadata","transcript"],"observedModalities":["metadata","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260929-224",
        title="A VERDADE NUA E CRUA PARA SAIR DAS DÍVIDAS (método único)",
        creator="Investimento sem terno", identity="investimento-sem-terno",
        url="https://www.youtube.com/watch?v=NqnOihGb4to",
        published="2026-04-15", duration="PT6M",
        accessible=[
            "título, criador e descrição pública integral de 2.629 caracteres; uma de três sondagens da página ficou indisponível",
            "data exata, duração de 6 minutos, 13 visualizações e uma curtida pública observada em uma sondagem anterior",
            "transcrição automática integral em português com 12 blocos temporais; fala acessível somente por substituição textual",
            "problema concreto, lista de grandes despesas e proposta falada de sacrifício extremo",
        ],
        missing=MISSING_COMMON + ["fonte da alegação de oito em dez brasileiros endividados", "mapeamento de saldo, taxa, parcela e capacidade", "proteção explícita de necessidades essenciais"],
        metrics={"viewsObserved":13,"likesObserved":1,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_longo", presentations=["comentario","camera_direta"], primary="autoridade_opiniao",
            secondary=["educativo","conscientizacao"],
            mix=[{"family":"autoridade_opiniao","percentage":45},{"family":"educativo","percentage":35},{"family":"conscientizacao","percentage":20}],
            objectives=["consciencia_problema","educar","seguidores"],
            topic="saída de dívidas por corte extremo", segment="finanças pessoais", subsegment="cortes de despesas para endividados",
            audience="adultos endividados buscando ação imediata", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["medo","aversao_perda","urgencia"], hooks=["verbal","problema","promessa"],
            narrative=["problema","progressao","promessa","cta"], proof=["alegacao_sem_prova","autoridade_percebida"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"medium"},
            evidence=[
                "A fala propõe listar os maiores gastos e fazer cortes imediatos.",
                "Exemplos incluem alimentação, itens domésticos e lazer familiar sem reconstruir capacidade de pagamento ou preservar um piso essencial.",
                "Faixas de juros e prevalência de endividamento são mencionadas sem fonte rastreável.",
            ],
        ),
        comparison={"level":2,"group":FINANCE_GROUP,"referenceIds":["obs-20260929-221","obs-20260929-222","obs-20260929-223"],"confidence":"high"},
        observations=[
            "Há problema e ação finita, mas não inventário da dívida, taxa por contrato, parcela ou capacidade de pagamento.",
            "O sacrifício é apresentado como método único e alcança necessidades que podem ser essenciais.",
            "Não há resultado comparável para tratá-lo como contraexemplo de eficácia.",
        ],
        interpretations=[
            "É caso-limite: clareza e urgência não compensam ausência de baseline e viabilidade.",
            "Cortes extremos sem piso essencial elevam o risco e o ônus de prova.",
        ],
        scores={"gancho":94,"clareza":81,"relevancia":86,"desejo":68,"confianca":30,"retencao":"not_assessed","acao":79,"objecoes":24},
        lenses={
            "apressado":"Recebe uma ordem de corte imediata.",
            "analitico":"Não encontra saldo, juros, capacidade ou proteção de essenciais.",
            "aspiracional":"É atraído pela promessa de ruptura rápida.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Rejeita método único, números sem fonte e sacrifício desproporcional.",
        },
        replicable=["Nomear o problema sem eufemismo.","Transformar diagnóstico em lista de despesas.","Distinguir custos ajustáveis de necessidades essenciais."],
        contingent=["Método único e cortes extremos não foram validados.","Dados estatísticos e faixas de juros não têm fonte acessível.","Audiovisual, comentários, retenção e resultado não foram medidos."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"problema e proposta finita de cortes aparecem na fala","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"sacrifício extremo é método único adequado para sair das dívidas","requiredModalities":["baseline","safety","intervention","outcome","comparison"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260929-225",
        title="DE ONDE VEM O VENTO? Aprenda com uma EXPERIÊNCIA!",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=JuxZTgWEKfs",
        published="2014-08-12", duration="PT3M24S",
        accessible=[
            "título, criador, categoria e descrição pública integral de 1.389 caracteres",
            "data exata, duração de 3 minutos e 24 segundos, 757.605 visualizações e cerca de 33 mil curtidas públicas",
            "transcrição automática integral em português com 6 blocos temporais; fala acessível somente por substituição textual",
            "materiais e procedimento falados: aquário, água quente e fria e corantes vermelho e azul",
            "explicação falada de densidade, subida do fluido quente, descida do fluido frio e analogia com o ar",
        ],
        missing=MISSING_COMMON + ["movimento visual dos corantes", "resultado visual", "orientação de segurança para água quente", "revisão científica externa"],
        metrics={"viewsObserved":757605,"likesObserved":"about_33000","commentsObserved":"not_assessed"},
        classification=cls(
            material="video_curto", presentations=["demonstracao","tutorial"], primary="demonstracao",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":35},{"family":"curiosidade","percentage":15}],
            objectives=["educar","visualizacao","compartilhamento","salvamento"],
            topic="convecção e origem do vento", segment="educação científica", subsegment="experimento doméstico de fluidos",
            audience="estudantes, famílias e professores interessados em ciência", awareness="consciente_solucao",
            production="intermediate", scale="large", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","surpresa","recompensa","confianca"], hooks=["pergunta","demonstracao_antecipada"],
            narrative=["promessa","progressao","payoff","conclusao"], proof=["mecanismo_explicado","autoridade_demonstrada"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"marca","name":"Manual do Mundo","confidence":"high"},
            evidence=[
                "A pergunta sobre o vento antecede materiais, procedimento e explicação de convecção.",
                "A fala relaciona densidade e temperatura em água e ar.",
                "Movimento, resultado visual e segurança operacional não foram observados.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de demonstração científica doméstica","referenceIds":[],"confidence":"low"},
        observations=[
            "Procedimento e mecanismo são rastreáveis na fala e na descrição.",
            "Sem o vídeo, não se confirma a circulação dos corantes nem se ensina o resultado como demonstração visual.",
            "Orientação acessível de segurança para água quente não foi localizada.",
        ],
        interpretations=[
            "A exploração registra alinhamento verbal entre pergunta, procedimento e mecanismo, sem provar execução ou compreensão.",
            "Uma referência isolada não gera hipótese nova.",
        ],
        scores={"gancho":89,"clareza":90,"relevancia":87,"desejo":75,"confianca":79,"retencao":"not_assessed","acao":70,"objecoes":62},
        lenses={
            "apressado":"Recebe pergunta e experimento cedo.",
            "analitico":"Encontra mecanismo falado, mas não o resultado visual.",
            "aspiracional":"Visualiza uma experiência doméstica acessível.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Exige confirmação visual, revisão científica e segurança.",
        },
        replicable=["Abrir com pergunta específica.","Listar materiais e procedimento.","Explicar o mecanismo sem depender apenas do espetáculo visual."],
        contingent=["Resultado e execução visuais não foram confirmados.","Segurança com água quente não foi documentada.","Popularidade não prova precisão ou compreensão."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"materiais, procedimento e mecanismo de convecção aparecem na fala e descrição","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"o movimento visual dos corantes confirma o resultado","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
            {"claim":"o procedimento é seguro sem supervisão","requiredModalities":["safety_guidance","expert_review"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 041")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260929-221", "obs-20260929-222", "obs-20260929-223"]
new_case = "obs-20260929-224"
pattern["statement"] = "Em educação financeira para iniciantes, nomear um problema concreto e organizar a resposta em etapas finitas torna problema, caminho e próxima ação identificáveis; em conteúdos sobre dívida, explicitar renda, despesas, saldo, juros, parcelas e capacidade de pagamento torna o caminho auditável e delimita ações viáveis. Cortes universais ou extremos sem preservar necessidades essenciais elevam o ônus de prova, e compreensão e resultado financeiro permanecem não medidos."
pattern["name"] = pattern["statement"]
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 14
pattern["supportingCount"] = 14
pattern["caseLimitCount"] = 3
pattern["creatorDiversityCount"] = 14
pattern["sourceDiversityCount"] = 14
pattern["conditions"] = [
    "conteúdo educativo de finanças pessoais para iniciantes",
    "problema financeiro concreto identificado",
    "caminho organizado em etapas finitas",
    "em dívida, renda, despesas, saldo, juros, parcelas e capacidade de pagamento explicitados quando aplicáveis",
    "ações preservam necessidades essenciais e são proporcionais ao baseline",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260929-221","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Renda disponível, obrigações mensais e anuais e gastos variáveis são reconstruídos antes de limites e prioridades.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["sem audiovisual, comentários, teste de execução ou resultado financeiro"]},
    {"referenceId":"obs-20260929-222","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Saldo, parcela, juros e capacidade de pagamento antecedem negociação, escolha da forma de quitação e monitoramento.","evidence":"Metadados, descrição integral com capítulos e transcrição automática integral.","limitations":["alegação percentual não auditada; sem audiovisual ou resultado"]},
    {"referenceId":"obs-20260929-223","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Inventário de dívida, duas estratégias de priorização, margem, negociação e reserva formam um caminho rastreável.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["promessa definitiva e generalizações sem prova; sem audiovisual ou resultado"]},
    {"referenceId":"obs-20260929-224","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Há problema e ação finita, mas método único e sacrifício extremo ignoram saldo, juros, capacidade e preservação de necessidades essenciais.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["não conta como apoio nem contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Quatorze apoios vêm de quatorze criadores e fontes; demonstram recorrência estrutural, não compreensão ou resultado financeiro.",
    "Nenhuma referência oferece retenção, teste de compreensão, baseline individual completo ou experimento causal.",
    "Comentários, métricas, fama, escala, produção e ofertas permanecem contexto não causal.",
    "O terceiro caso-limite mostra que ação clara não compensa cortes extremos sem capacidade de pagamento e piso essencial.",
    "Conselhos financeiros exigem adequação individual, revisão humana e avaliação de riscos e contratos.",
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 122,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260929-225"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=yPoBIw-sqbQ","reason":"foco principal em finanças empresariais; comparabilidade funcional inferior à dívida pessoal"},
        {"url":"https://www.youtube.com/watch?v=3CeGKeWNzTY","reason":"abordagem concentrada em cartão; o conjunto selecionado cobre baseline mais completo"},
        {"url":"https://www.youtube.com/watch?v=hbLXJlLM2bs","reason":"estrutura comparável, mas os três apoios escolhidos ofereceram maior diversidade de mecanismos"},
        {"url":"https://www.youtube.com/watch?v=X9WcWT1TRIU","reason":"descrição traz estatísticas e promessa de desconto sem fontes acessíveis"},
        {"url":"https://www.youtube.com/watch?v=jv1V0O8aIbE","reason":"embalagem de segredo bancário e evidência estrutural inferior ao caso-limite selecionado"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 5,
    "creativeFamiliesObserved": ["educativo","explicativo","oferta_direta","inspiracao","autoridade_opiniao","conscientizacao","demonstracao","curiosidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "as cinco páginas expuseram somente formatos cifrados sem URL direta; as cinco capas retornaram HTML de indisponibilidade de 195 bytes e as faixas nativas de legenda retornaram zero bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":5,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":0,
        "limitation":"transcrições automáticas obtidas por serviço público substituem somente a fala e podem repetir ou errar palavras; não sustentam cenas, voz, texto na tela ou ritmo",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":0,
        "sampledComments":0,
        "zeroReturnedReferences":0,
        "unavailableReferences":5,
        "limitation":"comentários e contagens não ficaram acessíveis; ausência de cobertura não foi registrada como zero",
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
    "caseLimitsFound": ["um caminho finito não se torna financeiramente viável quando ignora saldo, juros, capacidade de pagamento e preservação de necessidades essenciais"],
    "safetyFindings": [
        "nenhuma recomendação financeira foi tratada como adequada a todo perfil",
        "promessa, método único, comentários, autoridade percebida e métricas não foram tratados como prova de resultado",
        "o experimento científico não foi ensinado como execução visual confirmada ou procedimento seguro sem supervisão",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes elevam de onze para quatorze os apoios do padrão financeiro. Um caso-limite refina a exigência de capacidade de pagamento e preservação de necessidades essenciais. O padrão permanece provisório.",
    "nextTarget": "explicador financeiro brasileiro recente e curto, de criador pequeno ou médio, com audiovisual integral e exemplo preenchido que ligue renda, despesas essenciais, saldo, juros, parcela e sobra viável; buscar também um teste de compreensão ou execução e um caso em que os passos contradigam o próprio baseline",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "As cinco transcrições são automáticas integrais e substituem somente a fala.",
        "Comentários e suas contagens não ficaram acessíveis.",
        "Não houve baseline contemporâneo, retenção, teste de compreensão, adequação individual ou causalidade.",
        "O resultado do experimento científico e sua segurança operacional não foram confirmados visualmente.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
