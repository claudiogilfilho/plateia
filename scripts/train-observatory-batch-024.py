#!/usr/bin/env python3
import json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "knowledge/observatory/plateia-memory.json"
memory = json.loads(DB.read_text(encoding="utf-8"))

BATCH_IDS = {f"obs-20260912-{n}" for n in range(136, 141)}
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != "run-20260912-supervised-024"]

pattern = next(p for p in memory["patterns"] if p["id"] == "pat-20260911-011")
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS]
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS]
pattern["evidence"] = [x for x in pattern.get("evidence", []) if x.get("referenceId") not in BATCH_IDS]
pattern["supportingCount"] = len(pattern["supportReferenceIds"])
pattern["comparableSupportCount"] = len(pattern["supportReferenceIds"])
pattern["caseLimitCount"] = len(pattern["caseLimitReferenceIds"])
pattern["creatorDiversityCount"] = len(pattern["supportReferenceIds"])
pattern["sourceDiversityCount"] = len(pattern["supportReferenceIds"])
pattern["limitations"] = [x for x in pattern.get("limitations", []) if not x.startswith("O lote 024")]

NOW = "2026-09-12T11:55:29.000Z"
OBSERVED = "2026-09-12"

MISSING_AV = [
    "vídeo integral auditado quadro a quadro",
    "imagem em movimento efetivamente observada",
    "áudio ouvido",
    "texto na tela",
    "edição",
    "ritmo",
    "curva de retenção",
    "impressões e fontes de tráfego",
]

def classification(*, container, material, presentations, primary, secondary, mix,
                   objectives, advertising, intent, entity, topic, segment, subsegment,
                   audience, awareness, production, scale, replicability, duration,
                   mechanisms, hooks, narrative, proof, cta, confidence, evidence,
                   alternatives=None, missing=None):
    return {
        "taxonomyVersion": "3.0",
        "container": container,
        "materialFormat": material,
        "presentationFormats": presentations,
        "primaryFamily": primary,
        "secondaryFamilies": secondary,
        "functionalMix": mix,
        "objectives": objectives,
        "advertisingType": advertising,
        "commercialIntent": intent,
        "advertisedEntity": entity,
        "contentTopic": {"label": topic, "iabCode": None},
        "segment": segment,
        "subsegment": subsegment,
        "probableAudience": audience,
        "awarenessStage": awareness,
        "productionLevel": production,
        "creatorScale": scale,
        "replicability": replicability,
        "durationBand": duration,
        "pace": "unknown",
        "mechanisms": mechanisms,
        "hookTypes": hooks,
        "narrativeElements": narrative,
        "proofTypes": proof,
        "ctaTypes": cta,
        "distributionContext": {"organicPaid": "unknown", "trendDependency": "low"},
        "confidence": confidence,
        "evidence": evidence,
        "alternativeClassifications": alternatives or [],
        "missingInformation": missing or MISSING_AV,
        "needsHumanReview": True,
    }

