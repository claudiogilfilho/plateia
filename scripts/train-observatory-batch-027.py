#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Reuse the schema-compatible builders from the immediately preceding batch.
# Batch 026 is idempotent and part of the same branch.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-026.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
classification = ns["classification"]
make_ref = ns["make_ref"]

NOW = "2026-09-14T11:11:50.000Z"
OBSERVED = "2026-09-14"
RUN_ID = "run-20260914-supervised-027"
TARGET_ID = "hyp-20260826-022"
PATTERN_ID = "pat-20260914-014"
BATCH_IDS = {f"obs-20260914-{n}" for n in range(151, 156)}

# Update globals used by the imported builders.
make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED

memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]
memory["patterns"] = [p for p in memory["patterns"] if p.get("id") != PATTERN_ID]

hypothesis = next(h for h in memory["hypotheses"] if h["id"] == TARGET_ID)
hypothesis["supportReferenceIds"] = [x for x in hypothesis.get("supportReferenceIds", []) if x not in BATCH_IDS]
hypothesis["status"] = "observed_not_promoted"
hypothesis.pop("promotedPatternId", None)
hypothesis.pop("promotedAt", None)
hypothesis["reasonNotPromoted"] = "A referência precursora tinha cobertura secundária e não demonstrava a sequência completa."

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
        alternatives=None, missing=None, advertising="editorial_organico",
        intent="ausente", entity=None):
    return classification(
        material=material, presentations=presentations, primary=primary,
        secondary=secondary, mix=mix, objectives=objectives,
        advertising=advertising, intent=intent,
        entity=entity or {"kind": "nenhuma", "name": "nenhuma", "confidence": "medium"},
        topic=topic, segment=segment, subsegment=subsegment, audience=audience,
        awareness=awareness, production=production, scale=scale,
        replicability=replicability, duration=duration, mechanisms=mechanisms,
        hooks=hooks, narrative=narrative, proof=proof, cta=cta,
        confidence=confidence, evidence=evidence,
        alternatives=alternatives or [], missing=missing or MISSING_AV,
    )


def ref(**kwargs):
    item = make_ref(**kwargs)
    item["country"] = "BR"
    return item


