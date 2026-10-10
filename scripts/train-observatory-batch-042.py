#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-041.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]
make_ref = ns["make_ref"]

NOW = "2026-09-30T11:06:10.000Z"
OBSERVED = "2026-09-30"
RUN_ID = "run-20260930-supervised-042"
PATTERN_ID = "pat-20260823-003"
BATCH_IDS = {f"obs-20260930-{n}" for n in range(226, 231)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

FINANCE_GROUP = "educação financeira brasileira para iniciantes que transforma renda, despesas e dívida em um orçamento preenchido e uma capacidade de pagamento verificável"
MISSING_COMMON = MISSING_AV + [
    "curva de retenção e abandono",
    "fontes de tráfego e mídia paga",
    "teste de compreensão ou execução",
    "resultado financeiro dos espectadores",
]

refs = [
    build_ref(
        id="obs-20260930-226",
        title="Orçamento para quitar dividas na pratica",
        creator="Sem Dívidas", identity="sem-dividas",
        url="https://www.youtube.com/watch?v=aId5IG1Lr54",
        published="2022-10-26", duration="PT33M10S",
        accessible=[
            "título, criador, categoria, descrição pública integral de 195 caracteres e data exata",
            "duração de 33 minutos e 10 segundos, 182 visualizações e 21 curtidas públicas; contagem de comentários não acessível",
            "transcrição automática integral em português até 33 minutos e 2 segundos; fala acessível somente por substituição textual",
            "relato falado de caso real com autorização afirmada pela criadora e nomes e documentos deliberadamente ocultos",
            "construção falada de planilha com renda, despesas, cinco cartões, valores mensais de dívida e capacidade de pagamento",
        ],
        missing=MISSING_COMMON + ["documento independente do consentimento", "taxas de juros completas por dívida", "resultado posterior do caso"],
        metrics={"viewsObserved":182,"likesObserved":21,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_longo", presentations=["tutorial","demonstracao"], primary="educativo",
            secondary=["demonstracao","prova_estudo_caso"],
            mix=[{"family":"educativo","percentage":45},{"family":"demonstracao","percentage":35},{"family":"prova_estudo_caso","percentage":20}],
            objectives=["educar","apresentar_solucao","consciencia_problema"],
            topic="orçamento preenchido para quitação de dívidas", segment="finanças pessoais", subsegment="planejamento de dívida com planilha",
            audience="adultos endividados que precisam comparar renda, despesas e parcelas", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio","aversao_perda"], hooks=["problema","demonstracao_antecipada"],
            narrative=["situacao","problema","progressao","mecanismo","conclusao"], proof=["mecanismo_explicado","depoimento"],
            cta=["clicar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"produto","name":"planilha financeira","confidence":"high"},
            evidence=[
                "A fala atribui o caso a uma pessoa real, afirma autorização e diz ocultar nome e documentos.",
                "Renda, despesas, cartões e pagamentos são preenchidos antes de avaliar capacidade.",
                "A interface e os valores na tela não foram confirmados visualmente; consentimento foi apenas declarado pela criadora.",
            ],
        ),
        comparison={"level":1,"group":FINANCE_GROUP,"referenceIds":["obs-20260930-227","obs-20260930-228"],"confidence":"high"},
        observations=[
            "O exemplo preenchido conecta um caso declarado real a renda, despesas e pagamentos mensais.",
            "Cinco cartões são tratados separadamente antes da avaliação de capacidade.",
            "Identidade e documentos são protegidos na fala, mas o consentimento não foi documentado de forma independente.",
        ],
        interpretations=[
            "Um exemplo preenchido torna inputs e decisão auditáveis na fala sem provar eficácia financeira.",
            "Proveniência e proteção foram registradas; autorização declarada não equivale a consentimento verificado.",
        ],
        scores={"gancho":86,"clareza":94,"relevancia":95,"desejo":76,"confianca":84,"retencao":"not_assessed","acao":92,"objecoes":87},
        lenses={
            "apressado":"Identifica cedo o caso e a tarefa de organizar valores.",
            "analitico":"Encontra renda, despesas e dívidas preenchidas, mas pede juros e resultado posterior.",
            "aspiracional":"Visualiza a passagem do caos para uma planilha executável.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Separa autorização declarada, proteção de identidade e eficácia não demonstrada.",
        },
        replicable=["Preencher o exemplo antes de aconselhar.","Separar renda, despesas e cada dívida.","Declarar a origem do caso e proteger dados pessoais."],
        contingent=["Consentimento foi afirmado, não auditado.","A tela e os valores visuais não foram observados.","Resultado financeiro não foi acompanhado."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"caso preenchido liga renda, despesas, dívidas e capacidade na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260930-227",
        title="PLANILHA PARA ORGANIZAR AS DÍVIDAS | COMO FAZER UM LEVANTAMENTO DAS DÍVIDAS | DIA D SEM DÍVIDAS",
        creator="Jaime Cristofori", identity="jaime-cristofori",
        url="https://www.youtube.com/watch?v=0-ghYBUOoZ8",
        published="2022-05-26", duration="PT13M42S",
        accessible=[
            "título, criador, categoria, descrição pública integral de 1.639 caracteres e data exata",
            "duração de 13 minutos e 42 segundos, 366 visualizações, 32 curtidas e um comentário público indicados",
            "transcrição automática integral em português até 13 minutos e 35 segundos; fala acessível somente por substituição textual",
            "planilha falada com credor, motivo, saldo total, valor atrasado, taxa de juros e compromisso mensal",
            "exemplo numérico falado de renda de R$ 3.000 e parcelas comprometidas de R$ 2.800, usado para testar viabilidade",
        ],
        missing=MISSING_COMMON + ["amostra do comentário público", "adequação contratual individual", "resultado posterior do plano"],
        metrics={"viewsObserved":366,"likesObserved":32,"commentsObserved":1},
        classification=cls(
            material="video_longo", presentations=["tutorial","demonstracao"], primary="educativo",
            secondary=["explicativo","demonstracao"],
            mix=[{"family":"educativo","percentage":50},{"family":"explicativo","percentage":30},{"family":"demonstracao","percentage":20}],
            objectives=["educar","consciencia_problema","apresentar_solucao"],
            topic="levantamento preenchido de dívidas", segment="finanças pessoais", subsegment="diagnóstico de dívida por planilha",
            audience="adultos endividados que precisam mapear compromissos", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio","aversao_perda"], hooks=["problema","promessa"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","tratamento_objecao"],
            cta=["clicar","seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"produto","name":"planilha de levantamento de dívidas","confidence":"high"},
            evidence=[
                "A descrição pede primeiro saber para quem e quanto se deve.",
                "A fala separa saldo, atraso, juros e parcela antes de confrontar o compromisso com a renda.",
                "O exemplo de R$ 3.000 versus R$ 2.800 mostra inviabilidade sem prometer quitação.",
            ],
        ),
        comparison={"level":1,"group":FINANCE_GROUP,"referenceIds":["obs-20260930-226","obs-20260930-228"],"confidence":"high"},
        observations=[
            "O levantamento transforma dívida abstrata em campos específicos antes da negociação.",
            "Renda e compromisso mensal são comparados para testar se o plano cabe no orçamento.",
            "Versículos e links sociais são contexto editorial, não prova financeira.",
        ],
        interpretations=[
            "O teste de capacidade evita que uma planilha organizada seja confundida com plano viável.",
            "O procedimento é rastreável na fala; execução visual e resultado permanecem não medidos.",
        ],
        scores={"gancho":84,"clareza":96,"relevancia":95,"desejo":73,"confianca":86,"retencao":"not_assessed","acao":94,"objecoes":91},
        lenses={
            "apressado":"Recebe uma primeira tarefa e os campos mínimos.",
            "analitico":"Encontra saldo, atraso, juros, parcela e teste de capacidade.",
            "aspiracional":"Visualiza um diagnóstico antes da negociação.",
            "comunidade":"Um comentário foi indicado, mas não amostrado.",
            "cetico":"Vê o limite do plano quando os compromissos quase consomem a renda.",
        },
        replicable=["Mapear credor, saldo, atraso, juros e parcela.","Comparar compromissos mensais com renda disponível.","Usar o exemplo para revelar inviabilidade, não para prometer sucesso."],
        contingent=["Contratos e negociações exigem revisão individual.","O único comentário não foi amostrado.","Audiovisual e resultado não foram medidos."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"levantamento e exemplo ligam dívida, juros, parcela e renda na fala","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260930-228",
        title="Dica de Orçamento Pessoal: Calcule a Média para Estimar as Despesas",
        creator="Liivre", identity="liivre",
        url="https://www.youtube.com/watch?v=ZVRg23Tkup8",
        published="2018-02-10", duration="PT3M10S",
        accessible=[
            "título, criador, descrição pública integral de 1.926 caracteres e data exata",
            "duração de 3 minutos e 10 segundos, 20 visualizações e uma curtida pública; contagem de comentários não acessível",
            "transcrição automática integral em português até 3 minutos e 8 segundos; fala acessível somente por substituição textual",
            "exemplo preenchido de R$ 1.200 em 12 meses com média mensal de R$ 100 e média por ocorrência de R$ 400",
            "procedimento falado e descrito para despesas mensais, anuais e esporádicas com data incerta",
        ],
        missing=MISSING_COMMON + ["renda, dívida, juros e parcela no exemplo", "teste contemporâneo do método"],
        metrics={"viewsObserved":20,"likesObserved":1,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_curto", presentations=["tutorial"], primary="explicativo",
            secondary=["educativo","demonstracao"],
            mix=[{"family":"explicativo","percentage":45},{"family":"educativo","percentage":35},{"family":"demonstracao","percentage":20}],
            objectives=["educar","apresentar_solucao","salvamento"],
            topic="média histórica para estimar despesas", segment="finanças pessoais", subsegment="orçamento de despesas recorrentes e esporádicas",
            audience="adultos montando orçamento anual", awareness="consciente_solucao",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio"], hooks=["problema","numero"],
            narrative=["problema","mecanismo","progressao","conclusao"], proof=["mecanismo_explicado","dado"],
            cta=[], advertising="editorial_organico", intent="ausente",
            entity={"kind":"marca","name":"Liivre","confidence":"high"},
            evidence=[
                "Descrição e fala apresentam o mesmo exemplo aritmético preenchido.",
                "Os últimos doze meses funcionam como baseline antes de projetar despesas.",
                "O exemplo não inclui dívida nem demonstra resultado posterior.",
            ],
        ),
        comparison={"level":2,"group":FINANCE_GROUP,"referenceIds":["obs-20260930-226","obs-20260930-227"],"confidence":"medium"},
        observations=[
            "O baseline histórico antecede a estimativa de gastos futuros.",
            "A distinção entre média mensal e por ocorrência evita aplicar o mesmo número a despesas com cadências diferentes.",
            "É apoio de nível 2 porque não trata dívida, juros ou capacidade de pagamento.",
        ],
        interpretations=[
            "Um exemplo aritmético preenchido torna a regra verificável antes da aplicação.",
            "A transferência para dívida é parcial e não autoriza generalização de eficácia.",
        ],
        scores={"gancho":78,"clareza":96,"relevancia":89,"desejo":69,"confianca":88,"retencao":"not_assessed","acao":91,"objecoes":82},
        lenses={
            "apressado":"Recebe um cálculo curto e uma regra de lançamento.",
            "analitico":"Consegue refazer R$ 1.200 por 12 meses e por três ocorrências.",
            "aspiracional":"Visualiza um orçamento anual menos improvisado.",
            "comunidade":"Comentários não ficaram acessíveis.",
            "cetico":"Reconhece um cálculo correto, mas não vê resultado ou dívida.",
        },
        replicable=["Começar pelo histórico observável.","Preencher um cálculo simples antes de recomendar.","Separar média mensal de média por ocorrência."],
        contingent=["Apoio funcional de nível 2, não evidência sobre quitação.","Método de 2018 não foi testado contemporaneamente.","Audiovisual e resultado não foram medidos."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"baseline e exemplo preenchido tornam a estimativa de despesas auditável","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260930-229",
        title="Como Economizei R$ 5.000 em 6 Meses com Esta Planilha de Gastos | Educação Financeira",
        creator="Direto Ao Ponto", identity="direto-ao-ponto-jovem",
        url="https://www.youtube.com/watch?v=CnmrTHR3uKw",
        published="2025-09-02", duration="PT4M7S",
        accessible=[
            "título, criador, descrição pública integral de 2.525 caracteres e data exata",
            "duração de 4 minutos e 7 segundos, 29 visualizações, uma curtida e um comentário público indicados",
            "descrição com alegação de R$ 5.000 em seis meses, sistema de três categorias, quinze minutos semanais e resultados mensais declarados",
            "link para planilha, grupo VIP de WhatsApp e CTA comercial",
        ],
        missing=MISSING_COMMON + ["transcrição ou legenda acessível", "renda e despesas essenciais do baseline", "registros brutos, recibos ou extratos", "amostra do comentário"],
        metrics={"viewsObserved":29,"likesObserved":1,"commentsObserved":1},
        classification=cls(
            material="video_curto", presentations=["estudo_caso","tutorial"], primary="prova_estudo_caso",
            secondary=["educativo","oferta_direta"],
            mix=[{"family":"prova_estudo_caso","percentage":45},{"family":"educativo","percentage":30},{"family":"oferta_direta","percentage":25}],
            objectives=["venda","apresentar_solucao","educar","trafego"],
            topic="alegação de economia com planilha", segment="finanças pessoais", subsegment="controle de gastos com template",
            audience="iniciantes que querem economizar por planilha", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["desejo","prova_social","urgencia"], hooks=["numero","promessa","resultado_antecipado"],
            narrative=["promessa","progressao","prova","cta"], proof=["alegacao_sem_prova","ausencia_prova_necessaria"],
            cta=["clicar","comentar","seguir"], advertising="oferta_direta", intent="explicita",
            entity={"kind":"produto","name":"planilha e grupo VIP","confidence":"high"},
            evidence=[
                "A descrição declara valores mensais e total de R$ 5.000.",
                "Os valores mínimos explicitados somam R$ 4.600; os meses quatro a seis são descritos como R$ 1.000 ou mais.",
                "Baseline, registros e audiovisual não ficaram acessíveis para auditar a causalidade da planilha.",
            ],
        ),
        comparison={"level":2,"group":FINANCE_GROUP,"referenceIds":["obs-20260930-226","obs-20260930-227","obs-20260930-228"],"confidence":"high"},
        observations=[
            "Há promessa numérica, etapas declaradas e oferta de template, mas não baseline de renda e despesas essenciais.",
            "A descrição informa R$ 300, R$ 500, R$ 800 e R$ 1.000 ou mais nos três meses seguintes; o total exato depende dos valores não discriminados.",
            "Sem registros brutos e transcrição, a economia não pode ser atribuída à planilha.",
        ],
        interpretations=[
            "É caso-limite: números declarados e um procedimento prometido não substituem baseline e prova de resultado.",
            "Oferta, urgência e métricas permanecem contexto comercial.",
        ],
        scores={"gancho":94,"clareza":82,"relevancia":89,"desejo":91,"confianca":38,"retencao":"not_assessed","acao":88,"objecoes":35},
        lenses={
            "apressado":"Recebe uma promessa numérica e um template.",
            "analitico":"Pede baseline, dados brutos e reconciliação do total.",
            "aspiracional":"É atraído por economia rápida e rotina curta.",
            "comunidade":"Um comentário foi indicado, mas não amostrado.",
            "cetico":"Não aceita a planilha como causa sem registros comparáveis.",
        },
        replicable=["Declarar categorias e rotina de atualização.","Discriminar cada período quando houver total acumulado.","Apresentar baseline e registros antes de atribuir resultado."],
        contingent=["Alegação de economia não foi auditada.","O CTA leva a produto e grupo próprios.","Transcrição, audiovisual e comentário não ficaram acessíveis."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"a descrição declara rotina, valores mensais e economia total","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
            {"claim":"a planilha causou economia de R$ 5.000","requiredModalities":["baseline","raw_records","outcome","comparison"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_and_full_description_only",
    ),
    build_ref(
        id="obs-20260930-230",
        title="O desvio mágico da água (energia estática)",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=qVgU_e8c4zM",
        published="2011-11-01", duration="PT2M59S",
        accessible=[
            "título, criador, descrição pública integral de 1.186 caracteres e data exata",
            "duração de 2 minutos e 59 segundos, 596.611 visualizações, 12.426 curtidas e 816 comentários públicos indicados",
            "descrição classifica o material como experiência simples e identifica créditos de produção",
        ],
        missing=MISSING_COMMON + ["transcrição ou legenda acessível", "materiais", "procedimento", "resultado visual", "explicação científica", "amostra de comentários", "orientação de segurança"],
        metrics={"viewsObserved":596611,"likesObserved":12426,"commentsObserved":816},
        classification=cls(
            material="video_curto", presentations=["demonstracao"], primary="demonstracao",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":30},{"family":"curiosidade","percentage":20}],
            objectives=["educar","visualizacao","compartilhamento"],
            topic="desvio de água por eletricidade estática", segment="educação científica", subsegment="experimento doméstico de eletrostática",
            audience="estudantes e famílias interessados em experiências", awareness="consciente_solucao",
            production="intermediate", scale="large", replicability="unknown", duration="over_60s",
            mechanisms=["curiosidade","surpresa"], hooks=["textual","demonstracao_antecipada"],
            narrative=[], proof=["indeterminado"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"marca","name":"Manual do Mundo","confidence":"high"},
            evidence=[
                "Título e descrição identificam apenas o fenômeno, a natureza de experiência e os créditos.",
                "Sem fala, mídia ou procedimento acessível, o experimento não foi ensinado.",
                "Popularidade e escala não substituem cobertura do conteúdo.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de demonstração científica doméstica","referenceIds":[],"confidence":"low"},
        observations=[
            "A embalagem nomeia um fenômeno específico de energia estática.",
            "Materiais, execução, resultado e explicação não ficaram acessíveis; nenhuma inferência de cena foi feita.",
        ],
        interpretations=["Cobertura insuficiente para ensinar a referência ou criar hipótese."],
        scores={"gancho":82,"clareza":74,"relevancia":"not_assessed","desejo":"not_assessed","confianca":"not_assessed","retencao":"not_assessed","acao":"not_assessed","objecoes":"not_assessed"},
        lenses={
            "apressado":"Entende apenas o fenômeno prometido.",
            "analitico":"Não encontra procedimento ou mecanismo acessível.",
            "aspiracional":"Não avaliado além da embalagem.",
            "comunidade":"Contagem existe; comentários não foram amostrados.",
            "cetico":"Recusa aprender sem mídia, fala ou descrição substantiva.",
        },
        replicable=[],
        contingent=["Nenhum princípio de execução foi extraído.","Métricas e fama são apenas contexto.","A referência não gera hipótese."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a publicação promete uma experiência de energia estática com água","requiredModalities":["metadata","description"],"observedModalities":["metadata","description"],"sufficient":True},
            {"claim":"o procedimento e o resultado demonstram o fenômeno","requiredModalities":["video","audio_or_transcript"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_and_non_substantive_description_only",
    ),
]

# O primeiro apoio usa uma história de terceiro; a proveniência precisa substituir o padrão editorial genérico.
refs[0]["training"]["provenanceAndConsent"] = {
    "storyOrigin": "caso de pessoa atendida ou conhecida pela criadora, segundo a fala pública",
    "consentStatus": "creator_asserted_not_independently_documented",
    "identityProtection": "nome e documentos deliberadamente não mostrados, segundo a fala",
    "evidence": ["a criadora afirma ter pedido autorização e explica a ocultação dos dados"],
}

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 042")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260930-226", "obs-20260930-227", "obs-20260930-228"]
new_case = "obs-20260930-229"
pattern["statement"] = "Em educação financeira para iniciantes, nomear um problema concreto e organizar a resposta em etapas finitas torna problema, caminho e próxima ação identificáveis; em conteúdos sobre dívida, explicitar renda, despesas essenciais, saldo, juros, parcelas e capacidade de pagamento — de preferência em um exemplo preenchido — torna o caminho auditável e delimita ações viáveis. Resultado declarado sem baseline e registros comparáveis, ou cortes universais sem preservar necessidades essenciais, eleva o ônus de prova; compreensão e resultado financeiro permanecem não medidos."
pattern["name"] = pattern["statement"]
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 17
pattern["supportingCount"] = 17
pattern["caseLimitCount"] = 4
pattern["creatorDiversityCount"] = 17
pattern["sourceDiversityCount"] = 17
pattern["conditions"] = [
    "conteúdo educativo de finanças pessoais para iniciantes",
    "problema financeiro concreto identificado",
    "caminho organizado em etapas finitas",
    "em dívida, renda, despesas essenciais, saldo, juros, parcelas e capacidade de pagamento explicitados quando aplicáveis",
    "exemplo preenchido ou baseline observável antecede a recomendação quando há promessa numérica",
    "ações preservam necessidades essenciais e são proporcionais ao baseline",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260930-226","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Caso declarado real preenche renda, despesas, cartões e compromissos antes de avaliar capacidade.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["sem audiovisual, juros completos, resultado ou consentimento independente"]},
    {"referenceId":"obs-20260930-227","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Credor, saldo, atraso, juros e parcela são comparados à renda em exemplo preenchido.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["sem execução visual ou resultado posterior"]},
    {"referenceId":"obs-20260930-228","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Histórico de doze meses e cálculo preenchido tornam a estimativa de despesas auditável.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["não trata dívida, juros ou resultado"]},
    {"referenceId":"obs-20260930-229","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Resultado de R$ 5.000 e rotina são declarados, mas baseline, registros brutos e causalidade não estão acessíveis.","evidence":"Metadados e descrição integral.","limitations":["não conta como apoio nem contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Dezessete apoios vêm de dezessete criadores e fontes; demonstram recorrência estrutural, não compreensão ou resultado financeiro.",
    "Nenhuma referência oferece retenção, experimento causal ou acompanhamento comparável de resultado.",
    "Comentários, métricas, fama, escala, produção e ofertas permanecem contexto não causal.",
    "O quarto caso-limite mostra que resultado declarado sem baseline e registros não prova contribuição do mecanismo.",
    "Conselhos financeiros exigem adequação individual, revisão humana e avaliação de riscos e contratos.",
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 134,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260930-230"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=gHUvtRznLfc","reason":"comparabilidade financeira útil, mas os três apoios escolhidos trazem maior cobertura de exemplo preenchido e baseline"},
        {"url":"https://www.youtube.com/watch?v=UiR9cRtbBY0","reason":"estrutura comparável, mas diversidade de mecanismo inferior ao conjunto selecionado"},
        {"url":"https://www.youtube.com/watch?v=pCbRpuFWlrM","reason":"cobertura pública inferior aos apoios finais"},
        {"url":"https://www.youtube.com/watch?v=XwOOcibCE1M","reason":"cobertura pública inferior aos apoios finais"},
        {"url":"https://www.youtube.com/watch?v=moLLIg1oUuA","reason":"regra 50-30-20 sem transcrição acessível nesta execução"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["educativo","demonstracao","explicativo","prova_estudo_caso","oferta_direta","curiosidade"],
    "coverageSummary": {"complete":0,"partial":4,"insufficient":1},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "as cinco tentativas de mídia e as cinco tentativas de capa retornaram HTML de indisponibilidade de 195 bytes; legendas nativas expostas em parte das páginas retornaram zero bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, execução visual, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":3,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":2,
        "limitation":"transcrições automáticas obtidas por serviço público substituem somente a fala e podem repetir ou errar palavras; duas referências ficaram sem transcrição acessível",
    },
    "commentsCoverage": {
        "countsOnly":3,
        "sampledReferences":0,
        "sampledComments":0,
        "zeroReturnedReferences":0,
        "unavailableReferences":2,
        "limitation":"nenhum comentário foi amostrado; ausência de cobertura não foi registrada como zero",
    },
    "baselineCoverage": {
        "sampledProfiles":2,
        "contemporaneousBaselines":0,
        "limitation":"dois exemplos preenchidos aparecem na fala, mas não formam coorte contemporânea ou baseline de desempenho",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["uma promessa numérica com etapas declaradas não demonstra contribuição causal sem baseline, registros e comparação"],
    "safetyFindings": [
        "nenhuma recomendação financeira foi tratada como adequada a todo perfil",
        "promessa, oferta, comentário, fama e métricas não foram tratados como prova de resultado",
        "o relato de terceiro registra autorização apenas como afirmação da criadora e preservação de identidade como prática observada na fala",
        "a demonstração científica não foi ensinada porque procedimento e resultado não ficaram acessíveis",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes elevam de quatorze para dezessete os apoios do padrão financeiro. Um caso-limite acrescenta a exigência de baseline e registros para promessas numéricas. O padrão permanece provisório.",
    "nextTarget": "explicador financeiro brasileiro recente e curto, de criador pequeno ou médio, com audiovisual integral, planilha visível e exemplo preenchido que ligue renda, despesas essenciais, saldo, juros, parcela e sobra viável; buscar teste de execução ou compreensão e um caso em que os cálculos contradigam o baseline",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Três transcrições automáticas integrais substituem somente a fala; duas referências ficaram sem transcrição.",
        "Nenhum comentário foi amostrado.",
        "Não houve baseline contemporâneo, retenção, teste de compreensão, adequação individual ou causalidade.",
        "A exploração científica teve cobertura insuficiente e não foi ensinada.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
