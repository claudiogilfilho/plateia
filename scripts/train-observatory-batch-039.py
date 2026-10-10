#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-038.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-27T11:40:47.000Z"
OBSERVED = "2026-09-27"
RUN_ID = "run-20260927-supervised-039"
PATTERN_ID = "pat-20260823-002"
BATCH_IDS = {f"obs-20260927-{n}" for n in range(211, 216)}

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
              has_comments=True, transcript_provenance="youtube_automatic_transcript"):
    item = make_ref(
        id=id, title=title, creator=creator, identity=identity, url=url,
        published=published, duration=duration, accessible=accessible,
        missing=missing, metrics=metrics, cls=classification,
        comparison=comparison, observations=observations,
        interpretations=interpretations, scores=scores, lenses=lenses,
        replicable=replicable, contingent=contingent, role=role,
        evidence_level=evidence_level, eligible=eligible, claims=claims,
        source_type=source_type, comment_provenance=has_comments,
    )
    item["country"] = "BR"
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "conteúdo editorial público do próprio canal",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado identificável de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, diagnóstico, recomendação clínica, personagem ou roteiro",
        "usar medo, certeza absoluta ou aparência médica como substituto de fonte verificável",
        "tratar visualizações, marca hospitalar, fama, comentário ou produção como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
        "confundir estrutura comunicacional com precisão clínica, confiança real ou mudança de comportamento",
    ]
    item["provenance"] = [p for p in item["provenance"] if p != "youtube_automatic_transcript"]
    item["provenance"].append(transcript_provenance)
    return item


GROUP = "explicador brasileiro de saúde que nomeia risco ou pergunta, identifica autoridade, usa linguagem proporcional e oferece ação específica sem substituir atendimento"

