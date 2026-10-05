#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-046.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]

NOW = "2026-10-05T11:43:20.000Z"
OBSERVED = "2026-10-05"
RUN_ID = "run-20261005-supervised-047"
PATTERN_ID = "pat-20260824-004"
BATCH_IDS = {f"obs-20261005-{n}" for n in range(251, 256)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

GROUP = "Short educativo de ciência ou conhecimento com pergunta literal ou contradição específica no título e resposta correspondente na fala"
MISSING_COMMON = MISSING_AV + [
    "métrica de retenção",
    "teste representativo de compreensão",
    "revisão científica independente das alegações",
    "comparação causal controlada",
]

refs = [
    build_ref(
        id="obs-20261005-251",
        title="A IA vai ROUBAR seu emprego? A ciência responde!",
        creator="Carreira Acessível", identity="carreira-acessivel",
        url="https://www.youtube.com/watch?v=PpBdcLBtjA0",
        published="2026-08-24", duration="PT10S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 10 segundos, uma visualização e zero comentários indicados em 5 de outubro de 2026; curtidas não informadas",
            "transcrição automática integral em português até 10,4 segundos; fala acessível somente por substituição textual",
            "título pergunta se a inteligência artificial roubará empregos e a fala responde com substituição de tarefas repetitivas e foco em criatividade e empatia",
            "a descrição cita OIT e FGV, mas não fornece estudo, link, ano ou método rastreável",
            "nenhum comentário público foi retornado",
        ],
        missing=MISSING_COMMON + ["fontes identificáveis para os números e previsões da descrição"],
        metrics={"viewsObserved":1,"likesObserved":"not_measured","commentsObserved":0,"commentsSampled":0},
        classification=cls(
            material="video_curto", presentations=["comentario"], primary="explicativo",
            secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"explicativo","percentage":50},{"family":"educativo","percentage":30},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","consciencia_problema","comentario"],
            topic="impacto da inteligência artificial no trabalho", segment="carreira e futuro do trabalho", subsegment="automação de tarefas",
            audience="trabalhadores preocupados com inteligência artificial", awareness="consciente_problema",
            production="unknown", scale="small", replicability="high", duration="up_to_15s",
            mechanisms=["medo","alivio","curiosidade"], hooks=["pergunta","risco"],
            narrative=["problema","risco","mecanismo","conclusao","cta"], proof=["alegacao_sem_prova"],
            cta=["comentar","seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "O título nomeia inteligência artificial, emprego e uma pergunta binária.",
                "A fala responde diretamente à pergunta, mas comprime uma previsão complexa em dez segundos.",
                "As instituições citadas na descrição não estão ligadas a fontes identificáveis.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261005-252","obs-20261005-253"],"confidence":"medium"},
        observations=[
            "A embalagem permite identificar assunto, risco e promessa antes da reprodução.",
            "A fala mantém o mesmo assunto e oferece uma resposta curta baseada em tarefas, não em profissões inteiras.",
            "A pergunta específica sustenta clareza semântica, não a precisão da resposta nem a previsão sobre empregos.",
        ],
        interpretations=[
            "Pergunta e resposta formam uma unidade rastreável com baixo custo de entendimento.",
            "A compressão e a ausência de fontes elevam o ônus de prova científico.",
        ],
        scores={"gancho":90,"clareza":91,"relevancia":89,"desejo":76,"confianca":48,"retencao":"not_assessed","acao":70,"objecoes":47},
        lenses={
            "apressado":"Identifica imediatamente IA, emprego e uma resposta prometida.",
            "analitico":"Pede estudos rastreáveis, condições e distinção entre tarefa e ocupação.",
            "aspiracional":"Recebe criatividade e empatia como competências a desenvolver.",
            "comunidade":"O CTA pede opinião, mas nenhum comentário foi retornado.",
            "cetico":"Não aceita ciência como selo suficiente sem fonte ou método.",
        },
        replicable=["Formular uma pergunta que nomeie risco e objeto.","Responder ao mesmo objeto na primeira frase.","Separar clareza do título de força da evidência."],
        contingent=["A previsão depende de mercado, profissão, período e método.","As fontes citadas não foram rastreadas.","Audiovisual e retenção não foram observados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"o título nomeia IA e emprego em uma pergunta, e a fala responde ao mesmo problema","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True}],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261005-252",
        title="Viu um fantasma? Como a ciência explica eventos paranormais?",
        creator="UOL", identity="uol",
        url="https://www.youtube.com/watch?v=XHgIbKp_cBQ",
        published="2022-04-16", duration="PT1M",
        accessible=[
            "título, criador e data exata; descrição pública vazia",
            "duração pública de 60 segundos, 2.624 visualizações, 95 curtidas e 15 comentários indicados em 5 de outubro de 2026",
            "transcrição automática integral em português até 60,3 segundos; fala acessível somente por substituição textual",
            "a fala reformula experiências sobrenaturais e oferece enxaqueca, variação de temperatura e infrassom como explicações naturais possíveis",
            "15 comentários públicos amostrados; relatos e discordâncias individuais não foram tratados como evidência científica ou opinião coletiva",
        ],
        missing=MISSING_COMMON + ["fontes identificáveis para os estudos mencionados sobre infrassom"],
        metrics={"viewsObserved":2624,"likesObserved":95,"commentsObserved":15,"commentsSampled":15},
        classification=cls(
            material="video_curto", presentations=["comentario"], primary="curiosidade",
            secondary=["explicativo","educativo"],
            mix=[{"family":"curiosidade","percentage":45},{"family":"explicativo","percentage":35},{"family":"educativo","percentage":20}],
            objectives=["interromper_rolagem","educar","visualizacao"],
            topic="explicações naturais para experiências paranormais", segment="ciência e comportamento", subsegment="percepção e infrassom",
            audience="público geral interessado em ciência e paranormalidade", awareness="consciente_problema",
            production="unknown", scale="large", replicability="medium", duration="31_to_60s",
            mechanisms=["curiosidade","surpresa","vigilancia"], hooks=["pergunta","problema"],
            narrative=["problema","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","alegacao_sem_prova"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"marca","name":"UOL","confidence":"high"},
            evidence=[
                "O título apresenta duas perguntas específicas sobre fantasmas e explicação científica.",
                "A fala retorna às sensações citadas e nomeia explicações naturais possíveis.",
                "Estudos são mencionados sem autoria, periódico ou link rastreável.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261005-251","obs-20261005-253"],"confidence":"high"},
        observations=[
            "Pergunta, fenômeno e perspectiva explicativa estão explícitos no título.",
            "A fala mantém o fenômeno e oferece alternativas naturais sem negar de forma absoluta a experiência de terceiros.",
            "Comentários revelam objeções e relatos, mas não medem compreensão nem confirmam causalidade.",
        ],
        interpretations=[
            "A embalagem específica e a resposta correspondente tornam a promessa semanticamente rastreável.",
            "A ausência de fontes limita confiança científica, não a observação estrutural.",
        ],
        scores={"gancho":91,"clareza":92,"relevancia":83,"desejo":79,"confianca":59,"retencao":"not_assessed","acao":60,"objecoes":61},
        lenses={
            "apressado":"Entende fantasma, ciência e tipo de resposta pelo título.",
            "analitico":"Pede fontes e separação entre correlação, hipótese e mecanismo demonstrado.",
            "aspiracional":"Percebe uma leitura natural para sensações assustadoras.",
            "comunidade":"Comentários trazem relatos e resistência sem representatividade estatística.",
            "cetico":"Aceita possibilidades, mas não generaliza enxaqueca ou infrassom para todos os relatos.",
        },
        replicable=["Nomear a experiência e a lente explicativa.","Usar linguagem de possibilidade quando a evidência é limitada.","Tratar comentários como objeções, não como validação."],
        contingent=["As alegações científicas exigem fonte e revisão.","A marca e a distribuição não são replicáveis por si.","Audiovisual e retenção não foram observados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"o título pergunta por fantasmas e explicação científica, e a fala responde com hipóteses naturais correspondentes","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True}],
        source_type="youtube_public_watch_metadata_full_automatic_transcript_and_15_public_comments",
    ),
    build_ref(
        id="obs-20261005-253",
        title="Why Do We Yawn?",
        creator="Parentin101", identity="parentin101",
        url="https://www.youtube.com/watch?v=QpqzEXYzhBk",
        published="2025-03-16", duration="PT18S",
        accessible=[
            "título, criador e data exata; descrição pública vazia",
            "duração pública de 18 segundos, nove visualizações e zero comentários indicados em 5 de outubro de 2026; curtidas não informadas",
            "transcrição automática integral em inglês até 18,2 segundos; fala acessível somente por substituição textual",
            "a fala responde ao bocejo com resfriamento cerebral e contágio social declarados; essas generalizações não foram validadas",
            "nenhum comentário público foi retornado",
        ],
        missing=MISSING_COMMON + ["fontes científicas para as explicações sobre resfriamento cerebral e contágio"],
        metrics={"viewsObserved":9,"likesObserved":"not_measured","commentsObserved":0,"commentsSampled":0},
        classification=cls(
            material="video_curto", presentations=["outro"], primary="explicativo",
            secondary=["curiosidade","educativo"],
            mix=[{"family":"explicativo","percentage":45},{"family":"curiosidade","percentage":35},{"family":"educativo","percentage":20}],
            objectives=["educar","visualizacao","comentario"],
            topic="explicação do bocejo", segment="ciência e comportamento", subsegment="fisiologia cotidiana",
            audience="público geral interessado em fatos rápidos", awareness="consciente_problema",
            production="unknown", scale="small", replicability="high", duration="16_to_30s",
            mechanisms=["curiosidade","identificacao","surpresa"], hooks=["pergunta"],
            narrative=["problema","mecanismo","conclusao","cta"], proof=["alegacao_sem_prova"],
            cta=["comentar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "O título contém uma pergunta literal e específica sobre o bocejo.",
                "A fala oferece duas explicações ligadas ao mesmo fenômeno.",
                "Nenhuma fonte aparece na descrição ou na fala transcrita.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261005-251","obs-20261005-252"],"confidence":"high"},
        observations=[
            "O assunto pode ser identificado integralmente antes da reprodução.",
            "A fala responde sem mudar de objeto, mas apresenta explicações científicas como consenso sem fontes acessíveis.",
            "Baixa popularidade não reduz nem confirma a recorrência estrutural observada.",
        ],
        interpretations=[
            "Pergunta literal e resposta curta criam alinhamento semântico.",
            "Alinhamento não equivale a precisão científica, compreensão ou retenção.",
        ],
        scores={"gancho":84,"clareza":91,"relevancia":78,"desejo":70,"confianca":43,"retencao":"not_assessed","acao":62,"objecoes":48},
        lenses={
            "apressado":"Sabe que receberá uma explicação para o bocejo.",
            "analitico":"Pede fontes e grau de consenso das duas explicações.",
            "aspiracional":"Recebe uma curiosidade fácil de recontar.",
            "comunidade":"O CTA pede comentário, mas nenhum foi retornado.",
            "cetico":"Não aceita formulações definitivas sem evidência rastreável.",
        },
        replicable=["Usar uma pergunta literal sobre fenômeno cotidiano.","Responder ao mesmo fenômeno sem desvio temático.","Manter a precisão proporcional às fontes disponíveis."],
        contingent=["As explicações científicas não foram revisadas.","Não há descrição ou comentários.","Audiovisual e retenção não foram observados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"o título pergunta por que bocejamos e a fala responde ao mesmo fenômeno","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True}],
        source_type="youtube_public_watch_metadata_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261005-254",
        title="O morango e a ciência!",
        creator="Química Integral", identity="quimica-integral",
        url="https://www.youtube.com/watch?v=agrXszICxSo",
        published="2021-12-01", duration="PT1M32S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 1 minuto e 32 segundos, 1.979 visualizações, 259 curtidas e 29 comentários indicados em 5 de outubro de 2026",
            "transcrição automática integral em português até 92,2 segundos; fala acessível somente por substituição textual",
            "a fala identifica pseudofruto, células, reagentes, etapas de extração e DNA precipitado; o resultado visual não foi observado",
            "29 comentários públicos amostrados; perguntas sobre álcool e outras frutas e respostas do criador não constituem teste representativo",
            "a descrição contém links comerciais para vidrarias; afiliação formal e remuneração não foram confirmadas",
        ],
        missing=MISSING_COMMON + ["resultado visual da precipitação", "orientações completas de segurança para álcool e reagentes"],
        metrics={"viewsObserved":1979,"likesObserved":259,"commentsObserved":29,"commentsSampled":29},
        classification=cls(
            material="video_curto", presentations=["demonstracao","tutorial","camera_direta"], primary="demonstracao",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":55},{"family":"educativo","percentage":30},{"family":"curiosidade","percentage":15}],
            objectives=["educar","salvamento","visualizacao"],
            topic="extração de DNA do morango", segment="química e experimentos", subsegment="biologia molecular doméstica",
            audience="estudantes, professores e público interessado em experimentos", awareness="consciente_solucao",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","recompensa","surpresa"], hooks=["nenhum_identificado"],
            narrative=["situacao","mecanismo","progressao","payoff","conclusao"], proof=["demonstracao","mecanismo_explicado"],
            cta=["seguir"], advertising="editorial_organico", intent="implicita",
            entity={"kind":"produto","name":"vidrarias de laboratório em links externos","confidence":"medium"},
            evidence=[
                "O título nomeia morango e ciência, mas não pergunta nem identifica DNA ou extração.",
                "A fala contém um procedimento e um resultado declarados muito mais específicos que a embalagem.",
                "Perguntas dos comentários mostram dúvidas de execução, sem medir sucesso.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261005-251","obs-20261005-252","obs-20261005-253"],"confidence":"high"},
        observations=[
            "A entrega falada é específica, mas o título genérico não permite identificar a extração de DNA antes da reprodução.",
            "O caso preserva a distinção entre conteúdo substantivo e embalagem semanticamente específica.",
            "Sem audiovisual, não se confirmam execução, segurança ou resultado.",
        ],
        interpretations=["É caso-limite, não contraexemplo de desempenho: demonstração útil pode existir sob título genérico, mas não satisfaz o mecanismo de clareza antecipada."],
        scores={"gancho":63,"clareza":69,"relevancia":84,"desejo":77,"confianca":72,"retencao":"not_assessed","acao":70,"objecoes":64},
        lenses={
            "apressado":"Vê morango e ciência, mas não sabe qual fenômeno será entregue.",
            "analitico":"Rastreia materiais e etapas na fala, mas pede segurança e imagem do resultado.",
            "aspiracional":"Percebe um experimento doméstico reproduzível.",
            "comunidade":"Perguntas são respondidas, sem evidência de execução bem-sucedida.",
            "cetico":"Não confunde links comerciais ou curtidas com validação do procedimento.",
        },
        replicable=["Descrever materiais, mecanismo e resultado em sequência.","Responder dúvidas de substituição sem tratá-las como taxa de sucesso."],
        contingent=["O título não identifica extração de DNA.","Segurança e resultado visual não foram auditados.","Links comerciais exigem disclosure claro."],
        role="falsification_or_boundary", evidence_level=1, eligible=False,
        claims=[
            {"claim":"a fala descreve extração de DNA de morango","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o título formula pergunta ou contradição que nomeia o fenômeno","requiredModalities":["title","specific_question_or_contradiction"],"observedModalities":["title"],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_29_public_comments",
    ),
    build_ref(
        id="obs-20261005-255",
        title="Ciência em 1 minuto - Importância dos invertebrados para ciência nas praias",
        creator="Praia com vida", identity="praia-com-vida",
        url="https://www.youtube.com/watch?v=t8NVgWXb2Vo",
        published="2022-12-30", duration="PT1M",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 60 segundos, 1.690 visualizações, 110 curtidas e dois comentários indicados em 5 de outubro de 2026",
            "transcrição automática integral em português até 60,2 segundos; fala acessível somente por substituição textual",
            "a fala relaciona invertebrados de praia a bioindicação, poluição e espécie guarda-chuva",
            "a descrição lista quatro links DOI de artigos; vínculo de cada frase com cada artigo não foi auditado",
            "dois comentários públicos amostrados; ambos são elogios e não medem compreensão",
        ],
        missing=MISSING_COMMON + ["auditoria das imagens e exemplos", "verificação artigo a artigo das generalizações científicas"],
        metrics={"viewsObserved":1690,"likesObserved":110,"commentsObserved":2,"commentsSampled":2},
        classification=cls(
            material="video_curto", presentations=["comentario"], primary="educativo",
            secondary=["explicativo","autoridade_opiniao"],
            mix=[{"family":"educativo","percentage":45},{"family":"explicativo","percentage":35},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","consciencia_problema","autoridade"],
            topic="invertebrados como indicadores de conservação de praias", segment="ciência e conservação", subsegment="ecologia de praias",
            audience="público interessado em praias, ciência e conservação", awareness="consciente_problema",
            production="unknown", scale="small", replicability="high", duration="31_to_60s",
            mechanisms=["curiosidade","confianca","pertencimento"], hooks=["numero"],
            narrative=["situacao","problema","mecanismo","conclusao"], proof=["fonte","mecanismo_explicado"],
            cta=[], advertising="editorial_organico", intent="ausente",
            entity={"kind":"causa","name":"conservação de praias","confidence":"high"},
            evidence=[
                "Título e descrição delimitam invertebrados, ciência e praias.",
                "A fala organiza usos científicos em bioindicação, poluição e proteção indireta.",
                "Quatro DOI tornam fontes localizáveis, embora o vínculo por alegação não tenha sido auditado.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de autoridade educativa em conservação com fontes localizáveis","referenceIds":[],"confidence":"low"},
        observations=[
            "A fala transforma pesquisa ecológica em três aplicações identificáveis.",
            "A descrição fornece fontes localizáveis, mas isso não valida automaticamente cada generalização.",
            "Sem audiovisual, não se ensinam exemplos visuais, espécies mostradas ou ritmo.",
        ],
        interpretations=["A rastreabilidade por DOI é promissora para confiança editorial, mas uma referência isolada e sem auditoria não cria hipótese nova."],
        scores={"gancho":74,"clareza":88,"relevancia":82,"desejo":66,"confianca":84,"retencao":"not_assessed","acao":"not_assessed","objecoes":76},
        lenses={
            "apressado":"Entende tema e duração, embora o título não seja uma pergunta.",
            "analitico":"Valoriza os DOI, mas pede mapeamento de alegações para cada fonte.",
            "aspiracional":"Percebe como pesquisa pode orientar conservação real.",
            "comunidade":"Dois elogios não medem entendimento ou mudança de comportamento.",
            "cetico":"Distingue fonte localizável de revisão independente da síntese.",
        },
        replicable=["Transformar pesquisa em poucas aplicações nomeadas.","Disponibilizar fontes localizáveis na descrição.","Não usar popularidade como substituto de rastreabilidade."],
        contingent=["A síntese científica não foi revisada artigo a artigo.","Exemplos visuais não foram observados.","Compreensão e retenção não foram medidas."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a fala liga invertebrados a bioindicação, poluição e conservação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"os quatro artigos sustentam todas as generalizações da fala","requiredModalities":["papers","claim_source_mapping","expert_review"],"observedModalities":["doi_links"],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_two_public_comments",
    ),
]

for item in refs:
    item["country"] = "INT" if item["id"] == "obs-20261005-253" else "BR"
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin":"conteúdo editorial público do próprio canal; nenhum relato privado identificável de terceiro foi ensinado",
        "consentStatus":"not_applicable",
        "identityProtection":"not_applicable",
        "evidence":["título, descrição quando disponível, metadados públicos e transcrição automática"],
    }
    item["training"]["notRecommended"] = [
        "copiar frase, identidade visual, personagem ou roteiro",
        "tratar visualizações, curtidas, comentários, fama, tendência, mídia ou orçamento como causa de desempenho",
        "inferir cena, áudio ouvido, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
        "usar pergunta específica como selo de precisão científica",
        "reproduzir alegações científicas sem fonte, escopo e revisão proporcionais",
    ]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 047")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20261005-251", "obs-20261005-252", "obs-20261005-253"]
