#!/usr/bin/env python3
import json
from pathlib import Path

DB = Path(__file__).resolve().parents[1] / "knowledge/observatory/plateia-memory.json"
memory = json.loads(DB.read_text(encoding="utf-8"))

# Idempotência para repetir o lote durante auditorias locais.
batch_reference_ids = {f"obs-20260910-{value}" for value in range(126, 131)}
memory["references"] = [item for item in memory["references"] if item.get("id") not in batch_reference_ids]
memory["patterns"] = [item for item in memory["patterns"] if item.get("id") != "pat-20260910-010"]
memory["trainingRuns"] = [item for item in memory["trainingRuns"] if item.get("id") != "run-20260910-supervised-022"]
for item in memory["hypotheses"]:
    if item.get("id") == "hyp-20260825-019" and item.get("previousStatement"):
        item["statement"] = item.pop("previousStatement")
        item["status"] = "observed_not_promoted"
        item["supportReferenceIds"] = [value for value in item.get("supportReferenceIds", []) if value not in batch_reference_ids]
        for key in ["promotedPatternId", "consolidatedIntoPatternId", "promotionReason"]:
            item.pop(key, None)

NOW = "2026-09-10T12:12:55.000Z"
OBSERVED = "2026-09-10"

def ref(*, id, title, creator, identity, url, published, duration, metrics,
        accessible, missing, classification, comparison, observations,
        interpretations, scores, lenses, replicable, limitations, role,
        evidence_level, support, claims, provenance_consent, hypotheses=None,
        source_type="youtube_public_metadata_transcript_and_comments_after_public_search"):
    return {
        "id": id,
        "title": title,
        "creator": creator,
        "creatorIdentity": identity,
        "sourceIdentity": identity,
        "country": "BR",
        "url": url,
        "publishedAt": published,
        "duration": duration,
        "createdAt": NOW,
        "coverage": {
            "level": "partial",
            "accessible": accessible,
            "missing": missing,
        },
        "publicMetrics": {
            **metrics,
            "observedAt": OBSERVED,
            "sourceType": source_type,
            "causality": "not_inferred",
        },
        "classification": classification,
        "comparison": comparison,
        "observations": observations,
        "interpretations": interpretations,
        "scores": scores,
        "fiveLenses": lenses,
        "hypotheses": hypotheses or [],
        "replicable": replicable,
        "limitations": limitations,
        "provenance": [
            "public_content",
            "youtube_public_metadata",
            "youtube_automatic_transcript",
            "youtube_public_comments",
            "public_search",
            "public_metric",
            "observatory_inference",
        ],
        "sourceEvidence": [url],
        "training": {
            "evidencePolicyVersion": "1.1",
            "evidenceRole": role,
            "evidenceLevel": evidence_level,
            "requiredEvidenceObserved": support,
            "supportEligible": support,
            "claimCoverage": claims,
            "provenanceAndConsent": provenance_consent,
            "replicable": replicable,
            "contingent": limitations,
            "notRecommended": [
                "copiar frase, personagem ou roteiro",
                "ridicularizar quem errou ou expor pessoa sem consentimento proporcional",
                "inferir cenas, áudio, texto na tela, edição, ritmo, retenção ou causalidade",
                "usar visualizações, curtidas ou comentários como prova de eficácia",
            ],
            "hypotheses": hypotheses or [],
        },
        "viralAssessment": {
            "status": "indeterminate",
            "observedSignal": metrics.get("viewsObserved", "não mensurado"),
            "missingForRelativeAssessment": [
                "baseline funcional contemporâneo",
                "retenção",
                "impressões",
                "fontes de tráfego",
                "mídia paga",
            ],
            "confounders": ["tamanho do canal", "distribuição", "idade do vídeo", "tema"],
            "causalClaimAllowed": False,
        },
    }

missing_full = [
    "vídeo integral auditado quadro a quadro",
    "imagem em movimento efetivamente analisada",
    "áudio ouvido",
    "texto na tela",
    "edição",
    "ritmo",
    "curva de retenção",
    "baseline funcional contemporâneo",
    "impressões e fontes de tráfego",
]