refs = [
    build_ref(
        id="obs-20260927-211",
        title="Como saber se é infarto? | Primeiros Socorros",
        creator="Einstein Hospital Israelita", identity="einstein-hospital-israelita",
        url="https://www.youtube.com/watch?v=kdY-RKANFyc",
        published="2024-02-23", duration="PT2M53S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 2 minutos e 53 segundos",
            "transcrição automática integral em português com 61 segmentos e timestamps", "fala por substituição textual",
            "216.116 visualizações e 2.565 curtidas observadas", "amostra pública de 50 comentários",
            "Dr. Pedro Lemos identificado como cardiologista intervencionista e gerente de centro do Einstein",
            "diretriz de 2021 da Sociedade Brasileira de Cardiologia nomeada na descrição",
            "sintomas, duração indicativa, grupos de risco e orientação de procurar hospital apresentados na fala",
        ],
        missing=MISSING_AV + ["contagem pública total de comentários", "revisão clínica humana atual", "baseline comparável", "teste de compreensão"],
        metrics={"viewsObserved":216116,"likesObserved":2565,"commentsObserved":"not_measured"},
        classification=cls(
            material="video_curto", presentations=["camera_direta","institucional"], primary="explicativo",
            secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"explicativo","percentage":45},{"family":"educativo","percentage":35},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","consciencia_problema","confianca","compartilhamento"],
            topic="reconhecer sinais de infarto e procurar atendimento", segment="saúde", subsegment="cardiologia e primeiros socorros",
            audience="adultos buscando orientação inicial sobre sinais de infarto", awareness="consciente_problema",
            production="intermediate", scale="large", replicability="high", duration="over_60s",
            mechanisms=["vigilancia","urgencia","confianca","alivio"], hooks=["pergunta","risco","autoridade"],
            narrative=["problema","risco","mecanismo","conclusao"], proof=["especialista","fonte","mecanismo_explicado"],
            cta=["comparecer","seguir"], advertising="institucional", intent="implicita",
            entity={"kind":"servico","name":"Hospital Israelita Albert Einstein","confidence":"high"},
            evidence=[
                "A descrição identifica especialista, instituição e diretriz clínica de referência.",
                "A fala delimita sintomas clássicos, evita manobra doméstica e orienta atendimento hospitalar.",
                "Cinquenta comentários foram amostrados; perguntas e agradecimentos não medem compreensão nem segurança clínica.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20260927-212","obs-20260927-213"],"confidence":"high"},
        observations=[
            "Pergunta, sinais, autoridade e próximo passo aparecem de forma rastreável no título, descrição e fala.",
            "A recomendação central é procurar atendimento; o conteúdo não se apresenta como diagnóstico individual.",
            "A diretriz é nomeada, mas sua aplicação e atualização não receberam revisão clínica humana neste lote.",
        ],
        interpretations=[
            "Identificar fonte e limite de ação torna o caminho comunicacional verificável sem exigir que o público faça autodiagnóstico.",
            "Marca, métricas e comentários são contexto e não demonstram confiança, compreensão ou adesão.",
        ],
        scores={"gancho":94,"clareza":95,"relevancia":94,"desejo":70,"confianca":91,"retencao":"not_assessed","acao":94,"objecoes":88},
        lenses={
            "apressado":"Recebe pergunta, sinais e ação hospitalar cedo.",
            "analitico":"Encontra especialista e diretriz nomeados, mas precisa de revisão clínica atual.",
            "aspiracional":"A transformação proposta é agir com segurança diante do risco.",
            "comunidade":"Comentários trazem dúvidas e agradecimentos, sem evidência de aprendizagem.",
            "cetico":"Valoriza a fonte e rejeita interpretar o vídeo como diagnóstico pessoal.",
        },
        replicable=["Nomear uma pergunta clínica concreta.","Identificar credencial e fonte pública.","Encerrar com ação segura que não substitua atendimento."],
        contingent=["Precisão clínica não foi auditada por especialista humano.","Audiovisual e retenção não foram observados.","Instituição e autoridade não são transferíveis a criadores sem credenciais."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"pergunta, risco, autoridade identificável e ação hospitalar aparecem publicamente","requiredModalities":["metadata","description","transcript"],"observedModalities":["metadata","description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_50_public_comments",
    ),
    build_ref(
        id="obs-20260927-212",
        title="Sintomas de Infarto | Quando devo ir ao hospital?",
        creator="Hcor", identity="hcor",
        url="https://www.youtube.com/watch?v=MNicm8L0Sqk",
        published="2020-06-01", duration="PT2M15S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 2 minutos e 15 segundos",
            "transcrição automática integral em português com 42 segmentos e timestamps", "fala por substituição textual",
            "3.078 visualizações e 111 curtidas observadas", "único comentário público retornado",
            "Dr. Alexandre Abizaid identificado na descrição", "sintomas de infarto e orientação de procurar hospital presentes na fala",
            "contexto de medo hospitalar durante a pandemia explicitado",
        ],
        missing=MISSING_AV + ["credencial detalhada do médico na própria publicação", "revalidação pós-pandemia", "revisão clínica humana", "teste de compreensão"],
        metrics={"viewsObserved":3078,"likesObserved":111,"commentsObserved":1},
        classification=cls(
            material="video_curto", presentations=["camera_direta","institucional"], primary="explicativo",
            secondary=["educativo","conscientizacao"],
            mix=[{"family":"explicativo","percentage":45},{"family":"educativo","percentage":35},{"family":"conscientizacao","percentage":20}],
            objectives=["educar","consciencia_problema","confianca"], topic="sintomas de infarto e receio de procurar hospital na pandemia",
            segment="saúde", subsegment="cardiologia e emergência", audience="adultos com sintomas cardíacos ou receio de procurar atendimento",
            awareness="consciente_problema", production="simple", scale="large", replicability="high", duration="over_60s",
            mechanisms=["vigilancia","urgencia","confianca","alivio"], hooks=["pergunta","risco"],
            narrative=["situacao","problema","risco","conclusao"], proof=["especialista","autoridade_demonstrada","mecanismo_explicado"],
            cta=["comparecer","seguir"], advertising="institucional", intent="implicita",
            entity={"kind":"servico","name":"Hcor","confidence":"high"},
            evidence=[
                "O título pergunta quando ir ao hospital e a descrição identifica o médico.",
                "A fala enumera dor, irradiação, suor frio, náusea e falta de ar antes de orientar atendimento.",
                "A moldura é a pandemia de 2020; sua atualidade contextual não foi revalidada.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20260927-211","obs-20260927-213"],"confidence":"high"},
        observations=[
            "A pergunta e o risco são concretos, e a ação específica é não postergar o atendimento.",
            "A autoridade é atribuída a um médico em um canal hospitalar, embora a credencial detalhada não conste da publicação.",
            "O contexto pandêmico é datado; isso limita transferência literal, não a estrutura observada.",
        ],
        interpretations=[
            "Uma objeção contextual pode ser tratada antes da ação, desde que não seja confundida com recomendação universal atual.",
            "Um comentário de agradecimento não mede compreensão, segurança ou comportamento.",
        ],
        scores={"gancho":91,"clareza":92,"relevancia":88,"desejo":66,"confianca":82,"retencao":"not_assessed","acao":93,"objecoes":86},
        lenses={
            "apressado":"Entende sintomas, urgência e destino.",
            "analitico":"Recebe sinais e contexto, mas desconta a publicação de 2020.",
            "aspiracional":"A promessa é evitar complicação pelo atendimento em tempo hábil.",
            "comunidade":"Um comentário não sustenta inferência coletiva.",
            "cetico":"Exige atualização clínica e separa instituição de prova factual.",
        },
        replicable=["Transformar objeção concreta em pauta.","Nomear sinais antes da ação.","Indicar destino e urgência sem prometer diagnóstico remoto."],
        contingent=["Contexto de pandemia publicado em 2020.","Credencial detalhada não consta da descrição.","Audiovisual, retenção e efeito comportamental não foram medidos."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"pergunta, sinais, autoridade atribuída e ação hospitalar aparecem publicamente","requiredModalities":["metadata","description","transcript"],"observedModalities":["metadata","description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_1_public_comment",
    ),
    build_ref(
        id="obs-20260927-213",
        title="Pressão alta (hipertensão arterial) | Sintomas, diagnóstico e tratamento",
        creator="Hospital Alemão Oswaldo Cruz", identity="hospital-alemao-oswaldo-cruz",
        url="https://www.youtube.com/watch?v=K7QnivczWVo",
        published="2022-01-12", duration="PT3M14S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 3 minutos e 14 segundos",
            "transcrição automática integral em português com 78 segmentos e timestamps", "fala por substituição textual",
            "735.238 visualizações e 12.188 curtidas observadas", "amostra pública de 50 comentários",
            "Dr. Leandro Costa identificado como cardiologista do hospital", "caráter frequentemente assintomático e sinais extremos explicados",
            "avaliação periódica, procura imediata em sinais graves e acompanhamento médico apresentados como ações",
        ],
        missing=MISSING_AV + ["contagem pública total de comentários", "fontes clínicas listadas", "revisão clínica humana atual", "teste de compreensão"],
        metrics={"viewsObserved":735238,"likesObserved":12188,"commentsObserved":"not_measured"},
        classification=cls(
            material="video_curto", presentations=["camera_direta","institucional"], primary="explicativo",
            secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"explicativo","percentage":45},{"family":"educativo","percentage":35},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","consciencia_problema","confianca","comentario"], topic="hipertensão, sintomas, diagnóstico e tratamento",
            segment="saúde", subsegment="cardiologia e hipertensão", audience="adultos interessados em prevenção e acompanhamento de pressão alta",
            awareness="consciente_problema", production="simple", scale="large", replicability="high", duration="over_60s",
            mechanisms=["vigilancia","confianca","alivio","utilidade_pratica"], hooks=["problema","autoridade"],
            narrative=["problema","mecanismo","risco","conclusao","cta"], proof=["especialista","mecanismo_explicado","autoridade_demonstrada"],
            cta=["comentar","comparecer","seguir"], advertising="institucional", intent="implicita",
            entity={"kind":"servico","name":"Hospital Alemão Oswaldo Cruz","confidence":"high"},
            evidence=[
                "A abertura informa que a hipertensão costuma ser assintomática e identifica o cardiologista.",
                "A fala distingue sinais extremos, consulta periódica, tratamento farmacológico e não farmacológico.",
                "A descrição declara finalidade informativa e recomenda consultar autoridade de saúde.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260927-211","obs-20260927-212"],"confidence":"high"},
        observations=[
            "O risco é proporcionalmente qualificado: ausência de sintomas é diferenciada de valores extremos e sinais graves.",
            "A autoridade e o limite informativo são publicamente identificáveis.",
            "A resposta do hospital a um comentário recomenda avaliação; a amostra não mede aprendizagem.",
        ],
        interpretations=[
            "Distinguir rotina, alerta e emergência pode reduzir ambiguidade sem prometer diagnóstico pelo conteúdo.",
            "O volume de visualizações e a marca hospitalar não demonstram confiança real ou eficácia.",
        ],
        scores={"gancho":86,"clareza":94,"relevancia":91,"desejo":69,"confianca":89,"retencao":"not_assessed","acao":91,"objecoes":90},
        lenses={
            "apressado":"Recebe cedo que hipertensão pode ser silenciosa.",
            "analitico":"Encontra distinções e especialista, mas não referências clínicas listadas.",
            "aspiracional":"A transformação é acompanhamento preventivo e controle.",
            "comunidade":"Comentários contêm dúvidas e respostas, sem amostra representativa.",
            "cetico":"Valoriza ressalvas e exige revisão clínica contemporânea.",
        },
        replicable=["Distinguir ausência de sintomas de sinais graves.","Separar rotina, avaliação e emergência.","Declarar finalidade informativa e limite do conteúdo."],
        contingent=["Fontes clínicas não estão listadas.","A publicação é de 2022.","Audiovisual, retenção e efeito clínico não foram observados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"risco, autoridade, linguagem qualificada e ações específicas aparecem na fala e descrição","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_50_public_comments",
    ),
    build_ref(
        id="obs-20260927-214",
        title="Os 5 Sinais de Infarto: O Seu Corpo Avisa MESES Antes (Você Ignora!)",
        creator="Curiosidade Oculta Lab", identity="curiosidade-oculta-lab",
        url="https://www.youtube.com/watch?v=wgCv2wA4Bn4",
        published="2026-05-17", duration="PT2M34S",
        accessible=[
            "título", "criador", "descrição pública integral com capítulos", "data exata", "duração de 2 minutos e 34 segundos",
            "legenda humana integral em português do Brasil com 30 segmentos e timestamps", "fala por substituição textual",
            "93 visualizações, 11 curtidas e 6 comentários públicos retornados",
            "cinco sinais e orientação de assistência médica imediata", "três famílias de fontes mencionadas genericamente na descrição",
            "nenhum profissional de saúde, autor, página, DOI ou link clínico identificado",
        ],
        missing=MISSING_AV + ["autoridade médica identificável", "referências completas por alegação", "revisão clínica humana", "teste de compreensão"],
        metrics={"viewsObserved":93,"likesObserved":11,"commentsObserved":6},
        classification=cls(
            material="video_curto", presentations=["narracao_imagens","comentario"], primary="curiosidade",
            secondary=["polemica","conscientizacao"],
            mix=[{"family":"curiosidade","percentage":45},{"family":"polemica","percentage":30},{"family":"conscientizacao","percentage":25}],
            objectives=["interromper_rolagem","consciencia_problema","compartilhamento","comentario"],
            topic="alegados sinais meses antes de um infarto", segment="saúde", subsegment="cardiologia popular",
            audience="público geral preocupado com sinais precoces de infarto", awareness="consciente_problema",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["medo","urgencia","curiosidade","vigilancia"], hooks=["risco","urgencia","numero","promessa"],
            narrative=["risco","promessa","progressao","conclusao","cta"], proof=["fonte","alegacao_sem_prova","mecanismo_explicado"],
            cta=["comentar","compartilhar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"medium"},
            evidence=[
                "Título, descrição e legenda afirmam que o corpo avisa semanas ou meses antes e usam linguagem de fatalidade.",
                "A descrição nomeia Circulation, Mayo Clinic e SBC/Rede D'Or apenas em categorias, sem citação rastreável por alegação.",
                "O canal e a publicação não identificam profissional de saúde responsável pelo conteúdo.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260927-211","obs-20260927-212","obs-20260927-213"],"confidence":"high"},
        observations=[
            "Risco e ação aparecem, mas autoridade verificável e proporcionalidade permanecem ausentes.",
            "A legenda usa universalizações como ciência já provou, máquina perfeita e falha iminente.",
            "Fontes amplas não permitem ligar cada sinal à evidência correspondente.",
        ],
        interpretations=[
            "É caso-limite: aparência científica e orientação final não substituem autoria clínica e rastreabilidade.",
            "A ausência de revisão não prova que cada sinal seja falso; torna precisão e proporcionalidade não mensuradas.",
        ],
        scores={"gancho":95,"clareza":84,"relevancia":88,"desejo":72,"confianca":38,"retencao":"not_assessed","acao":76,"objecoes":35},
        lenses={
            "apressado":"Entende rápido o risco e a lista.",
            "analitico":"Não encontra autoria médica nem citação por alegação.",
            "aspiracional":"A promessa é detectar um perigo cedo.",
            "comunidade":"Seis comentários trazem reações, não compreensão.",
            "cetico":"Rejeita certeza ampla, medo e autoridade genérica.",
        },
        replicable=["Delimitar uma lista curta.","Oferecer orientação de procurar assistência.","Organizar descrição por capítulos."],
        contingent=["Autoridade médica não identificada.","Fontes não são rastreáveis por alegação.","Precisão clínica, cenas, áudio, ritmo e retenção não foram auditados."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"risco e ação aparecem na publicação","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"há autoridade identificável, linguagem proporcional e fonte rastreável por alegação","requiredModalities":["description","source_list","credential"],"observedModalities":["description"],"sufficient":False},
            {"claim":"os cinco sinais e mecanismos são clinicamente corretos","requiredModalities":["expert_review","primary_sources"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_human_caption_and_6_public_comments",
        transcript_provenance="youtube_human_caption",
    ),
    build_ref(
        id="obs-20260927-215",
        title="Governo identifica 97 perfis de médicos criados por IA e cobra remoção de vídeos | Cidade Alerta DF",
        creator="Record Brasília", identity="record-brasilia",
        url="https://www.youtube.com/watch?v=VXDDysumNq8",
        published="2026-09-11", duration="PT3M58S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata de 11 de setembro de 2026", "duração de 3 minutos e 58 segundos",
            "transcrição automática integral em português com 104 segmentos e timestamps", "fala por substituição textual",
            "1.889 visualizações e 18 curtidas observadas", "nenhum comentário público retornado e contagem total indisponível",
            "alegação jornalística de 97 perfis identificados entre janeiro e julho de 2026",
            "sinais verbais para desconfiar de avatar, promessa milagrosa, venda e credencial não verificada",
            "orientação de verificar CRM e denunciar em canais oficiais",
        ],
        missing=MISSING_AV + ["nota oficial primária acessível na busca pública", "identificação completa dos especialistas entrevistados na descrição", "contagem de comentários", "auditoria visual dos sinais de avatar"],
        metrics={"viewsObserved":1889,"likesObserved":18,"commentsObserved":"not_measured"},
        classification=cls(
            material="video_curto", presentations=["reportagem","comentario","institucional"], primary="noticia_atualidade",
            secondary=["conscientizacao","explicativo"],
            mix=[{"family":"noticia_atualidade","percentage":50},{"family":"conscientizacao","percentage":30},{"family":"explicativo","percentage":20}],
            objectives=["consciencia_problema","educar","confianca","compartilhamento"],
            topic="falsos médicos criados por IA e checagem de credenciais", segment="mídia e saúde", subsegment="desinformação médica e inteligência artificial",
            audience="usuários de redes sociais expostos a aconselhamento de saúde", awareness="consciente_problema",
            production="complex", scale="large", replicability="low", duration="over_60s",
            mechanisms=["vigilancia","medo","confianca","utilidade_pratica"], hooks=["risco","numero","novidade"],
            narrative=["problema","risco","prova","mecanismo","conclusao"], proof=["dado","especialista","autoridade_percebida"],
            cta=["compartilhar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"}, confidence="medium",
            evidence=[
                "A descrição e a transcrição atribuem o número de perfis ao Ministério da Saúde e a notificação à AGU.",
                "A fala orienta verificar CRM e desconfiar de promessas de cura garantida e venda pressionada.",
                "Os indícios visuais de avatar não foram auditados porque o vídeo não foi adquirido.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de reportagem sobre confiança e desinformação médica","referenceIds":[],"confidence":"low"},
        observations=[
            "A reportagem contrapõe aparência de autoridade a credencial verificável e ação de checagem.",
            "A fonte primária da alegação numérica não ficou acessível na pesquisa pública realizada.",
            "Movimento, sincronização labial e expressões foram apenas descritos, não observados.",
        ],
        interpretations=[
            "A exploração reforça a necessidade de rastrear autoridade, mas não é par funcional dos explicadores médicos.",
            "Sem fonte oficial acessível e audiovisual, não se cria hipótese nem se confirma o diagnóstico visual de IA.",
        ],
        scores={"gancho":91,"clareza":90,"relevancia":93,"desejo":68,"confianca":72,"retencao":"not_assessed","acao":88,"objecoes":70},
        lenses={
            "apressado":"Recebe o risco e o número na abertura.",
            "analitico":"Quer a nota oficial e nomes completos dos entrevistados.",
            "aspiracional":"A transformação é consumir orientação médica com mais segurança.",
            "comunidade":"Não houve comentários públicos retornados.",
            "cetico":"Aceita a regra de verificar CRM, mas não generaliza sinais visuais não auditados.",
        },
        replicable=["Ensinar uma verificação concreta de credencial.","Separar aparência de autoridade de registro profissional.","Nomear sinais de promessa absoluta e pressão comercial."],
        contingent=["Produção jornalística e acesso a fontes elevam complexidade.","A fonte primária da contagem não ficou acessível.","Sinais visuais, cenas, ritmo e retenção não foram observados."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a reportagem ensina verificar CRM e desconfiar de promessa absoluta","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"os sinais visuais de avatar são observáveis nesta publicação","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
            {"claim":"o governo identificou exatamente 97 perfis","requiredModalities":["official_primary_source"],"observedModalities":["report_description","transcript"],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_zero_returned_comments_and_public_search",
        has_comments=False,
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 039")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260927-211", "obs-20260927-212", "obs-20260927-213"]
new_case = "obs-20260927-214"
pattern["statement"] = "Em explicadores de saúde, combinar pergunta ou risco concreto, autoridade rastreável, linguagem proporcional e ação específica torna problema, fonte, limite e próximo passo identificáveis; efeitos sobre confiança, compreensão e comportamento permanecem não medidos."
pattern["name"] = pattern["statement"]
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 13
pattern["supportingCount"] = 13
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 8
pattern["sourceDiversityCount"] = 7
pattern["conditions"] = [
    "conteúdo educativo ou explicativo de saúde",
    "pergunta ou risco concreto",
    "autoridade identificável e rastreável",
    "linguagem proporcional sem promessa médica absoluta",
    "ação específica que não substitui atendimento",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260927-211","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta, sinais, cardiologista identificado, diretriz nomeada e ação hospitalar aparecem no pacote público.","evidence":"Metadados, descrição integral, transcrição automática integral e cinquenta comentários amostrados.","limitations":["sem audiovisual, revisão clínica humana ou teste de compreensão"]},
    {"referenceId":"obs-20260927-212","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Sintomas, risco, médico atribuído e ação de procurar hospital são explicitados, com objeção pandêmica tratada.","evidence":"Metadados, descrição integral, transcrição automática integral e um comentário.","limitations":["contexto publicado em 2020, sem revalidação clínica ou audiovisual"]},
    {"referenceId":"obs-20260927-213","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"O cardiologista diferencia rotina, caráter assintomático, sinais extremos e atendimento imediato, com limite informativo declarado.","evidence":"Metadados, descrição integral, transcrição automática integral e cinquenta comentários amostrados.","limitations":["sem fontes clínicas listadas, revisão humana ou audiovisual"]},
    {"referenceId":"obs-20260927-214","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Há risco, lista e ação, mas a publicação não identifica autoridade médica e usa certeza ampla com fontes genéricas.","evidence":"Metadados, descrição integral, legenda humana integral e seis comentários.","limitations":["não conta como apoio nem como contraexemplo clínico"]},
])
pattern["limitations"] = [
    "Treze apoios formais vêm de oito criadores e sete fontes; demonstram recorrência estrutural, não confiança, compreensão ou comportamento.",
    "Nenhuma referência oferece retenção, teste de compreensão, revisão clínica humana deste lote ou experimento causal.",
    "Marca hospitalar, fama, métricas e comentários permanecem contexto não causal.",
    "O novo caso-limite reforça que fontes genéricas e aviso médico não substituem autoria clínica e proporcionalidade.",
    "Publicações de 2020 a 2024 podem exigir atualização clínica; a comparação é comunicacional, não diretriz médica.",
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 114,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260927-215"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=QFSm6HhXU50","reason":"explicador comparável, porém publicado em 2013 e com orientação medicamentosa que exigiria revisão clínica específica; três apoios mais adequados foram selecionados"},
        {"url":"https://www.youtube.com/watch?v=TY-xHoBs2eo","reason":"transcrição integral e autoridade identificável, mas duração de 13 minutos e bloco terapêutico detalhado reduzem comparabilidade com o grupo curto selecionado"},
        {"url":"https://www.youtube.com/watch?v=JpbsbQiHho4","reason":"mesmo criador aparece repetidamente no pool e a seleção priorizou diversidade de fontes institucionais"},
        {"url":"https://www.youtube.com/watch?v=sY6huX32cr8","reason":"embalagem de alerta disponível, mas a cobertura e a autoridade pública ficaram inferiores às três referências-alvo"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 1,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["explicativo","educativo","autoridade_opiniao","conscientizacao","curiosidade","polemica","noticia_atualidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "para as cinco URLs, vídeo e áudio retornaram arquivos HTML de 195 bytes; as cinco capas também retornaram HTML de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":1,
        "fullAutomatic":4,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":0,
        "limitation":"quatro transcrições automáticas e uma legenda humana substituem somente a fala; não sustentam cenas, voz ou ritmo",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":4,
        "sampledComments":107,
        "zeroReturnedReferences":1,
        "limitation":"comentários públicos não são amostra representativa nem teste de compreensão, segurança ou confiança",
    },
    "baselineCoverage": {
        "sampledProfiles":0,
        "contemporaneousBaselines":0,
        "limitation":"datas, temas, escalas e instituições diferentes impedem benchmark causal de desempenho",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["alerta, fontes genéricas e orientação final não satisfazem o padrão sem autoridade identificável e linguagem proporcional"],
    "safetyFindings": [
        "precisão clínica não foi inferida de autoridade, marca, legenda, descrição, comentários ou métricas",
        "nenhuma orientação médica foi ensinada como recomendação ao usuário",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "a alegação jornalística recente foi registrada como não confirmada por fonte oficial primária acessível",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três fontes institucionais independentes elevam de dez para treze os apoios do padrão de explicação de saúde rastreável. Um caso-limite mostra que risco e aviso médico não compensam autoria ausente e certeza desproporcional. O padrão permanece provisório.",
    "nextTarget": "explicador brasileiro recente e curto de saúde, de profissional ou instituição pequena ou média, com audiovisual integral, credencial e fonte primária verificáveis, ação segura e teste de compreensão; buscar também um caso em que a credencial seja real, mas a recomendação exceda a evidência",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Quatro transcrições são automáticas integrais e uma legenda é humana integral.",
        "Foram amostrados 107 comentários; a amostra não é representativa.",
        "Não houve baseline, retenção, teste de compreensão, revisão clínica humana ou causalidade.",
        "A fonte oficial primária da exploração jornalística não ficou acessível na pesquisa pública.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