new_case = "obs-20261005-254"
pattern["name"] = "Pergunta ou contradição específica em Short educativo"
pattern["statement"] = "Em Shorts educativos de ciência ou conhecimento, uma pergunta literal ou contradição específica que nomeia o fenômeno permite identificar o assunto antes da reprodução; quando a fala responde ao mesmo objeto, embalagem e entrega declarada tornam-se semanticamente comparáveis. Esse alinhamento não valida precisão científica, completude, compreensão ou retenção."
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 11
pattern["supportingCount"] = 11
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 9
pattern["sourceDiversityCount"] = 9
pattern["conditions"] = [
    "formato vertical curto ou Short funcionalmente equivalente",
    "pergunta literal ou contradição específica nomeia o fenômeno no título",
    "fala ou legenda responde ao mesmo objeto quando a entrega é avaliada",
    "promessa e resposta permanecem proporcionais à evidência",
    "rótulos genéricos como ciência, experimento ou curiosidade não bastam",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20261005-251","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Título pergunta se a IA roubará empregos e a fala responde ao mesmo risco por tarefas e competências.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["dez segundos; estudos citados sem fonte rastreável; sem audiovisual ou revisão científica"]},
    {"referenceId":"obs-20261005-252","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Título pergunta por fantasmas e explicação científica; a fala oferece alternativas naturais correspondentes.","evidence":"Metadados, transcrição automática integral e quinze comentários amostrados.","limitations":["descrição vazia e estudos não identificados; sem audiovisual"]},
    {"referenceId":"obs-20261005-253","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Título pergunta por que bocejamos e a fala responde ao mesmo fenômeno.","evidence":"Metadados e transcrição automática integral.","limitations":["sem descrição, fontes, audiovisual ou revisão científica"]},
    {"referenceId":"obs-20261005-254","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"A fala entrega extração de DNA, mas o título genérico sobre morango e ciência não nomeia fenômeno, pergunta ou resultado.","evidence":"Metadados, descrição integral, transcrição automática integral e 29 comentários amostrados.","limitations":["não conta como apoio nem como contraexemplo de desempenho"]},
])
pattern["limitations"] = [
    "Onze apoios formais vêm de nove criadores e fontes; demonstram recorrência de clareza semântica, não precisão, compreensão, retenção ou desempenho.",
    "Os três novos apoios têm transcrição automática integral, mas nenhum audiovisual, áudio ouvido, texto na tela, edição ou ritmo auditado.",
    "O segundo caso-limite mostra que uma entrega substantiva pode existir sob título genérico; isso não satisfaz o mecanismo de identificação antecipada.",
    "Duas referências novas apresentam alegações científicas sem fontes rastreáveis, e a terceira cita instituições sem ligar estudos específicos.",
    "O apoio internacional amplia contexto linguístico, mas não substitui evidência brasileira contemporânea.",
    "Popularidade, escala, comentários e produção permanecem contexto não causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url":"https://www.youtube.com/watch?v=lgBS0mK0Q24","reason":"título recente e específico, mas nenhuma fala, legenda ou mídia utilizável foi adquirida"},
    {"url":"https://www.youtube.com/watch?v=lV0AhTvJI_I","reason":"contradição específica, porém a fala mistura ciência e conspiração sem fontes; menor segurança editorial"},
    {"url":"https://www.youtube.com/watch?v=ixdhq_Hm83s","reason":"título específico, mas a transcrição contém apenas música em telugu e não confirma a explicação"},
    {"url":"https://www.youtube.com/watch?v=x2gGfjL9z9U","reason":"fala acessível, porém metadados completos falharam e o conteúdo internacional excede a prioridade brasileira"},
    {"url":"https://www.youtube.com/watch?v=fYqWwAn2fqE","reason":"pergunta específica e transcrição acessível, mas publicação de 2022 e resposta conceitual menos comparável ao formato selecionado"},
    {"url":"https://www.youtube.com/watch?v=rp0N3tBoK3Y","reason":"pergunta específica e fala acessível, porém duração de 2 minutos e 43 segundos e transcrição muito ruidosa"},
    {"url":"https://www.youtube.com/watch?v=S0m0MfQ0zpg","reason":"tema relevante e legenda humana em inglês, porém publicação antiga e apresentação menos curta"},
    {"url":"https://www.youtube.com/watch?v=V86V44InmmY","reason":"título interrogativo, mas fala ruidosa e alegações sobre hemisférios cerebrais sem fontes"},
    {"url":"https://www.youtube.com/watch?v=Gue1bTYHCFE","reason":"apoio potencial com transcrição integral, mas publicação de 2022 e canal internacional localizado"},
    {"url":"https://www.youtube.com/watch?v=UErrG1UhF7k","reason":"título genérico e fala automática em inglês sem procedência compatível com o canal"},
    {"url":"https://www.youtube.com/watch?v=N-uQ92qnSEk","reason":"título científico genérico, mas a fala é oferta de suplementos e não entrega a promessa"},
    {"url":"https://www.youtube.com/watch?v=6Sy5NTNCBY4","reason":"sem transcrição e sem audiovisual adquirido"},
    {"url":"https://www.youtube.com/watch?v=8l1uBe_Bmd4","reason":"lista de sites, não pergunta ou contradição científica específica"},
    {"url":"https://www.youtube.com/watch?v=CYBLpszQDP8","reason":"lista geográfica, sem pergunta científica específica"},
    {"url":"https://www.youtube.com/watch?v=Su2P20-WuvQ","reason":"lista geográfica, sem pergunta científica específica"},
    {"url":"https://www.youtube.com/watch?v=JFngu9q_o-U","reason":"título específico, porém duração longa e fora do núcleo de Shorts comparáveis"},
    {"url":"https://www.youtube.com/watch?v=Gpl1EDwQ6XU","reason":"assunto específico, mas embalagem descritiva sem pergunta ou contradição e menor prioridade que a exploração selecionada"},
    {"url":"https://www.youtube.com/watch?v=PpBdcLBtjA0","reason":"selecionado como apoio; mantido aqui apenas para impedir contagem duplicada"},
]
discarded = [d for d in discarded if d["url"] != "https://www.youtube.com/watch?v=PpBdcLBtjA0"]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 248,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20261005-255"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 4,
    "internationalReferences": 1,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["explicativo","educativo","autoridade_opiniao","curiosidade","demonstracao"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "as cinco tentativas de vídeo falharam por formato indisponível e as cinco tentativas de capa produziram somente HTML de indisponibilidade de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, execução visual, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":5,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":0,
        "limitation":"cinco transcrições automáticas integrais substituem somente a fala e podem errar termos científicos; nenhuma legenda humana foi adquirida",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":3,
        "sampledComments":46,
        "zeroReturnedReferences":2,
        "unavailableReferences":0,
        "limitation":"as amostras são públicas, pequenas e não representativas; relatos, dúvidas, elogios e objeções não foram tratados como precisão, compreensão ou opinião coletiva",
    },
    "baselineCoverage": {
        "sampledProfiles":5,
        "contemporaneousBaselines":0,
        "limitation":"não houve coorte contemporânea, teste de compreensão, revisão científica ou experimento causal",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["uma demonstração científica substantiva pode ficar semanticamente opaca antes da reprodução quando o título só nomeia objeto e ciência genericamente"],
    "safetyFindings": [
        "pergunta específica foi tratada como mecanismo de clareza, não como prova de precisão científica",
        "alegações de emprego, infrassom, bocejo, DNA e conservação não foram ensinadas como validadas sem revisão proporcional",
        "comentários, popularidade, escala, mídia e produção permaneceram contexto não causal",
        "nenhuma cena, áudio ouvido, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToBatch":5,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores novos elevam de oito para onze os apoios do padrão de pergunta ou contradição específica em Short educativo. Um caso-limite separa conteúdo científico substantivo de embalagem semanticamente específica. O padrão permanece provisório.",
    "nextTarget": "Short científico brasileiro recente, de criador pequeno ou médio, com audiovisual integral, pergunta específica, fonte ligada à alegação e teste de compreensão; priorizar um caso em que título claro prometa um fenômeno, mas a explicação entregue outro ou induza uma conclusão cientificamente incorreta",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Cinco transcrições automáticas integrais substituem somente a fala e podem errar termos científicos.",
        "Quarenta e seis comentários foram amostrados sem representatividade estatística.",
        "Alegações científicas e previsões não receberam revisão humana especializada neste lote.",
        "Não houve retenção, auditoria visual, teste de compreensão ou causalidade controlada.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