def make_ref(*, id, title, creator, identity, url, published, duration, country,
             accessible, missing, metrics, cls, comparison, observations,
             interpretations, scores, lenses, replicable, limitations, role,
             evidence_level, eligible, claims, source_type, provenance=None):
    return {
        "id": id,
        "title": title,
        "creator": creator,
        "creatorIdentity": identity,
        "sourceIdentity": identity,
        "country": country,
        "url": url,
        "publishedAt": published,
        "duration": duration,
        "createdAt": NOW,
        "coverage": {"level": "partial", "accessible": accessible, "missing": missing},
        "publicMetrics": {
            **metrics,
            "observedAt": OBSERVED,
            "sourceType": source_type,
            "causality": "not_inferred",
        },
        "classification": cls,
        "comparison": comparison,
        "observations": observations,
        "interpretations": interpretations,
        "scores": scores,
        "fiveLenses": lenses,
        "hypotheses": [],
        "replicable": replicable,
        "limitations": limitations,
        "provenance": [
            "public_content", "youtube_public_metadata", "public_search",
            "youtube_automatic_transcript", "youtube_public_comments",
            "public_metric", "observatory_inference",
        ],
        "sourceEvidence": [url],
        "training": {
            "evidencePolicyVersion": "1.1",
            "evidenceRole": role,
            "evidenceLevel": evidence_level,
            "requiredEvidenceObserved": eligible,
            "supportEligible": eligible,
            "claimCoverage": claims,
            "provenanceAndConsent": provenance or {
                "storyOrigin": "not_applicable",
                "consentStatus": "not_applicable",
                "identityProtection": "not_applicable",
                "evidence": ["conteúdo instrucional ou humorístico sem relato pessoal de terceiro na cobertura acessível"],
            },
            "replicable": replicable,
            "contingent": limitations,
            "notRecommended": [
                "copiar frases, personagens ou roteiro",
                "tratar comentário genérico como aprendizagem",
                "inferir vídeo, áudio, texto na tela, edição, ritmo ou retenção",
                "usar alcance absoluto ou baseline heterogêneo como prova causal",
            ],
            "hypotheses": [],
        },
        "viralAssessment": {
            "status": "indeterminate",
            "observedSignal": metrics.get("viewsObserved", "not_assessed"),
            "missingForRelativeAssessment": [
                "coorte funcional contemporânea homogênea", "retenção", "impressões",
                "fontes de tráfego", "mídia paga",
            ],
            "confounders": ["tamanho do canal", "idade do vídeo", "tema", "distribuição"],
            "causalClaimAllowed": False,
        },
    }

