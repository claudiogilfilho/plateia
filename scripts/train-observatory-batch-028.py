#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Reuse the schema-compatible builders and the existing batch-027 reconstruction.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-027.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
classification = ns["classification"]
make_ref = ns["make_ref"]

NOW = "2026-09-15T11:26:25.000Z"
OBSERVED = "2026-09-15"
RUN_ID = "run-20260915-supervised-028"
PATTERN_ID = "pat-20260914-014"
BATCH_IDS = {f"obs-20260915-{n}" for n in range(156, 161)}

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


def cls(*, material="video_longo", presentations, primary, secondary, mix, objectives,
        topic, segment, subsegment, audience, awareness="consciente_produto",
        production="simple", scale="small", replicability="high", duration="over_60s",
        mechanisms, hooks, narrative, proof, cta, confidence="high", evidence,
        alternatives=None, missing=None, advertising="publicidade_nativa", intent="explicita",
        entity=None, trend="low"):
    return classification(
        material=material, presentations=presentations, primary=primary,
        secondary=secondary, mix=mix, objectives=objectives,
        advertising=advertising, intent=intent,
        entity=entity or {"kind": "produto", "name": topic, "confidence": "high"},
        topic=topic, segment=segment, subsegment=subsegment, audience=audience,
        awareness=awareness, production=production, scale=scale,
        replicability=replicability, duration=duration, mechanisms=mechanisms,
        hooks=hooks, narrative=narrative, proof=proof, cta=cta,
        confidence=confidence, evidence=evidence,
        alternatives=alternatives or [], missing=missing or MISSING_AV, trend=trend,
    )


def ref(**kwargs):
    item = make_ref(**kwargs)
    item["country"] = "BR"
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "experiência própria declarada ou experimento editorial do criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, personagens ou roteiro",
        "tratar popularidade, link de afiliado ou orçamento como prova causal",
        "aceitar alegações de produto ou segurança sem verificação independente",
        "inferir cenas, áudio, texto na tela, edição, ritmo ou retenção",
    ]
    return item


