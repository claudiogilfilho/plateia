#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-043.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]
make_ref = ns["make_ref"]

NOW = "2026-10-02T11:43:22.000Z"
OBSERVED = "2026-10-02"
RUN_ID = "run-20261002-supervised-044"
PATTERN_ID = "pat-20260829-007"
BATCH_IDS = {f"obs-20261002-{n}" for n in range(236, 241)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

GROUP = "prova comercial B2B brasileira com cliente identificável, estado anterior, intervenção e resultado comparável"
MISSING_COMMON = MISSING_AV + [
    "auditoria independente dos resultados",
    "método de cálculo completo e intervalo de incerteza",
    "teste representativo de compreensão ou confiança",
    "atribuição causal isolada da intervenção",
]

refs = [
    build_ref(
        id="obs-20261002-236",
        title="Case de Sucesso | Ribeiro Ferramentaria reduz em 30% o tempo de desbaste com uso do WORKNC",
        creator="SKA", identity="ska-oficial",
        url="https://www.youtube.com/watch?v=oQ1xZLm9bY0",
        published="2024-12-03", duration="PT5M8S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 5 minutos e 8 segundos, 931 visualizações, 24 curtidas e um comentário indicados em 2 de outubro de 2026",
            "transcrição automática integral em português até 5 minutos; fala acessível somente por substituição textual",
            "voz do fundador da Ribeiro, histórico da empresa, comparação com o software anterior, teste prévio, intervenção WORKNC e percentuais por etapa",
            "um comentário público amostrado; ele deseja sucesso e não testa a alegação",
        ],
        missing=MISSING_COMMON + ["datas exatas do teste e janela de medição", "volumes absolutos de produção antes e depois"],
        metrics={"viewsObserved":931,"likesObserved":24,"commentsObserved":1,"commentsSampled":1},
        classification=cls(
            material="video_longo", presentations=["depoimento","estudo_caso","narracao_imagens"], primary="prova_estudo_caso",
            secondary=["demonstracao","institucional"],
            mix=[{"family":"prova_estudo_caso","percentage":55},{"family":"demonstracao","percentage":25},{"family":"institucional","percentage":20}],
            objectives=["confianca","autoridade","apresentar_solucao","venda"],
            topic="ganhos de usinagem após migração de software", segment="tecnologia industrial B2B", subsegment="software CAM para ferramentaria",
            audience="gestores e engenheiros de ferramentarias avaliando software de usinagem", awareness="consciente_produto",
            production="intermediate", scale="small", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio"], hooks=["numero","resultado_antecipado"],
            narrative=["situacao","problema","mecanismo","prova","conclusao","cta"], proof=["depoimento","dado","mecanismo_explicado"],
            cta=["clicar"], advertising="conteudo_de_marca", intent="explicita",
            entity={"kind":"produto","name":"WORKNC e serviços SKA","confidence":"high"},
            evidence=[
                "A fala identifica a Ribeiro, o fundador e a busca iniciada em 2016 por ganho produtivo.",
                "O software anterior funciona como comparador; testes precedem a migração para o WORKNC.",
                "A fala relata 30% em desbaste, 25% em outras estratégias, 40% em furação e 20% em processamento.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261002-237","obs-20261002-238"],"confidence":"high"},
        observations=[
            "Estado anterior, teste comparativo, intervenção e resultados por etapa aparecem na fala do cliente.",
            "A voz identificável antecede o veredito e reconhece o custo de transição de software.",
            "Os percentuais são autodeclarados e não auditados; visualizações e curtidas são apenas contexto.",
        ],
        interpretations=[
            "A cadeia torna a alegação rastreável sem demonstrar causalidade ou generalização.",
            "Separar os ganhos por etapa reduz a ambiguidade de um único número agregado.",
        ],
        scores={"gancho":86,"clareza":95,"relevancia":93,"desejo":79,"confianca":88,"retencao":"not_assessed","acao":82,"objecoes":87},
        lenses={
            "apressado":"O título entrega intervenção e resultado, embora a fala comece pela história da empresa.",
            "analitico":"Encontra comparador, teste e quatro resultados por etapa; ainda exige baseline e método.",
            "aspiracional":"Visualiza maior eficiência sem depender de promessa abstrata.",
            "comunidade":"O único comentário não testa a experiência de uso.",
            "cetico":"Separa depoimento comercial de auditoria independente.",
        },
        replicable=["Nomear o estado anterior antes da solução.","Explicar como a alternativa foi testada.","Vincular cada número a uma etapa operacional específica."],
        contingent=["Relação comercial, suporte e marca são contexto.","Percentuais não têm auditoria independente.","Mídia e retenção não foram observadas."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"a fala liga estado anterior, teste, intervenção e resultados por etapa","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_comment_sample",
    ),
    build_ref(
        id="obs-20261002-237",
        title="Estudo de caso: Divimec",
        creator="PLMPRO Tecnologia", identity="plmpro-tecnologia",
        url="https://www.youtube.com/watch?v=-f_iK4CDKhI",
        published="2025-01-14", duration="PT4M16S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 4 minutos e 16 segundos, 156 visualizações, duas curtidas e zero comentários indicados em 2 de outubro de 2026",
            "transcrição automática integral em português até 4 minutos e 2 segundos; fala acessível somente por substituição textual",
            "depoimento da Divimec sobre fluxo 2D, pesquisa de mercado, implantação de Solid Edge e Teamcenter com suporte PLMPRO e dois resultados quantificados",
        ],
        missing=MISSING_COMMON + ["data da implantação", "definição operacional de erro de fabricação", "volumes absolutos antes e depois"],
        metrics={"viewsObserved":156,"likesObserved":2,"commentsObserved":0,"commentsSampled":0},
        classification=cls(
            material="video_longo", presentations=["depoimento","estudo_caso","institucional"], primary="prova_estudo_caso",
            secondary=["transformacao","autoridade_opiniao"],
            mix=[{"family":"prova_estudo_caso","percentage":60},{"family":"transformacao","percentage":25},{"family":"autoridade_opiniao","percentage":15}],
            objectives=["confianca","autoridade","apresentar_solucao","venda"],
            topic="migração de engenharia 2D para 3D", segment="tecnologia industrial B2B", subsegment="CAD e gestão de ciclo de produto",
            audience="gestores e projetistas industriais avaliando CAD 3D e PLM", awareness="consciente_produto",
            production="intermediate", scale="small", replicability="high", duration="over_60s",
            mechanisms=["confianca","alivio","desejo"], hooks=["resultado_antecipado","transformacao"],
            narrative=["situacao","problema","mecanismo","prova","transformacao","conclusao"], proof=["depoimento","dado","mecanismo_explicado"],
            cta=[], advertising="conteudo_de_marca", intent="explicita",
            entity={"kind":"produto","name":"Solid Edge, Teamcenter e suporte PLMPRO","confidence":"high"},
            evidence=[
                "A fala identifica a Divimec e o fluxo anterior integralmente em 2D.",
                "Pesquisa de mercado e critério do modelamento síncrono antecedem a escolha.",
                "Após implantação, a fala relata redução de 40% no desenvolvimento e 50% nos erros de fabricação.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261002-236","obs-20261002-238"],"confidence":"high"},
        observations=[
            "Problema anterior, critérios, intervenção e dois resultados aparecem em uma voz da empresa-cliente.",
            "A fala reconhece que migrar de 2D para 3D foi traumático, preservando uma objeção operacional.",
            "Os números permanecem autodeclarados e sem método publicado.",
        ],
        interpretations=[
            "A objeção de implantação fica integrada à prova em vez de apagada.",
            "Dois resultados de naturezas distintas tornam a promessa mais específica, não mais causal.",
        ],
        scores={"gancho":72,"clareza":94,"relevancia":92,"desejo":80,"confianca":87,"retencao":"not_assessed","acao":76,"objecoes":88},
        lenses={
            "apressado":"O título é genérico; a promessa aparece tarde na fala.",
            "analitico":"Consegue rastrear 2D, escolha, implantação e dois resultados.",
            "aspiracional":"Vê a passagem para um processo 3D mais previsível.",
            "comunidade":"Nenhum comentário público foi retornado.",
            "cetico":"Pede datas, volumes e definição de erro antes de generalizar.",
        },
        replicable=["Mostrar o fluxo anterior com precisão.","Explicitar o critério de escolha.","Preservar a dificuldade de implantação e quantificar resultados distintos."],
        contingent=["Parceria preexistente com Siemens influencia a escolha.","Resultados são autodeclarados.","Mídia e retenção não foram observadas."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"a fala liga processo 2D, escolha, implantação e dois resultados quantificados","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261002-238",
        title="Eficiência Energética - HRC™ Trás Aumento de Produção",
        creator="Metso", identity="metso",
        url="https://www.youtube.com/watch?v=2VA-Evd-2Iw",
        published="2025-07-31", duration="PT2M21S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 2 minutos e 21 segundos, 382 visualizações, nove curtidas e zero comentários indicados em 2 de outubro de 2026",
            "transcrição automática integral em português até 2 minutos e 17 segundos; fala acessível somente por substituição textual",
            "cliente Ciplan identificável no título e na descrição; comparação falada entre três moinhos e HRC, consumo de 11 versus 3,8 kWh por tonelada e efeitos de manutenção",
        ],
        missing=MISSING_COMMON + ["nome e cargo individual dos porta-vozes na fala acessível", "período do baseline", "volume total e custo energético antes e depois"],
        metrics={"viewsObserved":382,"likesObserved":9,"commentsObserved":0,"commentsSampled":0},
        classification=cls(
            material="video_curto", presentations=["depoimento","estudo_caso","demonstracao"], primary="prova_estudo_caso",
            secondary=["demonstracao","institucional"],
            mix=[{"family":"prova_estudo_caso","percentage":50},{"family":"demonstracao","percentage":35},{"family":"institucional","percentage":15}],
            objectives=["confianca","autoridade","apresentar_solucao","venda"],
            topic="capacidade de britagem com menor consumo", segment="mineração e agregados B2B", subsegment="planta industrial de areia",
            audience="engenheiros e gestores avaliando britagem de alta pressão", awareness="consciente_produto",
            production="intermediate", scale="large", replicability="medium", duration="over_60s",
            mechanisms=["confianca","alivio","desejo"], hooks=["numero","problema"],
            narrative=["problema","mecanismo","prova","conclusao"], proof=["dado","mecanismo_explicado","depoimento"],
            cta=[], advertising="conteudo_de_marca", intent="explicita",
            entity={"kind":"produto","name":"britador HRC da Metso","confidence":"high"},
            evidence=[
                "A fala nomeia a necessidade de elevar capacidade sem elevar consumo.",
                "O comparador usa 11 kWh/t; o HRC é descrito com cerca de 3,8 kWh/t.",
                "Três moinhos substituídos e menor intervenção de manutenção ligam mecanismo e resultado operacional.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20261002-236","obs-20261002-237"],"confidence":"medium"},
        observations=[
            "Problema, comparador, intervenção e métricas técnicas aparecem na fala e descrição.",
            "A organização-cliente é identificável, mas os nomes individuais dos porta-vozes não ficaram acessíveis.",
            "O caso é apoio de nível 2 por escala industrial e identificação pessoal incompleta.",
        ],
        interpretations=[
            "Unidades técnicas e comparador explícito tornam a promessa auditável na linguagem.",
            "A escala da planta e a marca limitam a transferibilidade de produção, não do encadeamento probatório.",
        ],
        scores={"gancho":89,"clareza":96,"relevancia":91,"desejo":81,"confianca":86,"retencao":"not_assessed","acao":75,"objecoes":88},
        lenses={
            "apressado":"Recebe cedo a tensão entre capacidade e energia.",
            "analitico":"Encontra unidade, comparador e mecanismo, mas pede janela e custo total.",
            "aspiracional":"Visualiza expansão com menor intensidade energética.",
            "comunidade":"Nenhum comentário público foi retornado.",
            "cetico":"Marca a identificação pessoal e auditoria como ausentes.",
        },
        replicable=["Começar pelo trade-off operacional.","Usar a mesma unidade para comparador e intervenção.","Ligar o número ao mecanismo e à substituição concreta."],
        contingent=["Planta, tecnologia e orçamento não são replicáveis por pequenos negócios.","Números são publicados pelo fornecedor.","Mídia e retenção não foram observadas."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala compara consumo e configuração antes e depois da intervenção","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261002-239",
        title="CHEFTIME: Startup reduz perdas de estoque com a implementação do Sistema de Gestão SAP B1",
        creator="ALFA ERP - SAP Gold Partner", identity="alfa-erp",
        url="https://www.youtube.com/watch?v=e4gLDK1ZjTQ",
        published="2022-05-05", duration="PT4M34S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 4 minutos e 34 segundos, 690 visualizações, 14 curtidas e três comentários indicados em 2 de outubro de 2026",
            "transcrição automática integral em português até 4 minutos e 27 segundos; fala acessível somente por substituição textual",
            "cliente CHEFTIME identificável, crescimento declarado de cerca de 400% em 2021, problema de controles manuais, implantação de um mês e resultado qualitativo",
            "três comentários amostrados; uma resposta do fornecedor afirma eliminação de 100% do desperdício sem publicar método ou baseline",
        ],
        missing=MISSING_COMMON + ["percentual de perdas antes e depois", "ordem temporal completa entre crescimento e implantação", "fonte independente para a resposta de 100%"],
        metrics={"viewsObserved":690,"likesObserved":14,"commentsObserved":3,"commentsSampled":3},
        classification=cls(
            material="video_longo", presentations=["depoimento","estudo_caso","institucional"], primary="prova_estudo_caso",
            secondary=["transformacao","oferta_direta"],
            mix=[{"family":"prova_estudo_caso","percentage":50},{"family":"transformacao","percentage":30},{"family":"oferta_direta","percentage":20}],
            objectives=["confianca","apresentar_solucao","venda"],
            topic="implantação de ERP em foodtech", segment="software de gestão B2B", subsegment="ERP para estoque e operação de alimentos",
            audience="gestores de empresas em expansão avaliando SAP Business One", awareness="consciente_produto",
            production="intermediate", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["confianca","desejo","alivio"], hooks=["resultado_antecipado","transformacao"],
            narrative=["situacao","problema","mecanismo","transformacao","cta"], proof=["depoimento","mecanismo_explicado"],
            cta=["clicar","conversar"], advertising="conteudo_de_marca", intent="explicita",
            entity={"kind":"produto","name":"SAP Business One e implementação ALFA ERP","confidence":"high"},
            evidence=[
                "O crescimento de cerca de 400% é declarado antes do problema e não fica ligado causalmente ao ERP.",
                "Planilhas manuais, escolha do SAP e implantação de cerca de um mês aparecem na fala.",
                "A fala associa o sistema a informação confiável e acompanhamento de desperdício, sem quantificar a redução.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261002-236","obs-20261002-237","obs-20261002-238"],"confidence":"high"},
        observations=[
            "Há cliente, problema, intervenção e período de implantação, mas o resultado atribuído à solução é qualitativo.",
            "O número de 400% pertence ao crescimento anterior ou simultâneo e não pode funcionar como resultado do ERP.",
            "A alegação de 100% aparece somente em resposta do fornecedor a comentário, sem baseline ou cálculo.",
        ],
        interpretations=[
            "É caso-limite, não contraexemplo: a cadeia narrativa existe, mas números não estão ligados de forma válida à intervenção.",
            "Mover um número forte para perto da solução não corrige sua falta de atribuição temporal.",
        ],
        scores={"gancho":86,"clareza":79,"relevancia":89,"desejo":83,"confianca":61,"retencao":"not_assessed","acao":80,"objecoes":56},
        lenses={
            "apressado":"Encontra uma transformação clara, mas pode associar indevidamente os 400% ao ERP.",
            "analitico":"Distingue crescimento, implantação e redução de perdas sem número verificável.",
            "aspiracional":"Vê integração e segurança para escalar.",
            "comunidade":"A pergunta por percentual revela a lacuna; a resposta comercial não publica cálculo.",
            "cetico":"Rejeita 400% e 100% como prova da intervenção sem baseline.",
        },
        replicable=["Separar crescimento do cliente de resultado da solução.","Declarar o período de implantação.","Publicar baseline e fórmula quando o comentário pedir percentual."],
        contingent=["Crescimento e aquisição pelo GPA são contexto.","Resposta da marca não equivale a auditoria.","Mídia e retenção não foram observadas."],
        role="falsification_or_boundary", evidence_level=1, eligible=False,
        claims=[
            {"claim":"a fala mostra problema, implantação e benefício qualitativo","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"o SAP causou o crescimento de 400% ou eliminou 100% do desperdício","requiredModalities":["audited_baseline","calculation","controlled_comparison"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_complete_comment_sample",
    ),
    build_ref(
        id="obs-20261002-240",
        title="Como pedir depoimento de clientes",
        creator="Gleicy Laranjeira | H2ON Marketing B2B", identity="gleicy-laranjeira-h2on",
        url="https://www.youtube.com/watch?v=MJ0Ecx6DVIc",
        published="2021-06-29", duration="PT10M32S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 10 minutos e 32 segundos, 1.040 visualizações, 44 curtidas e dois comentários indicados em 2 de outubro de 2026",
            "transcrição automática integral em português até 10 minutos e 30 segundos; fala acessível somente por substituição textual",
            "tutorial falado sobre pesquisa de satisfação, momento do pedido, autorização antes de republicar e cláusula contratual",
            "dois comentários públicos amostrados; um agradecimento e uma resposta da criadora, sem teste de execução",
            "fonte primária da Bain consultada separadamente para conferir a classificação NPS mencionada",
        ],
        missing=MISSING_COMMON + ["teste de execução do modelo", "consentimento documentado em um caso concreto", "representatividade dos depoimentos coletados"],
        metrics={"viewsObserved":1040,"likesObserved":44,"commentsObserved":2,"commentsSampled":2},
        classification=cls(
            material="video_longo", presentations=["camera_direta","tutorial","comentario"], primary="educativo",
            secondary=["comunidade","autoridade_opiniao"],
            mix=[{"family":"educativo","percentage":55},{"family":"comunidade","percentage":25},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","confianca","apresentar_solucao","lead"],
            topic="coleta e autorização de depoimentos", segment="marketing B2B", subsegment="prova social e estudos de caso",
            audience="pequenos negócios que querem coletar depoimentos de clientes", awareness="preparado_agir",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["confianca","pertencimento","alivio"], hooks=["problema","promessa"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","tratamento_objecao"],
            cta=["clicar","seguir"], advertising="geracao_de_leads", intent="explicita",
            entity={"kind":"produto","name":"kit de ferramentas de marketing","confidence":"high"},
            evidence=[
                "A fala transforma a coleta em processo ligado a satisfação, entrega e autorização.",
                "A criadora recomenda pedir permissão antes de reutilizar imagem, nome e depoimento.",
                "A classificação falada de notas acima de 7 como promotores conflita com a Bain: 9–10 são promotores e 7–8 são passivos.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de tutorial ético para coleta de prova social","referenceIds":[],"confidence":"medium"},
        observations=[
            "O tutorial separa obter feedback de obter autorização para republicação.",
            "Autorização por e-mail e cláusula contratual são tratadas como proteção adicional, sem caso concreto auditado.",
            "A classificação NPS contém imprecisão verificável e não foi ensinada como regra correta.",
        ],
        interpretations=["A cobertura sustenta uma observação sobre processo e consentimento; nenhuma hipótese nova foi criada."],
        scores={"gancho":81,"clareza":88,"relevancia":91,"desejo":74,"confianca":70,"retencao":"not_assessed","acao":90,"objecoes":84},
        lenses={
            "apressado":"Recebe um problema claro e múltiplos momentos para agir.",
            "analitico":"Valoriza processo e autorização, mas corrige o corte de NPS.",
            "aspiracional":"Visualiza um acervo contínuo de provas sociais.",
            "comunidade":"Comentários são positivos, porém não mostram aplicação do método.",
            "cetico":"Exige consentimento verificável, seleção não enviesada e métrica correta.",
        },
        replicable=["Transformar pedido de depoimento em processo recorrente.","Pedir autorização específica antes de republicar.","Separar elogio, permissão e estudo de caso."],
        contingent=["O corte de NPS precisa ser corrigido.","O kit ofertado cria contexto comercial.","Comentários não demonstram execução ou resultado."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a fala recomenda autorização antes da republicação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_complete_comment_sample_and_primary_method_check",
    ),
]

refs[-1]["training"]["provenanceAndConsent"] = {
    "storyOrigin":"tutorial editorial público sem história privada identificável ensinada",
    "consentStatus":"not_applicable",
    "identityProtection":"not_applicable",
    "evidence":["a própria referência ensina pedir autorização antes de republicar nome, imagem e depoimento"],
}

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 044")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20261002-236", "obs-20261002-237", "obs-20261002-238"]
new_case = "obs-20261002-239"
pattern["statement"] = "Em prova comercial B2B, organizar estado anterior, intervenção, período ou baseline, resultado quantificado e voz identificável do cliente torna a cadeia de alegação rastreável; números só contam como resultado quando sua unidade e janela pertencem à intervenção, e depoimentos ou respostas do fornecedor sem cálculo continuam autodeclarações, não causalidade nem auditoria."
pattern["name"] = "Prova comercial com cadeia problema–mecanismo–resultado–cliente"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 8
pattern["supportingCount"] = 8
pattern["caseLimitCount"] = 4
pattern["creatorDiversityCount"] = 8
pattern["sourceDiversityCount"] = 8
pattern["conditions"] = [
    "conteúdo de prova comercial B2B",
    "cliente ou responsável identificável",
    "estado anterior ou comparador explicitado",
    "intervenção e período ou baseline descritos",
    "resultado com unidade e janela ligadas à intervenção",
    "limitações, variáveis simultâneas e vínculo comercial registrados",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20261002-236","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Cliente, software anterior, teste, migração e percentuais por etapa aparecem na fala.","evidence":"Metadados, descrição integral, transcrição automática integral e um comentário amostrado.","limitations":["percentuais autodeclarados, sem janela e auditoria"]},
    {"referenceId":"obs-20261002-237","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Fluxo 2D, critério, implantação e reduções de tempo e erro aparecem na voz do cliente.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["sem data, volumes e definição operacional de erro"]},
    {"referenceId":"obs-20261002-238","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Problema, três moinhos, intervenção e consumo de 11 versus 3,8 kWh/t aparecem na fala.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["cliente corporativo identificado, mas porta-vozes sem nome acessível; escala industrial"]},
    {"referenceId":"obs-20261002-239","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"Crescimento de 400% precede a prova da intervenção; redução de perdas é qualitativa e 100% surge apenas em resposta da marca.","evidence":"Metadados, descrição integral, transcrição automática integral e três comentários amostrados.","limitations":["não conta como apoio nem contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Oito apoios vêm de oito criadores e fontes; demonstram recorrência estrutural, não eficácia ou causalidade.",
    "Todos os resultados permanecem autodeclarados por fornecedor, cliente ou parte comercialmente interessada.",
    "Nenhuma referência oferece auditoria independente, retenção, teste de compreensão ou experimento causal.",
    "O quarto caso-limite mostra que crescimento anterior e resposta comercial sem cálculo não podem ser anexados ao resultado da intervenção.",
    "Produção, fama, métricas e comentários permanecem contexto não causal.",
]

discarded = [
    {"url":"https://www.youtube.com/watch?v=DZZxq3_MiOw","reason":"entrevista longa sobre experiência do cliente, sem cadeia curta de baseline, intervenção e resultado observável"},
    {"url":"https://www.youtube.com/watch?v=oTG5-hJtLh4","reason":"podcast de posicionamento com alegações agregadas, sem caso-cliente comparável"},
    {"url":"https://www.youtube.com/watch?v=3coYCrBew_c","reason":"descrição oferece percentuais, mas não havia transcrição nem voz do cliente acessível"},
    {"url":"https://www.youtube.com/watch?v=YkNiujoWJoQ","reason":"depoimento recente com intervenção e cliente identificável, porém resultado apenas qualitativo e sem baseline"},
    {"url":"https://www.youtube.com/watch?v=J9NE2N7Aues","reason":"especialista externo relata economia da Caloi; a voz identificável do cliente não ficou acessível"},
    {"url":"https://www.youtube.com/watch?v=SDEixVdyIlI","reason":"depoimento identifica problema e serviços, mas não oferece resultado quantificado ligado à intervenção"},
    {"url":"https://www.youtube.com/watch?v=lMvDZ3AdnNg","reason":"case longo com dado de retrabalho, menor concisão e comparabilidade que os apoios selecionados"},
    {"url":"https://www.youtube.com/watch?v=_UhDPT91B8Q","reason":"aula sobre Customer Success, não estudo de caso com cliente e baseline"},
    {"url":"https://www.youtube.com/watch?v=AZCdokqoY9A","reason":"podcast de liderança comercial, sem cadeia comparável de intervenção e resultado"},
    {"url":"https://www.youtube.com/watch?v=5iT6kT0Iz7A","reason":"descrição ampla e resultado qualitativo, sem métrica atribuível ao ERP"},
    {"url":"https://www.youtube.com/watch?v=FsV-TTucbDg","reason":"conteúdo educativo e oferta, não prova de cliente comparável"},
    {"url":"https://www.youtube.com/watch?v=_9FjcEjOJBc","reason":"crescimento da administradora é narrado em podcast e não isolado como resultado do software"},
    {"url":"https://www.youtube.com/watch?v=sgvieA2wJ90","reason":"curso sobre IA em vendas, não caso-cliente com baseline e resultado"},
    {"url":"https://www.youtube.com/watch?v=fFl3aFtBKio","reason":"referência portuguesa e entrevista de estratégia, sem intervenção e resultado comparável"},
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 19,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20261002-240"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["prova_estudo_caso","demonstracao","institucional","transformacao","autoridade_opiniao","educativo","comunidade","oferta_direta"],
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
        "limitation":"as cinco transcrições automáticas substituem somente a fala e podem errar termos técnicos; nenhuma cena, tela ou áudio foi inferido delas",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":3,
        "sampledComments":6,
        "zeroReturnedReferences":2,
        "unavailableReferences":0,
        "limitation":"as amostras são públicas, pequenas e não representativas; uma resposta do fornecedor não foi tratada como auditoria",
    },
    "baselineCoverage": {
        "sampledProfiles":3,
        "contemporaneousBaselines":0,
        "limitation":"três comparadores aparecem na fala, mas nenhum forma coorte contemporânea, auditoria ou experimento causal",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["crescimento anterior e alegação comercial sem cálculo não podem ser usados como resultado da intervenção"],
    "safetyFindings": [
        "nenhum resultado autodeclarado foi tratado como causal ou auditado",
        "a imprecisão de NPS da exploração foi verificada contra fonte primária e não ensinada",
        "autorização mencionada em tutorial não foi confundida com consentimento de caso concreto",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes elevam de cinco para oito os apoios do padrão de prova comercial B2B. Um caso-limite separa crescimento prévio e resposta comercial sem cálculo do resultado atribuível. O padrão permanece provisório.",
    "nextTarget": "case B2B brasileiro recente e curto, de fornecedor pequeno ou médio, com audiovisual integral, cliente e responsável nomeados, baseline temporal, método de cálculo e resultado auditável; priorizar um caso em que os registros contradigam o percentual publicado",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Cinco transcrições automáticas integrais substituem somente a fala e podem errar termos técnicos.",
        "Seis comentários foram amostrados sem representatividade estatística.",
        "Não houve retenção, auditoria independente, teste de compreensão ou causalidade.",
        "A exploração teve uma imprecisão de NPS e foi mantida como observação, sem hipótese nova.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