refs = [
    ref(
        id="obs-20260914-151",
        title="Usei o Apple Watch Series 11 por 30 dias: minha opinião",
        creator="Cerqueira Tech", identity="cerqueira-tech",
        url="https://www.youtube.com/watch?v=dcgNoEuesaY",
        published=None, duration="PT3M24S",
        accessible=[
            "título", "criador", "duração", "data relativa indexada: cerca de três meses",
            "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "3.256 visualizações na triagem pública",
            "70 curtidas exibidas no índice público", "período de uso de 30 dias",
            "critérios de mapas, pagamento, exercícios, assistente, ligações e praticidade",
            "veredito condicionado ao uso de iPhone e às necessidades declaradas",
        ],
        missing=MISSING_AV + ["data exata de publicação", "descrição integral", "comentários públicos"],
        metrics={"viewsObserved": "3.256", "likesObserved": "70 indexadas", "commentsObserved": "not_assessed"},
        cls=cls(
            material="video_longo", presentations=["comentario", "indeterminado"],
            primary="comparacao", secondary=["autoridade_opiniao", "demonstracao"],
            mix=[{"family":"comparacao","percentage":50},{"family":"autoridade_opiniao","percentage":30},{"family":"demonstracao","percentage":20}],
            objectives=["educar","apresentar_solucao","confianca"],
            topic="review pós-uso do Apple Watch Series 11", segment="tecnologia de consumo",
            subsegment="wearables e ecossistema Apple", audience="usuários de iPhone considerando um smartwatch",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["aproximacao","confianca","recompensa"], hooks=["numero","problema","verbal"],
            narrative=["situacao","prova","conclusao"], proof=["depoimento","demonstracao"],
            cta=["comentar","seguir"], evidence=[
                "A abertura declara 30 dias de uso real e diferencia o vídeo de uma leitura de ficha técnica.",
                "Os critérios aparecem antes do veredito: mapas, pagamento, exercícios, assistente, calculadora e ligações.",
                "Entre 02:05 e 02:58, o veredito é condicionado ao ecossistema e aos hábitos do comprador.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260914-152","obs-20260914-153"],"confidence":"high"},
        observations=[
            "O contexto de teste é declarado nos primeiros segundos.",
            "A fala organiza seis usos cotidianos antes do veredito.",
            "A conclusão separa quem tende a se beneficiar de quem provavelmente precisa apenas de um relógio comum.",
        ],
        interpretations=[
            "Período, uso e critérios tornam a recomendação semanticamente auditável.",
            "A sequência é recorrente, mas sua utilidade ou efeito sobre compra não foi medido.",
        ],
        scores={"gancho":88,"clareza":94,"relevancia":91,"desejo":78,"confianca":84,"retencao":"not_assessed","acao":78,"objecoes":87},
        lenses={
            "apressado":"Entende período, produto e promessa de uso real nos primeiros segundos.",
            "analitico":"Recebe critérios e ressalvas, mas não dados instrumentados nem preço.",
            "aspiracional":"Percebe praticidade cotidiana sem promessa de transformação extrema.",
            "comunidade":"É convidado a declarar sua necessidade; respostas não foram acessadas.",
            "cetico":"Valoriza o veredito condicionado, mas desconta ausência de disclosure e teste audiovisual auditado.",
        },
        replicable=["Declarar período e natureza do uso antes dos critérios.","Avaliar usos concretos antes do veredito.","Condicionar a recomendação ao perfil que realmente se beneficia."],
        contingent=["Sem audiovisual, áudio ouvido, texto na tela, edição, ritmo ou retenção.","Sem preço, disclosure, comentários ou baseline funcional.","Métricas públicas são contexto, não causa."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"contexto de teste aparece antes do veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"critérios concretos aparecem antes do veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="public_search_youtube_index_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260914-152",
        title="Flashforge AD5X após 30 dias: Vale a pena? Análise sincera após 1 mês de uso!",
        creator="A&B_3D", identity="a-e-b-3d",
        url="https://www.youtube.com/watch?v=gc_mLqwTKTw",
        published=None, duration="PT4M45S",
        accessible=[
            "título", "criador", "duração", "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "5.069 visualizações na triagem pública",
            "período de uso de um mês", "amostras de impressão descritas na fala",
            "configuração de filamento declarada", "faixa de preço falada",
            "comparação com outra impressora", "ressalva para iniciantes", "veredito falado",
        ],
        missing=MISSING_AV + ["data de publicação", "descrição integral", "curtidas", "comentários públicos"],
        metrics={"viewsObserved":"5.069","likesObserved":"not_assessed","commentsObserved":"not_assessed"},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="demonstracao",
            secondary=["comparacao","educativo"],
            mix=[{"family":"demonstracao","percentage":45},{"family":"comparacao","percentage":35},{"family":"educativo","percentage":20}],
            objectives=["educar","apresentar_solucao","confianca","comentario"],
            topic="review pós-uso da impressora Flashforge AD5X", segment="tecnologia maker",
            subsegment="impressão 3D doméstica", audience="iniciantes e makers considerando uma impressora multicolorida",
            production="simple", scale="small", replicability="high", mechanisms=["confianca","recompensa","aproximacao"],
            hooks=["numero","pergunta","demonstracao_antecipada"], narrative=["situacao","prova","progressao","conclusao"],
            proof=["depoimento","demonstracao","dado"], cta=["comentar","conversar"],
            evidence=[
                "A abertura declara que o criador esperou um mês para testar antes de opinar.",
                "Antes do veredito, a fala descreve peças, ajustes e configuração de filamento.",
                "Entre 01:33 e 04:22, preço, comparação, ausência de problemas e ressalva para iniciantes qualificam a recomendação.",
            ],
        ),
        comparison={"level":2,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260914-151","obs-20260914-153"],"confidence":"high"},
        observations=[
            "O período de teste é declarado antes de qualquer recomendação.",
            "Resultados, configuração, preço e comparação precedem ou sustentam o veredito.",
            "A recomendação a iniciantes recebe ressalva sobre configuração inicial.",
        ],
        interpretations=["O veredito fica rastreável a critérios falados, mesmo sem verificação visual das peças.","A demonstração descrita não substitui auditoria das imagens."],
        scores={"gancho":83,"clareza":89,"relevancia":92,"desejo":82,"confianca":81,"retencao":"not_assessed","acao":80,"objecoes":84},
        lenses={
            "apressado":"Recebe período, produto e pergunta de compra em menos de vinte segundos.",
            "analitico":"Encontra preço, comparação e ressalvas; quer protocolo visual e disclosure.",
            "aspiracional":"Projetos e impressão multicolorida sugerem possibilidades, sem cenas auditadas.",
            "comunidade":"O CTA promete responder dúvidas ou produzir novo vídeo; execução não foi verificada.",
            "cetico":"Não aceita adjetivos de qualidade como medição e separa fala de evidência visual.",
        },
        replicable=["Esperar uso suficiente e declarar o período.","Expor peças, configurações e preço antes de recomendar.","Adicionar ressalva operacional para iniciantes."],
        contingent=["Peças e qualidade foram apenas descritas na fala.","Sem audiovisual, comentários, disclosure, retenção ou baseline.","Comparação de preço foi observacional e sem mercado controlado."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"contexto de teste aparece antes do veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"resultados, configuração e preço qualificam o veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="public_search_youtube_index_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260914-153",
        title="TESTEI UM MONOCICLO ELÉTRICO POR 30 DIAS: VALE A PENA?",
        creator="Reset", identity="reset",
        url="https://www.youtube.com/watch?v=wpkDpxQ1UCE",
        published="2025-11-05", duration="PT14M54S",
        accessible=[
            "título", "criador", "descrição indexada", "data exata indexada", "duração",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "127.061 visualizações na triagem pública", "período de um mês quase diário",
            "critérios de portabilidade, aprendizagem, autonomia, velocidade, suspensão, preço, risco e cenário de uso",
            "opinião adicional de outro usuário na transcrição", "veredito condicionado ao cenário",
        ],
        missing=MISSING_AV + ["descrição integral", "curtidas", "comentários públicos", "disclosure comercial completo"],
        metrics={"viewsObserved":"127.061","likesObserved":"not_assessed","commentsObserved":"not_assessed"},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="comparacao",
            secondary=["demonstracao","autoridade_opiniao"],
            mix=[{"family":"comparacao","percentage":45},{"family":"demonstracao","percentage":35},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["educar","apresentar_solucao","confianca","venda"],
            topic="review pós-uso de monociclo elétrico", segment="mobilidade elétrica",
            subsegment="monociclo para lazer e deslocamento", audience="adultos avaliando veículo elétrico pessoal",
            production="intermediate", scale="large", replicability="medium", duration="over_60s",
            mechanisms=["curiosidade","confianca","vigilancia","recompensa"], hooks=["numero","pergunta","risco"],
            narrative=["situacao","risco","prova","progressao","conclusao"], proof=["depoimento","demonstracao","tratamento_objecao"],
            cta=["compartilhar","clicar"], confidence="high", advertising="publicidade_nativa", intent="explicita",
            entity={"kind":"produto","name":"monociclos vendidos pela loja de um amigo do criador","confidence":"high"},
            evidence=[
                "A abertura declara um mês de uso e promete recomendação honesta.",
                "A fala percorre portabilidade, aprendizagem, suspensão, autonomia, preço e risco antes do fechamento.",
                "Entre 07:20 e 14:17, a recomendação muda conforme lazer, mobilidade diária, terreno, experiência e companhia.",
                "O encerramento direciona à loja de um amigo e menciona possível desconto.",
            ],
        ),
        comparison={"level":2,"group":"review brasileiro pós-uso para decisão de compra, com período, critérios e veredito condicionado","referenceIds":["obs-20260914-151","obs-20260914-152"],"confidence":"medium"},
        observations=[
            "O teste de um mês é declarado na abertura.",
            "A recomendação é dividida por cenário: lazer, deslocamento urbano, terreno, suspensão e exposição corporal.",
            "O vínculo comercial com a loja aparece na fala e limita independência percebida.",
        ],
        interpretations=["Critérios e ressalvas tornam o veredito condicional, não universal.","Risco e vínculo comercial exigem leitura mais cética; desempenho não pode ser inferido pelas visualizações."],
        scores={"gancho":90,"clareza":88,"relevancia":91,"desejo":80,"confianca":76,"retencao":"not_assessed","acao":82,"objecoes":86},
        lenses={
            "apressado":"Entende produto, período e pergunta rapidamente.",
            "analitico":"Recebe múltiplos critérios, mas quer protocolo, acidentes e disclosure formal.",
            "aspiracional":"O uso recreativo é atraente, contrabalançado por risco explícito.",
            "comunidade":"Uma segunda opinião amplia perspectivas, sem amostra representativa.",
            "cetico":"Desconta o encaminhamento comercial e exige separar experiência de segurança comprovada.",
        },
        replicable=["Declarar duração e frequência do teste.","Separar critérios de produto de cenários de uso.","Condicionar o veredito ao risco e ao perfil do comprador."],
        contingent=["Produto e teste exigem custo, espaço e habilidade.","Vínculo com vendedor e desconto são contexto comercial.","Sem audiovisual, comentários, incidentes documentados, retenção ou baseline."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"período e intenção do teste aparecem antes do veredito","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"critérios e cenários qualificam a recomendação","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="public_search_youtube_index_description_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260914-154",
        title="Usei o MacBook Air M5 por 30 Dias e essa é minha opinião sincera",
        creator="Ricardo Franzen", identity="ricardo-franzen",
        url="https://www.youtube.com/watch?v=kZ8YSZt5SEw",
        published=None, duration="PT19M06S",
        accessible=[
            "título", "criador", "duração", "transcrição automática integral em português com timestamps",
            "fala por substituição textual", "14.142 visualizações na triagem pública",
            "período de um mês", "uso diário para edição", "software, carga de trabalho, calor, portas, tela e bateria",
            "ausência de link de afiliado declarada", "veredito positivo apresentado na abertura",
        ],
        missing=MISSING_AV + ["data de publicação", "descrição integral", "curtidas", "comentários públicos"],
        metrics={"viewsObserved":"14.142","likesObserved":"not_assessed","commentsObserved":"not_assessed"},
        cls=cls(
            presentations=["comentario","indeterminado"], primary="autoridade_opiniao",
            secondary=["comparacao","demonstracao"],
            mix=[{"family":"autoridade_opiniao","percentage":45},{"family":"comparacao","percentage":35},{"family":"demonstracao","percentage":20}],
            objectives=["educar","apresentar_solucao","confianca"], topic="review pós-uso do MacBook Air M5",
            segment="tecnologia de consumo", subsegment="computadores para edição de vídeo",
            audience="criadores considerando notebook Apple para edição", production="simple", scale="medium",
            replicability="high", mechanisms=["confianca","desejo","recompensa"], hooks=["numero","resultado_antecipado","problema"],
            narrative=["conclusao","situacao","prova","problema"], proof=["depoimento","alegacao_sem_prova"],
            cta=["comentar"], evidence=[
                "Nos primeiros cinco segundos, a fala já qualifica a experiência como incrível.",
                "Depois, declara edição diária, Final Cut, carga, calor, tela, portas e bateria.",
                "A recomendação explícita reaparece no final e declara ausência de link comercial.",
            ],
        ),
        comparison={"level":1,"group":"review brasileiro pós-uso para decisão de compra, mas com veredito antes dos critérios","referenceIds":["obs-20260914-151","obs-20260914-152","obs-20260914-153"],"confidence":"high"},
        observations=["O período e o uso profissional aparecem cedo, mas o julgamento positivo vem antes do conjunto de critérios.","Critérios e única ressalva de tela surgem depois da conclusão antecipada.","A ausência de link é declarada, mas compra, preço e configuração exata não ficaram integralmente auditáveis."],
        interpretations=["É funcionalmente comparável, porém não apoia a sequência critérios-antes-do-veredito.","Sem medida de utilidade, não é contraexemplo causal; refina apenas a fronteira estrutural."],
        scores={"gancho":86,"clareza":85,"relevancia":88,"desejo":84,"confianca":75,"retencao":"not_assessed","acao":76,"objecoes":72},
        lenses={
            "apressado":"Recebe uma conclusão forte antes de entender limites e configuração.",
            "analitico":"Encontra carga de trabalho e software, mas precisa reorganizar os critérios.",
            "aspiracional":"A edição diária sem travar sustenta desejo declarado.",
            "comunidade":"Dúvidas são convidadas no fim; comentários não foram acessados.",
            "cetico":"Questiona o veredito precoce e os absolutos antes das ressalvas.",
        },
        replicable=["Declarar período, uso principal e software.","Relacionar recomendação a uma carga de trabalho concreta."],
        contingent=["Caso-limite: veredito aparece antes dos critérios.","Sem audiovisual, comentários, configuração completa, retenção ou baseline.","Experiência pessoal não equivale a benchmark de desempenho."],
        role="falsification_or_boundary", evidence_level=1, eligible=False,
        claims=[
            {"claim":"período e uso principal aparecem cedo","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"critérios concretos aparecem antes do veredito","requiredModalities":["transcript","criteria_before_verdict"],"observedModalities":["transcript"],"sufficient":False},
            {"claim":"a ordem reduz utilidade","requiredModalities":["utility_measure"],"observedModalities":[],"sufficient":False},
        ],
        source_type="public_search_youtube_index_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260914-155",
        title="Curau Brûlée Cremoso e Crocante",
        creator="Tastemade Brasil", identity="tastemade-brasil",
        url="https://www.youtube.com/watch?v=aiBxC17KvW4",
        published=None, duration="PT4M40S",
        accessible=[
            "título", "criador", "duração indexada", "data relativa indexada: cerca de dois meses",
            "458 visualizações na triagem pública", "canal oficial e publicação individual identificados",
        ],
        missing=MISSING_AV + ["data exata", "descrição", "fala ou transcrição", "ingredientes", "etapas", "resultado visual", "curtidas", "comentários públicos"],
        metrics={"viewsObserved":"458","likesObserved":"not_assessed","commentsObserved":"not_assessed"},
        cls=cls(
            presentations=["indeterminado"], primary="curiosidade",
            secondary=["demonstracao","educativo"],
            mix=[{"family":"curiosidade","percentage":50},{"family":"demonstracao","percentage":30},{"family":"educativo","percentage":20}],
            objectives=["visualizacao","educar","salvamento"], topic="curau com acabamento brûlée",
            segment="alimentação e culinária", subsegment="sobremesa brasileira reinterpretada",
            audience="pessoas interessadas em receitas e confeitaria", awareness="consciente_solucao",
            production="intermediate", scale="large", replicability="unknown", mechanisms=["curiosidade","recompensa","desejo"],
            hooks=["textual","resultado_antecipado"], narrative=["promessa"], proof=[], cta=[], confidence="low",
            evidence=["O título combina um prato familiar com dois atributos de textura contrastantes.","O índice público identifica publicação, canal, duração e visualizações."],
            missing=MISSING_AV + ["fala","ingredientes","etapas","resultado","CTA"],
        ),
        comparison={"level":4,"group":"exploração de demonstração culinária; cobertura insuficiente para comparação estrutural","referenceIds":[],"confidence":"low"},
        observations=["O título nomeia prato e contraste de textura: cremoso e crocante.","Nenhuma execução, ingrediente ou entrega visual ficou acessível."],
        interpretations=["O contraste pode orientar uma futura busca, mas não autoriza ensinar estrutura, ritmo ou receita."],
        scores={"gancho":78,"clareza":76,"relevancia":72,"desejo":80,"confianca":"not_assessed","retencao":"not_assessed","acao":"not_assessed","objecoes":"not_assessed"},
        lenses={
            "apressado":"Entende prato e promessa de textura pelo título.",
            "analitico":"Não consegue avaliar ingredientes, processo ou entrega.",
            "aspiracional":"O contraste de textura sugere uma recompensa, sem imagem auditada.",
            "comunidade":"Comentários e participação não foram acessados.",
            "cetico":"Mantém toda afirmação sobre execução como não mensurada.",
        },
        replicable=["Nomear no título o prato e o contraste sensorial prometido."],
        contingent=["Exploração de outra família; não sustenta o padrão de reviews.","Cobertura insuficiente para ensinar receita, demonstração, ritmo ou retenção.","Produção e replicabilidade material ficaram não mensuradas."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"o título promete contraste de textura","requiredModalities":["title"],"observedModalities":["title"],"sufficient":True},
            {"claim":"a receita entrega as texturas prometidas","requiredModalities":["video_or_frames","recipe"],"observedModalities":[],"sufficient":False},
        ],
        source_type="public_search_youtube_index_only",
        comment_provenance=False,
    ),
]

existing_urls = {r.get("url") for r in memory["references"]}
for item in refs:
    if item["url"] in existing_urls:
        raise SystemExit(f"URL duplicada: {item['url']}")
    existing_urls.add(item["url"])
memory["references"].extend(refs)

new_supports = ["obs-20260914-151", "obs-20260914-152", "obs-20260914-153"]
hypothesis["supportReferenceIds"].extend(new_supports)
hypothesis["status"] = "promoted_to_provisional"
hypothesis["promotedPatternId"] = PATTERN_ID
hypothesis["promotedAt"] = NOW
hypothesis.pop("reasonNotPromoted", None)

memory["patterns"].append({
    "id": PATTERN_ID,
    "status": "provisional",
    "stage": "provisional",
    "name": "Contexto e critérios antes do veredito pós-uso",
    "statement": "Em reviews pós-uso para decisão de compra, declarar o período e o cenário de teste, apresentar critérios concretos e então condicionar o veredito ao perfil de uso torna a lógica da recomendação rastreável. Efeitos sobre utilidade percebida, confiança, retenção ou conversão não foram medidos.",
    "creativeFamily": "comparacao",
    "objective": "orientar decisão de compra",
    "segment": "reviews de tecnologia e mobilidade de consumo",
    "mechanism": ["confianca", "aproximacao", "recompensa", "vigilancia"],
    "conditions": [
        "experiência pós-uso com período declarado",
        "cenário ou frequência de uso identificável",
        "dois ou mais critérios concretos apresentados antes da conclusão principal",
        "veredito ligado ao perfil, cenário ou necessidade do comprador",
        "sequência diretamente observável em transcrição, áudio ou vídeo",
    ],
    "supportReferenceIds": new_supports,
    "precursorReferenceIds": ["obs-20260826-051"],
    "comparableSupportCount": 3,
    "supportingCount": 3,
    "counterexampleCount": 0,
    "caseLimitCount": 1,
    "counterexampleReferenceIds": [],
    "caseLimitReferenceIds": ["obs-20260914-154"],
    "comparisonLevel": 2,
    "confidence": "medium",
    "creatorDiversityCount": 3,
    "sourceDiversityCount": 3,
    "patternType": "compreensao",
    "evidence": [
        {"referenceId":"obs-20260914-151","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Trinta dias e uso real são declarados; seis critérios cotidianos precedem um veredito condicionado a ecossistema e hábitos.","evidence":"Título, índice público e transcrição automática integral.","limitations":["sem audiovisual, comentários, preço ou retenção"]},
        {"referenceId":"obs-20260914-152","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Um mês de teste, peças, configurações, preço e comparação sustentam recomendação com ressalva para iniciantes.","evidence":"Título, índice público e transcrição automática integral.","limitations":["qualidade visual das peças não auditada","sem disclosure ou retenção"]},
        {"referenceId":"obs-20260914-153","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Um mês quase diário, critérios de portabilidade, autonomia, preço, suspensão e risco antecedem recomendações diferentes por cenário.","evidence":"Título, descrição indexada, data e transcrição automática integral.","limitations":["vínculo comercial com loja","sem audiovisual, comentários ou retenção"]},
        {"referenceId":"obs-20260914-154","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"O período e o uso profissional são claros, mas o julgamento positivo aparece nos primeiros segundos, antes do conjunto de critérios.","evidence":"Título, índice público e transcrição automática integral.","limitations":["não é contraexemplo causal porque utilidade e desempenho não foram medidos"]},
    ],
    "limitations": [
        "Os três apoios independentes demonstram recorrência estrutural, não eficácia.",
        "Nenhum vídeo, áudio, capa, texto na tela, edição, ritmo ou retenção foi auditado.",
        "Os produtos, durações e escalas de criador diferem; não formam benchmark numérico.",
        "A referência precursora permanece contexto por cobertura secundária.",
        "O caso-limite mostra que declarar período e uso não basta quando o veredito antecede os critérios.",
        "Validação exige revisão humana ou evidência experimental apropriada.",
    ],
    "validation": "requires_human_or_experimental_evidence",
    "taxonomyVersion": "3.0",
})

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("mrsMuQbNlzM", "suplemento ingerível; maior risco de confundir experiência com alegação de saúde"),
        ("zKOSsEAdm9c", "mesmo produto do apoio selecionado e menor diversidade de fonte"),
        ("PNxnC8ORrXo", "mesmo criador de outro candidato e produto antigo; diversidade inferior"),
        ("i74CDqkgEyU", "mesmo criador de outro candidato e cobertura redundante"),
        ("x4rdpgaMV1Q", "notebook semelhante ao caso-limite e duração ainda maior"),
        ("5raF67nilvQ", "mesmo criador de outro candidato e duração longa"),
        ("WU5aDPW8Gfw", "mesmo criador de outro candidato e cobertura redundante"),
        ("sWv0FeCcwgs", "mesmo criador de outro candidato e duração longa"),
        ("sOmqj_uKJG4", "produto semelhante a outros candidatos; diversidade inferior"),
        ("LPVR2JoJzQQ", "mesmo criador de outro candidato e cobertura redundante"),
        ("mnc4Gp-t57Q", "bom candidato, mas duração maior e sobreposição com review de impressão 3D selecionado"),
        ("rqTDNjkk3CM", "wearable com duração longa; menor ganho de diversidade que o monociclo"),
        ("8AsGRez8YVY", "notebook semelhante ao caso-limite selecionado"),
        ("faWkStPfFoQ", "cosmético com cobertura insuficiente e maior risco de alegação pessoal não verificável"),
        ("gzY_RtObHOk", "mesmo criador de candidato anterior e cobertura redundante"),
        ("1bd-ny10Tqo", "título disponível, mas cobertura inferior aos apoios com transcrição adquirida"),
        ("sDvD5UHdpkM", "compilação culinária longa e menos específica que a exploração escolhida"),
        ("i9nJAtmrX3I", "compilação de cinco receitas; menor isolamento do mecanismo"),
        ("jzEPDMxgDgk", "compilação de dez receitas; menor comparabilidade estrutural"),
        ("ZxJVKpK2d-Q", "programa culinário longo e produção menos replicável"),
        ("4GaEvdJxpLs", "episódio culinário com múltiplas receitas e produção complexa"),
        ("zc_Jv8LYU8g", "compilação de tortas; menor isolamento da promessa"),
        ("ZWw9M783m1M", "compilação de pudins; menor isolamento da promessa"),
        ("lWMw2_Fgd4g", "compilação de bolos; redundante com outras listas"),
        ("DxUrAAlTCxw", "compilação de sanduíches; menor especificidade que o caso escolhido"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 30,
    "referenceIds": [f"obs-20260914-{n}" for n in range(151, 156)],
    "targetKnowledgeId": TARGET_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": ["obs-20260914-154"],
    "controlledExplorationReferenceIds": ["obs-20260914-155"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["comparacao","autoridade_opiniao","demonstracao","educativo","curiosidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"downloads e páginas diretas foram bloqueados por verificação automatizada, 429 ou timeout; capas também expiraram","effect":"imagem em movimento, áudio ouvido, texto na tela, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullAutomatic":4,"partialAutomatic":0,"none":1,"limitation":"transcrições automáticas substituem apenas fala e podem conter erros; a exploração não teve transcrição"},
    "commentsCoverage": {"unavailable":5,"limitation":"comentários públicos não foram adquiridos"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"produtos, idades, durações e escalas heterogêneos impedem benchmark de desempenho"},
    "patternsCreated": [PATTERN_ID],
    "patternsStrengthened": [],
    "patternsRefined": [],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [TARGET_ID],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["declarar período e cenário não equivale a apresentar critérios antes do veredito"],
    "safetyFindings": ["nenhuma alegação de segurança do veículo foi ensinada como fato","nenhum comentário ou dado pessoal foi reproduzido"],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores brasileiros independentes sustentam recorrência estrutural de período, cenário e critérios antes de um veredito condicionado. O padrão é provisório; utilidade, confiança, retenção e conversão não foram medidas.",
    "nextTarget": "review brasileiro pós-uso curto com audiovisual integral, disclosure, critérios pré-declarados e teste de compreensão; buscar caso comparável em que critérios contradigam o veredito ou em que público não identifique para quem a recomendação vale",
    "limitations": ["Nenhum audiovisual, áudio ou capa foi adquirido.","Uma referência não teve transcrição.","Sem comentários, retenção, teste de compreensão, conversão ou baseline homogêneo.","Datas exatas de quatro referências não ficaram acessíveis.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"newPattern":PATTERN_ID}, ensure_ascii=False))
