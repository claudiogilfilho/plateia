#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-042.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]
make_ref = ns["make_ref"]

NOW = "2026-10-01T11:08:37.000Z"
OBSERVED = "2026-10-01"
RUN_ID = "run-20261001-supervised-043"
PATTERN_ID = "pat-20260823-003"
BATCH_IDS = {f"obs-20261001-{n}" for n in range(231, 236)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

FINANCE_GROUP = "educação financeira brasileira para iniciantes que preenche entradas, despesas e saldo em planilha antes de recomendar uma próxima ação"
MISSING_COMMON = MISSING_AV + [
    "teste representativo de compreensão ou execução",
    "resultado financeiro dos espectadores",
]

refs = [
    build_ref(
        id="obs-20261001-231",
        title="Planilha para Controle de Despesas Mensais no Excel | Super Simples de Fazer!",
        creator="Excelente João", identity="excelente-joao",
        url="https://www.youtube.com/watch?v=F737hQiZRwg",
        published="2024-06-20", duration="PT10M",
        accessible=[
            "título, criador, descrição pública integral de 2.031 caracteres e data exata",
            "duração pública de 10 minutos, 257.265 visualizações, 8.249 curtidas e 270 comentários indicados",
            "transcrição automática integral em português até 9 minutos e 58 segundos; fala acessível somente por substituição textual e com repetições do serviço",
            "exemplo falado de salário de R$ 2.000, hora extra de R$ 300, despesas, totais mensais e diferença entre entradas e saídas",
            "dez comentários públicos amostrados; uma dúvida sobre SOMASE e uma discussão sobre organização anual evidenciam barreiras de execução, sem teste representativo",
        ],
        missing=MISSING_COMMON + ["valores visuais completos das linhas preenchidas", "juros, dívida e capacidade de pagamento", "resultado após uso da planilha"],
        metrics={"viewsObserved":257265,"likesObserved":8249,"commentsObserved":270,"commentsSampled":10},
        classification=cls(
            material="video_longo", presentations=["tutorial","tela_gravada","demonstracao"], primary="demonstracao",
            secondary=["educativo","explicativo"],
            mix=[{"family":"demonstracao","percentage":45},{"family":"educativo","percentage":35},{"family":"explicativo","percentage":20}],
            objectives=["educar","apresentar_solucao","salvamento"],
            topic="planilha mensal de entradas, saídas e saldo", segment="finanças pessoais", subsegment="controle financeiro em Excel",
            audience="iniciantes que querem construir uma planilha de orçamento", awareness="preparado_agir",
            production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio"], hooks=["promessa","demonstracao_antecipada"],
            narrative=["promessa","mecanismo","progressao","conclusao","cta"], proof=["mecanismo_explicado","dado"],
            cta=["comentar","clicar"], advertising="geracao_de_leads", intent="explicita",
            entity={"kind":"produto","name":"curso de Excel e planilha","confidence":"high"},
            evidence=[
                "A fala começa pelo resultado da planilha e depois a reconstrói do zero.",
                "Salário, hora extra, despesas, totais e diferença são preenchidos ou calculados na fala.",
                "A tela não foi observada; os campos visuais são registrados apenas quando verbalizados.",
            ],
        ),
        comparison={"level":2,"group":FINANCE_GROUP,"referenceIds":["obs-20261001-232","obs-20261001-233"],"confidence":"high"},
        observations=[
            "Entradas e saídas são preenchidas antes de calcular totais e diferença por mês.",
            "A planilha muda o mês e atualiza os resultados, segundo a fala.",
            "Comentários amostrados revelam dúvidas de implementação; não demonstram aprendizagem geral.",
        ],
        interpretations=[
            "Preencher um caso simples antes de exibir o saldo torna o cálculo auditável na fala.",
            "A recorrência estrutural não prova que espectadores executaram corretamente ou melhoraram suas finanças.",
        ],
        scores={"gancho":88,"clareza":94,"relevancia":92,"desejo":76,"confianca":84,"retencao":"not_assessed","acao":93,"objecoes":82},
        lenses={
            "apressado":"Vê cedo o resultado prometido e o caminho de construção.",
            "analitico":"Consegue rastrear entradas, saídas, totais e diferença, mas não audita a tela.",
            "aspiracional":"Visualiza uma rotina financeira menos improvisada.",
            "comunidade":"Dúvidas concretas de fórmula e estrutura aparecem na amostra.",
            "cetico":"Separa cálculo verbalizado de execução visual e resultado financeiro.",
        },
        replicable=["Preencher entradas e saídas antes de aconselhar.","Calcular total e diferença por período.","Antecipar o resultado e reconstruir o caminho."],
        contingent=["Oferta de curso e métricas são contexto.","Comentários não são amostra representativa.","Audiovisual, retenção e resultado não foram medidos."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"o exemplo falado liga entradas, despesas e diferença mensal","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_comment_sample",
    ),
    build_ref(
        id="obs-20261001-232",
        title="Planilha de Controle Financeiro - Download Gratuito (Atualizada 2025)",
        creator="Prof Ítalo Teotônio", identity="prof-italo-teotonio",
        url="https://www.youtube.com/watch?v=XRayCFDwrGo",
        published="2025-01-27", duration="PT4M38S",
        accessible=[
            "título, criador, descrição pública integral de 651 caracteres e data exata",
            "duração pública de 4 minutos e 38 segundos, 493.177 visualizações, 5.854 curtidas e 219 comentários indicados",
            "transcrição automática integral em português até 4 minutos e 35 segundos; fala acessível somente por substituição textual e com repetições do serviço",
            "exemplo falado que altera receita de janeiro de R$ 3.000 para R$ 5.000 e acrescenta despesa de R$ 500 antes de atualizar o painel",
            "vinte comentários públicos amostrados; dúvidas sobre limpar, localizar e preservar fórmulas da planilha indicam barreiras de execução",
        ],
        missing=MISSING_COMMON + ["painel e fórmulas visualmente confirmados", "separação entre despesas essenciais e não essenciais", "dívida, juros e resultado posterior"],
        metrics={"viewsObserved":493177,"likesObserved":5854,"commentsObserved":219,"commentsSampled":20},
        classification=cls(
            material="video_curto", presentations=["tutorial","tela_gravada","demonstracao"], primary="educativo",
            secondary=["demonstracao","oferta_direta"],
            mix=[{"family":"educativo","percentage":45},{"family":"demonstracao","percentage":35},{"family":"oferta_direta","percentage":20}],
            objectives=["educar","apresentar_solucao","lead"],
            topic="uso de planilha de receitas, despesas e saldo", segment="finanças pessoais", subsegment="dashboard financeiro em Excel",
            audience="iniciantes que querem baixar e adaptar uma planilha pronta", awareness="preparado_agir",
            production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio","recompensa"], hooks=["promessa","resultado_antecipado"],
            narrative=["promessa","mecanismo","prova","conclusao","cta"], proof=["mecanismo_explicado","dado","tratamento_objecao"],
            cta=["clicar"], advertising="geracao_de_leads", intent="explicita",
            entity={"kind":"produto","name":"planilha e curso gratuito","confidence":"high"},
            evidence=[
                "A fala apresenta cartões de receitas, despesas e saldo antes do procedimento.",
                "Dois valores são alterados e o painel é atualizado, segundo a transcrição.",
                "Comentários de uso relatam desconfiguração e dúvidas de limpeza; não foram tratados como taxa de falha.",
            ],
        ),
        comparison={"level":2,"group":FINANCE_GROUP,"referenceIds":["obs-20261001-231","obs-20261001-233"],"confidence":"high"},
        observations=[
            "Uma receita e uma despesa são alteradas antes da atualização do saldo.",
            "O arquivo é oferecido preenchido, o que ajuda a mostrar a estrutura e cria dúvidas sobre como limpá-lo.",
            "A transcrição explica a dependência de atualizar tabelas dinâmicas.",
        ],
        interpretations=[
            "Um microteste com valores preenchidos torna a relação entrada-despesa-saldo verificável na fala.",
            "Material pronto reduz a barreira inicial, mas comentários sugerem que limpeza e fórmulas exigem instrução adicional.",
        ],
        scores={"gancho":84,"clareza":92,"relevancia":91,"desejo":82,"confianca":83,"retencao":"not_assessed","acao":91,"objecoes":86},
        lenses={
            "apressado":"Recebe uma visão geral e um exemplo curto de atualização.",
            "analitico":"Consegue conferir os dois lançamentos falados e a necessidade de atualizar.",
            "aspiracional":"Vê um painel anual pronto para adaptação.",
            "comunidade":"Dúvidas de limpeza e fórmulas delimitam a facilidade prometida.",
            "cetico":"Não confunde download ou elogio com execução correta.",
        },
        replicable=["Mostrar um exemplo preenchido e depois alterá-lo.","Explicar a atualização necessária do painel.","Tratar dúvidas de limpeza e preservação de fórmulas."],
        contingent=["Download e curso próprio criam contexto comercial.","Comentários não medem taxa de sucesso.","A tela e o resultado financeiro não foram observados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"o exemplo falado altera receita, despesa e saldo no painel","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_comment_sample",
    ),
    build_ref(
        id="obs-20261001-233",
        title="PLANILHA DE ORGANIZAÇÃO FINANCEIRA GRÁTIS - Aprenda a organizar suas finanças!",
        creator="Primo Pobre", identity="primo-pobre",
        url="https://www.youtube.com/watch?v=SJ7-ImU4UYc",
        published="2023-03-16", duration="PT19M53S",
        accessible=[
            "título, criador, descrição pública integral de 2.491 caracteres e data exata",
            "duração pública de 19 minutos e 53 segundos, 1.751.052 visualizações, 95.977 curtidas e aproximadamente 2.000 comentários indicados",
            "transcrição automática integral em português até 19 minutos e 50 segundos; fala acessível somente por substituição textual e com repetições do serviço",
            "orçamento falado com duas rendas, benefícios, renda extra, despesas essenciais e não essenciais, total de R$ 4.112,90, entrada de R$ 5.130 e sobra de R$ 1.017",
            "vinte comentários públicos amostrados; dúvidas sobre baixar, editar e localizar a planilha delimitam execução sem provar falha geral",
        ],
        missing=MISSING_COMMON + ["planilha visualmente confirmada", "taxas de juros e dívidas", "adequação individual das recomendações e produtos citados"],
        metrics={"viewsObserved":1751052,"likesObserved":95977,"commentsObserved":2000,"commentsSampled":20},
        classification=cls(
            material="video_longo", presentations=["camera_direta","tutorial","tela_gravada"], primary="explicativo",
            secondary=["educativo","oferta_direta"],
            mix=[{"family":"explicativo","percentage":45},{"family":"educativo","percentage":40},{"family":"oferta_direta","percentage":15}],
            objectives=["educar","consciencia_problema","apresentar_solucao","venda"],
            topic="orçamento familiar preenchido", segment="finanças pessoais", subsegment="renda, despesas essenciais, saldo e reserva",
            audience="adultos de baixa ou média renda organizando o orçamento familiar", awareness="preparado_agir",
            production="simple", scale="large", replicability="high", duration="over_60s",
            mechanisms=["aversao_perda","confianca","alivio"], hooks=["problema","risco"],
            narrative=["problema","progressao","mecanismo","prova","conclusao","cta"], proof=["mecanismo_explicado","dado","tratamento_objecao"],
            cta=["clicar","seguir"], advertising="parceria_com_criador", intent="explicita",
            entity={"kind":"produto","name":"planilha, seguro parceiro e conteúdos próprios","confidence":"high"},
            evidence=[
                "A fala preenche duas rendas, benefícios e renda extra antes das despesas.",
                "Despesas essenciais e não essenciais são somadas antes de calcular a sobra.",
                "Seguro e conteúdos próprios aparecem no percurso; parceria e escala não foram tratadas como prova.",
            ],
        ),
        comparison={"level":1,"group":FINANCE_GROUP,"referenceIds":["obs-20261001-231","obs-20261001-232"],"confidence":"high"},
        observations=[
            "A renda total de R$ 5.130 antecede despesas essenciais e não essenciais de R$ 4.112,90 e sobra de R$ 1.017.",
            "A sobra leva a uma decisão local de aumentar investimento, enquanto um saldo negativo levaria a cortar gastos ou aumentar renda.",
            "O exemplo preserva moradia, saúde e outras necessidades na categorização, embora a adequação individual não tenha sido testada.",
        ],
        interpretations=[
            "O orçamento preenchido conecta baseline, categorias, saldo e próxima ação de forma rastreável na fala.",
            "Tom prescritivo, parceria e escala são condições contingentes, não prova causal.",
        ],
        scores={"gancho":89,"clareza":95,"relevancia":95,"desejo":80,"confianca":78,"retencao":"not_assessed","acao":94,"objecoes":88},
        lenses={
            "apressado":"Encontra a distinção entre entrada, despesa e sobra.",
            "analitico":"Consegue refazer os totais falados e seguir a decisão sobre a sobra.",
            "aspiracional":"Visualiza uma família saindo da desorganização para um plano.",
            "comunidade":"Dúvidas de acesso e edição aparecem na amostra.",
            "cetico":"Exige adequação individual para seguro, investimento e renda extra.",
        },
        replicable=["Preencher renda antes das despesas.","Separar essenciais e não essenciais.","Ligar o saldo a uma próxima ação proporcional."],
        contingent=["Parceria e oferta foram registradas separadamente.","O exemplo não inclui juros ou dívida.","Comentários, audiovisual e resultado não demonstram eficácia."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"o orçamento falado liga renda, despesas essenciais, saldo e próxima ação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_comment_sample",
    ),
    build_ref(
        id="obs-20261001-234",
        title="$ COMO FAZER UMA PLANILHA FINANCEIRA PARA SEUS GASTOS MENSAIS PELO CELULAR",
        creator="Manual Tech", identity="manual-tech",
        url="https://www.youtube.com/watch?v=lRj63pOI-Tk",
        published="2021-05-02", duration="PT7M30S",
        accessible=[
            "título, criador, descrição pública integral de 819 caracteres e data exata",
            "duração pública de 7 minutos e 30 segundos, 228.262 visualizações, 7.295 curtidas e 168 comentários indicados",
            "transcrição automática integral em português até 7 minutos e 24 segundos; fala acessível somente por substituição textual e com repetições do serviço",
            "passo a passo falado no Google Planilhas pelo celular com data, descrição, valor, alimentação, luz e soma das despesas",
            "dez comentários públicos amostrados; há indicação de versão atualizada e dúvidas sobre aplicativo gratuito, sem teste representativo",
        ],
        missing=MISSING_COMMON + ["renda ou receitas", "saldo ou sobra", "separação de despesas essenciais", "dívida, juros, parcela e capacidade", "execução visual confirmada"],
        metrics={"viewsObserved":228262,"likesObserved":7295,"commentsObserved":168,"commentsSampled":10},
        classification=cls(
            material="video_longo", presentations=["tutorial","tela_gravada","demonstracao"], primary="demonstracao",
            secondary=["educativo"],
            mix=[{"family":"demonstracao","percentage":60},{"family":"educativo","percentage":40}],
            objectives=["educar","apresentar_solucao"],
            topic="planilha móvel de despesas", segment="finanças pessoais", subsegment="registro de gastos no Google Planilhas",
            audience="iniciantes que só dispõem de celular", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["alivio","confianca"], hooks=["promessa"],
            narrative=["promessa","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado"],
            cta=["comentar","seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"produto","name":"Google Planilhas","confidence":"high"},
            evidence=[
                "A fala constrói campos de data, descrição e valor e soma despesas domésticas.",
                "Nenhuma receita, renda ou sobra é preenchida na transcrição.",
                "Sem renda, o total de despesas não testa capacidade de pagamento.",
            ],
        ),
        comparison={"level":2,"group":FINANCE_GROUP,"referenceIds":["obs-20261001-231","obs-20261001-232","obs-20261001-233"],"confidence":"high"},
        observations=[
            "O tutorial resolve o registro e a soma de despesas no celular.",
            "A planilha falada não contém o lado das receitas nem calcula sobra.",
            "A referência delimita a diferença entre registrar gastos e avaliar capacidade financeira.",
        ],
        interpretations=[
            "É caso-limite: uma tabela de despesas pode ser útil sem preencher os requisitos de orçamento auditável do padrão.",
            "Não é contraexemplo de eficácia; apenas não mede se os gastos cabem na renda.",
        ],
        scores={"gancho":82,"clareza":89,"relevancia":86,"desejo":71,"confianca":77,"retencao":"not_assessed","acao":88,"objecoes":57},
        lenses={
            "apressado":"Recebe um caminho executável pelo celular.",
            "analitico":"Vê soma de gastos, mas não encontra receita ou saldo.",
            "aspiracional":"Visualiza controle básico sem computador.",
            "comunidade":"Amostra aponta versão atualizada e dúvidas de aplicativo.",
            "cetico":"Não confunde soma de despesas com orçamento viável.",
        },
        replicable=["Reduzir a ferramenta ao dispositivo disponível.","Registrar data, categoria e valor.","Distinguir planilha de gastos de orçamento completo."],
        contingent=["A interface de 2021 não foi revalidada visualmente.","A versão atualizada citada não foi analisada.","Não conta como apoio nem como contraexemplo de eficácia."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"o tutorial falado registra e soma despesas no celular","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a planilha mede capacidade de pagamento","requiredModalities":["income","expenses","balance"],"observedModalities":["expenses"],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_comment_sample",
    ),
    build_ref(
        id="obs-20261001-235",
        title="3 SALADAS DE BATATA PARA FAZER EM CASA | Receitas Comentadas da Tastemade Brasil",
        creator="Tastemade Brasil", identity="tastemade-brasil",
        url="https://www.youtube.com/watch?v=TWJSb5MDNhw",
        published="2020-10-14", duration="PT4M25S",
        accessible=[
            "título, criador, descrição pública integral de 332 caracteres e data exata",
            "duração pública de 4 minutos e 25 segundos, 8.125 visualizações, 936 curtidas e 17 comentários indicados",
            "transcrição automática integral em português até 4 minutos e 17 segundos; fala acessível somente por substituição textual e com repetições do serviço",
            "sequência falada de três saladas, incluindo maionese de leite, alertas sobre fogo baixo e dessalga e alternativas de ingredientes",
            "os 17 comentários públicos foram amostrados; dúvidas sobre cenoura crua e consistência mostram lacunas pontuais, sem teste de execução",
        ],
        missing=MISSING_COMMON + ["quantidades completas dos ingredientes", "execução visual", "textura e ponto observados", "resultado final provado ou degustado", "segurança alimentar validada"],
        metrics={"viewsObserved":8125,"likesObserved":936,"commentsObserved":17,"commentsSampled":17},
        classification=cls(
            material="video_curto", presentations=["tutorial","demonstracao","camera_direta"], primary="demonstracao",
            secondary=["educativo","entretenimento"],
            mix=[{"family":"demonstracao","percentage":55},{"family":"educativo","percentage":30},{"family":"entretenimento","percentage":15}],
            objectives=["educar","salvamento","compartilhamento"],
            topic="três variações de salada de batata", segment="culinária", subsegment="receita comentada",
            audience="pessoas buscando acompanhamentos para almoço em família", awareness="preparado_agir",
            production="intermediate", scale="large", replicability="unknown", duration="over_60s",
            mechanisms=["desejo","aproximacao","alivio"], hooks=["numero","promessa"],
            narrative=["promessa","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","ausencia_prova_necessaria"],
            cta=["comentar"], advertising="conteudo_de_marca", intent="implicita",
            entity={"kind":"marca","name":"Tastemade Brasil","confidence":"high"},
            evidence=[
                "A fala percorre três receitas e verbaliza alguns tempos, cuidados e substituições.",
                "A descrição direciona para receitas completas; quantidades não aparecem na transcrição acessível.",
                "Sem vídeo, textura, ponto e resultado visual não foram ensinados.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de receita comentada com três variações","referenceIds":[],"confidence":"medium"},
        observations=[
            "A estrutura repete variação, sequência, cuidado e substituição em três receitas.",
            "Dúvidas dos comentários apontam passos que a fala não resolve completamente.",
            "A referência não foi ensinada como receita completa porque quantidades e execução visual faltaram.",
        ],
        interpretations=["A cobertura sustenta somente uma observação estrutural; nenhuma hipótese ou padrão foi criado."],
        scores={"gancho":82,"clareza":78,"relevancia":84,"desejo":80,"confianca":68,"retencao":"not_assessed","acao":61,"objecoes":72},
        lenses={
            "apressado":"Entende que receberá três variações rápidas.",
            "analitico":"Encontra sequência e cuidados, mas faltam quantidades e validação visual.",
            "aspiracional":"Visualiza variedade para o almoço, sem ponto final observado.",
            "comunidade":"Dúvidas de ingrediente e textura aparecem na amostra completa de comentários.",
            "cetico":"Recusa tratar a descrição verbal como prova do resultado culinário.",
        },
        replicable=["Nomear cada variação antes dos passos.","Verbalizar cuidados de fogo, dessalga e substituição.","Responder dúvidas de ingrediente diretamente no material."],
        contingent=["Quantidades completas estavam fora da cobertura.","Produção, marca e métricas não provam utilidade.","Execução, textura, sabor e resultado não foram medidos."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a fala organiza três variações e alguns cuidados de execução","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"as receitas completas chegam ao ponto e textura prometidos","requiredModalities":["video","ingredient_quantities","execution","result"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_complete_comment_sample",
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 043")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20261001-231", "obs-20261001-232", "obs-20261001-233"]
new_case = "obs-20261001-234"
pattern["statement"] = "Em educação financeira para iniciantes, nomear um problema concreto e organizar a resposta em etapas finitas torna problema, caminho e próxima ação identificáveis; em conteúdos sobre dívida, explicitar renda, despesas essenciais, saldo, juros, parcelas e capacidade de pagamento — de preferência em um exemplo preenchido — torna o caminho auditável e delimita ações viáveis. Em planilhas de orçamento, somar despesas sem preencher renda e saldo não demonstra capacidade de pagamento. Resultado declarado sem baseline e registros comparáveis, ou cortes universais sem preservar necessidades essenciais, eleva o ônus de prova; compreensão e resultado financeiro permanecem não medidos."
pattern["name"] = pattern["statement"]
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 20
pattern["supportingCount"] = 20
pattern["caseLimitCount"] = 5
pattern["creatorDiversityCount"] = 20
pattern["sourceDiversityCount"] = 20
pattern["conditions"] = [
    "conteúdo educativo de finanças pessoais para iniciantes",
    "problema financeiro concreto identificado",
    "caminho organizado em etapas finitas",
    "em planilhas de orçamento, renda, despesas e saldo preenchidos antes da próxima ação",
    "em dívida, despesas essenciais, juros, parcelas e capacidade de pagamento explicitados quando aplicáveis",
    "exemplo preenchido ou baseline observável antecede a recomendação quando há promessa numérica",
    "ações preservam necessidades essenciais e são proporcionais ao baseline",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20261001-231","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Entradas, saídas, totais e diferença são preenchidos e calculados na fala antes do uso mensal.","evidence":"Metadados, descrição integral, transcrição automática integral e dez comentários amostrados.","limitations":["sem audiovisual, dívida, juros ou resultado financeiro"]},
    {"referenceId":"obs-20261001-232","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Receita e despesa preenchidas são alteradas antes da atualização do painel e do saldo.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários amostrados.","limitations":["sem confirmação visual ou teste representativo de execução"]},
    {"referenceId":"obs-20261001-233","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Renda, essenciais, não essenciais, saldo e próxima ação aparecem em um orçamento falado preenchido.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários amostrados.","limitations":["sem audiovisual, juros, adequação individual ou resultado"]},
    {"referenceId":"obs-20261001-234","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"A planilha registra e soma despesas, mas não contém renda ou saldo e por isso não mede capacidade.","evidence":"Metadados, descrição integral, transcrição automática integral e dez comentários amostrados.","limitations":["não conta como apoio nem como contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Vinte apoios vêm de vinte criadores e fontes; demonstram recorrência estrutural, não compreensão ou resultado financeiro.",
    "Nenhuma referência oferece retenção, experimento causal ou acompanhamento comparável de resultado.",
    "Comentários, métricas, fama, escala, produção, downloads e ofertas permanecem contexto não causal.",
    "O quinto caso-limite mostra que somar despesas sem renda e saldo não testa capacidade de pagamento.",
    "Conselhos financeiros exigem adequação individual, revisão humana e avaliação de riscos e contratos.",
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 58,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20261001-235"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=8cPE9bOHXrw","reason":"transcrição pública expirou nesta execução e a cobertura ficou inferior aos apoios escolhidos"},
        {"url":"https://www.youtube.com/watch?v=xyNfNGS1H68","reason":"conteúdo sobre dívida tem transcrição integral, mas não oferece planilha preenchida comparável ao alvo específico"},
        {"url":"https://www.youtube.com/watch?v=CB5zuxQl5ro","reason":"exemplo hipotético de poupança não preenche despesas essenciais e saldo com a granularidade dos apoios finais"},
        {"url":"https://www.youtube.com/watch?v=3o-IZl6fNBM","reason":"tutorial de aplicativo tem menor comparabilidade funcional com planilha preenchida de orçamento"},
        {"url":"https://www.youtube.com/watch?v=sI63SIeBFfo","reason":"exploração culinária com cobertura pública inferior à receita comentada selecionada"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["demonstracao","educativo","explicativo","oferta_direta","entretenimento"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "as cinco tentativas de vídeo e as cinco tentativas de capa produziram somente HTML de indisponibilidade de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, execução visual, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":5,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":0,
        "limitation":"as cinco transcrições automáticas substituem somente a fala e repetem trechos ou podem errar palavras; nenhuma cena, tela ou áudio foi inferido delas",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":5,
        "sampledComments":77,
        "zeroReturnedReferences":0,
        "unavailableReferences":0,
        "limitation":"as amostras são públicas, convenientes e não representativas; dúvidas não foram convertidas em taxa de falha",
    },
    "baselineCoverage": {
        "sampledProfiles":3,
        "contemporaneousBaselines":0,
        "limitation":"três exemplos preenchidos aparecem na fala, mas não formam coorte contemporânea nem acompanhamento de desempenho",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["uma planilha de despesas sem renda e saldo organiza gastos, mas não demonstra capacidade de pagamento"],
    "safetyFindings": [
        "nenhuma recomendação financeira foi tratada como adequada a todo perfil",
        "parcerias, ofertas, comentários, fama e métricas não foram tratados como prova de resultado",
        "a receita não foi ensinada como completa porque quantidades, execução e resultado visual não ficaram acessíveis",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes elevam de dezessete para vinte os apoios do padrão financeiro. Um caso-limite acrescenta que planilha de despesas sem renda e saldo não mede capacidade. O padrão permanece provisório.",
    "nextTarget": "explicador financeiro brasileiro recente e curto, de criador pequeno ou médio, com audiovisual integral, planilha visível e teste de execução por usuários; priorizar dívida com renda, despesas essenciais, saldo, juros, parcela e sobra viável e buscar um caso em que a fórmula ou o saldo contradiga a recomendação",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Cinco transcrições automáticas integrais substituem somente a fala e contêm repetições do serviço.",
        "Setenta e sete comentários foram amostrados sem representatividade estatística.",
        "Não houve baseline contemporâneo, retenção, teste representativo, adequação individual ou causalidade.",
        "A exploração culinária teve cobertura parcial e não foi ensinada como receita completa.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
