#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Rebuild the last approved checkpoint and reuse its schema helpers.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-031.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-18T11:58:07.000Z"
OBSERVED = "2026-09-18"
RUN_ID = "run-20260918-supervised-032"
PATTERN_ID = "pat-20260824-004"
BATCH_IDS = {f"obs-20260918-{n}" for n in range(176, 181)}

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
              comment_provenance=False):
    item = make_ref(
        id=id, title=title, creator=creator, identity=identity, url=url,
        published=published, duration=duration, accessible=accessible,
        missing=missing, metrics=metrics, cls=classification,
        comparison=comparison, observations=observations,
        interpretations=interpretations, scores=scores, lenses=lenses,
        replicable=replicable, contingent=contingent, role=role,
        evidence_level=evidence_level, eligible=eligible, claims=claims,
        source_type=source_type, comment_provenance=comment_provenance,
    )
    item["country"] = "BR"
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "conteúdo editorial público do próprio criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhuma história privada identificável de terceiro foi ensinada"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, analogias, imagens ou roteiro",
        "tratar título claro como prova de retenção, precisão científica ou desempenho",
        "inferir cena, áudio, texto na tela, edição ou ritmo sem mídia reproduzida",
        "usar visualizações, curtidas, comentários ou fama como prova causal",
    ]
    return item