refs = [
    ref(
        id="obs-20260915-156",
        title="Usei o Amazfit Bip 6 por 30 Dias... Vale a Pena?",
        creator="TecNoob", identity="tecnoob",
        url="https://www.youtube.com/watch?v=Tl682ohqWoY",
        published="2026-08-01", duration="PT12M30S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "2.418 visualizações, 83 curtidas e 5 comentários declarados nos metadados públicos",
            "amostra pública de 3 comentários, sem inferência de representatividade",
            "período de uso superior a 30 dias", "declaração falada de ausência de patrocínio",
            "critérios falados de design, tela, recursos, sensores, mapas, chamadas, bateria e uso real",
            "veredito condicionado à utilização dos recursos", "links comerciais e grupo de ofertas na descrição",
        ],
        missing=MISSING_AV + ["2 comentários não adquiridos", "disclosure do caráter afiliado dos links", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":2418,"likesObserved":83,"commentsObserved":5},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="comparacao",
            secondary=["autoridade_opiniao","educativo"],
            mix=[{"family":"comparacao","percentage":50},{"family":"autoridade_opiniao","percentage":30},{"family":"educativo","percentage":20}],
            objectives=["educar","apresentar_solucao","confianca","venda"],
            topic="review pós-uso do Amazfit Bip 6", segment="tecnologia de consumo",
            subsegment="smartwatches", audience="pessoas comparando relógios inteligentes de entrada e intermediários",
            mechanisms=["confianca","aproximacao","vigilancia","recompensa"],
            hooks=["numero","pergunta","problema"], narrative=["situacao","prova","progressao","conclusao"],
            proof=["depoimento","tratamento_objecao"], cta=["clicar"],
            evidence=[
                "A fala declara mais de 30 dias de uso antes da avaliação.",
                "Recursos desejados são confrontados com os que o criador efetivamente usou.",
                "Entre 10:25 e 12:10, a recomendação muda conforme necessidade, preço e uso dos recursos.",
                "A descrição inclui links comerciais; a fala diz que o vídeo não foi patrocinado.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260915-157","obs-20260915-158"],"confidence":"high"},
        observations=[
            "O contexto de uso aparece antes dos critérios.",
            "Mapa, música e chamadas são avaliados também pelo não uso, evitando confundir presença de recurso com utilidade.",
            "O fechamento recomenda pagar menos quando os recursos adicionais não serão usados.",
            "Na amostra de três comentários, aparecem uma dúvida de configuração, uma atualização de recurso e um elogio à objetividade; isso não mede compreensão.",
        ],
        interpretations=[
            "A sequência torna rastreável por que dois perfis podem chegar a decisões diferentes.",
            "A recorrência estrutural não demonstra efeito sobre confiança, retenção ou compra.",
        ],
        scores={"gancho":89,"clareza":94,"relevancia":94,"desejo":76,"confianca":80,"retencao":"not_assessed","acao":82,"objecoes":91},
        lenses={
            "apressado":"Percebe produto, preço aproximado, período e dúvida de compra no primeiro minuto.",
            "analitico":"Recebe critérios e não uso; ainda precisa verificar especificações e links comerciais.",
            "aspiracional":"A estética é valorizada, mas não substitui a utilidade dos recursos.",
            "comunidade":"Há convite para grupo de ofertas; conversas não foram acessadas.",
            "cetico":"Valoriza a ressalva por perfil, mas desconta alegações não verificadas e disclosure incompleto.",
        },
        replicable=["Declarar período e cenário antes dos critérios.","Comparar recursos prometidos com usos efetivos.","Recomendar a faixa de produto conforme necessidade, não de forma universal."],
        contingent=["Especificações, imagens e testes não foram verificados independentemente.","Links comerciais podem afetar independência percebida.","Métricas públicas não demonstram causalidade."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"período e cenário precedem a avaliação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"critérios concretos precedem veredito condicionado","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260915-157",
        title="TESTEI A UTMIFY POR 30 DIAS! VALEU A PENA? Opinião Sincera!",
        creator="Rodrigo Tannús - Digital com Propósito", identity="rodrigo-tannus-digital-com-proposito",
        url="https://www.youtube.com/watch?v=X2Q6_bAGPvQ",
        published="2026-09-03", duration="PT8M23S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "406 visualizações e 7 curtidas nos metadados públicos; comentários não declarados",
            "período de 30 dias", "declaração falada de ausência de patrocínio",
            "critérios falados de suporte, integração, atribuição, relatórios e otimização",
            "falhas e limites declarados durante a gravação", "link de afiliado com desconto e oferta de mentoria na descrição",
        ],
        missing=MISSING_AV + ["comentários públicos", "verificação dos painéis e valores citados", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":406,"likesObserved":7,"commentsObserved":"not_assessed"},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="autoridade_opiniao",
            secondary=["comparacao","demonstracao"],
            mix=[{"family":"autoridade_opiniao","percentage":45},{"family":"comparacao","percentage":35},{"family":"demonstracao","percentage":20}],
            objectives=["educar","apresentar_solucao","venda","confianca"],
            topic="review pós-uso da UTMify", segment="marketing digital",
            subsegment="atribuição e gestão de campanhas", audience="gestores de tráfego e infoprodutores avaliando ferramenta de atribuição",
            production="simple", scale="small", replicability="high",
            mechanisms=["confianca","utilidade_pratica","vigilancia","recompensa"],
            hooks=["numero","pergunta","problema"], narrative=["situacao","prova","problema","conclusao"],
            proof=["depoimento","dado","tratamento_objecao"], cta=["clicar","comprar","seguir"],
            evidence=[
                "A abertura declara 30 dias de teste e ausência de patrocínio.",
                "A fala descreve suporte, integrações, atribuição, relatórios, erros e diferenças entre Brasil e exterior.",
                "A recomendação é mais forte para operações internacionais ou plataformas com marcação ruim.",
                "Há comissão de indicação, desconto e oferta de mentoria; valores e telas não foram verificados visualmente.",
            ],
        ),
        comparison={"level":2,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260915-156","obs-20260915-158"],"confidence":"high"},
        observations=[
            "O período de teste antecede a avaliação.",
            "A experiência inclui benefícios, falhas de integração e um erro ocorrido durante a própria gravação, observáveis apenas na fala transcrita.",
            "O veredito distingue cenário internacional, qualidade da plataforma de origem e necessidade de visão consolidada.",
        ],
        interpretations=[
            "Critérios e falhas faladas tornam a recomendação auditável no nível textual.",
            "A relação de afiliado exige separar estrutura editorial de prova comercial.",
        ],
        scores={"gancho":87,"clareza":88,"relevancia":92,"desejo":79,"confianca":72,"retencao":"not_assessed","acao":91,"objecoes":86},
        lenses={
            "apressado":"Entende período, ferramenta e proposta de opinião real rapidamente.",
            "analitico":"Recebe critérios e falhas, mas não pode auditar os painéis nem o faturamento citado.",
            "aspiracional":"A promessa de visão consolidada é atraente, sem prova visual acessível.",
            "comunidade":"Cursos e mentoria são oferecidos; comentários não foram acessados.",
            "cetico":"Considera o vínculo afiliado e não transforma valores declarados em evidência independente.",
        },
        replicable=["Declarar o período e o ambiente de teste.","Preservar falhas e limites junto dos benefícios.","Condicionar o uso da ferramenta ao mercado e à infraestrutura do comprador."],
        contingent=["Painéis, resultados e valores foram apenas declarados na fala.","Link de afiliado e mentoria criam conflito comercial potencial.","Sem audiovisual, comentários, retenção ou baseline."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"período e ambiente precedem a avaliação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"critérios, falhas e cenário qualificam o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260915-158",
        title="USEI o IPHONE 17 por 30 DIAS: vale a pena COMPRAR?!",
        creator="André Felipe", identity="andre-felipe",
        url="https://www.youtube.com/watch?v=zkryQP5vohI",
        published="2026-07-09", duration="PT15M21S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "9.045 visualizações, 402 curtidas e 37 comentários declarados nos metadados públicos",
            "amostra pública de 14 comentários, sem inferência de representatividade",
            "período de 30 dias como smartphone principal",
            "critérios falados de tela, hardware, câmeras, software, bateria, design, preço e longevidade",
            "cenários falados de usuário leve e pesado", "links comerciais e grupos de ofertas na descrição",
        ],
        missing=MISSING_AV + ["23 comentários não adquiridos", "disclosure do caráter afiliado dos links", "verificação de desempenho e bateria", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":9045,"likesObserved":402,"commentsObserved":37},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="comparacao",
            secondary=["autoridade_opiniao","educativo"],
            mix=[{"family":"comparacao","percentage":50},{"family":"autoridade_opiniao","percentage":30},{"family":"educativo","percentage":20}],
            objectives=["educar","apresentar_solucao","venda","confianca"],
            topic="review pós-uso do iPhone 17", segment="tecnologia de consumo",
            subsegment="smartphones", audience="compradores comparando gerações e perfis de uso de iPhone",
            production="simple", scale="medium", replicability="high",
            mechanisms=["confianca","aproximacao","recompensa","vigilancia"],
            hooks=["numero","pergunta","verbal"], narrative=["situacao","prova","progressao","conclusao"],
            proof=["depoimento","mecanismo_explicado","tratamento_objecao"], cta=["comentar","clicar","seguir"],
            evidence=[
                "A abertura declara 30 dias como aparelho principal e enumera os critérios de decisão.",
                "Preço relativo e horizonte de atualização aparecem antes da recomendação.",
                "A autonomia é condicionada ao perfil leve ou pesado de uso.",
                "A descrição e o fechamento direcionam a links comerciais; testes visuais não foram auditados.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260915-156","obs-20260915-157"],"confidence":"high"},
        observations=[
            "O contexto e a lista de critérios são declarados antes da análise.",
            "A recomendação principal depende do preço relativo; a bateria depende do perfil de uso.",
            "Há pontos positivos e negativos falados, inclusive USB e limitações atuais de IA.",
            "A amostra de 14 comentários contém dúvidas de preço, bateria e configuração, além de discordância taxonômica; não demonstra efeito do formato.",
        ],
        interpretations=[
            "Pré-declarar critérios facilita rastrear a lógica do veredito na transcrição.",
            "Links comerciais e afirmações técnicas precisam de verificação separada.",
        ],
        scores={"gancho":92,"clareza":94,"relevancia":93,"desejo":84,"confianca":78,"retencao":"not_assessed","acao":86,"objecoes":88},
        lenses={
            "apressado":"Recebe período, produto, pergunta e critérios em menos de um minuto.",
            "analitico":"Vê estrutura extensa de critérios, mas precisa de medições reproduzíveis.",
            "aspiracional":"Longevidade e ecossistema são atraentes, condicionados ao preço.",
            "comunidade":"O criador promete ler dúvidas; o texto das respostas não foi acessado.",
            "cetico":"Desconta links comerciais e previsões futuras não verificadas.",
        },
        replicable=["Declarar o papel do produto e o período de uso.","Enumerar os critérios antes de avaliá-los.","Separar decisão por preço e cenário de uso."],
        contingent=["Autonomia, câmeras, desempenho e longevidade foram apenas declarados.","Links comerciais podem afetar independência percebida.","Sem audiovisual, comentários amostrados, retenção ou baseline."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"período e critérios são pré-declarados","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"preço e perfil de uso condicionam o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260915-159",
        title="30 DIAS com JBL WAVE FLEX valeu A PENA?",
        creator="lando pereira", identity="lando-pereira",
        url="https://www.youtube.com/watch?v=bImdLYifLvE",
        published="2024-04-04", duration="PT4M25S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "6.950 visualizações, 112 curtidas e 35 comentários declarados nos metadados públicos",
            "período de 30 dias no título e na descrição", "uso cotidiano falado",
            "testes falados de conexão, distância, bateria e quedas", "veredito universal falado",
            "link comercial na descrição e no fechamento",
        ],
        missing=MISSING_AV + ["texto dos comentários", "disclosure de afiliado", "verificação visual dos testes", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":6950,"likesObserved":112,"commentsObserved":35},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="demonstracao",
            secondary=["autoridade_opiniao","comparacao"],
            mix=[{"family":"demonstracao","percentage":45},{"family":"autoridade_opiniao","percentage":35},{"family":"comparacao","percentage":20}],
            objectives=["apresentar_solucao","venda","confianca"],
            topic="review pós-uso do JBL Wave Flex", segment="tecnologia de consumo",
            subsegment="fones Bluetooth", audience="pessoas considerando fone Bluetooth de uso cotidiano",
            production="simple", scale="small", replicability="high",
            mechanisms=["utilidade_pratica","confianca","recompensa"], hooks=["numero","pergunta"],
            narrative=["situacao","prova","conclusao"], proof=["depoimento","demonstracao"], cta=["clicar","comprar"],
            evidence=[
                "A fala descreve uso diário e testes de conexão, alcance, bateria e quedas.",
                "O fechamento recomenda a compra de modo universal e promete ausência de arrependimento.",
                "Não aparecem perfil excluído, trade-off relevante ou condição de compra na transcrição.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso com período e critérios, mas sem veredito condicionado ao perfil","referenceIds":["obs-20260915-156","obs-20260915-158"],"confidence":"high"},
        observations=[
            "Há período, uso e critérios concretos antes do fechamento.",
            "O veredito final é universal e não explicita para quem o produto deixa de valer.",
            "A ausência de trade-off delimita o padrão, mas não prova menor utilidade ou desempenho.",
        ],
        interpretations=[
            "Critérios, sozinhos, não equivalem a uma recomendação condicionada.",
            "Sem teste com público, o caso é limite estrutural, não contraexemplo causal.",
        ],
        scores={"gancho":80,"clareza":86,"relevancia":87,"desejo":83,"confianca":67,"retencao":"not_assessed","acao":83,"objecoes":56},
        lenses={
            "apressado":"Entende produto e promessa de experiência rapidamente.",
            "analitico":"Recebe vários testes falados, mas quase nenhuma condição ou ressalva.",
            "aspiracional":"A conveniência é reforçada por conexão e bateria.",
            "comunidade":"Comentários existem, porém não foram amostrados.",
            "cetico":"Rejeita a promessa universal de ausência de arrependimento e pede auditoria dos testes.",
        },
        replicable=["Organizar a experiência por testes concretos.","Mostrar critérios antes da conclusão."],
        contingent=["Não copiar o veredito universal ou promessa de não arrependimento.","Testes foram apenas descritos na transcrição.","Sem audiovisual, comentários amostrados, retenção ou baseline."],
        role="case_limit", evidence_level=1, eligible=False,
        claims=[
            {"claim":"período e critérios precedem o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"veredito é condicionado ao perfil","requiredModalities":["transcript","profile_condition"],"observedModalities":["transcript"],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260915-160",
        title="PÃO só CAI com MANTEIGA VIRADA para BAIXO? Nós testamos",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=hw0u2ZcQaNM",
        published="2022-02-17", duration="PT11M03S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "1.991.172 visualizações, 130.780 curtidas e 2.200 comentários declarados nos metadados públicos",
            "pergunta, hipótese popular, procedimento, controle tardio, resultados e variáveis na transcrição",
            "conclusão falada sobre manteiga, borda da mesa e velocidade do impulso",
        ],
        missing=MISSING_AV + ["texto dos comentários", "contagens auditadas quadro a quadro", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":1991172,"likesObserved":130780,"commentsObserved":2200},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="demonstracao",
            secondary=["educativo","humor"],
            mix=[{"family":"demonstracao","percentage":60},{"family":"educativo","percentage":30},{"family":"humor","percentage":10}],
            objectives=["educar","visualizacao","comentario"],
            topic="teste experimental da queda do pão com manteiga", segment="divulgação científica",
            subsegment="física cotidiana", audience="público geral interessado em experiências e mitos cotidianos",
            awareness="consciente_problema", production="intermediate", scale="large", replicability="medium",
            mechanisms=["curiosidade","recompensa","confianca","surpresa"],
            hooks=["pergunta","afirmacao_contraintuitiva","problema"], narrative=["situacao","promessa","prova","problema","conclusao"],
            proof=["demonstracao","dado"], cta=["outro_conteudo","comentar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"nenhuma","confidence":"high"},
            evidence=[
                "A abertura formula a crença popular e anuncia um teste.",
                "A transcrição preserva resultados instáveis e a constatação de que faltava um controle sem manteiga.",
                "A conclusão relaciona resultados à borda da mesa e à velocidade do impulso, não à manteiga.",
                "Contagens e cenas não foram verificadas visualmente.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de demonstração científica; fora do grupo de reviews pós-uso","referenceIds":[],"confidence":"high"},
        observations=[
            "A pergunta é testada em condições que mudam ao longo da investigação.",
            "O controle sem manteiga é reconhecido como necessário depois dos primeiros resultados.",
            "A fala liga as diferenças à borda da mesa e à intensidade do impulso.",
        ],
        interpretations=[
            "Registrar uma lacuna de controle dentro do conteúdo pode converter erro de procedimento em explicação.",
            "É uma observação de exploração e não altera a contagem do padrão-alvo de reviews.",
        ],
        scores={"gancho":91,"clareza":90,"relevancia":84,"desejo":79,"confianca":85,"retencao":"not_assessed","acao":74,"objecoes":88},
        lenses={
            "apressado":"Identifica pergunta e teste logo na abertura.",
            "analitico":"Valoriza controle e variáveis, mas pede contagens visualmente auditadas.",
            "aspiracional":"A investigação cotidiana torna ciência acessível.",
            "comunidade":"Há convite a outros testes; comentários não foram amostrados.",
            "cetico":"Aceita somente a estrutura transcrita e não as cenas ou contagens não auditadas.",
        },
        replicable=["Começar por uma crença testável.","Reconhecer controle ausente e corrigi-lo.","Relacionar resultado às variáveis realmente modificadas."],
        contingent=["Não ensinar a máquina, as cenas ou as contagens sem auditoria audiovisual.","Mesmo criador já aparece em apoios do padrão experimental existente.","Popularidade não prova compreensão ou retenção."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"pergunta, controle, variáveis e conclusão aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"contagens e resultados visuais foram confirmados","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
        comment_provenance=False,
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 028")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260915-156", "obs-20260915-157", "obs-20260915-158"]
new_case = "obs-20260915-159"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 6
pattern["supportingCount"] = 6
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260915-156","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Mais de 30 dias, recursos desejados versus usados e um veredito que recomenda pagar menos quando o perfil não precisa deles.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["sem audiovisual ou comentários amostrados","links comerciais com disclosure incompleto"]},
    {"referenceId":"obs-20260915-157","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Trinta dias, suporte, integrações, relatórios e falhas precedem recomendação condicionada ao mercado e à plataforma de origem.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["painéis e valores não verificados","link de afiliado e oferta de mentoria"]},
    {"referenceId":"obs-20260915-158","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Trinta dias como aparelho principal e critérios pré-declarados antecedem recomendação por preço e autonomia por perfil de uso.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["sem verificação dos testes","links comerciais com disclosure incompleto"]},
    {"referenceId":"obs-20260915-159","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"Período e testes concretos aparecem, mas a conclusão é universal e não explicita perfil excluído ou trade-off.","evidence":"Metadados, descrição e transcrição automática integral.","limitations":["não é contraexemplo causal porque utilidade e desempenho não foram medidos"]},
])
pattern["limitations"] = [
    "Seis apoios formais vêm de seis criadores e seis fontes independentes; demonstram recorrência estrutural, não eficácia.",
    "Os produtos e mercados diferem; a comparação é funcional e não autoriza benchmark numérico.",
    "Nenhum audiovisual, áudio ouvido, capa, texto na tela, edição, ritmo ou retenção foi auditado.",
    "Três apoios novos contêm links comerciais; patrocínio, afiliação e independência editorial não são equivalentes.",
    "Os dois casos-limite mostram que declarar uso ou critérios não basta quando o veredito não é condicionado ao perfil ou antecede a avaliação.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("cMgusFeuoPA", "review de fone com maior sobreposição temática; diversidade inferior ao lote selecionado"),
        ("sZ-uR6auMAc", "ferramenta de IA com possível sobreposição comercial e menor isolamento do cenário de uso"),
        ("wXpRobocl38", "review maker longo; menor diversidade que a exploração científica escolhida"),
        ("FOKPdbCsG8Y", "serviço de IPTV sem procedência verificável; risco de ensinar oferta potencialmente irregular"),
        ("PNxnC8ORrXo", "URL já presente em triagem histórica da memória"),
        ("mrsMuQbNlzM", "suplemento ingerível; risco de confundir experiência com alegação de saúde"),
        ("i74CDqkgEyU", "mesmo criador de candidato histórico e cobertura redundante"),
        ("rqTDNjkk3CM", "wearable semelhante ao apoio selecionado e menor ganho de diversidade"),
        ("WCte68_K-o0", "mesmo canal de vários candidatos recentes; diversidade de fonte inferior"),
        ("OFEqgXFEaPM", "demonstração visual cuja entrega não pôde ser auditada; exploração escolhida oferece variáveis faladas mais claras"),
        ("YzFGVZyAXKo", "experimento com fogo e maior risco operacional; menor replicabilidade"),
        ("3ZBUo_89MMQ", "experimento com micro-ondas e metal; maior risco e produção mais complexa"),
        ("f63_8FwXLLk", "narrativa histórica de acidente; família menos alinhada ao teste controlado escolhido"),
        ("U57YwQpQ-2A", "candidato de demonstração com cobertura inferior à exploração selecionada"),
        ("H09Kp9TPDIs", "candidato de demonstração redundante para este lote"),
        ("8Z6vRkY8yKc", "candidato de demonstração redundante para este lote"),
        ("gIsb1jGQXcQ", "candidato de demonstração redundante para este lote"),
        ("alzph3wPh1Y", "candidato de demonstração redundante para este lote"),
        ("ryeD8bkUj5M", "candidato de demonstração redundante para este lote"),
        ("Cw5fwkqnM-g", "publicação indisponível na verificação pública"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 25,
    "referenceIds": [f"obs-20260915-{n}" for n in range(156, 161)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260915-160"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["comparacao","autoridade_opiniao","demonstracao","educativo","humor"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads não ofereceram formato utilizável e requisições de capa expiraram por timeout","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullAutomatic":5,"partialAutomatic":0,"none":0,"limitation":"transcrições automáticas substituem apenas fala e podem conter erros"},
    "commentsCoverage": {"countsOnly":3,"sampledReferences":2,"sampledComments":17,"limitation":"foram amostrados 3 de 5 comentários no Amazfit e 14 de 37 no iPhone; os demais tiveram somente contagens públicas"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"produtos, idades, durações e escalas heterogêneos impedem benchmark de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["período e critérios não bastam quando a conclusão promete adequação universal e não explicita perfil excluído ou trade-off"],
    "safetyFindings": ["alegações técnicas, financeiras e de segurança foram registradas como falas não verificadas","nenhum comentário ou dado pessoal foi reproduzido"],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três novos criadores brasileiros sustentam a recorrência de período, cenário e critérios antes de um veredito condicionado. O padrão passa a seis apoios independentes, permanece provisório e não demonstra confiança, retenção ou conversão.",
    "nextTarget": "review brasileiro curto com audiovisual integral, disclosure explícito de patrocínio ou afiliação e teste de compreensão; procurar caso em que critérios contradigam o veredito ou em que públicos diferentes interpretem incorretamente para quem a recomendação vale",
    "limitations": ["Nenhum audiovisual, áudio ou capa foi adquirido.","As 17 amostras de comentários não são representativas; retenção, teste de compreensão, conversão e baseline homogêneo seguem ausentes.","Alegações de produto e resultados comerciais não foram verificadas independentemente.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