refs = [
    ref(
        id="obs-20260910-126",
        title="O lado engraçado dos erros de inglês — episódio 11: aquele do refrigerante",
        creator="English by Thaisa",
        identity="english-by-thaisa",
        url="https://www.youtube.com/watch?v=3AvXEQzimWM",
        published="2024-12-20",
        duration="PT12M42S",
        metrics={"viewsObserved": "58", "likesObserved": "9", "commentsObserved": "2 integralmente extraídos", "subscriberCountObserved": "1,98 mil"},
        accessible=[
            "título", "criadora", "descrição oficial integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "58 visualizações", "9 curtidas", "2 comentários integralmente extraídos", "1,98 mil inscritos",
        ],
        missing=missing_full,
        classification={
            "taxonomyVersion": "3.0", "container": "youtube_video", "materialFormat": "video_longo",
            "presentationFormats": ["camera_direta", "comentario"], "primaryFamily": "educativo",
            "secondaryFamilies": ["storytelling", "humor"],
            "functionalMix": [{"family":"educativo","percentage":45},{"family":"storytelling","percentage":35},{"family":"humor","percentage":20}],
            "objectives": ["educar", "identificacao", "comunidade"], "advertisingType": "editorial_organico",
            "commercialIntent": "implicita", "advertisedEntity": {"kind":"servico","name":"English by Thaisa","confidence":"high"},
            "contentTopic": {"label":"erro de compreensão em situação de viagem transformado em aula de inglês","iabCode":None},
            "segment": "educação e idiomas", "subsegment": "inglês para adultos e viagem",
            "probableAudience": "brasileiros inseguros ao ouvir ou falar inglês em situações reais",
            "awarenessStage": "consciente_problema", "productionLevel": "simple", "creatorScale": "small",
            "replicability": "high", "durationBand": "over_60s", "pace": "unknown",
            "mechanisms": ["humor", "identificacao", "alivio", "confianca"],
            "hookTypes": ["problema", "identificacao"], "narrativeElements": ["situacao","problema","conflito","virada","conclusao","cta"],
            "proofTypes": ["depoimento"], "ctaTypes": ["comentar", "enviar_mensagem"],
            "distributionContext": {"organicPaid":"unknown","trendDependency":"low"}, "confidence": "high",
            "evidence": [
                "A transcrição apresenta o medo de errar, narra a confusão regular versus diet, explica o vocabulário e encerra com aplicação e convite.",
                "A amiga é descrita sem nome; autorização para publicação não aparece de forma verificável.",
            ],
            "alternativeClassifications": ["storytelling como família principal"],
            "missingInformation": missing_full, "needsHumanReview": True,
        },
        comparison={"level":2,"group":"educação de idiomas que reenquadra erro ou constrangimento em explicação sem humilhação","referenceIds":["obs-20260825-047","obs-20260826-053"],"confidence":"high"},
        observations=[
            "A criadora explicita que o objetivo é tornar o erro leve e aprender com ele antes de narrar o caso.",
            "A história começa por volta de 4:09; a tensão surge quando a adolescente não entende regular ou diet; depois vem explicação e aplicação.",
            "A abertura dedica mais de quatro minutos à série, apresentação e CTA antes do caso; isso é estrutura observável, não evidência de abandono.",
            "Os dois comentários não medem compreensão; um elogia o conteúdo e critica a aparência técnica do vídeo.",
        ],
        interpretations=[
            "O erro funciona como contexto concreto para a correção e como redução de vergonha.",
            "A proteção de identidade reduz exposição, mas consentimento permanece não documentado.",
        ],
        scores={"gancho":72,"clareza":92,"relevancia":88,"desejo":78,"confianca":84,"retencao":"not_assessed","acao":86,"objecoes":82},
        lenses={
            "apressado":"Entende a proposta cedo, mas espera cerca de quatro minutos até a história específica.",
            "analitico":"Recebe contexto, erro, explicação e aplicação; falta fonte externa porque o caso é experiencial.",
            "aspiracional":"O reenquadramento permite imaginar comunicação mais confiante apesar de erros.",
            "comunidade":"O convite para enviar histórias abre ciclo de participação, sem evidência de volume de envios.",
            "cetico":"Pode questionar consentimento da amiga e a demora até o caso; retenção não foi medida.",
        },
        replicable=["Nomear o erro sem tratar a pessoa como incapaz.","Organizar caso, explicação e aplicação futura.","Anonimizar a pessoa e pedir consentimento antes da publicação."],
        limitations=["Transcrição automática pode conter erros.","Consentimento da pessoa narrada não foi documentado.","Audiovisual, ritmo e retenção não foram auditados."],
        role="target_support", evidence_level=2, support=True,
        claims=[
            {"claim":"um erro de compreensão é apresentado","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o erro é seguido por explicação e aplicação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o enquadramento verbal evita humilhação explícita","requiredModalities":["transcript","description"],"observedModalities":["transcript","description"],"sufficient":True},
        ],
        provenance_consent={"storyOrigin":"relato de amiga da criadora","consentStatus":"not_explicitly_documented","identityProtection":"anonymized","evidence":["a transcrição diz que a história veio de uma amiga; a adolescente não é nomeada"]},
    ),
    ref(
        id="obs-20260910-127", title="10 erros mais engraçados em inglês", creator="Bem Poliglota",
        identity="bem-poliglota", url="https://www.youtube.com/watch?v=l6p4zMmgJJo", published="2020-01-14", duration="PT9M18S",
        metrics={"viewsObserved":"1.464","likesObserved":"195","commentsObserved":"56 integralmente extraídos","subscriberCountObserved":"41,4 mil"},
        accessible=["título","criadora","descrição oficial integral","data exata","duração","transcrição automática integral em português com timestamps","fala por substituição textual","1.464 visualizações","195 curtidas","56 comentários integralmente extraídos","41,4 mil inscritos"],
        missing=missing_full,
        classification={
            "taxonomyVersion":"3.0","container":"youtube_video","materialFormat":"video_longo","presentationFormats":["camera_direta","comentario"],
            "primaryFamily":"educativo","secondaryFamilies":["humor","identificacao"],
            "functionalMix":[{"family":"educativo","percentage":55},{"family":"humor","percentage":30},{"family":"identificacao","percentage":15}],
            "objectives":["educar","identificacao","compartilhamento"],"advertisingType":"editorial_organico","commercialIntent":"implicita",
            "advertisedEntity":{"kind":"servico","name":"cursos e materiais Bem Poliglota","confidence":"high"},
            "contentTopic":{"label":"erros comuns de brasileiros ao falar inglês e seus significados involuntários","iabCode":None},
            "segment":"educação e idiomas","subsegment":"inglês para brasileiros","probableAudience":"brasileiros iniciantes ou intermediários em inglês",
            "awarenessStage":"consciente_problema","productionLevel":"simple","creatorScale":"medium","replicability":"high","durationBand":"over_60s","pace":"unknown",
            "mechanisms":["humor","identificacao","alivio","recompensa"],"hookTypes":["numero","problema"],
            "narrativeElements":["problema","progressao","conclusao","cta"],"proofTypes":["mecanismo_explicado"],"ctaTypes":["comentar","seguir"],
            "distributionContext":{"organicPaid":"unknown","trendDependency":"low"},"confidence":"high",
            "evidence":["A abertura declara que não pretende zombar nem fazer alguém se sentir mal; dez erros são explicados por contraste de significado.","Um comentário relata medo aumentado de errar; a criadora responde que essa não era a intenção."],
            "alternativeClassifications":["humor como família principal"],"missingInformation":missing_full,"needsHumanReview":True,
        },
        comparison={"level":2,"group":"educação de idiomas que reenquadra erro ou constrangimento em explicação sem humilhação","referenceIds":["obs-20260910-126","obs-20260910-128"],"confidence":"high"},
        observations=["A intenção de preservar dignidade aparece nos primeiros segundos.","Cada erro recebe contraste entre intenção e significado produzido.","O CTA pede histórias de micos; 56 comentários foram extraídos, inclusive objeção sobre aumentar medo de errar e resposta tranquilizadora da criadora."],
        interpretations=["A estrutura combina humor com correção explícita e cuidado para não punir o erro.","O comentário crítico mostra um limite: listar erros também pode elevar vigilância e ansiedade em parte do público."],
        scores={"gancho":88,"clareza":91,"relevancia":89,"desejo":77,"confianca":89,"retencao":"not_assessed","acao":82,"objecoes":88},
        lenses={"apressado":"Entende tema, quantidade e intenção nos primeiros segundos.","analitico":"Recebe exemplos e correções, mas a transcrição automática degrada algumas palavras.","aspiracional":"Pode sentir que erros são corrigíveis sem vergonha.","comunidade":"Comentários adicionam relatos e um limite emocional concreto.","cetico":"Pode temer que uma lista de erros aumente autocensura; a própria conversa pública confirma esse risco."},
        replicable=["Declarar explicitamente que o erro será corrigido sem humilhação.","Contrastar intenção, forma incorreta e significado resultante.","Monitorar comentários para detectar quando o conteúdo aumenta medo em vez de aliviar."],
        limitations=["Transcrição automática contém erros em termos ingleses.","Comentários não são amostra representativa.","Audiovisual, ritmo, retenção e baseline não foram auditados."],
        role="target_support", evidence_level=2, support=True,
        claims=[
            {"claim":"erros de inglês são apresentados","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"os erros recebem correção ou explicação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"a criadora rejeita humilhação explícita","requiredModalities":["transcript","comments"],"observedModalities":["transcript","comments"],"sufficient":True},
        ],
        provenance_consent={"storyOrigin":"exemplos didáticos e relatos genéricos","consentStatus":"not_applicable","identityProtection":"not_applicable","evidence":["nenhuma pessoa específica é identificada nos exemplos transcritos"]},
    ),
    ref(
        id="obs-20260910-128", title="Erros de tradução engraçados", creator="Teacher Livia",
        identity="teacher-livia", url="https://www.youtube.com/watch?v=9D_zk9xPjXo", published="2019-10-03", duration="PT6M1S",
        metrics={"viewsObserved":"253","likesObserved":"12","commentsObserved":"3 integralmente extraídos","subscriberCountObserved":"351"},
        accessible=["título","criadora","descrição oficial integral","data exata","duração","transcrição automática integral em português com timestamps","fala por substituição textual","253 visualizações","12 curtidas","3 comentários integralmente extraídos","351 inscritos"],
        missing=missing_full,
        classification={
            "taxonomyVersion":"3.0","container":"youtube_video","materialFormat":"video_longo","presentationFormats":["camera_direta","comentario"],
            "primaryFamily":"educativo","secondaryFamilies":["humor","curiosidade"],
            "functionalMix":[{"family":"educativo","percentage":50},{"family":"humor","percentage":30},{"family":"curiosidade","percentage":20}],
            "objectives":["educar","comentario","compartilhamento"],"advertisingType":"geracao_de_leads","commercialIntent":"explicita",
            "advertisedEntity":{"kind":"servico","name":"aulas particulares da Teacher Livia","confidence":"high"},
            "contentTopic":{"label":"erros públicos de tradução usados como exercício e explicação","iabCode":None},
            "segment":"educação e idiomas","subsegment":"tradução e vocabulário em inglês","probableAudience":"brasileiros aprendendo inglês e tradução",
            "awarenessStage":"consciente_problema","productionLevel":"simple","creatorScale":"small","replicability":"high","durationBand":"over_60s","pace":"unknown",
            "mechanisms":["humor","curiosidade","recompensa","identificacao"],"hookTypes":["problema","verbal"],
            "narrativeElements":["problema","progressao","mecanismo","conclusao","cta"],"proofTypes":["mecanismo_explicado"],"ctaTypes":["comentar","compartilhar","clicar"],
            "distributionContext":{"organicPaid":"unknown","trendDependency":"unknown"},"confidence":"medium",
            "evidence":["A transcrição apresenta imagens de traduções erradas, pergunta ao público onde está o erro e explica os termos.","A descrição identifica serviços e canais da professora."],
            "alternativeClassifications":["curiosidade como família principal"],"missingInformation":missing_full,"needsHumanReview":True,
        },
        comparison={"level":2,"group":"educação de idiomas que reenquadra erro ou constrangimento em explicação sem humilhação","referenceIds":["obs-20260910-126","obs-20260910-127"],"confidence":"medium"},
        observations=["A abertura convida a rir junto e usar os erros como exercício.","Os exemplos recebem pergunta de identificação e correção verbal.","Um comentário adiciona outro exemplo de tradução e recebe resposta da criadora."],
        interpretations=["A audiência pode participar antes da explicação, convertendo o erro em problema resolvível.","As imagens de origem não foram atribuídas na cobertura, o que limita procedência e contexto."],
        scores={"gancho":84,"clareza":83,"relevancia":84,"desejo":72,"confianca":74,"retencao":"not_assessed","acao":84,"objecoes":73},
        lenses={"apressado":"Entende que verá erros engraçados e correções.","analitico":"A explicação aparece, mas a procedência das imagens não ficou clara.","aspiracional":"A forma de quiz torna o erro praticável.","comunidade":"Comentários podem acrescentar exemplos; a amostra é de três.","cetico":"Pode questionar autoria, contexto das imagens e fidelidade da transcrição automática."},
        replicable=["Transformar erro em pergunta antes da correção.","Explicar por que a tradução falha, não apenas exibir o absurdo.","Atribuir a origem de imagens e exemplos quando identificável."],
        limitations=["A transcrição automática tem baixa fidelidade em trechos.","Imagens e texto na tela não foram observados nem atribuídos.","Audiovisual, ritmo, retenção e baseline não foram auditados."],
        role="target_support", evidence_level=2, support=True,
        claims=[
            {"claim":"erros de tradução são apresentados","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"os erros recebem pergunta e explicação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o humor é ligado ao aprendizado verbal","requiredModalities":["transcript","description"],"observedModalities":["transcript","description"],"sufficient":True},
        ],
        provenance_consent={"storyOrigin":"imagens públicas de tradução sem autoria individual observável","consentStatus":"unknown","identityProtection":"not_applicable","evidence":["nenhuma pessoa é identificada; a procedência das imagens não ficou acessível"]},
    ),
    ref(
        id="obs-20260910-129", title="Seu inglês é ruim? Nem o Macron escapa!", creator="Lingoat — Aprenda Inglês",
        identity="lingoat-aprenda-ingles", url="https://www.youtube.com/shorts/1B4nIV8vU1I", published="2026-07-23", duration="PT0M13S",
        metrics={"viewsObserved":"164","likesObserved":"4","commentsObserved":"1 integralmente extraído","subscriberCountObserved":"12,3 mil"},
        accessible=["título","criador","descrição oficial integral","data exata","duração","transcrição automática parcial de aproximadamente cinco segundos","fala parcial por substituição textual","164 visualizações","4 curtidas","1 comentário integralmente extraído","12,3 mil inscritos"],
        missing=missing_full + ["fala completa", "correção linguística completa", "fonte primária da fala pública reutilizada"],
        classification={
            "taxonomyVersion":"3.0","container":"youtube_short","materialFormat":"video_curto","presentationFormats":["comentario","reacao"],
            "primaryFamily":"humor","secondaryFamilies":["educativo","identificacao"],
            "functionalMix":[{"family":"humor","percentage":45},{"family":"educativo","percentage":35},{"family":"identificacao","percentage":20}],
            "objectives":["identificacao","educar","comentario"],"advertisingType":"editorial_organico","commercialIntent":"implicita",
            "advertisedEntity":{"kind":"servico","name":"Lingoat","confidence":"medium"},"contentTopic":{"label":"gafe pública em inglês usada para normalizar erro","iabCode":None},
            "segment":"educação e idiomas","subsegment":"motivação para brasileiros que falam inglês","probableAudience":"brasileiros inseguros com o inglês",
            "awarenessStage":"consciente_problema","productionLevel":"simple","creatorScale":"medium","replicability":"medium","durationBand":"up_to_15s","pace":"unknown",
            "mechanisms":["humor","identificacao","alivio"],"hookTypes":["pergunta","autoridade","problema"],"narrativeElements":["problema","personagem","cta"],
            "proofTypes":["alegacao_sem_prova"],"ctaTypes":["comentar"],"distributionContext":{"organicPaid":"unknown","trendDependency":"high"},"confidence":"low",
            "evidence":["Título e descrição atribuem uma gafe a Emmanuel Macron e propõem normalizar erros.","A transcrição disponível termina antes da gafe, correção ou lição completa."],
            "alternativeClassifications":["curiosidade como família principal"],"missingInformation":missing_full + ["fala completa","fonte primária"],"needsHumanReview":True,
        },
        comparison={"level":2,"group":"caso-limite de educação de idiomas que usa erro de terceiro conhecido","referenceIds":["obs-20260825-047","obs-20260910-127"],"confidence":"low"},
        observations=["A promessa é reduzir vergonha por comparação com uma autoridade pública.","A fala transcrita cobre apenas a preparação; não mostra a gafe, a explicação nem a correção."],
        interpretations=["Usar erro de terceiro famoso pode produzir identificação, mas não demonstra o mecanismo educativo sem correção observável.","Fama e circulação prévia do clipe são contingentes."],
        scores={"gancho":86,"clareza":72,"relevancia":78,"desejo":68,"confianca":58,"retencao":"not_assessed","acao":78,"objecoes":61},
        lenses={"apressado":"Identifica celebridade, problema e humor no título.","analitico":"Não consegue verificar a correção ou a fonte primária pela cobertura disponível.","aspiracional":"Recebe permissão para errar, apoiada em comparação com figura pública.","comunidade":"Há convite a contar micos; apenas um comentário foi extraído.","cetico":"Pode ver exploração de uma gafe sem valor educativo demonstrado."},
        replicable=["Se usar erro público, apresentar fonte, contexto e correção proporcional.","Evitar que a celebridade substitua o aprendizado."],
        limitations=["Transcrição parcial; gafe e correção não ficaram acessíveis.","Audiovisual, texto na tela, ritmo e retenção não foram auditados.","Não conta como apoio nem contraexemplo."],
        role="falsification_or_boundary", evidence_level=2, support=False,
        claims=[
            {"claim":"o título usa gafe pública para normalizar erro","requiredModalities":["title","description"],"observedModalities":["title","description"],"sufficient":True},
            {"claim":"a gafe é mostrada e corrigida","requiredModalities":["full_transcript_or_video"],"observedModalities":["partial_transcript"],"sufficient":False},
        ],
        provenance_consent={"storyOrigin":"fala pública atribuída a figura política","consentStatus":"public_figure_context_not_equivalent_to_permission_for_reuse","identityProtection":"not_applicable","evidence":["o título e a descrição identificam Emmanuel Macron; a fonte primária do trecho não foi acessada"]},
        source_type="youtube_public_metadata_partial_transcript_and_comments_after_public_search",
    ),
    ref(
        id="obs-20260910-130", title="Como fazer neve super fácil com 2 ingredientes", creator="Professora Coruja",
        identity="professora-coruja", url="https://www.youtube.com/shorts/VReuSWo1ggg", published="2022-11-24", duration="PT0M47S",
        metrics={"viewsObserved":"12.828","likesObserved":"203","commentsObserved":"2 integralmente extraídos","subscriberCountObserved":"357 mil"},
        accessible=["título","criadora","descrição oficial integral","data exata","duração","transcrição automática integral em português com timestamps","fala por substituição textual","12.828 visualizações","203 curtidas","2 comentários integralmente extraídos","357 mil inscritos"],
        missing=missing_full + ["resultado visual", "orientação de segurança sobre contato com olhos ou ingestão"],
        classification={
            "taxonomyVersion":"3.0","container":"youtube_short","materialFormat":"video_curto","presentationFormats":["demonstracao","tutorial"],
            "primaryFamily":"demonstracao","secondaryFamilies":["educativo","transformacao"],
            "functionalMix":[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":30},{"family":"transformacao","percentage":20}],
            "objectives":["educar","compartilhamento","seguidores"],"advertisingType":"geracao_de_leads","commercialIntent":"implicita",
            "advertisedEntity":{"kind":"servico","name":"clube, site e materiais Professora Coruja","confidence":"high"},
            "contentTopic":{"label":"atividade sensorial de neve artificial com bicarbonato e creme de cabelo","iabCode":None},
            "segment":"educação infantil e atividades pedagógicas","subsegment":"atividade sensorial de Natal","probableAudience":"professores e responsáveis por crianças",
            "awarenessStage":"consciente_solucao","productionLevel":"simple","creatorScale":"large","replicability":"high","durationBand":"31_to_60s","pace":"unknown",
            "mechanisms":["curiosidade","recompensa","desejo"],"hookTypes":["promessa","numero","transformacao"],"narrativeElements":["promessa","mecanismo","payoff","cta"],
            "proofTypes":["mecanismo_explicado"],"ctaTypes":["comentar","compartilhar","seguir"],"distributionContext":{"organicPaid":"unknown","trendDependency":"unknown"},"confidence":"high",
            "evidence":["A transcrição informa dois ingredientes, proporção, preparo e resultado declarado em 47 segundos.","Um comentário pergunta se o material arde os olhos; a fala transcrita não contém orientação de segurança."],
            "alternativeClassifications":["tutorial como apresentação principal"],"missingInformation":missing_full + ["resultado visual","segurança"],"needsHumanReview":True,
        },
        comparison={"level":3,"group":"exploração controlada de demonstração curta com resultado antecipado; não comparável ao alvo de idiomas","referenceIds":["obs-20260823-003","obs-20260903-091"],"confidence":"medium"},
        observations=["A promessa, os materiais, a proporção e o resultado declarado aparecem na transcrição.","A descrição mistura atividade gratuita, clube, produtos e links.","Um comentário levanta risco de irritação ocular; nenhuma resposta ou cautela aparece na cobertura."],
        interpretations=["A estrutura é replicável como tutorial falado curto.","A ausência de segurança observável impede ensinar a atividade como recomendação para crianças."],
        scores={"gancho":92,"clareza":94,"relevancia":88,"desejo":84,"confianca":60,"retencao":"not_assessed","acao":86,"objecoes":48},
        lenses={"apressado":"Entende resultado e número de ingredientes quase imediatamente.","analitico":"Recebe proporção, mas não segurança, textura observada ou verificação visual.","aspiracional":"A atividade parece simples e festiva.","comunidade":"Há pedido de marcação e compartilhamento; um comentário levanta segurança.","cetico":"Não deve executar com crianças sem orientação de contato, ingestão, alergia e supervisão."},
        replicable=["Antecipar resultado, limitar materiais e informar proporção.","Em atividade infantil, incluir segurança, supervisão e descarte antes do CTA."],
        limitations=["Resultado foi declarado na fala, não observado em vídeo.","Nenhuma orientação de segurança foi encontrada.","Audiovisual, ritmo, retenção e baseline não foram auditados."],
        role="controlled_exploration", evidence_level=3, support=False,
        claims=[
            {"claim":"dois ingredientes e proporção são informados","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o resultado visual foi verificado","requiredModalities":["video_or_frames"],"observedModalities":["transcript"],"sufficient":False},
            {"claim":"transcrição e descrição não apresentam orientação de segurança para crianças","requiredModalities":["transcript","description"],"observedModalities":["transcript","description"],"sufficient":True},
        ],
        provenance_consent={"storyOrigin":"not_applicable","consentStatus":"not_applicable","identityProtection":"not_applicable","evidence":["tutorial de atividade; nenhuma história pessoal é usada"]},
    ),
]

existing_urls = {item.get("url") for item in memory["references"]}
for item in refs:
    if item["url"] in existing_urls:
        raise SystemExit(f"URL duplicada: {item['url']}")
memory["references"].extend(refs)

hyp = next(item for item in memory["hypotheses"] if item["id"] == "hyp-20260825-019")
hyp["previousStatement"] = hyp["statement"]
hyp["statement"] = "Em educação de idiomas, apresentar um erro real, plausível ou publicamente reconhecido, preservar a dignidade de quem errou e explicar a correção pode transformar constrangimento em aprendizagem; efeitos sobre participação, retenção ou conversão permanecem não medidos."
hyp["status"] = "promoted_to_provisional"
hyp["supportReferenceIds"] = list(dict.fromkeys(hyp.get("supportReferenceIds", []) + ["obs-20260910-126","obs-20260910-127","obs-20260910-128"]))
hyp["promotedPatternId"] = "pat-20260910-010"
hyp["consolidatedIntoPatternId"] = "pat-20260910-010"
hyp["promotionReason"] = "A formulação anterior misturava marketing de oportunidade com um mecanismo educacional mais geral. Três novas referências comparáveis, de criadores independentes e com transcrição integral, mostram erro, enquadramento não humilhante e correção; marketing de oportunidade, fama e oferta foram rebaixados a condições contingentes."

pattern = {
    "id":"pat-20260910-010", "status":"provisional", "stage":"provisional",
    "name":"Erro de idioma reenquadrado com dignidade e correção",
    "statement":hyp["statement"], "creativeFamily":"educativo", "objective":"educar", "segment":"educação e idiomas",
    "mechanism":["humor","identificacao","alivio","confianca"],
    "conditions":["erro real, plausível ou publicamente reconhecido","correção ou explicação diretamente observável","enquadramento que não humilha a pessoa","aprendizado ou aplicação identificável"],
    "supportReferenceIds":["obs-20260910-126","obs-20260910-127","obs-20260910-128"],
    "precursorReferenceIds":["obs-20260825-047","obs-20260826-053"],
    "comparableSupportCount":3,"supportingCount":3,"counterexampleCount":0,"caseLimitCount":1,
    "counterexampleReferenceIds":[],"caseLimitReferenceIds":["obs-20260910-129"],"comparisonLevel":2,
    "confidence":"medium","creatorDiversityCount":3,"sourceDiversityCount":3,"patternType":"outro",
    "evidence":[
        {"referenceId":"obs-20260910-126","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Relato de erro de compreensão é narrado, explicado e convertido em aplicação sem nomear a adolescente.","evidence":"Transcrição automática integral, descrição e comentários.","limitations":["consentimento não documentado","sem audiovisual ou retenção"]},
        {"referenceId":"obs-20260910-127","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Lista de erros explicita intenção de não humilhar, contrasta sentidos e responde a comentário sobre medo de errar.","evidence":"Transcrição automática integral, descrição e 56 comentários.","limitations":["comentários não representativos","sem audiovisual ou retenção"]},
        {"referenceId":"obs-20260910-128","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Erros de tradução são apresentados como quiz, recebem explicação e convite para novos exemplos.","evidence":"Transcrição automática integral, descrição e três comentários.","limitations":["transcrição ruidosa","origem das imagens não acessível"]},
        {"referenceId":"obs-20260910-129","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"low","observation":"Gafe de figura pública é prometida como normalização do erro, mas a fala disponível termina antes da gafe e da correção.","evidence":"Título, descrição e transcrição parcial.","limitations":["não conta como apoio nem contraexemplo"]},
    ],
    "limitations":[
        "O padrão descreve recorrência estrutural, não eficácia.",
        "Somente três referências têm cobertura suficiente para apoio; as duas precursoras permanecem contexto parcial.",
        "Nenhum audiovisual, ritmo, retenção, aprendizagem ou conversão foi medido.",
        "Consentimento e procedência devem ser auditados quando erros pertencem a pessoas ou imagens de terceiros.",
        "Um comentário mostra que enumerar erros também pode aumentar ansiedade e autocensura.",
    ],
    "validation":"requires_human_or_experimental_evidence","taxonomyVersion":"3.0",
}
memory["patterns"].append(pattern)

memory["trainingRuns"].append({
    "id":"run-20260910-supervised-022","executedAt":NOW,"batchPolicyVersion":"1.1","requestedBatchSize":5,"candidatesFound":20,
    "referenceIds":["obs-20260910-126","obs-20260910-127","obs-20260910-128","obs-20260910-129","obs-20260910-130"],
    "targetKnowledgeId":"hyp-20260825-019","targetReferenceIds":["obs-20260910-126","obs-20260910-127","obs-20260910-128"],
    "falsificationOrBoundaryReferenceIds":["obs-20260910-129"],"controlledExplorationReferenceIds":["obs-20260910-130"],
    "discarded":[
        {"url":"https://www.youtube.com/watch?v=lF0qh2CSIXg","reason":"tema comparável, mas o lote já atingiu a cota com três criadores e esta fonte exigiria auditoria adicional"},
        {"url":"https://www.youtube.com/watch?v=PC2B-QrSX-k","reason":"vídeo de 34 minutos descartado em favor de referências com transcrição integral mais compacta"},
        {"url":"https://www.youtube.com/watch?v=99hHGBg-FCs","reason":"produção institucional e dependência de marca; reservado para teste posterior"},
        {"url":"https://www.youtube.com/watch?v=3ai0mdkIzBU","reason":"origem e comparabilidade com público brasileiro inferiores"},
        {"url":"https://www.youtube.com/watch?v=o5KojLIs_rg","reason":"segmento internacional e uso de propriedade audiovisual de série"},
        {"url":"https://www.youtube.com/watch?v=jtVh-Jqr7t8","reason":"origem do canal e substância educativa insuficientes na triagem"},
        {"url":"https://www.youtube.com/watch?v=o9YAakiCi3k","reason":"dicas de pronúncia sem enquadramento de erro constrangedor"},
        {"url":"https://www.youtube.com/watch?v=MsRO9xKVsfg","reason":"produção internacional e comparação funcional inferior"}
    ],
    "analyzed":5,"brazilianReferences":5,"internationalReferences":0,"unknownOriginReferences":0,
    "smallOrMediumCreatorReferences":4,"coverageSummary":{"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition":{"attempted":True,"succeeded":0,"failure":"downloads em baixa resolução falharam após timeouts e respostas 502; capas também não foram recuperadas","effect":"imagem em movimento, áudio ouvido, texto na tela, edição e ritmo ficaram não mensurados"},
    "transcriptCoverage":{"fullAutomatic":4,"partialAutomatic":1,"none":0,"limitation":"transcrições automáticas substituem apenas fala e podem conter erros; não substituem imagem, áudio, edição ou ritmo"},
    "commentsCoverage":{"fullOrDeclaredZero":5,"partialSample":0},
    "baselineCoverage":{"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"métricas absolutas observadas sem baseline funcional"},
    "patternsCreated":["pat-20260910-010"],"patternsStrengthened":[],"patternsRefined":[],
    "hypothesesCreated":[],"hypothesesStrengthened":["hyp-20260825-019"],"validatedPatternsCreated":0,"contradictionsFound":[],
    "caseLimitsFound":["erro de terceiro famoso sem correção observável não conta como apoio, mesmo quando o título promete normalizar a vergonha"],
    "safetyFindings":["consentimento e anonimização registrados para relato de amiga","origem de imagens de tradução permaneceu não verificada","atividade infantil com bicarbonato e creme não foi ensinada como segura porque faltam alertas e um comentário pergunta sobre irritação ocular"],
    "evidenceGateSummary":{"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome":"A hipótese foi corrigida para separar o mecanismo educacional de erro, dignidade e correção das condições contingentes de marketing de oportunidade. Três apoios independentes com transcrição integral sustentam um novo padrão provisório; nenhuma eficácia foi inferida.",
    "nextTarget":"vídeo curto brasileiro de ensino de idiomas com audiovisual integral, erro autoatribuído ou consentido, correção observável, comentários e baseline; buscar um caso comparável em que o humor aumente vergonha ou prejudique compreensão",
    "limitations":["Nenhum audiovisual ou áudio foi reproduzido.","Transcrições automáticas podem conter erros.","Sem retenção, baseline, aprendizagem ou conversão.","Comentários não são representativos.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"])}, ensure_ascii=False))
