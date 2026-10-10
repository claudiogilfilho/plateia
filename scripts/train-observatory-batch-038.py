#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-037.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-24T11:23:26.000Z"
OBSERVED = "2026-09-24"
RUN_ID = "run-20260924-supervised-038"
PATTERN_ID = "pat-20260828-006"
BATCH_IDS = {f"obs-20260924-{n}" for n in range(206, 211)}

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
              has_comments=True, has_transcript=True):
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
        "storyOrigin": "conteúdo editorial público do próprio criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado identificável de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, personagens, imagens ou roteiro",
        "converter correção histórica em certeza sem fontes acessíveis e revisão factual",
        "tratar popularidade, comentário, marca, oferta ou orçamento como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
        "confundir recorrência estrutural com compreensão, precisão histórica ou desempenho",
    ]
    if not has_transcript:
        item["provenance"] = [p for p in item["provenance"] if p != "youtube_automatic_transcript"]
    return item


GROUP = "vídeo educativo brasileiro de história que explicita uma versão familiar, apresenta correção delimitada e nomeia fontes ou qualifica proporcionalmente a alegação"

refs = [
    build_ref(
        id="obs-20260924-206",
        title="5 COISAS QUE VOCÊ APRENDEU ERRADO SOBRE O DESCOBRIMENTO DO BRASIL",
        creator="Rabiscos da História", identity="rabiscos-da-historia",
        url="https://www.youtube.com/watch?v=lhr_giMqIXo",
        published="2026-08-21", duration="PT17M51S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata no microformato público", "duração de 17 minutos e 51 segundos",
            "transcrição automática integral em português com 409 segmentos e timestamps", "fala por substituição textual",
            "781 visualizações e 9 curtidas observadas", "amostra integral dos 2 comentários públicos retornados",
            "versão escolar familiar e cinco correções delimitadas na descrição e na fala",
            "qualificação explícita entre hipótese, evidência e exagero sobre a rota de Cabral",
            "Carta de Pero Vaz de Caminha nomeada como fonte e limitada aos primeiros contatos",
        ],
        missing=MISSING_AV + ["revisão factual humana", "bibliografia completa", "baseline comparável", "teste de compreensão"],
        metrics={"viewsObserved":781,"likesObserved":9,"commentsObserved":2},
        classification=cls(
            presentations=["narracao_imagens","comentario"], primary="storytelling",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"storytelling","percentage":45},{"family":"educativo","percentage":35},{"family":"curiosidade","percentage":20}],
            objectives=["educar","visualizacao","comentario","compartilhamento"],
            topic="simplificações sobre a chegada portuguesa em 1500", segment="história",
            subsegment="história do Brasil colonial", audience="público geral interessado em história do Brasil",
            awareness="consciente_problema", production="simple", scale="small", replicability="high",
            duration="over_60s", mechanisms=["curiosidade","contraste","confianca"],
            hooks=["pergunta","afirmacao_contraintuitiva","numero"], narrative=["situacao","problema","progressao","prova","conclusao"],
            proof=["evidencia_documental","mecanismo_explicado"], cta=["comentar","seguir","compartilhar"],
            advertising="editorial_organico", intent="ausente", entity={"kind":"indeterminado","name":"","confidence":"low"},
            evidence=[
                "A abertura transcrita reconstrói a versão escolar do descobrimento e a chama de simples demais.",
                "Na discussão da rota, a fala separa hipótese de fato comprovado e evita afirmar intenção ou acidente como certeza.",
                "Na seção do primeiro contato, a Carta de Caminha é nomeada e seu alcance é limitado; dois comentários falam de música e velocidade, não de compreensão.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260924-207","obs-20260924-208"],"confidence":"high"},
        observations=[
            "A correção preserva a versão familiar como ponto de partida, mas evita dizer que ela é inteiramente falsa.",
            "A fala torna visível a incerteza sobre a rota e o limite documental da Carta de Caminha.",
            "Os comentários não medem compreensão, precisão ou retenção.",
        ],
        interpretations=[
            "Delimitar o que a fonte permite afirmar pode sustentar curiosidade sem trocar simplificação por certeza absoluta.",
            "A estrutura é recorrente; a exatidão histórica de cada afirmação ainda requer revisão especializada.",
        ],
        scores={"gancho":92,"clareza":94,"relevancia":89,"desejo":82,"confianca":86,"retencao":"not_assessed","acao":80,"objecoes":88},
        lenses={
            "apressado":"Recebe tema, conflito e lista na abertura.",
            "analitico":"Encontra distinção entre hipótese e evidência, mas precisa da bibliografia completa.",
            "aspiracional":"A promessa é rever uma memória escolar conhecida.",
            "comunidade":"O CTA pede qual ponto surpreendeu; dois comentários não testam entendimento.",
            "cetico":"Valoriza a qualificação e exige checagem histórica independente.",
        },
        replicable=["Começar pela versão que o público já reconhece.","Corrigir uma afirmação por vez.","Nomear a fonte e declarar o que ela não permite concluir."],
        contingent=["Transcrição automática pode conter erros.","Bibliografia completa não foi publicada.","Audiovisual e precisão histórica não foram auditados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"versão familiar, correções específicas e qualificação da incerteza aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"uma fonte histórica é nomeada e seu alcance é limitado","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_2_public_comments",
    ),
    build_ref(
        id="obs-20260924-207",
        title="15 Vezes Que a Escola Te Ensinou Uma Mentira Sobre o Brasil Colonial",
        creator="Relíquias Perdidas 937", identity="reliquias-perdidas-937",
        url="https://www.youtube.com/watch?v=gxoilg4NUqI",
        published="2026-09-10", duration="PT20M8S",
        accessible=[
            "título", "criador", "descrição pública integral com capítulos", "data exata", "duração de 20 minutos e 8 segundos",
            "transcrição automática integral em português com 429 segmentos e timestamps", "fala por substituição textual",
            "1.268 visualizações e 23 curtidas observadas", "amostra integral dos 2 comentários públicos retornados",
            "quinze versões familiares e correções enumeradas na fala",
            "fontes nomeadas na descrição: Slave Voyages, Pesquisa FAPESP, acervo Kahal Zur Israel e registros do Tratado de Methuen",
            "uso de imagens geradas por IA declarado na descrição, sem imagens adquiridas para auditoria",
        ],
        missing=MISSING_AV + ["links diretos para todas as fontes por afirmação", "revisão factual humana", "verificação das reconstruções de IA", "teste de compreensão"],
        metrics={"viewsObserved":1268,"likesObserved":23,"commentsObserved":2},
        classification=cls(
            presentations=["narracao_imagens","montagem","comentario"], primary="storytelling",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"storytelling","percentage":40},{"family":"educativo","percentage":40},{"family":"curiosidade","percentage":20}],
            objectives=["educar","visualizacao","comentario","seguidores"],
            topic="correções sobre o Brasil colonial", segment="história", subsegment="Brasil colonial",
            audience="público geral interessado em história do Brasil", awareness="consciente_problema",
            production="intermediate", scale="medium", replicability="medium", duration="over_60s",
            mechanisms=["curiosidade","contraste","surpresa","confianca"], hooks=["afirmacao_contraintuitiva","numero","promessa"],
            narrative=["situacao","problema","progressao","prova","conclusao"], proof=["evidencia_documental","dado","mecanismo_explicado"],
            cta=["comentar","seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"indeterminado","name":"","confidence":"low"},
            evidence=[
                "A abertura transcrita enumera versões escolares familiares e promete tratá-las com fontes documentadas.",
                "A descrição organiza quinze correções por capítulos e nomeia quatro conjuntos documentais ou historiográficos.",
                "A descrição declara imagens de IA; sua correspondência histórica não pôde ser vista nem verificada.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260924-206","obs-20260924-208"],"confidence":"medium"},
        observations=[
            "A enumeração mantém o contraste entre versão escolar e correção ao longo de quinze tópicos.",
            "A descrição torna parte da procedência rastreável, mas não liga cada afirmação a uma citação específica.",
            "A declaração de IA reduz ambiguidade sobre a origem das imagens, sem validar sua fidelidade.",
        ],
        interpretations=[
            "Capítulos e fontes nomeadas podem tornar um conjunto extenso navegável e parcialmente verificável.",
            "A escala de quinze alegações aumenta a necessidade de citação por item e revisão humana.",
        ],
        scores={"gancho":90,"clareza":91,"relevancia":88,"desejo":84,"confianca":76,"retencao":"not_assessed","acao":79,"objecoes":73},
        lenses={
            "apressado":"Recebe a tese e uma lista extensa logo na abertura.",
            "analitico":"Vê conjuntos de fontes, mas quer correspondência entre afirmação e citação.",
            "aspiracional":"A promessa é reconstruir uma visão mais complexa do período colonial.",
            "comunidade":"O CTA pede qual fato merece aprofundamento; dois comentários não formam teste.",
            "cetico":"Desconta hipérbole do título, imagens de IA e ausência de revisão independente.",
        },
        replicable=["Enumerar versões e correções com capítulos.","Publicar fontes consultadas e declarar mídia sintética.","Separar o que é simplificação do que seria falsidade completa."],
        contingent=["Fontes não estão ligadas individualmente às quinze alegações.","Imagens de IA não foram observadas.","Precisão histórica não foi revisada."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"versões familiares e correções específicas são organizadas na fala e nos capítulos","requiredModalities":["transcript","description"],"observedModalities":["transcript","description"],"sufficient":True},
            {"claim":"conjuntos de fontes são nomeados publicamente","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_2_public_comments",
    ),
    build_ref(
        id="obs-20260924-208",
        title='"Egito" é um nome muito errado',
        creator="Estranha História", identity="estranha-historia",
        url="https://www.youtube.com/watch?v=PlUUVgdoNh4",
        published="2026-01-13", duration="PT22M30S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 22 minutos e 30 segundos",
            "transcrição automática integral em português com 582 segmentos e timestamps", "fala por substituição textual",
            "242.984 visualizações e 19.098 curtidas observadas", "amostra pública de 50 comentários",
            "contradição sobre o nome Egito e explicação de Kemet, Masr e Misr na fala",
            "duas referências acadêmicas completas na descrição: Ian Shaw (2003) e Marc Van De Mieroop (2021)",
            "links afiliados, curso, associação e publicidade da Insider identificados na descrição",
        ],
        missing=MISSING_AV + ["revisão factual humana", "páginas específicas das obras citadas", "contagem pública total de comentários", "teste de compreensão"],
        metrics={"viewsObserved":242984,"likesObserved":19098,"commentsObserved":"not_measured"},
        classification=cls(
            presentations=["camera_direta","comentario","narracao_imagens"], primary="storytelling",
            secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"storytelling","percentage":40},{"family":"educativo","percentage":40},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","autoridade","visualizacao","venda"], topic="origem e transmissão dos nomes usados para o Egito",
            segment="história", subsegment="história antiga e historiografia", audience="público interessado em história antiga e arqueologia",
            awareness="consciente_problema", production="intermediate", scale="large", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","contraste","confianca"], hooks=["afirmacao_contraintuitiva","problema"],
            narrative=["problema","situacao","progressao","prova","conclusao"], proof=["fonte","mecanismo_explicado"],
            cta=["seguir","comprar"], advertising="publicidade_nativa", intent="explicita",
            entity={"kind":"marca","name":"Insider, curso, livros e clube de leitura","confidence":"high"},
            evidence=[
                "A abertura transcrita contradiz o nome familiar e apresenta Kemet, Masr e Misr como problema histórico.",
                "A fala explica a transmissão de nomes por tradições historiográficas e fontes greco-romanas.",
                "A descrição oferece duas referências acadêmicas completas; ofertas e escala foram tratadas apenas como contexto.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260924-206","obs-20260924-207"],"confidence":"high"},
        observations=[
            "Uma palavra cotidiana funciona como versão familiar antes da correção etimológica e historiográfica.",
            "A descrição fornece duas obras acadêmicas identificáveis, embora sem páginas por afirmação.",
            "Amostra de cinquenta comentários contém perguntas, pedidos e questões comerciais; não mede compreensão.",
        ],
        interpretations=[
            "Um objeto verbal específico pode concentrar a correção e reduzir a amplitude da promessa.",
            "Referências acadêmicas aumentam rastreabilidade, mas não substituem revisão factual nem teste de aprendizagem.",
        ],
        scores={"gancho":94,"clareza":93,"relevancia":87,"desejo":84,"confianca":90,"retencao":"not_assessed","acao":83,"objecoes":88},
        lenses={
            "apressado":"Entende a contradição específica pelo título e pela abertura.",
            "analitico":"Recebe mecanismo historiográfico e duas obras verificáveis.",
            "aspiracional":"A correção promete ler nomes históricos com mais precisão.",
            "comunidade":"Comentários trazem novas perguntas, não teste de aprendizagem.",
            "cetico":"Separa referências do bloco comercial e pede páginas ou revisão independente.",
        },
        replicable=["Escolher um termo familiar e formular uma contradição específica.","Explicar a cadeia histórica que produziu o termo.","Publicar referências acadêmicas completas separadas das ofertas."],
        contingent=["As obras citadas não foram conferidas página a página.","Ofertas comerciais coexistem com o conteúdo.","Audiovisual e retenção não foram observados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"termo familiar, correção delimitada e mecanismo historiográfico aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"duas referências acadêmicas identificáveis sustentam a pauta publicamente","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_50_public_comments",
    ),
    build_ref(
        id="obs-20260924-209",
        title="5 Mentiras que Você Aprendeu na Escola Sobre a História do Brasil",
        creator="Provando Historia", identity="provando-historia",
        url="https://www.youtube.com/watch?v=uZpU0HBuovE",
        published="2025-07-31", duration="PT5M19S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 5 minutos e 19 segundos",
            "transcrição automática integral em português com 119 segmentos e timestamps", "fala por substituição textual",
            "623 visualizações, 4 curtidas e zero comentários retornados",
            "cinco versões familiares e correções na fala",
            "menção genérica a autores, documentos e cartas, sem obras, autores, arquivos ou links identificáveis",
        ],
        missing=MISSING_AV + ["fontes identificáveis para as cinco alegações", "revisão factual humana", "comentários públicos", "teste de compreensão"],
        metrics={"viewsObserved":623,"likesObserved":4,"commentsObserved":0},
        classification=cls(
            presentations=["narracao_imagens","comentario"], primary="storytelling",
            secondary=["polemica","educativo"],
            mix=[{"family":"storytelling","percentage":40},{"family":"polemica","percentage":35},{"family":"educativo","percentage":25}],
            objectives=["educar","visualizacao","compartilhamento","comentario"], topic="cinco correções amplas sobre a história do Brasil",
            segment="história", subsegment="história política e social do Brasil", audience="público geral atraído por revisão da história escolar",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","indignacao","contraste"], hooks=["afirmacao_contraintuitiva","numero","conflito"],
            narrative=["problema","progressao","conclusao"], proof=["alegacao_sem_prova","mecanismo_explicado"], cta=["comentar","seguir","compartilhar"],
            advertising="editorial_organico", intent="ausente", entity={"kind":"indeterminado","name":"","confidence":"low"},
            evidence=[
                "A abertura promete desmentir o que o público acreditou e atribui omissão à escola.",
                "A fala cobre independência, abolição, chegada portuguesa, conflitos e ditadura em cinco minutos.",
                "As fontes aparecem apenas como categorias genéricas; não há identificação pública suficiente para rastrear as correções.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260924-206","obs-20260924-207","obs-20260924-208"],"confidence":"high"},
        observations=[
            "A versão familiar e a correção são reconhecíveis, mas a formulação usa mentira, farsa, manipulação e verdade sem sustentação proporcional acessível.",
            "Cinco temas historicamente amplos são comprimidos sem uma trilha pública de fontes.",
            "O caso delimita que contraste e especificidade não bastam quando a prova fica genérica.",
        ],
        interpretations=[
            "Este é caso-limite de embalagem corretiva: o mecanismo estrutural aparece, mas a condição de rastreabilidade não.",
            "A ausência de fontes acessíveis não prova que as afirmações são falsas; torna sua sustentação não mensurada.",
        ],
        scores={"gancho":91,"clareza":84,"relevancia":85,"desejo":79,"confianca":38,"retencao":"not_assessed","acao":72,"objecoes":41},
        lenses={
            "apressado":"Entende rapidamente a promessa de cinco correções.",
            "analitico":"Não encontra autores, obras ou documentos rastreáveis.",
            "aspiracional":"A promessa de verdade oculta pode atrair, sem garantir precisão.",
            "comunidade":"O CTA pede choque, mas zero comentários foram retornados.",
            "cetico":"Rejeita certeza ampla sem fonte identificável e revisão independente.",
        },
        replicable=["Delimitar o número de correções.","Partir de versões escolares reconhecíveis.","Separar uma alegação por bloco."],
        contingent=["Não há fontes identificáveis na descrição.","As correções cobrem períodos muito distintos.","Ausência de revisão não equivale a falsidade factual."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"versão familiar e correções específicas aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"as correções são qualificadas e sustentadas por fontes rastreáveis","requiredModalities":["transcript","description","source_list"],"observedModalities":["transcript","description"],"sufficient":False},
            {"claim":"as alegações são verdadeiras ou falsas","requiredModalities":["expert_review","primary_sources"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_zero_returned_comments",
        has_comments=False,
    ),
    build_ref(
        id="obs-20260924-210",
        title="POR QUE o CENTRO da TERRA é tão QUENTE?",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=q53mI5lhep4",
        published="2026-09-19", duration="PT18M14S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 18 minutos e 14 segundos",
            "545.328 visualizações e 17.609 curtidas observadas", "amostra pública de 50 comentários",
            "pergunta científica literal, tópicos de crosta, manto, núcleo e sismologia descritos",
            "experimento com marreta e câmera térmica declarado na descrição, sem procedimento ou resultado visual observado",
            "créditos públicos de roteiro, conteúdo, produção, fotografia, edição e arte",
        ],
        missing=MISSING_AV + ["transcrição ou legenda", "fala", "procedimento do experimento", "resultado do experimento", "fontes científicas", "contagem pública total de comentários", "teste de compreensão"],
        metrics={"viewsObserved":545328,"likesObserved":17609,"commentsObserved":"not_measured"},
        classification=cls(
            presentations=["demonstracao","camera_direta","narracao_imagens"], primary="explicativo",
            secondary=["demonstracao","curiosidade"],
            mix=[{"family":"explicativo","percentage":45},{"family":"demonstracao","percentage":35},{"family":"curiosidade","percentage":20}],
            objectives=["educar","visualizacao","autoridade","seguidores"], topic="origem e função do calor interno da Terra",
            segment="ciência", subsegment="geologia e física da Terra", audience="público geral e estudantes interessados em ciência",
            awareness="consciente_problema", production="complex", scale="large", replicability="medium", duration="over_60s",
            mechanisms=["curiosidade","surpresa","confianca"], hooks=["pergunta"],
            narrative=["problema","promessa","progressao"], proof=["demonstracao","autoridade_percebida"], cta=["seguir","comprar"],
            advertising="publicidade_nativa", intent="implicita", entity={"kind":"marca","name":"livros e associação do canal","confidence":"high"},
            confidence="medium",
            evidence=[
                "Título e descrição delimitam a pergunta sobre o calor interno da Terra.",
                "A descrição declara um experimento com marreta e câmera térmica, mas mídia e transcrição não ficaram acessíveis.",
                "Cinquenta comentários públicos foram amostrados; reações e perguntas não medem compreensão nem precisão.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de explicação científica com demonstração declarada","referenceIds":[],"confidence":"low"},
        observations=[
            "A embalagem combina pergunta literal, fenômeno específico e experimento declarado.",
            "Somente descrição e metadados sustentam a análise; a demonstração e o resultado não foram ensinados.",
            "Escala, curtidas e comentários são contexto, não evidência do mecanismo nem da compreensão.",
        ],
        interpretations=[
            "A referência preserva diversidade do lote, mas não gera hipótese sem acesso ao conteúdo corporal.",
            "Uma pergunta científica específica pode ser triada pela embalagem; a entrega exige audiovisual ou transcrição.",
        ],
        scores={"gancho":91,"clareza":88,"relevancia":86,"desejo":84,"confianca":"not_assessed","retencao":"not_assessed","acao":70,"objecoes":"not_assessed"},
        lenses={
            "apressado":"Entende imediatamente a pergunta científica.",
            "analitico":"Precisa de fontes, transcrição e resultado do experimento.",
            "aspiracional":"A promessa é compreender uma região inacessível do planeta.",
            "comunidade":"Comentários trazem perguntas e reações, sem teste de aprendizagem.",
            "cetico":"Não aceita o experimento ou a explicação sem observar a execução.",
        },
        replicable=["Formular uma pergunta literal sobre um fenômeno.","Antecipar o caminho explicativo sem prometer conclusão já provada.","Declarar créditos e recursos de produção."],
        contingent=["Experimento, cenas, fala e resultado não foram acessados.","Produção em equipe e câmera térmica elevam recursos necessários.","Nenhuma precisão científica foi verificada."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a embalagem delimita uma pergunta científica e promete explicação","requiredModalities":["metadata","description"],"observedModalities":["metadata","description"],"sufficient":True},
            {"claim":"o experimento demonstra o mecanismo ou o resultado","requiredModalities":["video","audio_or_transcript"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_no_transcript_and_50_public_comments",
        has_transcript=False,
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 038")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260924-206", "obs-20260924-207", "obs-20260924-208"]
new_case = "obs-20260924-209"
pattern["statement"] = "Em storytelling educativo de história, começar por uma versão familiar e apresentar uma correção ou contradição específica pode tornar o assunto claro e abrir uma lacuna de conhecimento, desde que a correção seja delimitada, proporcional à evidência e sustentada por fontes rastreáveis."
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 7
pattern["supportingCount"] = 7
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 7
pattern["sourceDiversityCount"] = 7
pattern["conditions"] = [
    "storytelling educativo de história",
    "narrativa familiar explicitada",
    "correção específica sem ocultar o assunto",
    "fontes rastreáveis ou qualificação proporcional à alegação",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260924-206","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"A versão escolar é seguida por cinco correções; a fala separa hipótese de fato e limita o alcance da Carta de Caminha.","evidence":"Metadados, descrição integral, transcrição automática integral e dois comentários.","limitations":["sem audiovisual, bibliografia completa ou revisão factual"]},
    {"referenceId":"obs-20260924-207","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Quinze versões familiares são contrapostas a correções, com capítulos e conjuntos de fontes nomeados publicamente.","evidence":"Metadados, descrição integral, transcrição automática integral e dois comentários.","limitations":["sem mapeamento de fonte por alegação, auditoria das imagens de IA ou revisão factual"]},
    {"referenceId":"obs-20260924-208","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"O termo familiar Egito abre uma correção etimológica e historiográfica apoiada por duas referências acadêmicas completas na descrição.","evidence":"Metadados, descrição integral, transcrição automática integral e cinquenta comentários.","limitations":["sem páginas específicas, audiovisual ou revisão factual"]},
    {"referenceId":"obs-20260924-209","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Versões e correções são reconhecíveis, mas mentira, farsa e verdade são afirmadas sem fontes identificáveis publicamente.","evidence":"Metadados, descrição integral, transcrição automática integral e zero comentários retornados.","limitations":["não conta como apoio nem como contraexemplo factual"]},
])
pattern["limitations"] = [
    "Cobertura ainda predominantemente textual; nenhum apoio teve audiovisual integral auditado.",
    "Fontes nomeadas variam de um documento ou livro a conjuntos amplos sem página por alegação.",
    "Nenhuma correção histórica recebeu revisão humana especializada neste lote.",
    "Os formatos, durações, temas e escalas variam.",
    "O padrão descreve clareza, contraste e rastreabilidade; não prova compreensão, precisão, retenção ou persuasão.",
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 111,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260924-210"],
    "discarded": [
        {"url":"https://www.youtube.com/watch?v=TPKeY_MrBto","reason":"descrição útil e artigo ligado, mas nenhuma transcrição pública; redundante após três apoios com fala integral"},
        {"url":"https://www.youtube.com/watch?v=laceIONtuZI","reason":"correções em formato de ranking, porém procedência pública menos rastreável que os três apoios escolhidos"},
        {"url":"https://www.youtube.com/watch?v=X_-ZpqBO1jg","reason":"transcrição integral, mas alegações amplas e sem fontes identificáveis; redundante com o caso-limite selecionado"},
        {"url":"https://www.youtube.com/watch?v=RktnI1EFbDE","reason":"fonte não listada na descrição e menor rastreabilidade que o apoio de história antiga selecionado"},
    ],
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["storytelling","educativo","curiosidade","polemica","autoridade_opiniao","explicativo","demonstracao"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "para as cinco URLs, sondagens dos streams retornaram HTTP 206 com HTML de 195 bytes e sondagens das capas retornaram HTTP 200 com o mesmo HTML de indisponibilidade; o storyboard também continha apenas respostas de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":4,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":1,
        "limitation":"quatro transcrições automáticas substituem somente a fala; a exploração científica ficou restrita a descrição e metadados após bloqueio temporário da legenda",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":4,
        "sampledComments":104,
        "zeroReturnedReferences":1,
        "limitation":"amostras públicas de comentários não são representativas nem teste de compreensão, precisão ou retenção",
    },
    "baselineCoverage": {
        "sampledProfiles":0,
        "contemporaneousBaselines":0,
        "limitation":"datas, durações, temas, produções e escalas diferentes impedem benchmark causal de desempenho",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["chamar uma versão de mentira ou farsa e oferecer correções específicas não satisfaz o padrão quando as fontes permanecem genéricas e não rastreáveis"],
    "safetyFindings": [
        "precisão histórica não foi inferida da confiança narrativa, de métricas ou da fama do canal",
        "ofertas, publicidade, IA declarada, escala e comentários permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, edição, ritmo, retenção, frase ou roteiro foi inventado",
        "a exploração sem transcrição não foi tratada como demonstração observada",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes ampliam de quatro para sete os apoios do padrão de versão histórica familiar seguida de correção rastreável. Um caso-limite mostra que contraste e especificidade não compensam fontes genéricas. O padrão permanece provisório e não demonstra precisão, compreensão, retenção ou desempenho.",
    "nextTarget": "vídeo histórico brasileiro curto, de criador pequeno ou médio, com audiovisual integral, correção única, fonte primária ligada à afirmação e teste de compreensão; buscar também um caso em que a fonte citada contradiga ou não sustente a correção",
    "limitations": [
        "Nenhum vídeo, áudio, capa ou storyboard utilizável foi adquirido.",
        "Quatro transcrições são automáticas integrais; uma referência ficou sem transcrição.",
        "Foram amostrados 104 comentários; a amostra não é representativa.",
        "A correspondência entre cada correção e suas fontes não foi completa em dois dos três apoios.",
        "Não houve baseline, retenção, teste de compreensão, revisão factual humana ou causalidade.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
