#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-032.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-19T11:37:30.000Z"
OBSERVED = "2026-09-19"
RUN_ID = "run-20260919-supervised-033"
PATTERN_ID = "pat-20260910-010"
BATCH_IDS = {f"obs-20260919-{n}" for n in range(181, 186)}

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
        "evidence": ["erros pessoais são autoatribuídos; nenhum terceiro privado identificável foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, histórias, personagens ou roteiro",
        "usar erro de terceiro sem consentimento ou para humilhação",
        "tratar visualizações, curtidas, comentários, fama ou orçamento como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
    ]
    return item


refs = [
    build_ref(
        id="obs-20260919-181",
        title='5 "ERROS" DE PRONÚNCIA mais comuns entre os BRASILEIROS (vogais) | English in Brazil',
        creator="English in Brazil by Carina Fragozo", identity="english-in-brazil-carina-fragozo",
        url="https://www.youtube.com/watch?v=0fzsZDM_ebM",
        published="2021-08-20", duration="PT14M40S",
        accessible=[
            "título", "criadora", "descrição pública", "data exata", "duração de 14 minutos e 40 segundos",
            "transcrição automática integral em português com 334 segmentos e timestamps", "fala por substituição textual",
            "35.517 visualizações e 4.679 curtidas nos metadados consultados", "amostra pública limitada de 30 comentários",
            "cinco categorias de pronúncia, pares contrastivos, explicações articulatórias e exercício com feedback declarados na fala",
        ],
        missing=MISSING_AV + ["total público de comentários", "baseline comparável", "teste de aprendizagem", "auditoria independente do aplicativo anunciado"],
        metrics={"viewsObserved":35517,"likesObserved":4679,"commentsObserved":"not_assessed"},
        classification=cls(
            presentations=["camera_direta","tutorial"], primary="educativo", secondary=["demonstracao","oferta_direta"],
            mix=[{"family":"educativo","percentage":65},{"family":"demonstracao","percentage":25},{"family":"oferta_direta","percentage":10}],
            objectives=["educar","lead","venda"], topic="erros comuns de pronúncia de vogais em inglês",
            segment="educação e idiomas", subsegment="pronúncia para brasileiros", audience="brasileiros aprendendo inglês",
            production="unknown", scale="large", replicability="high", duration="over_60s",
            mechanisms=["identificacao","alivio","confianca","utilidade_pratica"], hooks=["numero","problema"],
            narrative=["problema","progressao","mecanismo","conclusao","cta"], proof=["mecanismo_explicado","demonstracao"], cta=["experimentar","clicar"],
            advertising="parceria_com_criador", intent="explicita", entity={"kind":"servico","name":"ELSA Speak","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:25, a fala delimita erros de vogais comuns entre brasileiros.",
                "Entre 1:54 e 3:56, explica vogal de apoio, origem no português e risco de incompreensão.",
                "Entre 4:23 e 12:24, contrasta pares de vogais e relaciona som, articulação e significado.",
                "Entre 14:21 e 14:36, propõe prática com feedback no aplicativo anunciado.",
            ],
        ),
        comparison={"level":2,"group":"conteúdo brasileiro de inglês que apresenta erro plausível sem humilhar e oferece correção observável","referenceIds":["obs-20260919-182","obs-20260919-183"],"confidence":"high"},
        observations=[
            "Os erros são enquadrados como fenômenos recorrentes de transferência entre línguas, não como incapacidade individual.",
            "A fala explica contrastes e convida à prática; o resultado de aprendizagem e o feedback do aplicativo não foram auditados.",
            "Comentários amostrados incluem dúvida articulatória e discordância sobre generalização; são contexto, não medida de compreensão.",
        ],
        interpretations=[
            "Nomear o erro, explicar sua origem e demonstrar a correção preserva dignidade enquanto oferece ação pedagógica.",
            "Oferta comercial e métricas não demonstram confiança, aprendizagem, retenção ou conversão.",
        ],
        scores={"gancho":86,"clareza":94,"relevancia":90,"desejo":80,"confianca":84,"retencao":"not_assessed","acao":88,"objecoes":78},
        lenses={
            "apressado":"Recebe problema, público e recorte de vogais no título e na abertura.",
            "analitico":"Consegue reconstruir pares, mecanismo e correção pela transcrição; exige auditoria do aplicativo.",
            "aspiracional":"A recompensa é comunicar-se com menos ambiguidade.",
            "comunidade":"O enquadramento coletivo reduz personalização; comentários não representam todos os alunos.",
            "cetico":"Separa ensino observável de eficácia, publicidade e desempenho.",
        },
        replicable=["Enquadrar o erro como fenômeno plausível.","Contrastar produção problemática e alternativa correta.","Ligar correção a significado e prática sem copiar exemplos."],
        contingent=["Transcrição automática pode conter erros.","Generalizações sobre brasileiros precisam de proporcionalidade.","Publicidade do aplicativo é contexto comercial."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"a fala apresenta erros plausíveis sem humilhação e explica correções praticáveis","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_30_public_comments",
        comment_provenance=True,
    ),
    build_ref(
        id="obs-20260919-182",
        title="Dicas Para Praticar/Aprender Inglês + Primeiro Mico Falando Inglês",
        creator="Gaby Gomes", identity="gaby-gomes",
        url="https://www.youtube.com/watch?v=Dqur329dHaU",
        published="2015-03-19", duration="PT12M12S",
        accessible=[
            "título", "criadora", "descrição pública", "data exata", "duração de 12 minutos e 12 segundos",
            "transcrição automática integral em português com 300 segmentos e timestamps", "fala por substituição textual",
            "726 visualizações, 40 curtidas e 3 comentários nos metadados consultados", "amostra integral dos 3 comentários públicos retornados",
            "relato pessoal do pedido de chip, distinção falada entre chip e ship e recomendação de praticar sem medo de errar",
        ],
        missing=MISSING_AV + ["baseline comparável", "teste de aprendizagem", "confirmação independente da situação narrada"],
        metrics={"viewsObserved":726,"likesObserved":40,"commentsObserved":3},
        classification=cls(
            presentations=["camera_direta","depoimento","tutorial"], primary="storytelling", secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"storytelling","percentage":45},{"family":"educativo","percentage":40},{"family":"autoridade_opiniao","percentage":15}],
            objectives=["educar","identificacao","confianca"], topic="prática de inglês e primeiro mal-entendido no intercâmbio",
            segment="educação e idiomas", subsegment="relato de aprendizagem em intercâmbio", audience="brasileiros inseguros para praticar inglês",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["identificacao","alivio","aproximacao","utilidade_pratica"], hooks=["narrativo","problema"],
            narrative=["situacao","problema","virada","conclusao","cta"], proof=["depoimento","mecanismo_explicado"], cta=["comentar","seguir"],
            evidence=[
                "Entre 5:55 e 7:17, narra que tentou comprar um chip e não foi compreendida.",
                "Entre 6:10 e 7:17, distingue a palavra pretendida da pronúncia que remete a ship.",
                "Entre 11:01 e 11:29, recomenda praticar, aceitar correções e aprender com erros.",
            ],
        ),
        comparison={"level":2,"group":"conteúdo brasileiro de inglês que apresenta erro plausível sem humilhar e oferece correção observável","referenceIds":["obs-20260919-181","obs-20260919-183"],"confidence":"high"},
        observations=[
            "A própria narradora assume o erro, preserva sua dignidade e explica a ambiguidade de pronúncia.",
            "O relato conduz a uma orientação de prática e aceitação de correção; não há teste de aprendizagem.",
        ],
        interpretations=[
            "Autoatribuição reduz o risco de expor terceiros e transforma constrangimento em exemplo pedagógico.",
            "O caso apoia estrutura narrativa e correção, não prova efeito sobre confiança ou fluência.",
        ],
        scores={"gancho":82,"clareza":86,"relevancia":88,"desejo":76,"confianca":82,"retencao":"not_assessed","acao":81,"objecoes":74},
        lenses={
            "apressado":"Título promete dicas e um mico real.",
            "analitico":"Reconstrói erro, distinção e aprendizado pela transcrição.",
            "aspiracional":"Mostra progresso possível apesar do início inseguro.",
            "comunidade":"O relato pessoal convida identificação; três comentários não medem comunidade.",
            "cetico":"Não transforma intercâmbio, curso ou relato em prova universal.",
        },
        replicable=["Usar erro próprio, não de terceiro.","Explicar por que a forma gerou mal-entendido.","Concluir com aprendizado e ação proporcionais."],
        contingent=["Relato pessoal não é verificável externamente.","Transcrição automática é ruidosa.","Contexto de intercâmbio não representa todos os alunos."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"a narradora autoatribui erro plausível, explica a distinção e extrai aprendizado sem humilhação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_3_public_comments",
        comment_provenance=True,
    ),
    build_ref(
        id="obs-20260919-183",
        title="Passei VERGONHA falando inglês nos EUA: como superei?",
        creator="Cintya Sabino", identity="cintya-sabino",
        url="https://www.youtube.com/watch?v=3xWtVj2skdw",
        published="2021-05-25", duration="PT58S",
        accessible=[
            "título", "criadora", "descrição pública", "data exata", "duração de 58 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "8.183 visualizações, 382 curtidas e 33 comentários declarados nos metadados consultados",
            "relato pessoal, palavra dita, correção recebida e aprendizado final",
        ],
        missing=MISSING_AV + ["texto exato em inglês comprometido por erros da transcrição automática", "comentários individuais", "baseline comparável", "teste de aprendizagem"],
        metrics={"viewsObserved":8183,"likesObserved":382,"commentsObserved":33},
        classification=cls(
            material="video_curto", presentations=["camera_direta","depoimento"], primary="storytelling", secondary=["educativo","humor"],
            mix=[{"family":"storytelling","percentage":55},{"family":"educativo","percentage":30},{"family":"humor","percentage":15}],
            objectives=["educar","identificacao","confianca"], topic="erro pessoal de vocabulário em inglês durante intercâmbio",
            segment="educação e idiomas", subsegment="micro-relato de erro e correção", audience="brasileiros com medo de errar ao falar inglês",
            production="simple", scale="large", replicability="high", duration="31_to_60s",
            mechanisms=["aproximacao","identificacao","alivio","humor"], hooks=["narrativo","problema"],
            narrative=["situacao","problema","virada","conclusao"], proof=["depoimento","mecanismo_explicado"], cta=[],
            evidence=[
                "Entre 0:00 e 0:22, contextualiza uma confraternização do intercâmbio.",
                "Entre 0:22 e 0:43, narra a palavra inadequada, o riso e a correção recebida; a grafia exata está ruidosa na transcrição.",
                "Entre 0:43 e 0:58, afirma que o erro fixou a palavra e recomenda não abandonar a prática por vergonha.",
            ],
        ),
        comparison={"level":2,"group":"conteúdo brasileiro de inglês que apresenta erro plausível sem humilhar e oferece correção observável","referenceIds":["obs-20260919-181","obs-20260919-182"],"confidence":"medium"},
        observations=[
            "A criadora narra o próprio erro, registra a correção e encerra com aprendizado explícito.",
            "A transcrição automática preserva a estrutura, mas não permite ensinar com segurança a grafia inglesa específica.",
        ],
        interpretations=[
            "Um micro-relato autoatribuído pode preservar dignidade e tornar correção e consequência reconhecíveis em menos de um minuto.",
            "Riso narrado e métricas não provam humor, retenção, confiança ou aprendizagem.",
        ],
        scores={"gancho":89,"clareza":82,"relevancia":87,"desejo":75,"confianca":76,"retencao":"not_assessed","acao":74,"objecoes":70},
        lenses={
            "apressado":"Recebe vergonha, inglês e superação no título.",
            "analitico":"Vê estrutura completa, mas não deve confiar na grafia transcrita.",
            "aspiracional":"Promete superar o medo pelo aprendizado do erro.",
            "comunidade":"Autoexposição evita usar um terceiro como alvo.",
            "cetico":"Não presume cena, atuação, tom ou eficácia.",
        },
        replicable=["Contar erro próprio em contexto mínimo.","Incluir correção e consequência de aprendizagem.","Evitar reproduzir a fala específica quando a transcrição é incerta."],
        contingent=["Transcrição automática erra palavras inglesas.","O relato não foi verificado externamente.","Comentários não foram amostrados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"o micro-relato contém erro autoatribuído, correção e aprendizado sem expor terceiro","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20260919-184",
        title="Tenho vergonha de falar inglês 😰",
        creator="Marcela Mallett", identity="marcela-mallett",
        url="https://www.youtube.com/watch?v=ACl7RbiZgzg",
        published="2020-06-29", duration="PT4M30S",
        accessible=[
            "título", "criadora", "descrição pública", "data exata", "duração de 4 minutos e 30 segundos",
            "transcrição automática integral em português com 111 segmentos e timestamps", "fala por substituição textual",
            "2.975 visualizações e 457 curtidas nos metadados consultados", "amostra pública limitada de 30 comentários",
            "conselhos de prática, gravação da própria voz e shadowing",
        ],
        missing=MISSING_AV + ["total público de comentários", "erro concreto apresentado", "correção de erro", "baseline comparável", "teste de confiança ou aprendizagem"],
        metrics={"viewsObserved":2975,"likesObserved":457,"commentsObserved":"not_assessed"},
        classification=cls(
            presentations=["camera_direta","comentario","tutorial"], primary="autoridade_opiniao", secondary=["educativo","explicativo"],
            mix=[{"family":"autoridade_opiniao","percentage":45},{"family":"educativo","percentage":40},{"family":"explicativo","percentage":15}],
            objectives=["educar","confianca","venda"], topic="vergonha de falar inglês e técnicas de prática",
            segment="educação e idiomas", subsegment="confiança e speaking", audience="brasileiros inseguros ao falar inglês",
            production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["alivio","confianca","utilidade_pratica"], hooks=["problema","identificacao"],
            narrative=["problema","mecanismo","progressao","conclusao","cta"], proof=["mecanismo_explicado"], cta=["clicar","comprar"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"curso de inglês da criadora","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:35, apresenta vergonha e falta de confiança como problema.",
                "Entre 0:35 e 1:23, recomenda prática, gravação e análise da própria pronúncia.",
                "A transcrição não apresenta um erro concreto, uma pessoa que errou ou uma correção específica.",
            ],
        ),
        comparison={"level":2,"group":"conteúdo brasileiro sobre vergonha de falar inglês sem erro e correção observáveis","referenceIds":["obs-20260919-181","obs-20260919-182","obs-20260919-183"],"confidence":"high"},
        observations=[
            "O tema emocional e as técnicas de prática são observáveis na fala.",
            "Não há erro concreto nem correção específica; portanto, o material não apoia o mecanismo-alvo.",
        ],
        interpretations=[
            "Falar de vergonha ou prática não equivale a reenquadrar um erro com dignidade e correção.",
            "É caso-limite estrutural, não contraexemplo de eficácia.",
        ],
        scores={"gancho":82,"clareza":87,"relevancia":86,"desejo":72,"confianca":70,"retencao":"not_assessed","acao":79,"objecoes":66},
        lenses={
            "apressado":"Reconhece o problema emocional no título.",
            "analitico":"Identifica técnicas, mas não encontra erro e correção comparáveis.",
            "aspiracional":"Promete mais confiança pela prática.",
            "comunidade":"Comentários mostram identificação, sem medir mudança de comportamento.",
            "cetico":"Recusa contar tema adjacente como apoio ao padrão.",
        },
        replicable=["Distinguir aconselhamento geral de estudo de caso com erro e correção.","Oferecer técnica prática sem atribuir culpa."],
        contingent=["A relação entre prática e vergonha não foi testada.","Oferta do curso é contexto comercial.","Comentários são amostra limitada."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"a fala oferece técnicas para vergonha e confiança","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a fala apresenta erro concreto e correção específica","requiredModalities":["transcript"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_30_public_comments",
        comment_provenance=True,
    ),
    build_ref(
        id="obs-20260919-185",
        title="Como assobiar com as duas mãos",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=DigFDu_IYFs",
        published="2008-07-17", duration="PT38S",
        accessible=[
            "título", "criador", "descrição pública", "data exata", "duração de 38 segundos",
            "transcrição automática integral em português com 9 segmentos e timestamps", "fala por substituição textual parcial e ruidosa",
            "2.310.035 visualizações e 37.377 curtidas nos metadados consultados", "amostra pública limitada de 30 comentários",
            "posição das mãos, cavidade fechada e espaço para sopro descritos de forma aproximada na transcrição",
        ],
        missing=MISSING_AV + ["total público de comentários", "confirmação visual da posição das mãos", "assobio ouvido", "resultado individual reproduzido", "baseline comparável"],
        metrics={"viewsObserved":2310035,"likesObserved":37377,"commentsObserved":"not_assessed"},
        classification=cls(
            material="video_curto", presentations=["tutorial","demonstracao"], primary="demonstracao", secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":55},{"family":"educativo","percentage":35},{"family":"curiosidade","percentage":10}],
            objectives=["educar","salvamento","compartilhamento"], topic="assobio produzido com as duas mãos",
            segment="tutorial prático", subsegment="habilidade manual em vídeo curto", audience="público geral que quer aprender uma habilidade simples",
            production="simple", scale="large", replicability="high", duration="31_to_60s",
            mechanisms=["utilidade_pratica","curiosidade","recompensa"], hooks=["promessa","demonstracao_antecipada"],
            narrative=["promessa","progressao","payoff"], proof=["demonstracao"], cta=["experimentar"],
            evidence=[
                "Entre 0:07 e 0:24, a transcrição descreve encaixe das mãos, cavidade e espaço para soprar.",
                "A transcrição é curta e ruidosa; sem vídeo ou áudio, gesto e resultado não podem ser confirmados.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de microtutorial demonstrativo fora do grupo-alvo de erros de idioma","referenceIds":[],"confidence":"high"},
        observations=[
            "O objeto e a promessa são claros no título; passos aproximados aparecem na fala transcrita.",
            "A demonstração visual e o assobio não foram observados, então execução e resultado não foram ensinados.",
            "Comentários amostrados incluem relatos públicos de sucesso; não substituem auditoria visual nem teste controlado.",
        ],
        interpretations=[
            "Microtutorial é exploração de família adjacente e não apoia o padrão-alvo.",
            "Popularidade histórica e relatos em comentários não provam clareza, retenção ou replicabilidade real.",
        ],
        scores={"gancho":84,"clareza":76,"relevancia":80,"desejo":73,"confianca":58,"retencao":"not_assessed","acao":78,"objecoes":54},
        lenses={
            "apressado":"Entende a habilidade prometida no título.",
            "analitico":"Não consegue validar gesto ou resultado sem audiovisual.",
            "aspiracional":"A recompensa é uma habilidade rápida e concreta.",
            "comunidade":"Relatos de sucesso são anedóticos e não representativos.",
            "cetico":"Recusa ensinar passos visuais a partir de transcrição ruidosa.",
        },
        replicable=["Nomear habilidade e resultado no título.","Dividir o gesto em poucas etapas, quando o visual estiver disponível."],
        contingent=["Execução depende de posição visual não observada.","Transcrição automática é muito ruidosa.","Métricas acumuladas por muitos anos não formam baseline."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"o título promete habilidade específica e a fala descreve passos aproximados","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"a posição das mãos e o som final foram demonstrados com sucesso","requiredModalities":["video","audio"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_full_but_noisy_automatic_transcript_and_30_public_comments",
        comment_provenance=True,
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 033")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260919-181", "obs-20260919-182", "obs-20260919-183"]
new_case = "obs-20260919-184"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 6
pattern["supportingCount"] = 6
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260919-181","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Erros recorrentes são tratados como fenômenos plausíveis de transferência e recebem correções articulatórias sem humilhação individual.","evidence":"Metadados, descrição, transcrição automática integral e 30 comentários amostrados.","limitations":["sem audiovisual, retenção ou teste de aprendizagem","publicidade do aplicativo"]},
    {"referenceId":"obs-20260919-182","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Relato autoatribuído de pronúncia ambígua recebe explicação e aprendizado explícito.","evidence":"Metadados, descrição, transcrição automática integral e três comentários.","limitations":["relato pessoal não verificado","sem audiovisual ou retenção"]},
    {"referenceId":"obs-20260919-183","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Micro-relato autoatribuído preserva erro, correção e consequência de aprendizagem em menos de um minuto.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["palavra inglesa ruidosa na transcrição","sem audiovisual, comentários ou retenção"]},
    {"referenceId":"obs-20260919-184","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"O vídeo aborda vergonha e técnicas de prática, mas não apresenta erro concreto nem correção específica.","evidence":"Metadados, descrição, transcrição automática integral e 30 comentários amostrados.","limitations":["não é contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Seis apoios formais vêm de seis criadores e fontes; demonstram recorrência estrutural, não eficácia.",
    "Os três novos apoios possuem transcrição integral, mas nenhum audiovisual, ritmo, retenção, baseline ou teste de aprendizagem.",
    "O segundo caso-limite confirma que falar de vergonha ou prática não basta: erro concreto e correção precisam estar observáveis.",
    "Transcrições automáticas, especialmente de palavras inglesas, podem conter erros e não autorizam copiar a fala.",
    "Consentimento e procedência continuam obrigatórios quando o erro pertence a terceiros; autoatribuição reduz, mas não elimina, riscos editoriais.",
    "Popularidade, escala, publicidade e comentários permanecem contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("99hHGBg-FCs", "descrição e comentários acessíveis, mas sem transcrição ou audiovisual para observar erro e correção"),
        ("7tkxwMcdFqU", "publicação indisponível"),
        ("o8FhftuVKRI", "metadados e transcrição não puderam ser adquiridos"),
        ("mu7tC62Tw2I", "fala sobre medo de errar, mas cobertura redundante com caso-limite mais completo"),
        ("HPLc1sN5HV8", "ensina tradução de expressão; funcionalmente diferente de erro reenquadrado"),
        ("OLj4eTVkJkQ", "referência indicada em comentário, mas cobertura insuficiente na triagem"),
        ("eTywQuhzNG8", "já presente na memória"),
        ("3AvXEQzimWM", "já é apoio do padrão na memória"),
        ("l6p4zMmgJJo", "já é apoio do padrão na memória"),
        ("9D_zk9xPjXo", "já é apoio do padrão na memória"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 78,
    "referenceIds": [f"obs-20260919-{n}" for n in range(181, 186)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260919-185"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 2,
    "replicableReferences": 5,
    "creativeFamiliesObserved": ["educativo","storytelling","demonstracao","autoridade_opiniao","humor"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"os cinco downloads de vídeo expiraram após 75 segundos; cinco tentativas de capa também terminaram sem arquivo","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":5,"partialAutomatic":0,"none":0,"limitation":"transcrições automáticas substituem somente a fala e podem errar palavras em inglês; uma transcrição é especialmente ruidosa"},
    "commentsCoverage": {"countsOnly":1,"sampledReferences":4,"sampledComments":93,"limitation":"três amostras foram limitadas a 30 comentários; amostras públicas não são representativas"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"datas, canais, durações, temas e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["vergonha, insegurança ou prática em geral não contam como apoio sem erro concreto e correção observável"],
    "safetyFindings": [
        "somente erros autoatribuídos ou generalizados de modo não identificável foram ensinados",
        "palavras inglesas ruidosas na transcrição não foram reproduzidas como correção confiável",
        "métricas e publicidade permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, ritmo, retenção, frase ou roteiro foi inventado",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes reforçam a recorrência de erro plausível ou autoatribuído, dignidade preservada e correção observável. O padrão passa de três para seis apoios e de um para dois casos-limite; permanece provisório e não demonstra aprendizagem, confiança, retenção ou desempenho.",
    "nextTarget": "vídeo brasileiro recente e curto de criador pequeno ou médio, com audiovisual integral, erro autoatribuído ou consentido, correção observável e teste de compreensão ou mudança de confiança; procurar também um caso comparável em que a correção humilhe, confunda ou aumente autocensura",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "As cinco transcrições são automáticas; palavras inglesas e a exploração demonstrativa têm ruído relevante.",
        "Comentários foram amostrados em quatro publicações e não são representativos.",
        "Não houve baseline, retenção, replay, teste de compreensão, confiança ou aprendizagem.",
        "As publicações são de 2008 a 2021; ausência de coorte recente limita comparação editorial contemporânea.",
        "Nenhum resultado autoriza causalidade ou validação.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