refs = [
    make_ref(
        id="obs-20260912-136",
        title='"Least of all" — como usar essa expressão em inglês?',
        creator="Teacher Gabriel Borges",
        identity="teacher-gabriel-borges",
        url="https://www.youtube.com/shorts/6AQqU8dlxLU",
        published="2025-02-25",
        duration="PT44S",
        country="BR",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral com timestamps", "fala por substituição textual",
            "6.482 visualizações", "1.146 curtidas", "9 comentários integralmente extraídos",
            "328 mil inscritos", "amostra pública dos 12 Shorts mais recentes do canal",
        ],
        missing=MISSING_AV,
        metrics={
            "viewsObserved": "6.482", "likesObserved": "1.146",
            "commentsObserved": "9 integralmente extraídos", "subscriberCountObserved": "328 mil",
            "channelBaseline": {
                "sampleSize": 12, "surface": "Shorts recentes do canal",
                "medianViews": 14000, "rangeViews": [1700, 364000],
                "limitation": "amostra heterogênea, sem datas individuais e não ajustada por idade, tema ou distribuição",
            },
        },
        cls=classification(
            container="youtube_short", material="video_curto", presentations=["indeterminado"],
            primary="educativo", secondary=["comunidade", "curiosidade"],
            mix=[{"family":"educativo","percentage":60},{"family":"comunidade","percentage":25},{"family":"curiosidade","percentage":15}],
            objectives=["educar", "comentario", "lead"], advertising="geracao_de_leads", intent="explicita",
            entity={"kind":"servico","name":"método de inglês do Teacher Gabriel Borges","confidence":"high"},
            topic="significado, pronúncia e aplicação de least of all", segment="educação e idiomas",
            subsegment="vocabulário e expressão em inglês", audience="brasileiros aprendendo inglês",
            awareness="consciente_solucao", production="unknown", scale="large", replicability="high",
            duration="31_to_60s", mechanisms=["curiosidade", "recompensa", "pertencimento"],
            hooks=["pergunta", "verbal"], narrative=["problema", "mecanismo", "cta"],
            proof=["mecanismo_explicado"], cta=["comentar", "clicar"], confidence="high",
            evidence=[
                "A transcrição explica significado, pronúncia e um exemplo.",
                "A descrição pede uma frase com a expressão; dois comentários apresentam frases aplicadas.",
            ],
            alternatives=["explicativo como família principal"],
        ),
        comparison={"level":2,"group":"microaula de inglês com tarefa produtiva no comentário","referenceIds":["obs-20260911-131","obs-20260911-132","obs-20260911-133"],"confidence":"high"},
        observations=[
            "A explicação transcrita termina com CTA comercial; a tarefa produtiva aparece na descrição.",
            "Dois dos nove comentários contêm frases com a expressão ensinada.",
            "O criador responde a um elogio sobre aprendizagem, mas não corrige publicamente as duas frases aplicadas.",
        ],
        interpretations=[
            "O CTA estende a unidade da aula para uma produção escrita observável.",
            "A presença de duas respostas confirma execução pontual, não qualidade pedagógica ou aprendizagem.",
        ],
        scores={"gancho":86,"clareza":93,"relevancia":87,"desejo":76,"confianca":82,"retencao":"not_assessed","acao":91,"objecoes":78},
        lenses={
            "apressado":"A pergunta e a expressão delimitam rapidamente o assunto.",
            "analitico":"Recebe significado, pronúncia e exemplo; falta correção das produções observadas.",
            "aspiracional":"Pode imaginar uso mais natural da expressão.",
            "comunidade":"Duas pessoas executam a tarefa; a mediação pedagógica específica não aparece.",
            "cetico":"Não consegue atribuir respostas, alcance ou aprendizagem ao CTA sem comparação controlada.",
        },
        replicable=[
            "Pedir uma unidade curta e diretamente ligada ao conteúdo.",
            "Deixar exemplos suficientes para o público produzir sem copiar.",
            "Separar o CTA de prática do CTA comercial.",
        ],
        limitations=["Transcrição automática pode errar termos em inglês.","Sem correção específica das frases observadas.","Sem audiovisual, retenção ou baseline homogêneo."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a unidade é ensinada","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o CTA pede aplicação da unidade","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
            {"claim":"há respostas aplicadas, como contexto adicional não necessário ao apoio estrutural","requiredModalities":["comments"],"observedModalities":["comments"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_comments_and_channel_sample_after_public_search",
    ),
    make_ref(
        id="obs-20260912-137", title="Qual a diferença entre bring e take?", creator="Punkify",
        identity="punkify", url="https://www.youtube.com/shorts/wCi52ik_gaM", published="2025-12-24",
        duration="PT34S", country="BR",
        accessible=["título","criador","descrição integral","data exata","duração","transcrição automática integral com timestamps","fala por substituição textual","59 visualizações","2 curtidas","zero comentários declarado","9,77 mil inscritos","amostra pública dos 12 Shorts mais recentes do canal"],
        missing=MISSING_AV,
        metrics={"viewsObserved":"59","likesObserved":"2","commentsObserved":"zero declarado","subscriberCountObserved":"9,77 mil","channelBaseline":{"sampleSize":12,"surface":"Shorts recentes do canal","medianViews":280.5,"rangeViews":[27,1400],"limitation":"amostra heterogênea, sem datas individuais e não ajustada por idade, tema ou distribuição"}},
        cls=classification(
            container="youtube_short",material="video_curto",presentations=["indeterminado"],primary="educativo",secondary=["comunidade","explicativo"],
            mix=[{"family":"educativo","percentage":65},{"family":"comunidade","percentage":20},{"family":"explicativo","percentage":15}],objectives=["educar","comentario","seguidores"],
            advertising="editorial_organico",intent="implicita",entity={"kind":"servico","name":"Punkify","confidence":"medium"},topic="diferença de uso entre bring e take",segment="educação e idiomas",subsegment="vocabulário de inglês",audience="brasileiros aprendendo inglês",awareness="consciente_problema",production="unknown",scale="medium",replicability="high",duration="31_to_60s",mechanisms=["curiosidade","recompensa","pertencimento"],hooks=["pergunta","problema"],narrative=["problema","mecanismo","cta"],proof=["mecanismo_explicado"],cta=["comentar"],confidence="high",evidence=["A transcrição diferencia os verbos por exemplos.","A descrição pede uma frase com uma das palavras; nenhum comentário estava disponível."],alternatives=["explicativo como família principal"]),
        comparison={"level":2,"group":"microaula de inglês com tarefa produtiva no comentário","referenceIds":["obs-20260912-136","obs-20260911-132"],"confidence":"high"},
        observations=["A fala transcrita contém explicação e exemplos, mas não o CTA de comentário.","A descrição pede uma frase aplicada; o contador público declara zero comentários."],
        interpretations=["A tarefa é semanticamente alinhada à aula, porém sua execução pública não foi observada.","Zero comentários isolado não demonstra falha sem impressões, retenção e baseline funcional comparável."],
        scores={"gancho":88,"clareza":91,"relevancia":86,"desejo":73,"confianca":80,"retencao":"not_assessed","acao":84,"objecoes":76},
        lenses={"apressado":"A pergunta torna a dúvida explícita no título.","analitico":"Recebe exemplos, mas não regra detalhada nem correção de produção.","aspiracional":"A promessa reduz uma confusão recorrente.","comunidade":"Há convite de prática, sem participação pública observada.","cetico":"Não pode tratar zero comentários como prova contra o formato."},
        replicable=["Transformar uma distinção binária em tarefa curta.","Pedir uma frase com escolha entre duas unidades.","Prever feedback mesmo quando a resposta pública for baixa."],
        limitations=["Nenhum comentário público observado.","CTA produtivo só na descrição.","Sem audiovisual, retenção ou coorte homogênea."],
        role="target_support",evidence_level=2,eligible=True,
        claims=[{"claim":"a distinção é ensinada","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},{"claim":"o CTA pede aplicação","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True}],
        source_type="youtube_public_metadata_full_automatic_transcript_declared_zero_comments_and_channel_sample_after_public_search",
    ),
    make_ref(
        id="obs-20260912-138", title='Quando não usar "Me too"', creator="Teacher Tarcísio",
        identity="teacher-tarcisio", url="https://www.youtube.com/shorts/ciyrenCXKXg", published="2026-05-05",
        duration="PT53S", country="BR",
        accessible=["título","criador","descrição integral","data exata","duração","transcrição automática integral com timestamps","fala por substituição textual","226 visualizações","1 comentário integralmente extraído","344 inscritos","amostra pública dos 12 Shorts mais recentes do canal"],
        missing=MISSING_AV,
        metrics={"viewsObserved":"226","likesObserved":"not_assessed","commentsObserved":"1 integralmente extraído","subscriberCountObserved":"344","channelBaseline":{"sampleSize":12,"surface":"Shorts recentes do canal","medianViews":114.5,"rangeViews":[17,1900],"limitation":"amostra heterogênea e não ajustada por idade, tema ou distribuição"}},
        cls=classification(
            container="youtube_short",material="video_curto",presentations=["indeterminado"],primary="educativo",secondary=["identificacao","comunidade"],
            mix=[{"family":"educativo","percentage":60},{"family":"identificacao","percentage":25},{"family":"comunidade","percentage":15}],objectives=["educar","comentario","seguidores"],advertising="geracao_de_leads",intent="explicita",entity={"kind":"servico","name":"perfis e curso Teacher Tarcísio","confidence":"high"},topic="me too versus me neither",segment="educação e idiomas",subsegment="concordância em inglês",audience="brasileiros iniciantes em inglês",awareness="consciente_problema",production="unknown",scale="small",replicability="high",duration="31_to_60s",mechanisms=["identificacao","alivio","recompensa"],hooks=["problema","verbal"],narrative=["problema","mecanismo","conclusao","cta"],proof=["mecanismo_explicado"],cta=["comentar","seguir"],confidence="high",evidence=["A transcrição explica a regra por contraste afirmativo e negativo.","A descrição pede frase negativa; o único comentário é elogio genérico."],alternatives=["explicativo como família principal"]),
        comparison={"level":2,"group":"microaula de inglês com tarefa produtiva no comentário","referenceIds":["obs-20260912-136","obs-20260912-137"],"confidence":"high"},
        observations=["A fala transcrita explica a regra e termina pedindo que o público siga no Instagram.","A tarefa de escrever frase negativa aparece na descrição.","O único comentário não executa o exercício."],
        interpretations=["Há alinhamento estrutural entre a regra ensinada e a tarefa descrita.","O comentário genérico não mede compreensão ou prática."],
        scores={"gancho":91,"clareza":92,"relevancia":88,"desejo":78,"confianca":84,"retencao":"not_assessed","acao":86,"objecoes":82},
        lenses={"apressado":"O erro e a regra aparecem rapidamente na transcrição.","analitico":"Recebe contraste e exemplos; falta feedback aplicado.","aspiracional":"Pode sentir menor risco de errar ao concordar.","comunidade":"A tarefa existe, mas não recebeu resposta aplicada observável.","cetico":"A promessa de verificar domínio não é cumprida por evidência pública disponível."},
        replicable=["Ancorar a tarefa na regra recém-explicada.","Pedir uma frase que exponha entendimento, não preferência.","Responder com correção proporcional quando houver produção."],
        limitations=["Um comentário genérico não é evidência de prática.","CTA produtivo só na descrição.","Sem audiovisual, retenção ou teste de aprendizagem."],
        role="target_support",evidence_level=2,eligible=True,
        claims=[{"claim":"a regra é ensinada","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},{"claim":"o CTA pede aplicação","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True}],
        source_type="youtube_public_metadata_full_automatic_transcript_comments_and_channel_sample_after_public_search",
    ),
    make_ref(
        id="obs-20260912-139", title='Como usar "this, that, these & those"', creator="Inglês Compartilhado por Tainá Alves",
        identity="ingles-compartilhado-taina-alves", url="https://www.youtube.com/shorts/BXUeKSI8YT8", published="2023-10-12",
        duration="PT9S", country="BR",
        accessible=["título","criadora","descrição integral","data exata","duração","13.842 visualizações","1.020 curtidas","16 comentários integralmente extraídos","47,6 mil inscritos"],
        missing=MISSING_AV + ["transcrição ou legenda","fala por substituição textual","unidade mostrada no vídeo"],
        metrics={"viewsObserved":"13.842","likesObserved":"1.020","commentsObserved":"16 integralmente extraídos","subscriberCountObserved":"47,6 mil"},
        cls=classification(
            container="youtube_short",material="video_curto",presentations=["indeterminado"],primary="educativo",secondary=["comunidade","curiosidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"comunidade","percentage":30},{"family":"curiosidade","percentage":15}],objectives=["educar","comentario","seguidores"],advertising="editorial_organico",intent="implicita",entity={"kind":"servico","name":"Inglês Compartilhado por Tainá Alves","confidence":"medium"},topic="pronomes demonstrativos em inglês",segment="educação e idiomas",subsegment="gramática de inglês",audience="brasileiros iniciantes em inglês",awareness="consciente_problema",production="unknown",scale="medium",replicability="medium",duration="up_to_15s",mechanisms=["curiosidade","pertencimento","recompensa"],hooks=["problema"],narrative=["problema","cta"],proof=["alegacao_sem_prova"],cta=["comentar","seguir"],confidence="medium",evidence=["A descrição contém explicação escrita e três CTAs diferentes.","Há respostas da criadora, mas a relação com o desafio do vídeo não pode ser reconstruída sem o audiovisual."],alternatives=["comunidade como família principal"],missing=MISSING_AV + ["transcrição ou legenda","unidade mostrada no vídeo"]),
        comparison={"level":2,"group":"caso-limite de microaula de inglês com múltiplos CTAs","referenceIds":["obs-20260912-136","obs-20260912-138"],"confidence":"medium"},
        observations=["A descrição pede emoji, uma frase e a tradução de quatro palavras, competindo pela mesma resposta.","Um comentário de uma palavra recebe correção, mas não é possível verificar qual comando ele respondeu.","A maioria dos comentários extraídos é elogio, emoji ou agradecimento."],
        interpretations=["Múltiplos comandos tornam a unidade de resposta ambígua.","A correção observada mostra mediação pontual, mas não prova execução do exercício principal."],
        scores={"gancho":78,"clareza":72,"relevancia":84,"desejo":70,"confianca":76,"retencao":"not_assessed","acao":58,"objecoes":64},
        lenses={"apressado":"O título delimita o tema, mas a descrição oferece três ações.","analitico":"Tem explicação textual; falta correspondência verificável com o vídeo.","aspiracional":"Promete domínio de distinção básica.","comunidade":"Há respostas da criadora, porém o exercício executado é ambíguo.","cetico":"Não consegue saber se a tarefa principal foi feita ou corrigida."},
        replicable=["Manter apenas uma unidade de resposta por publicação.","Dizer exatamente o que será corrigido.","Fixar exemplo sem resolver a tarefa pelo público."],
        limitations=["Sem vídeo, áudio, texto na tela ou transcrição.","Três CTAs competem entre si.","Não conta como apoio nem contraexemplo."],
        role="falsification_or_boundary",evidence_level=2,eligible=False,
        claims=[{"claim":"o vídeo ensina a unidade descrita","requiredModalities":["video_or_transcript"],"observedModalities":["description"],"sufficient":False},{"claim":"a descrição propõe tarefa aplicada","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},{"claim":"há feedback ligado ao exercício principal","requiredModalities":["comments","video_or_transcript"],"observedModalities":["comments"],"sufficient":False}],
        source_type="youtube_public_metadata_description_and_comments_after_public_search",
    ),
    make_ref(
        id="obs-20260912-140", title="Esse truque pode mudar tudo no seu relacionamento", creator="Matheus Ceará",
        identity="matheus-ceara", url="https://www.youtube.com/shorts/0nDLjwlrtpA", published="2024-12-05",
        duration="PT36S", country="BR",
        accessible=["título com hashtags","criador","categoria pública Comedy","data exata","duração","20.696 visualizações","1.371 curtidas","4 comentários integralmente extraídos","1,56 milhão de inscritos"],
        missing=MISSING_AV + ["descrição substantiva","transcrição ou legenda","fala por substituição textual","conflito e payoff"],
        metrics={"viewsObserved":"20.696","likesObserved":"1.371","commentsObserved":"4 integralmente extraídos","subscriberCountObserved":"1,56 milhão"},
        cls=classification(
            container="youtube_short",material="video_curto",presentations=["indeterminado"],primary="humor",secondary=["identificacao","entretenimento"],
            mix=[{"family":"humor","percentage":55},{"family":"identificacao","percentage":25},{"family":"entretenimento","percentage":20}],objectives=["identificacao","compartilhamento","visualizacao"],advertising="editorial_organico",intent="ausente",entity={"kind":"nenhuma","name":"","confidence":"medium"},topic="humor sobre relacionamento",segment="entretenimento e comédia",subsegment="relacionamentos",audience="adultos brasileiros que consomem humor de casal",awareness="inconsciente",production="unknown",scale="large",replicability="unknown",duration="31_to_60s",mechanisms=["humor","identificacao"],hooks=["promessa"],narrative=[],proof=[],cta=[],confidence="low",evidence=["Título, hashtags e categoria identificam humor sobre relacionamento.","Os quatro comentários expressam riso; a execução humorística não ficou acessível."],alternatives=["identificação como família principal"],missing=MISSING_AV + ["descrição substantiva","transcrição ou legenda","conflito e payoff"]),
        comparison={"level":4,"group":"exploração controlada de humor de relacionamento sem substância audiovisual acessível","referenceIds":[],"confidence":"low"},
        observations=["O título promete um truque de relacionamento e marca o conteúdo como humor.","Os quatro comentários extraídos expressam riso ou agradecimento."],
        interpretations=["Os comentários são reação pública, não revelam construção, timing ou motivo do humor.","A escala do criador e o alcance são contingentes."],
        scores={"gancho":72,"clareza":58,"relevancia":"not_assessed","desejo":"not_assessed","confianca":"not_assessed","retencao":"not_assessed","acao":"not_assessed","objecoes":"not_assessed"},
        lenses={"apressado":"Reconhece tema e tom pelo título.","analitico":"Não dispõe de premissa, conflito ou payoff.","aspiracional":"Não há transformação verificável.","comunidade":"Comentários indicam riso, sem amostra representativa.","cetico":"Título e métricas não explicam o mecanismo humorístico."},
        replicable=[],
        limitations=["Cobertura insuficiente para ensinar cenas, personagem, timing, ritmo ou payoff.","Comentários não explicam causalidade.","Produção e replicabilidade não avaliadas."],
        role="controlled_exploration",evidence_level=4,eligible=False,
        claims=[{"claim":"é humor sobre relacionamento","requiredModalities":["title","category"],"observedModalities":["title","category"],"sufficient":True},{"claim":"a execução humorística pode ser ensinada","requiredModalities":["video_or_transcript"],"observedModalities":[],"sufficient":False}],
        source_type="youtube_public_metadata_title_category_and_comments_after_public_search",
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
for item in refs:
    if item["url"] in existing_urls:
        raise SystemExit(f"URL duplicada: {item['url']}")
    existing_urls.add(item["url"])
memory["references"].extend(refs)

new_supports = ["obs-20260912-136", "obs-20260912-137", "obs-20260912-138"]
pattern["supportReferenceIds"].extend(new_supports)
pattern["caseLimitReferenceIds"].append("obs-20260912-139")
pattern["supportingCount"] = len(pattern["supportReferenceIds"])
pattern["comparableSupportCount"] = len(pattern["supportReferenceIds"])
pattern["caseLimitCount"] = len(pattern["caseLimitReferenceIds"])
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["evidence"].extend([
    {"referenceId":"obs-20260912-136","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Tarefa descrita aplica a expressão ensinada; dois comentários apresentam frases, sem correção específica observável.","evidence":"Descrição, transcrição integral e nove comentários.","limitations":["feedback corretivo ausente","sem audiovisual ou retenção"]},
    {"referenceId":"obs-20260912-137","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Descrição converte a distinção bring/take em frase; zero comentários foram declarados.","evidence":"Descrição, transcrição integral e contador de comentários.","limitations":["execução pública não observada","CTA apenas na descrição"]},
    {"referenceId":"obs-20260912-138","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Descrição pede frase negativa após regra transcrita; o único comentário é genérico.","evidence":"Descrição, transcrição integral e um comentário.","limitations":["execução pública não observada","CTA apenas na descrição"]},
    {"referenceId":"obs-20260912-139","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"medium","observation":"Descrição mistura emoji, frase e tradução; sem audiovisual não é possível ligar a correção observada ao exercício principal.","evidence":"Descrição e 16 comentários.","limitations":["não conta como apoio nem contraexemplo"]},
])
pattern["limitations"].append("O lote 024 separou três camadas: tarefa proposta, resposta aplicada e feedback corretivo. Há seis apoios para a primeira; somente duas frases públicas em uma referência sustentam a segunda, e nenhuma correção específica sustenta a terceira.")

memory["trainingRuns"].append({
    "id":"run-20260912-supervised-024",
    "executedAt":NOW,
    "batchPolicyVersion":"1.1",
    "requestedBatchSize":5,
    "candidatesFound":23,
    "referenceIds":["obs-20260912-136","obs-20260912-137","obs-20260912-138","obs-20260912-139","obs-20260912-140"],
    "targetKnowledgeId":"pat-20260911-011",
    "targetReferenceIds":["obs-20260912-136","obs-20260912-137","obs-20260912-138"],
    "falsificationOrBoundaryReferenceIds":["obs-20260912-139"],
    "controlledExplorationReferenceIds":["obs-20260912-140"],
    "discarded":[
        {"url":"https://www.youtube.com/shorts/Sy23-4loHVQ","reason":"CTA aplicado na descrição, mas sem transcrição e com zero comentários; redundante com apoio de maior cobertura"},
        {"url":"https://www.youtube.com/shorts/x4Czhwe7GJM","reason":"mesmo mecanismo, sem comentários e sem ganho de diversidade"},
        {"url":"https://www.youtube.com/shorts/5HpzgC0S7hk","reason":"mesma criadora do candidato anterior e cobertura inferior"},
        {"url":"https://www.youtube.com/watch?v=2ctnHD4KXwQ","reason":"tutorial de ferramenta de correção, não CTA convertido em exercício"},
        {"url":"https://www.youtube.com/watch?v=8ANANvmFI5M","reason":"aula sobre feedback entre pares, mas não publicação com tarefa aplicada observável"},
        {"url":"https://www.youtube.com/watch?v=gfuM9SMC3K8","reason":"tutorial de ChatGPT, comparação funcional insuficiente"},
        {"url":"https://www.youtube.com/watch?v=JTZQ5Rvzbtg","reason":"pergunta retrospectiva sobre erros corrigidos, não unidade produtiva curta"},
        {"url":"https://www.instagram.com/reel/DboZl6_B_Gd/","reason":"promessa pública de correção relevante, mas página e comentários ficaram inacessíveis após throttling"},
    ],
    "analyzed":5,
    "brazilianReferences":5,
    "internationalReferences":0,
    "unknownOriginReferences":0,
    "smallOrMediumCreatorReferences":3,
    "coverageSummary":{"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition":{"attempted":True,"succeeded":0,"failure":"downloads diretos retornaram timeout ou exigência de token GVS; capas também expiraram","effect":"imagem em movimento, áudio ouvido, texto na tela, edição e ritmo ficaram não mensurados"},
    "transcriptCoverage":{"fullAutomatic":3,"partialAutomatic":0,"none":2,"limitation":"transcrições automáticas substituem apenas fala e podem errar palavras em inglês"},
    "commentsCoverage":{"fullOrDeclaredZero":5,"partialSample":0,"unavailable":0},
    "baselineCoverage":{"sampledProfiles":3,"contemporaneousBaselines":0,"limitation":"amostras atuais de 12 Shorts por canal são heterogêneas e não ajustadas por idade, tema ou distribuição"},
    "patternsCreated":[],
    "patternsStrengthened":["pat-20260911-011"],
    "patternsRefined":["pat-20260911-011"],
    "hypothesesCreated":[],
    "hypothesesStrengthened":[],
    "validatedPatternsCreated":0,
    "contradictionsFound":[],
    "caseLimitsFound":["múltiplos CTAs e resposta ambígua não demonstram execução do exercício principal"],
    "safetyFindings":["comentários públicos foram resumidos sem reproduzir usernames","nenhuma resposta foi tratada como prova de aprendizagem"],
    "evidenceGateSummary":{"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome":"O padrão ganhou três apoios estruturais e passou de três para seis criadores. A evidência de execução permanece estreita: duas frases em uma referência; feedback corretivo específico não foi observado.",
    "nextTarget":"microaula brasileira com audiovisual integral, uma única tarefa aplicada, múltiplas respostas públicas e correção do professor; buscar caso comparável em que respostas revelem erro persistente após feedback",
    "limitations":["Nenhum audiovisual ou áudio foi reproduzido.","Duas referências não tiveram transcrição.","Sem retenção, teste de aprendizagem ou conversão.","Baselines são heterogêneos.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({
    "references": len(memory["references"]),
    "patterns": len(memory["patterns"]),
    "hypotheses": len(memory["hypotheses"]),
    "runs": len(memory["trainingRuns"]),
    "targetSupports": pattern["supportingCount"],
    "targetCaseLimits": pattern["caseLimitCount"],
}, ensure_ascii=False))
