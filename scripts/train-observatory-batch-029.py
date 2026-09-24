#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Reuse the schema-compatible builders and reconstruct all earlier batches first.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-028.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
classification = ns["classification"]
make_ref = ns["make_ref"]

NOW = "2026-09-16T11:13:18.000Z"
OBSERVED = "2026-09-16"
RUN_ID = "run-20260916-supervised-029"
PATTERN_ID = "pat-20260914-014"
BATCH_IDS = {f"obs-20260916-{n}" for n in range(161, 166)}

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
        "storyOrigin": "experiência própria declarada ou produção editorial pública do criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, personagens ou roteiro",
        "tratar popularidade, link comercial, fama ou orçamento como prova causal",
        "aceitar alegações técnicas, de saúde, segurança ou custo sem verificação independente",
        "inferir cenas, áudio, texto na tela, edição, ritmo ou retenção",
    ]
    return item


refs = [
    ref(
        id="obs-20260916-161",
        title="Acer Nitro V15 depois de 6 MESES: o que PIOROU e o que me SURPREENDEU?",
        creator="Escolha Certa", identity="escolha-certa",
        url="https://www.youtube.com/watch?v=I9QIATQjDOY",
        published="2026-09-13", duration="PT13M56S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "9.992 visualizações, 162 curtidas e 10 comentários declarados nos metadados públicos",
            "amostra pública de 7 comentários, sem inferência de representatividade",
            "período de seis meses, compra com dinheiro próprio e ausência de patrocínio declarados na fala",
            "critérios falados de tela, desempenho, memória, mobilidade, sistema, preço e cenários de uso",
            "veredito falado com perfis indicados, perfis excluídos e limiar de preço",
            "links comerciais e indicações do YouTube Shopping na descrição e na fala",
        ],
        missing=MISSING_AV + ["3 comentários não adquiridos", "disclosure do caráter afiliado dos links", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":9992,"likesObserved":162,"commentsObserved":10},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="comparacao",
            secondary=["autoridade_opiniao","educativo"],
            mix=[{"family":"comparacao","percentage":50},{"family":"autoridade_opiniao","percentage":30},{"family":"educativo","percentage":20}],
            objectives=["educar","apresentar_solucao","confianca","venda"],
            topic="review pós-uso do Acer Nitro V15", segment="tecnologia de consumo",
            subsegment="notebooks gamers", audience="pessoas comparando notebooks para jogos, trabalho ou faculdade",
            mechanisms=["confianca","vigilancia","utilidade_pratica","recompensa"],
            hooks=["pergunta","problema","numero"], narrative=["situacao","promessa","prova","conclusao"],
            proof=["depoimento","tratamento_objecao"], cta=["clicar","comprar"],
            evidence=[
                "Entre 0:00 e 1:13, a fala declara seis meses, compra própria, ausência de patrocínio e positivos e negativos.",
                "Entre 12:09 e 13:06, o veredito separa jogos em Full HD, trabalho e faculdade de colorização, 1440p no ultra e instalação de Windows.",
                "O fechamento ainda condiciona a compra a aproximadamente R$ 7.500 e manda comparar alternativas acima disso.",
                "Amostra de sete comentários contém principalmente preço, configuração e elogio; não mede compreensão.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260916-162","obs-20260916-163"],"confidence":"high"},
        observations=[
            "O período e a independência declarada aparecem antes dos critérios.",
            "O fechamento nomeia usos adequados, inadequados e um limite de preço.",
            "A venda por links permanece contexto comercial, não prova da recomendação.",
        ],
        interpretations=[
            "A recomendação é rastreável porque critérios e perfis excluídos precedem o CTA comercial.",
            "A recorrência estrutural não demonstra confiança, retenção ou conversão.",
        ],
        scores={"gancho":93,"clareza":95,"relevancia":94,"desejo":82,"confianca":82,"retencao":"not_assessed","acao":87,"objecoes":94},
        lenses={
            "apressado":"Recebe produto, período, risco de arrependimento e promessa de prós e contras nos primeiros segundos.",
            "analitico":"Consegue seguir critérios e perfis, mas precisa verificar medições e faixa de preço.",
            "aspiracional":"Desempenho e mobilidade são atraentes, sem apagar limitações de tela e sistema.",
            "comunidade":"Há poucos comentários públicos amostrados; eles não formam baseline.",
            "cetico":"Valoriza compra própria e perfis excluídos, mas desconta links comerciais e alegações não auditadas.",
        },
        replicable=["Declarar período, cenário e independência antes da análise.","Separar perfis indicados e excluídos.","Usar limiar de preço antes do CTA comercial."],
        contingent=["Testes e cenas não foram verificados visualmente.","Preço e especificações são temporais.","Métricas públicas não demonstram causalidade."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"período, cenário e critérios precedem a avaliação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"perfis indicados, excluídos e preço condicionam o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_comment_sample",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260916-162",
        title="HAVAL H6 GT após 6 meses: me arrependi ou compraria de novo?",
        creator="Wesley TestDrive", identity="wesley-testdrive",
        url="https://www.youtube.com/watch?v=CtOCGNLUP2s",
        published="2025-04-19", duration="PT18M29S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "314.570 visualizações, 12.393 curtidas e 775 comentários declarados nos metadados públicos",
            "amostra pública de 20 comentários, sem inferência de representatividade",
            "seis meses como proprietário e ausência de pagamento da marca declarados na fala",
            "doze critérios pré-declarados, incluindo compra, conforto, desempenho, consumo, manutenção, custos e negativos",
            "cenário doméstico com painéis solares e uso majoritariamente elétrico declarado",
            "veredito pessoal de recompra após os critérios",
        ],
        missing=MISSING_AV + ["755 comentários não adquiridos", "verificação de custos, garantias, consumo e desempenho", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":314570,"likesObserved":12393,"commentsObserved":775},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="autoridade_opiniao",
            secondary=["comparacao","educativo"],
            mix=[{"family":"autoridade_opiniao","percentage":45},{"family":"comparacao","percentage":40},{"family":"educativo","percentage":15}],
            objectives=["educar","confianca","apresentar_solucao"],
            topic="review pós-uso do Haval H6 GT", segment="automotivo",
            subsegment="SUV híbrido", audience="pessoas avaliando SUV híbrido e custos de uso",
            production="simple", scale="medium", replicability="high",
            mechanisms=["confianca","vigilancia","aproximacao","utilidade_pratica"],
            hooks=["numero","pergunta","problema"], narrative=["situacao","prova","progressao","conclusao"],
            proof=["depoimento","tratamento_objecao"], cta=["comentar","seguir"], advertising="editorial_organico", intent="ausente",
            evidence=[
                "Entre 0:00 e 0:52, a fala declara seis meses, ausência de pagamento da marca e doze critérios.",
                "Entre 0:58 e 1:19, painéis solares e uso predominantemente elétrico delimitam o cenário de custo.",
                "Entre 15:10 e 16:48, recompra, conforto, família, painéis e perfil do proprietário antecedem o veredito pessoal.",
                "Comentários amostrados incluem dúvidas sobre estrada, custo, confiabilidade e adequação sem carregamento; não são teste representativo.",
            ],
        ),
        comparison={"level":2,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260916-161","obs-20260916-163"],"confidence":"high"},
        observations=[
            "O cenário energético doméstico é declarado antes de consumo e custo.",
            "O veredito é de recompra para o próprio perfil e não apaga pontos negativos falados.",
            "A amostra de comentários explicita condições ausentes de alguns espectadores, como estrada e falta de carregamento.",
        ],
        interpretations=[
            "Contexto doméstico e familiar evita universalizar diretamente o custo percebido.",
            "A experiência de um proprietário não valida confiabilidade de longo prazo nem economia para terceiros.",
        ],
        scores={"gancho":90,"clareza":93,"relevancia":92,"desejo":86,"confianca":80,"retencao":"not_assessed","acao":76,"objecoes":91},
        lenses={
            "apressado":"Vê período, independência declarada e a lista de critérios no primeiro minuto.",
            "analitico":"Recebe cenário e critérios, mas não medições auditadas nem horizonte longo.",
            "aspiracional":"Conforto e desempenho aparecem como experiência pessoal, não garantia universal.",
            "comunidade":"As dúvidas públicas ampliam cenários; a amostra não representa a audiência.",
            "cetico":"Desconta custos, garantias e comparações não verificadas, além do período ainda curto para durabilidade.",
        },
        replicable=["Pré-declarar critérios de avaliação.","Expor infraestrutura e rotina que alteram custo.","Formular recompra como veredito pessoal após prós e contras."],
        contingent=["Custos, garantias e desempenho foram apenas declarados.","Seis meses não medem confiabilidade de longo prazo.","Comentários não provam desempenho do vídeo."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"período, cenário energético e critérios precedem o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o veredito é ligado ao perfil e à experiência do proprietário","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_comment_sample",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260916-163",
        title="COMPRAS NA SHOPEE NA VIDA REAL: Como estão após 6 meses de uso",
        creator="Bruna Leal", identity="bruna-leal",
        url="https://www.youtube.com/watch?v=NB9wFQDXPjs",
        published="2025-09-20", duration="PT19M26S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "1.319.758 visualizações, 53.238 curtidas e 1.800 comentários declarados nos metadados públicos",
            "amostra pública de 20 comentários, sem inferência de representatividade",
            "períodos de seis a onze meses, usos domésticos, funcionamento, desgaste e decisão de manter ou recomprar na fala",
            "lista de links de compra na descrição; natureza afiliada não confirmada",
        ],
        missing=MISSING_AV + ["1.780 comentários não adquiridos", "disclosure do caráter comercial dos links", "verificação visual de desgaste e funcionamento", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":1319758,"likesObserved":53238,"commentsObserved":1800},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="demonstracao",
            secondary=["autoridade_opiniao","comparacao"],
            mix=[{"family":"demonstracao","percentage":45},{"family":"autoridade_opiniao","percentage":35},{"family":"comparacao","percentage":20}],
            objectives=["educar","apresentar_solucao","venda","confianca"],
            topic="review pós-uso de compras domésticas da Shopee", segment="casa e consumo",
            subsegment="utensílios e pequenos eletrodomésticos", audience="pessoas avaliando compras domésticas de marketplace",
            production="simple", scale="medium", replicability="high",
            mechanisms=["utilidade_pratica","confianca","vigilancia","contraste"],
            hooks=["numero","problema","promessa"], narrative=["situacao","prova","progressao","conclusao"],
            proof=["depoimento","demonstracao","tratamento_objecao"], cta=["comentar","clicar","comprar"],
            evidence=[
                "Entre 0:18 e 1:04, a fala declara mais de seis meses, funcionamento atual e intenção de avaliar se cada compra valeu.",
                "Cada produto recebe contexto de uso e condição atual antes de um julgamento local.",
                "Entre 17:08 e 18:38, o ralo é avaliado por estética, vedação, ferrugem e limpeza; a criadora mantém o item, mas duvida da recompra.",
                "Amostra de vinte comentários acrescenta experiências divergentes com vários itens; isso mapeia objeções, não eficácia.",
            ],
        ),
        comparison={"level":2,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260916-161","obs-20260916-162"],"confidence":"high"},
        observations=[
            "Período e estado atual organizam uma revisão por produto.",
            "A decisão pode ser manter, recomprar, não recomprar ou permanecer em dúvida, conforme desgaste e rotina.",
            "Comentários públicos relatam resultados distintos; não substituem auditoria do produto nem do vídeo.",
        ],
        interpretations=[
            "Vereditos locais evitam transformar um marketplace ou uma categoria inteira em recomendação única.",
            "A diversidade de produtos reduz comparabilidade material, mas preserva a função editorial do review pós-uso.",
        ],
        scores={"gancho":88,"clareza":92,"relevancia":94,"desejo":80,"confianca":82,"retencao":"not_assessed","acao":84,"objecoes":93},
        lenses={
            "apressado":"Entende período, variedade e pergunta de funcionamento na abertura.",
            "analitico":"Recebe desgaste e uso por item, mas não medições padronizadas.",
            "aspiracional":"Organização e conveniência são equilibradas por falhas e manutenção.",
            "comunidade":"Experiências divergentes aparecem na amostra, sem representatividade.",
            "cetico":"Valoriza a dúvida de recompra, mas pede verificação visual e disclosure dos links.",
        },
        replicable=["Revisitar produtos após uso real.","Avaliar cada item com critérios adequados ao uso.","Preservar dúvidas e decisões negativas antes dos links de compra."],
        contingent=["Desgaste e funcionamento não foram vistos no vídeo.","Links podem ser comerciais, mas o disclosure não foi confirmado.","Escala de visualizações não prova causalidade."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"período, contexto e critérios locais precedem cada julgamento","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"manter ou recomprar é condicionado ao desgaste e à rotina","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_comment_sample",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260916-164",
        title="PULSE ELITE do PS5 após 6 MESES: Ainda Vale a Pena em 2025?",
        creator="Menezes_tech", identity="menezes-tech",
        url="https://www.youtube.com/watch?v=bntPO7fIs3U",
        published="2025-08-18", duration="PT11M55S",
        accessible=[
            "título", "criador", "descrição integral com capítulos declarados", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "18.495 visualizações, 697 curtidas e 166 comentários declarados nos metadados públicos",
            "amostra pública de 20 comentários, sem inferência de representatividade",
            "seis meses de uso diário, conforto, limpeza, áudio, bateria, conexões e cuidados declarados na fala",
            "veredito falado de compra universal", "links de compra na descrição e no fechamento",
        ],
        missing=MISSING_AV + ["146 comentários não adquiridos", "disclosure de afiliado", "verificação visual de desgaste, conectividade e material", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":18495,"likesObserved":697,"commentsObserved":166},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="comparacao",
            secondary=["autoridade_opiniao","demonstracao"],
            mix=[{"family":"comparacao","percentage":40},{"family":"autoridade_opiniao","percentage":40},{"family":"demonstracao","percentage":20}],
            objectives=["apresentar_solucao","venda","confianca"],
            topic="review pós-uso do headset Pulse Elite", segment="tecnologia de consumo",
            subsegment="headsets para jogos", audience="jogadores considerando um headset para PlayStation",
            production="simple", scale="small", replicability="high",
            mechanisms=["confianca","utilidade_pratica","recompensa"], hooks=["numero","pergunta"],
            narrative=["situacao","prova","conclusao"], proof=["depoimento","tratamento_objecao"], cta=["clicar","comprar","comentar"],
            evidence=[
                "A abertura declara seis meses, uso diário e critérios de conforto e funcionamento.",
                "Entre 9:37 e 11:08, cuidados de limpeza, conforto, áudio e conexões antecedem a conclusão.",
                "Entre 10:48 e 11:08, o fechamento diz a qualquer pessoa em dúvida que deve comprar, sem explicitar perfil excluído ou limiar de preço.",
                "Comentários amostrados relatam quebras, desconexões e devolução; são experiências não controladas e não provam desempenho relativo.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso com período e critérios, mas conclusão universal sem perfil excluído","referenceIds":["obs-20260916-161","obs-20260916-163"],"confidence":"high"},
        observations=[
            "O período e vários critérios concretos aparecem antes da conclusão.",
            "O veredito manda comprar de forma universal, apesar de cuidados especiais e preço não condicionado.",
            "A amostra pública contém experiências contrárias, mas não é um teste controlado nem um contraexemplo causal.",
        ],
        interpretations=[
            "Critérios e experiência própria não bastam quando a conclusão elimina perfis e condições de decisão.",
            "Divergência em comentários é sinal para investigar, não prova de que o formato falhou.",
        ],
        scores={"gancho":84,"clareza":88,"relevancia":88,"desejo":84,"confianca":67,"retencao":"not_assessed","acao":89,"objecoes":58},
        lenses={
            "apressado":"Entende período, produto e promessa de veredito rapidamente.",
            "analitico":"Recebe critérios, mas não uma condição clara de preço, uso ou perfil.",
            "aspiracional":"A ideia premium domina o fechamento, apesar de manutenção especial.",
            "comunidade":"Comentários públicos introduzem falhas e devoluções não contempladas pela recomendação universal.",
            "cetico":"Rejeita o salto de experiência pessoal para obrigação de compra e pede disclosure dos links.",
        },
        replicable=["Declarar período e rotina.","Organizar a avaliação por critérios concretos."],
        contingent=["Não copiar a recomendação universal.","Comentários divergentes não são evidência representativa.","Desgaste, áudio e conectividade não foram auditados."],
        role="case_limit", evidence_level=1, eligible=False,
        claims=[
            {"claim":"período e critérios precedem o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"veredito é condicionado a perfil, cenário ou preço","requiredModalities":["transcript","profile_condition"],"observedModalities":["transcript"],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_comment_sample",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260916-165",
        title="Uma Breve História (do Início) do Universo",
        creator="Ciência Todo Dia", identity="ciencia-todo-dia",
        url="https://www.youtube.com/watch?v=8UqNVzY0EVg",
        published="2022-10-05", duration="PT14M55S",
        accessible=[
            "título", "criador", "descrição integral", "data exata", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "1.731.564 visualizações, 117.839 curtidas e 2.600 comentários declarados nos metadados públicos",
            "amostra pública de 20 comentários, sem inferência de representatividade",
            "enquadramento inicial do conhecimento científico atual, limites declarados e progressão narrativa na fala",
            "link comercial para curso e convite a membros na descrição",
        ],
        missing=MISSING_AV + ["2.580 comentários não adquiridos", "fontes científicas declaradas na página do vídeo", "verificação independente das afirmações científicas", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":1731564,"likesObserved":117839,"commentsObserved":2600},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="educativo",
            secondary=["storytelling","autoridade_opiniao"],
            mix=[{"family":"educativo","percentage":55},{"family":"storytelling","percentage":35},{"family":"autoridade_opiniao","percentage":10}],
            objectives=["educar","visualizacao","confianca"],
            topic="história cosmológica do universo", segment="divulgação científica",
            subsegment="cosmologia", audience="público geral interessado em ciência e universo",
            awareness="inconsciente", production="intermediate", scale="large", replicability="medium",
            mechanisms=["curiosidade","confianca","recompensa","tensao"],
            hooks=["promessa","narrativo"], narrative=["situacao","promessa","progressao","conclusao"],
            proof=["mecanismo_explicado"], cta=["seguir","outro_conteudo"], advertising="publicidade_nativa", intent="implicita",
            entity={"kind":"servico","name":"curso e comunidade do canal","confidence":"medium"},
            evidence=[
                "Entre 0:24 e 0:36, a fala delimita o conteúdo ao melhor entendimento atual da física e admite mudança futura.",
                "Entre 1:09 e 1:44, a fala distingue o que não se sabe do que o modelo consegue explicar.",
                "A transcrição contém uma inconsistência automática entre milhões e bilhões; a descrição pública registra 13,8 bilhões, e nenhum número foi ensinado como fato pelo Observatório.",
                "Comentários amostrados incluem dúvidas, interpretações religiosas e pedidos de explicação; não medem compreensão.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de explicador científico; fora do grupo funcional de reviews pós-uso","referenceIds":[],"confidence":"high"},
        observations=[
            "A abertura apresenta o conhecimento como provisório e dependente do melhor modelo atual.",
            "Limites de explicação são preservados dentro da progressão narrativa.",
            "A transcrição automática é suficiente para observar o enquadramento verbal, não as cenas nem a precisão factual completa.",
        ],
        interpretations=[
            "Declarar fronteiras epistêmicas pode ser um mecanismo editorial transferível para explicadores.",
            "Uma referência isolada gera somente observação; não altera padrões nem cria hipótese formal neste lote.",
        ],
        scores={"gancho":91,"clareza":88,"relevancia":85,"desejo":78,"confianca":83,"retencao":"not_assessed","acao":67,"objecoes":89},
        lenses={
            "apressado":"Recebe viagem, escala e ressalva epistemológica no início.",
            "analitico":"Valoriza limites declarados, mas pede fontes e correção da transcrição.",
            "aspiracional":"A viagem cósmica cria escala sem substituir a ressalva científica.",
            "comunidade":"Comentários mostram dúvidas e visões divergentes, sem teste de compreensão.",
            "cetico":"Aceita apenas o enquadramento observado e não as afirmações científicas não verificadas.",
        },
        replicable=["Delimitar o que o modelo atual explica.","Nomear incertezas antes da progressão narrativa.","Separar observação, modelo e desconhecido."],
        contingent=["Não reutilizar afirmações científicas sem fontes primárias.","A transcrição automática contém erro numérico.","Popularidade não prova aprendizagem ou retenção."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"a fala delimita conhecimento atual e desconhecidos","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"cenas, visualizações e fatos científicos foram integralmente verificados","requiredModalities":["video","sources"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_full_automatic_transcript_and_comment_sample",
        comment_provenance=True,
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 029")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260916-161", "obs-20260916-162", "obs-20260916-163"]
new_case = "obs-20260916-164"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 9
pattern["supportingCount"] = 9
pattern["caseLimitCount"] = 3
pattern["creatorDiversityCount"] = 9
pattern["sourceDiversityCount"] = 9
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260916-161","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Seis meses, compra própria e critérios antecedem perfis indicados, excluídos e limiar de preço.","evidence":"Metadados, descrição, transcrição automática integral e sete comentários amostrados.","limitations":["sem audiovisual","links comerciais com disclosure de afiliação incompleto"]},
    {"referenceId":"obs-20260916-162","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Seis meses, doze critérios e cenário com painéis solares antecedem recompra pessoal e ponderação de negativos.","evidence":"Metadados, descrição, transcrição automática integral e vinte comentários amostrados.","limitations":["custos e garantias não verificados","período curto para confiabilidade"]},
    {"referenceId":"obs-20260916-163","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Uso de seis a onze meses, condição atual e critérios por produto antecedem manter, recomprar ou permanecer em dúvida.","evidence":"Metadados, descrição, transcrição automática integral e vinte comentários amostrados.","limitations":["desgaste não visto","natureza comercial dos links não confirmada"]},
    {"referenceId":"obs-20260916-164","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"Período e critérios aparecem, mas a conclusão manda qualquer pessoa em dúvida comprar, sem perfil excluído ou condição de preço.","evidence":"Metadados, descrição, transcrição automática integral e vinte comentários amostrados.","limitations":["comentários divergentes não são contraexemplo causal","produto e falhas não auditados"]},
])
pattern["limitations"] = [
    "Nove apoios formais vêm de nove criadores e nove fontes independentes; demonstram recorrência estrutural, não eficácia.",
    "Produtos, mercados e períodos diferem; a comparação é funcional e não autoriza benchmark numérico.",
    "Nenhum audiovisual, áudio ouvido, capa, texto na tela, edição, ritmo ou retenção foi auditado neste lote.",
    "Links comerciais e declarações de independência precisam ser registrados separadamente; ausência de patrocínio não prova ausência de afiliação.",
    "Os três casos-limite mostram que período e critérios não bastam quando o julgamento antecede a avaliação ou termina universal, sem perfil excluído ou trade-off.",
    "Ainda não há contraexemplo genuíno com teste de compreensão, confiança, conversão ou utilidade.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("RQuWMuORMmw", "reclassificado na triagem: assinatura, idioma, disponibilidade e ajuste condicionam a recomendação; não era caso-limite genuíno"),
        ("Tix2znquyVM", "mesmo canal de apoio selecionado e forte sobreposição funcional; diversidade inferior"),
        ("F1BLjs8ZeYk", "apoio potencial, mas redundante com reviews de smartphone já presentes"),
        ("JS9EaXgcd7k", "review de console com escala e produção menos replicáveis que os selecionados"),
        ("nIxEU0EWuoA", "canal institucional de grande escala; diversidade e replicabilidade inferiores"),
        ("G6Y5W7uXess", "review de smartphone redundante para este lote"),
        ("hFZOuB0AGpQ", "não é experiência pós-uso própria claramente demonstrada; comparação funcional inferior"),
        ("K7zaWEblMZU", "smartphone redundante para este lote"),
        ("EhEJ0PcDguo", "mesmo criador do apoio automotivo escolhido"),
        ("ajeqqeDMbQU", "candidato automotivo redundante e menor isolamento do período de teste"),
        ("oz_8vAVJUf4", "alegações legais e de segurança sobre motocicleta elétrica exigiriam verificação adicional"),
        ("-90OWvT4_3g", "candidato válido, mas menor ganho de diversidade que o review multiproduto selecionado"),
        ("xyrwjGXy1uk", "review de tênis válido, mas conclusão já condicionada; não servia ao papel de limite"),
        ("IdQRsVndGuk", "apoio potencial de smartphone redundante"),
        ("Fj6qMOtuDkA", "mistura relatos de terceiros, descrição de especificações e vínculo afiliado; comparabilidade inferior"),
        ("enD9tQbVpHs", "review de smartphone redundante e menor ganho de diversidade"),
        ("E8oJbOI0wmg", "motocicleta elétrica envolve alegações de segurança e custo não verificadas"),
        ("xJ7AaMWbqJA", "automotivo redundante para este lote"),
        ("S6GEFBitEXE", "smartphone redundante para este lote"),
        ("UEt6cWSnu9c", "smartphone redundante para este lote"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 50,
    "referenceIds": [f"obs-20260916-{n}" for n in range(161, 166)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260916-165"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["comparacao","autoridade_opiniao","demonstracao","educativo","storytelling"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads dos cinco vídeos expiraram após repetidos timeouts ou respostas 502 dos hosts de mídia; capas também expiraram sem bytes recebidos","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullAutomatic":5,"partialAutomatic":0,"none":0,"limitation":"transcrições automáticas substituem apenas fala e podem conter erros; uma inconsistência numérica foi explicitamente registrada na exploração"},
    "commentsCoverage": {"countsOnly":0,"sampledReferences":5,"sampledComments":87,"limitation":"foram amostrados 7, 20, 20, 20 e 20 comentários; amostras não são representativas e não medem eficácia"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"produtos, datas, durações e escalas heterogêneos impedem benchmark de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["período e critérios não bastam quando a conclusão manda comprar universalmente, sem perfil excluído, condição de preço ou trade-off"],
    "safetyFindings": ["alegações técnicas, de saúde, garantia, custo e segurança foram mantidas como falas não verificadas","nenhum comentário, nome de usuário ou dado pessoal foi reproduzido na memória","um falso caso-limite foi descartado após leitura integral da transcrição"],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três novos criadores brasileiros sustentam a recorrência de período, cenário e critérios antes de um veredito condicionado. O padrão passa a nove apoios independentes, recebe um terceiro caso-limite e permanece provisório, sem evidência de confiança, retenção, utilidade ou conversão.",
    "nextTarget": "review brasileiro curto com audiovisual integral, disclosure explícito de patrocínio ou afiliação, critérios pré-declarados e teste de compreensão; procurar caso em que os próprios critérios contradigam o veredito ou públicos diferentes interpretem incorretamente para quem a recomendação vale",
    "limitations": ["Nenhum audiovisual, áudio ou capa foi adquirido.","As 87 amostras de comentários não são representativas; retenção, teste de compreensão, conversão e baseline homogêneo seguem ausentes.","Alegações de produto e fatos científicos não foram verificados independentemente.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