refs = [
    build_ref(
        id="obs-20260918-176",
        title="Por que o universo parece tão silencioso?",
        creator="silva", identity="silva-ciencia",
        url="https://www.youtube.com/watch?v=60MLzzp3yo4",
        published="2026-06-06", duration="PT57S",
        accessible=[
            "título", "criador", "data exata", "duração de 57 segundos",
            "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "5 visualizações, 1 curtida e zero comentários declarados",
            "pergunta literal e fenômeno do paradoxo de Fermi nomeados antes da reprodução",
        ],
        missing=MISSING_AV + ["descrição pública substantiva", "comentários", "baseline funcional contemporâneo", "verificação científica independente"],
        metrics={"viewsObserved":5,"likesObserved":1,"commentsObserved":0},
        classification=cls(
            material="video_curto", presentations=["narracao_imagens"],
            primary="educativo", secondary=["curiosidade"],
            mix=[{"family":"educativo","percentage":70},{"family":"curiosidade","percentage":30}],
            objectives=["educar","interromper_rolagem","comentario"],
            topic="paradoxo de Fermi e silêncio do universo", segment="divulgação científica",
            subsegment="astronomia em vídeo curto", audience="público geral curioso sobre vida extraterrestre",
            production="unknown", scale="small", replicability="high", duration="31_to_60s",
            mechanisms=["curiosidade","tensao","antecipacao"], hooks=["pergunta","problema"],
            narrative=["problema","mecanismo","conflito","continuidade_serial","cta"],
            proof=["mecanismo_explicado"], cta=["comentar","proxima_parte","seguir"],
            evidence=[
                "O título pergunta por que o universo parece silencioso e nomeia o assunto antes da reprodução.",
                "Entre 0:00 e 0:09, a transcrição repete a pergunta e nomeia o paradoxo de Fermi.",
                "Entre 0:42 e 0:56, abre duas explicações para uma continuação e pede opinião.",
            ],
        ),
        comparison={"level":1,"group":"Short educativo brasileiro de ciência com pergunta literal e fenômeno nomeado no título","referenceIds":["obs-20260918-177","obs-20260918-178"],"confidence":"high"},
        observations=[
            "A pergunta e o fenômeno científico são identificáveis no título e reiterados na abertura transcrita.",
            "A transcrição promete teorias para uma segunda parte, mas a exatidão científica não foi auditada.",
        ],
        interpretations=[
            "A embalagem permite reconhecer tema e lacuna antes da reprodução.",
            "Isso não mede retenção, compreensão nem qualidade científica.",
        ],
        scores={"gancho":88,"clareza":92,"relevancia":82,"desejo":72,"confianca":58,"retencao":"not_assessed","acao":76,"objecoes":64},
        lenses={
            "apressado":"Identifica universo silencioso e a pergunta imediatamente.",
            "analitico":"Reconstrói a premissa pela fala, mas exige revisão das cifras e teorias.",
            "aspiracional":"A recompensa prometida é resolver um mistério cósmico.",
            "comunidade":"O CTA pede opinião, mas não havia comentários públicos declarados.",
            "cetico":"Separa clareza do título de exatidão, retenção e alcance.",
        },
        replicable=["Nomear fenômeno e pergunta no título.","Repetir a pergunta na primeira frase.","Delimitar o que será explicado sem copiar texto."],
        contingent=["Transcrição automática pode conter erros.","Tema cósmico e promessa de continuação não provam desempenho.","Métricas baixas são contexto, não contraexemplo."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"o título nomeia uma pergunta e o fenômeno antes da reprodução","requiredModalities":["title"],"observedModalities":["title"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260918-177",
        title="Por que você ODEIA certas músicas? A Ciência explica!",
        creator="Oxe, Sério?", identity="oxe-serio",
        url="https://www.youtube.com/watch?v=NgToKvPOVc4",
        published="2025-07-02", duration="PT1M35S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 1 minuto e 35 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "3 visualizações e zero comentários declarados; curtidas não exibidas",
            "pergunta sobre gosto musical e promessa de explicação científica",
        ],
        missing=MISSING_AV + ["comentários", "baseline funcional contemporâneo", "fontes para as generalizações neurocientíficas"],
        metrics={"viewsObserved":3,"likesObserved":"not_assessed","commentsObserved":0},
        classification=cls(
            material="video_curto", presentations=["narracao_imagens","comentario"],
            primary="educativo", secondary=["curiosidade","humor"],
            mix=[{"family":"educativo","percentage":60},{"family":"curiosidade","percentage":25},{"family":"humor","percentage":15}],
            objectives=["educar","interromper_rolagem","seguidores"],
            topic="preferência e rejeição musical", segment="divulgação científica",
            subsegment="neurociência popular em vídeo curto", audience="público geral interessado em música e cérebro",
            production="unknown", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","identificacao","humor"], hooks=["pergunta","identificacao"],
            narrative=["problema","mecanismo","situacao","conclusao","cta"],
            proof=["mecanismo_explicado","alegacao_sem_prova"], cta=["seguir"],
            evidence=[
                "O título explicita rejeição musical e promete explicação científica.",
                "Entre 0:00 e 0:08, a fala reformula a pergunta como diferença de preferência.",
                "Entre 0:27 e 1:24, a fala atribui preferência a previsibilidade e familiaridade; fontes não aparecem na cobertura acessível.",
            ],
        ),
        comparison={"level":1,"group":"Short educativo brasileiro de ciência com pergunta literal e fenômeno nomeado no título","referenceIds":["obs-20260918-176","obs-20260918-178"],"confidence":"high"},
        observations=[
            "Pergunta, objeto e promessa de explicação aparecem integralmente no título.",
            "A fala responde com familiaridade e previsão, mas generalizações e fontes não foram auditadas.",
        ],
        interpretations=[
            "A embalagem delimita a lacuna semântica antes da reprodução.",
            "Clareza do tema não valida a neurociência popular nem demonstra desempenho.",
        ],
        scores={"gancho":90,"clareza":91,"relevancia":86,"desejo":78,"confianca":54,"retencao":"not_assessed","acao":68,"objecoes":52},
        lenses={
            "apressado":"Reconhece gosto musical e explicação científica no título.",
            "analitico":"Exige fontes e linguagem menos universalizante.",
            "aspiracional":"Promete autoconhecimento cotidiano.",
            "comunidade":"Usa gêneros musicais como identificação; não havia comentários declarados.",
            "cetico":"Não transforma dopamina, gosto ou métricas em prova causal.",
        },
        replicable=["Formular pergunta cotidiana com objeto específico.","Prometer uma explicação delimitada.","Distinguir hipótese explicativa de fato comprovado."],
        contingent=["Alegações neurocientíficas precisam de fontes.","Humor e gêneros citados são escolhas do criador.","Métricas baixas não refutam a clareza semântica."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"o título nomeia pergunta, objeto e natureza da explicação","requiredModalities":["title"],"observedModalities":["title"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260918-178",
        title="Você sabia como uma âncora funcionava?",
        creator="Ciência Cantada", identity="ciencia-cantada",
        url="https://www.youtube.com/watch?v=1oWuw20XOwg",
        published="2025-10-20", duration="PT1M43S",
        accessible=[
            "título", "criador", "data exata", "duração de 1 minuto e 43 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "34 visualizações e 1 curtida; contagem de comentários não exibida",
            "pergunta sobre âncoras e explicação verbal da corrente e da catenária",
        ],
        missing=MISSING_AV + ["descrição pública substantiva", "comentários", "baseline funcional contemporâneo", "verificação técnica independente"],
        metrics={"viewsObserved":34,"likesObserved":1,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_curto", presentations=["narracao_imagens","tutorial"],
            primary="educativo", secondary=["curiosidade","explicativo"],
            mix=[{"family":"educativo","percentage":65},{"family":"curiosidade","percentage":20},{"family":"explicativo","percentage":15}],
            objectives=["educar","interromper_rolagem","compartilhamento"],
            topic="funcionamento de âncoras e catenária", segment="divulgação científica",
            subsegment="engenharia cotidiana em vídeo curto", audience="público geral curioso sobre navios e mecânica",
            production="unknown", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","surpresa","utilidade_pratica"], hooks=["pergunta","afirmacao_contraintuitiva"],
            narrative=["problema","mecanismo","progressao","conclusao"],
            proof=["mecanismo_explicado"], cta=[],
            evidence=[
                "O título pergunta como a âncora funciona e nomeia o objeto antes da reprodução.",
                "Entre 0:00 e 0:18, a fala contradiz a explicação baseada apenas no peso.",
                "Entre 0:18 e 1:29, a fala desenvolve fundo, corrente e catenária; as imagens não foram observadas.",
            ],
        ),
        comparison={"level":1,"group":"Short educativo brasileiro de ciência com pergunta literal e fenômeno nomeado no título","referenceIds":["obs-20260918-176","obs-20260918-177"],"confidence":"high"},
        observations=[
            "Objeto, pergunta e contradição específica aparecem no pacote título-abertura.",
            "A progressão verbal é acessível; qualquer demonstração ou diagrama visual permanece não observado.",
        ],
        interpretations=[
            "Pergunta concreta e crença negada tornam o assunto identificável antes da reprodução.",
            "Isso não comprova compreensão, retenção nem exatidão de todos os números citados.",
        ],
        scores={"gancho":92,"clareza":93,"relevancia":83,"desejo":76,"confianca":66,"retencao":"not_assessed","acao":62,"objecoes":68},
        lenses={
            "apressado":"Identifica âncora e dúvida funcional imediatamente.",
            "analitico":"Segue a explicação verbal, mas precisa de fonte e confirmação visual.",
            "aspiracional":"A recompensa é compreender um mecanismo invisível do cotidiano.",
            "comunidade":"Não houve comentários acessíveis para avaliar participação.",
            "cetico":"Desconta números, imagens presumidas e métricas de alcance.",
        },
        replicable=["Usar objeto concreto no título.","Negar uma explicação intuitiva na abertura.","Desenvolver mecanismo em etapas sem copiar analogias."],
        contingent=["Números e explicação técnica precisam de revisão.","Hashtags e embalagem viral são contexto.","Audiovisual e desempenho não foram auditados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"o título nomeia objeto e pergunta; a fala abre com contradição específica","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260918-179",
        title="Poder da ciência!!",
        creator="Entretenimento Total", identity="entretenimento-total",
        url="https://www.youtube.com/watch?v=K3VutA9eawU",
        published="2024-08-26", duration="PT1M",
        accessible=[
            "título", "criador", "data exata", "duração de 60 segundos",
            "3 visualizações, 1 curtida e zero comentários declarados",
            "hashtag de ciência sem fenômeno, pergunta ou contradição específica",
        ],
        missing=MISSING_AV + ["descrição pública substantiva", "fala", "transcrição", "legenda", "comentários", "assunto efetivamente entregue", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":3,"likesObserved":1,"commentsObserved":0},
        classification=cls(
            material="video_curto", presentations=["indeterminado"],
            primary="curiosidade", secondary=["educativo"],
            mix=[{"family":"curiosidade","percentage":60},{"family":"educativo","percentage":40}],
            objectives=["visualizacao","interromper_rolagem"],
            topic="ciência não especificada", segment="entretenimento científico",
            subsegment="vídeo curto genérico", audience="público geral de vídeos curtos",
            production="unknown", scale="small", replicability="high", duration="31_to_60s",
            mechanisms=["curiosidade","surpresa"], hooks=["promessa"],
            narrative=["promessa"], proof=["ausencia_prova_necessaria"], cta=[],
            confidence="medium",
            evidence=[
                "O título usa apenas uma promessa genérica de ciência.",
                "Não houve descrição, transcrição ou mídia suficiente para identificar o fenômeno entregue.",
            ],
        ),
        comparison={"level":1,"group":"Short brasileiro rotulado como ciência, mas sem pergunta ou fenômeno específico no título","referenceIds":["obs-20260918-176","obs-20260918-177","obs-20260918-178"],"confidence":"medium"},
        observations=[
            "O título não permite identificar qual pergunta, fenômeno ou contradição será tratado.",
            "Como o conteúdo não ficou acessível, nenhuma análise de entrega foi ensinada.",
        ],
        interpretations=[
            "É caso-limite de clareza semântica, não contraexemplo de retenção ou qualidade.",
            "Métricas baixas não autorizam inferência causal.",
        ],
        scores={"gancho":62,"clareza":30,"relevancia":"not_assessed","desejo":54,"confianca":"not_assessed","retencao":"not_assessed","acao":"not_assessed","objecoes":28},
        lenses={
            "apressado":"Vê ciência, mas não sabe qual assunto receberá.",
            "analitico":"Não dispõe de conteúdo suficiente para avaliar explicação.",
            "aspiracional":"A promessa de poder é ampla e não delimitada.",
            "comunidade":"Zero comentários declarados não mede interesse.",
            "cetico":"Recusa inferir cenas, entrega ou retenção.",
        },
        replicable=["Evitar título genérico; nomear pergunta, objeto ou fenômeno."],
        contingent=["Somente a embalagem textual foi acessível.","Não é possível ensinar fala, cena, áudio, ritmo ou entrega.","Métricas não explicam desempenho."],
        role="case_limit", evidence_level=1, eligible=False,
        claims=[
            {"claim":"o título não nomeia pergunta, fenômeno ou contradição específica","requiredModalities":["title"],"observedModalities":["title"],"sufficient":True},
            {"claim":"o vídeo não entrega valor ou retém menos","requiredModalities":["video","transcript","retention"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_only",
    ),
    build_ref(
        id="obs-20260918-180",
        title="Partiu Experimento - Convecção",
        creator="Partiu Física", identity="partiu-fisica",
        url="https://www.youtube.com/watch?v=sHKiPJCb8XE",
        published="2020-06-18", duration="PT5M22S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 5 minutos e 22 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "16.128 visualizações, 457 curtidas e 16 comentários declarados",
            "amostra pública integral de 16 comentários", "materiais, procedimento, resultado declarado e explicação verbal",
        ],
        missing=MISSING_AV + ["confirmação visual do movimento do corante", "baseline funcional contemporâneo", "revisão independente do procedimento e da segurança"],
        metrics={"viewsObserved":16128,"likesObserved":457,"commentsObserved":16},
        classification=cls(
            material="video_longo", presentations=["demonstracao","tutorial","camera_direta"],
            primary="demonstracao", secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":60},{"family":"educativo","percentage":30},{"family":"curiosidade","percentage":10}],
            objectives=["educar","salvamento","compartilhamento"],
            topic="experimento de convecção térmica", segment="educação científica",
            subsegment="física experimental escolar", audience="estudantes e professores buscando demonstração de propagação de calor",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","curiosidade","confianca"], hooks=["promessa","demonstracao_antecipada"],
            narrative=["promessa","mecanismo","tentativa","prova","conclusao","cta"],
            proof=["demonstracao","mecanismo_explicado"], cta=["experimentar","compartilhar","seguir"],
            evidence=[
                "A abertura transcrita declara o objetivo e lista materiais simples.",
                "A fala descreve o preparo, aquecimento, deslocamento do corante e interpretação como corrente de convecção.",
                "Os 16 comentários incluem dúvidas sobre materiais e temperatura, resposta do criador e um relato público de reprodução bem-sucedida; não são auditoria do experimento.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de demonstração experimental; fora do grupo-alvo de títulos de Shorts","referenceIds":[],"confidence":"high"},
        observations=[
            "Objetivo, materiais, procedimento, resultado declarado e explicação aparecem na transcrição.",
            "Comentários registram dúvidas, ajuste sobre temperatura da água e um relato de reprodução; o resultado visual não foi observado.",
        ],
        interpretations=[
            "A cadeia verbal favorece reprodutibilidade descritiva, mas não confirma visualmente o fenômeno nem sua segurança.",
            "A exploração não apoia o padrão-alvo e não cria hipótese nova.",
        ],
        scores={"gancho":72,"clareza":90,"relevancia":88,"desejo":68,"confianca":82,"retencao":"not_assessed","acao":86,"objecoes":78},
        lenses={
            "apressado":"Recebe objetivo e materiais logo no começo.",
            "analitico":"Consegue reconstruir o procedimento pela fala, sem confirmar o movimento visual.",
            "aspiracional":"A recompensa é reproduzir e compreender um fenômeno escolar.",
            "comunidade":"Comentários trazem dúvidas, resposta e relato de reprodução, sem representatividade.",
            "cetico":"Exige vídeo, revisão de segurança e controle de temperatura.",
        },
        replicable=["Declarar objetivo e materiais antes do procedimento.","Relacionar cada passo ao mecanismo físico.","Responder dúvidas operacionais sem prometer resultado universal."],
        contingent=["Uso de vela exige supervisão e orientação de segurança.","Resultado visual não foi observado.","Comentários não substituem auditoria nem experimento controlado."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"a fala organiza objetivo, materiais, procedimento, resultado declarado e explicação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o movimento visual ocorreu exatamente como descrito","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_16_public_comments",
        comment_provenance=True,
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 032")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260918-176", "obs-20260918-177", "obs-20260918-178"]
new_case = "obs-20260918-179"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 8
pattern["supportingCount"] = 8
pattern["caseLimitCount"] = 1
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260918-176","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta literal e paradoxo de Fermi aparecem no título e na abertura transcrita.","evidence":"Metadados e transcrição automática integral.","limitations":["sem audiovisual, retenção ou revisão científica"]},
    {"referenceId":"obs-20260918-177","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta cotidiana sobre rejeição musical e promessa científica delimitam o assunto antes da reprodução.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["fontes neurocientíficas não acessíveis","sem audiovisual ou retenção"]},
    {"referenceId":"obs-20260918-178","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Objeto, pergunta e contradição sobre o peso da âncora aparecem no pacote título-abertura.","evidence":"Metadados e transcrição automática integral.","limitations":["sem confirmação visual, retenção ou revisão técnica"]},
    {"referenceId":"obs-20260918-179","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"medium","observation":"O título genérico rotula ciência, mas não nomeia pergunta, fenômeno ou contradição; o conteúdo não ficou acessível.","evidence":"Metadados públicos apenas.","limitations":["sem descrição, transcrição ou mídia","não é contraexemplo de desempenho"]},
])
pattern["limitations"] = [
    "Oito apoios formais vêm de seis criadores e fontes; demonstram recorrência de clareza semântica, não retenção, compreensão ou desempenho.",
    "Os três novos apoios possuem título e transcrição integral, mas nenhum audiovisual, comentário, baseline funcional ou teste de compreensão.",
    "O primeiro caso-limite mostra que rotular ciência genericamente não nomeia o assunto; como a entrega não foi acessada, não é contraexemplo causal.",
    "Precisão científica e adequação das explicações exigem revisão independente; título claro não valida conteúdo.",
    "Popularidade, hashtags, escala e produção permanecem contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("Wh48t0WSqSk", "pergunta comparável, mas publicação de 2021 e cobertura redundante com três apoios mais recentes"),
        ("fYqWwAn2fqE", "definição comparável, mas publicação de 2022 e redundante"),
        ("YfB928SsdMQ", "título genérico sobre curiosidades, sem fenômeno específico"),
        ("Uhbp2M2dLJ8", "lista de mistérios com promessa ampla; origem e fontes insuficientes"),
        ("-dAYRmJ0i04", "lista de mistérios com promessa ampla; origem e fontes insuficientes"),
        ("8afZM58BX64", "título afirma ciência por trás da fala, mas não formula pergunta literal ou contradição específica"),
        ("t8NVgWXb2Vo", "tema nomeado, porém estrutura descritiva e não pergunta/contradição"),
        ("CNV5qBwshHw", "lista de curiosidades geográficas, funcionalmente adjacente mas não pergunta científica literal"),
        ("tXMStTLvh6s", "lista de curiosidades geográficas redundante"),
        ("yzDOOORlp_w", "quiz sem fenômeno identificável no título"),
        ("xqoL5Hzxork", "aula nomeia fatores, mas não pergunta ou contradição no título"),
        ("coJxF7dDUZ8", "alegação religiosa forte com custo de prova e risco de desinformação"),
        ("aFGSs9qEE5U", "experimento escolar com cobertura inferior à exploração selecionada"),
        ("ay8iO7IdmLU", "experimento curto sem transcrição disponível na triagem"),
        ("gTGcMC1PL9A", "experimento sem transcrição e mídia indisponível"),
        ("TL0179xT9mw", "experimento sem cobertura suficiente para ensinar o resultado"),
        ("htEhA83rTBg", "experimento muito curto e sem cobertura suficiente"),
        ("MAovGPfRE4Y", "experimento com cobertura inferior e sem auditoria visual"),
        ("l1_0ZsvMZRY", "exploração alternativa com uso de chama e imprecisão conceitual possível na transcrição"),
        ("zNOYfRmBYoA", "compilação de experimentos, menos controlada para uma única exploração"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 80,
    "referenceIds": [f"obs-20260918-{n}" for n in range(176, 181)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260918-180"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 5,
    "replicableReferences": 5,
    "creativeFamiliesObserved": ["educativo","curiosidade","explicativo","humor","demonstracao"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads de vídeo falharam por timeout ou formato indisponível; as cinco capas expiraram sem bytes","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":4,"partialAutomatic":0,"none":1,"limitation":"transcrições automáticas substituem somente a fala e podem conter erros"},
    "commentsCoverage": {"countsOnly":3,"sampledReferences":1,"sampledComments":16,"limitation":"amostras públicas não são representativas; zero exibido é dado da plataforma, não desinteresse comprovado"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"canais, datas, temas e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["rotular ciência sem nomear pergunta, objeto ou fenômeno não fornece a mesma clareza semântica"],
    "safetyFindings": [
        "alegações científicas não foram ensinadas como fatos sem revisão independente",
        "o caso de cobertura insuficiente não recebeu análise de cena, fala ou entrega",
        "métricas permaneceram contexto não causal",
        "nenhuma frase, analogia, imagem ou roteiro foi recomendado para cópia",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes reforçam a recorrência de pergunta ou contradição específica que nomeia o assunto antes da reprodução. O padrão passa de cinco para oito apoios e recebe o primeiro caso-limite; permanece provisório e não demonstra retenção, compreensão, precisão científica ou desempenho.",
    "nextTarget": "Short científico brasileiro de criador pequeno ou médio com audiovisual integral, pergunta específica no título, confirmação visual da entrega e teste de compreensão; procurar um caso comparável cujo título seja claro, mas a explicação entregue outro fenômeno ou induza interpretação errada",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "Quatro transcrições são automáticas e podem conter erros; uma referência possui somente metadados.",
        "Somente a exploração forneceu 16 comentários; não há representatividade estatística.",
        "Não houve baseline, retenção, replay, teste de compreensão ou revisão científica independente.",
        "Nenhum resultado autoriza causalidade ou validação.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
