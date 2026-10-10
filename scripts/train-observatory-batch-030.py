#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Reconstruct the remote corpus in order, including the non-chained batches 023–025.
for batch in ("023", "024", "025"):
    runpy.run_path(str(Path(__file__).with_name(f"train-observatory-batch-{batch}.py")))
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-029.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
classification = ns["classification"]
make_ref = ns["make_ref"]

NOW = "2026-09-17T11:06:04.000Z"
OBSERVED = "2026-09-17"
RUN_ID = "run-20260917-supervised-030"
PATTERN_ID = "pat-20260912-012"
BATCH_IDS = {f"obs-20260917-{n}" for n in range(166, 171)}

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
        topic, segment, subsegment, audience, awareness="consciente_problema",
        production="simple", scale="small", replicability="high", duration="over_60s",
        mechanisms, hooks, narrative, proof=None, cta=None, confidence="high", evidence,
        alternatives=None, missing=None, advertising="editorial_organico", intent="ausente",
        entity=None, trend="low"):
    return classification(
        material=material, presentations=presentations, primary=primary,
        secondary=secondary, mix=mix, objectives=objectives,
        advertising=advertising, intent=intent,
        entity=entity or {"kind": "indeterminado", "name": "", "confidence": "low"},
        topic=topic, segment=segment, subsegment=subsegment, audience=audience,
        awareness=awareness, production=production, scale=scale,
        replicability=replicability, duration=duration, mechanisms=mechanisms,
        hooks=hooks, narrative=narrative, proof=proof or [], cta=cta or [],
        confidence=confidence, evidence=evidence,
        alternatives=alternatives or [], missing=missing or MISSING_AV, trend=trend,
    )


def ref(*, country="BR", **kwargs):
    item = make_ref(**kwargs)
    item["country"] = country
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "roteiro ou performance editorial pública do próprio criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, personagens, premissas específicas ou roteiro",
        "reproduzir estereótipos, humilhação ou linguagem ofensiva",
        "tratar visualizações, fama, elenco, mídia paga ou orçamento como prova causal",
        "inferir cenas, atuação, áudio, texto na tela, edição, ritmo, riso ou retenção",
    ]
    return item


refs = [
    ref(
        id="obs-20260917-166",
        title="RH DA DISCÓRDIA",
        creator="Porta dos Fundos", identity="porta-dos-fundos",
        url="https://www.youtube.com/watch?v=GKzLJ6dEdcA",
        published="2023-04-27", duration="PT4M59S",
        accessible=[
            "título", "criador", "descrição parcial indexada", "data exata indexada",
            "duração de 4 minutos e 59 segundos", "transcrição pública integral em português com timestamps",
            "fala por substituição textual", "3.665.769 visualizações indexadas em pesquisa pública",
            "148 mil curtidas exibidas pelo índice público; contagem exata não adquirida",
            "premissa verbal de dinâmica positiva do RH e progressão das respostas na transcrição",
        ],
        missing=MISSING_AV + [
            "descrição integral", "contagem exata de curtidas", "contagem e amostra de comentários",
            "data de observação da métrica no próprio player", "baseline funcional contemporâneo",
        ],
        metrics={"viewsObserved":3665769,"likesObserved":None,"commentsObserved":None},
        cls=cls(
            presentations=["dialogo","esquete"], primary="humor",
            secondary=["storytelling","identificacao"],
            mix=[{"family":"humor","percentage":60},{"family":"storytelling","percentage":30},{"family":"identificacao","percentage":10}],
            objectives=["visualizacao","compartilhamento"],
            topic="dinâmica de integração no trabalho que vira exposição de conflitos",
            segment="humor de situação cotidiana", subsegment="ambiente de trabalho",
            audience="adultos familiarizados com empresas, RH e conflitos entre colegas",
            production="complex", scale="large", replicability="medium",
            mechanisms=["identificacao","surpresa","humor","tensao"],
            hooks=["conflito","problema"], narrative=["situacao","progressao","climax","conclusao"],
            evidence=[
                "Entre 0:22 e 0:40, a regra é escrever uma coisa boa sobre um colega.",
                "Entre 0:47 e 1:16, elogio à saúde vira acusação de atestados.",
                "Entre 1:23 e 2:33, atenção e amorosidade são reaplicados como roubo de ideias e bajulação.",
                "Entre 2:57 e 4:20, a dinâmica escala para acusação conjugal, eliminação e perda coletiva de benefício.",
            ],
        ),
        comparison={"level":1,"group":"esquete de tensão cotidiana com reaplicação e escalada da mesma regra verbal","referenceIds":["obs-20260917-167","obs-20260917-168"],"confidence":"high"},
        observations=[
            "A regra positiva é entendida antes do primeiro desvio.",
            "Cada novo participante preserva a forma do elogio e aumenta a consequência social.",
            "A punição coletiva fecha a escalada, mas atuação e reação visual não foram observadas.",
        ],
        interpretations=[
            "A transcrição sustenta premissa, reaplicação e progressão; não sustenta riso ou retenção.",
            "Elenco conhecido, produção e volume de visualizações são contingências, não partes ensinadas do mecanismo.",
        ],
        scores={"gancho":89,"clareza":94,"relevancia":88,"desejo":74,"confianca":82,"retencao":"not_assessed","acao":"not_assessed","objecoes":80},
        lenses={
            "apressado":"Entende dinâmica, local e regra antes do primeiro desvio.",
            "analitico":"Consegue mapear as reaplicações verbais, sem dados de efeito.",
            "aspiracional":"A cena oferece reconhecimento social, não transformação aspiracional.",
            "comunidade":"A tensão de trabalho é compartilhável, mas comentários não foram adquiridos.",
            "cetico":"Desconta elenco, fama, atuação não vista e ausência de métricas comparáveis.",
        },
        replicable=["Definir uma regra social simples.","Reaplicar a mesma forma com consequências crescentes.","Fechar a progressão sem copiar ambiente, acusações ou personagens."],
        contingent=["Produção, elenco e distribuição não são replicáveis por padrão.","Atuação, montagem e riso não foram auditados.","Métricas não demonstram causalidade."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"a fala estabelece uma regra cotidiana e a reaplica com consequências crescentes","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_search_metadata_and_full_public_portuguese_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260917-167",
        title="LIQUIDIFICADOR (AO VIVO)",
        creator="Barbixas", identity="barbixas",
        url="https://www.youtube.com/watch?v=u5Suc4KdMk8",
        published="2014-01-13", duration="PT4M47S",
        accessible=[
            "título", "criador", "descrição parcial indexada", "data exata indexada",
            "duração de 4 minutos e 47 segundos", "legenda pública integral em português com timestamps",
            "fala por substituição textual", "5.654.867 visualizações indexadas em pesquisa pública",
            "premissa verbal do produto defeituoso, regra do atendimento por telefone e repetição circular na transcrição",
        ],
        missing=MISSING_AV + [
            "descrição integral", "curtidas", "contagem e amostra de comentários",
            "imagem e som da apresentação ao vivo", "baseline funcional contemporâneo",
        ],
        metrics={"viewsObserved":5654867,"likesObserved":None,"commentsObserved":None},
        cls=cls(
            presentations=["dialogo","esquete","dramatizacao"], primary="humor",
            secondary=["storytelling","demonstracao"],
            mix=[{"family":"humor","percentage":55},{"family":"storytelling","percentage":35},{"family":"demonstracao","percentage":10}],
            objectives=["visualizacao","compartilhamento"],
            topic="troca de liquidificador defeituoso presa em regra burocrática",
            segment="humor de situação cotidiana", subsegment="atendimento ao consumidor",
            audience="adultos que reconhecem burocracia e falhas de atendimento",
            production="intermediate", scale="large", replicability="medium",
            mechanisms=["identificacao","surpresa","humor","recompensa"],
            hooks=["problema","conflito"], narrative=["situacao","progressao","loop","climax"],
            evidence=[
                "Entre 0:21 e 0:55, produto defeituoso e atendimento apenas por telefone definem o conflito.",
                "Entre 0:59 e 1:21, o cliente precisa sair da loja para ser atendido.",
                "Entre 2:38 e 3:20, a mesma regra é reaplicada ao formulário.",
                "Entre 3:45 e 4:38, o produto desaparece e a história retorna ao início com outro cliente.",
            ],
        ),
        comparison={"level":1,"group":"esquete de tensão cotidiana com reaplicação e escalada da mesma regra verbal","referenceIds":["obs-20260917-166","obs-20260917-168"],"confidence":"high"},
        observations=[
            "O obstáculo burocrático é introduzido como regra explícita.",
            "A regra retorna com exigências sucessivas até produzir perda do produto e reinício.",
            "A legenda sustenta a cadeia verbal; reação do público e atuação ficaram não mensuradas.",
        ],
        interpretations=[
            "Repetição com nova consequência mantém o desvio ligado ao problema inicial.",
            "A circularidade final é observável na fala, não uma prova de eficácia.",
        ],
        scores={"gancho":91,"clareza":96,"relevancia":90,"desejo":76,"confianca":84,"retencao":"not_assessed","acao":"not_assessed","objecoes":88},
        lenses={
            "apressado":"Recebe defeito, atendente e regra absurda logo no início.",
            "analitico":"Consegue reconstruir cada reaplicação sem depender da cena.",
            "aspiracional":"Não há promessa aspiracional; a recompensa é resolução cômica.",
            "comunidade":"Burocracia é reconhecível, mas comentários não foram observados.",
            "cetico":"Aceita a estrutura verbal e recusa inferências sobre plateia, ritmo e desempenho.",
        },
        replicable=["Apresentar problema e regra incompatível.","Reaplicar a regra a um novo obstáculo.","Usar retorno circular sem copiar produto, atendente ou falas."],
        contingent=["A versão é apresentação teatral com produção intermediária.","Reação do público não foi ouvida nem vista.","Views acumuladas em muitos anos não servem como benchmark."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"a mesma regra burocrática é reaplicada e aumenta a consequência","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_search_metadata_and_full_public_portuguese_caption",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260917-168",
        title="ME EMPRESTA UM LÁPIS?",
        creator="Maneirando", identity="maneirando",
        url="https://www.youtube.com/watch?v=7OcAVy1U9OY",
        published=None, duration="PT5M5S",
        accessible=[
            "título", "criador", "descrição parcial indexada", "duração de 5 minutos e 5 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "158.027 visualizações indexadas em pesquisa pública",
            "progressão falada de materiais completos para perdas, empréstimos e pedidos absurdos",
        ],
        missing=MISSING_AV + [
            "data de publicação", "descrição integral", "curtidas", "contagem e amostra de comentários",
            "confirmação visual de eventuais encenações", "baseline funcional contemporâneo",
        ],
        metrics={"viewsObserved":158027,"likesObserved":None,"commentsObserved":None},
        cls=cls(
            presentations=["camera_direta","comentario"], primary="humor",
            secondary=["storytelling","comunidade"],
            mix=[{"family":"humor","percentage":55},{"family":"storytelling","percentage":30},{"family":"comunidade","percentage":15}],
            objectives=["visualizacao","comunidade"],
            topic="desaparecimento de material escolar e pedidos de empréstimo",
            segment="humor de situação cotidiana", subsegment="vida escolar",
            audience="jovens e adultos que reconhecem rotinas escolares",
            production="simple", scale="medium", replicability="high",
            mechanisms=["identificacao","surpresa","humor","pertencimento"],
            hooks=["identificacao","problema"], narrative=["situacao","progressao","climax","conclusao"],
            evidence=[
                "Entre 0:54 e 1:18, estojo cheio vira apenas um pequeno lápis.",
                "Entre 1:20 e 1:56, grafite, caneta, lápis e borracha são pedidos em sequência.",
                "Entre 1:57 e 2:06, o pedido escala para itens impossíveis ligados a um pacto.",
                "Entre 2:40 e 3:26, papel, livro e caderno ampliam a mesma regra de falta de material.",
            ],
        ),
        comparison={"level":2,"group":"humor falado de tensão cotidiana com reaplicação e escalada da mesma regra","referenceIds":["obs-20260917-166","obs-20260917-167"],"confidence":"medium"},
        observations=[
            "A progressão de itens preserva a regra de falta ou perda de material.",
            "O salto para um pedido impossível cria a consequência absurda.",
            "É monólogo cômico, não esquete dialogada; conta apenas como comparação funcional de nível 2.",
        ],
        interpretations=[
            "O mecanismo aparece em apresentação adjacente mais simples, sem provar que o padrão se generaliza a todo monólogo.",
            "A transcrição é suficiente para a progressão verbal e insuficiente para atuação, texto ou ritmo.",
        ],
        scores={"gancho":82,"clareza":88,"relevancia":86,"desejo":70,"confianca":74,"retencao":"not_assessed","acao":66,"objecoes":78},
        lenses={
            "apressado":"Reconhece material escolar e perda progressiva rapidamente.",
            "analitico":"Distingue exemplos encadeados de digressões laterais.",
            "aspiracional":"A identificação escolar domina; não há transformação aspiracional.",
            "comunidade":"Há convite falado a comentários, mas respostas não foram acessadas.",
            "cetico":"Trata a comparação como nível 2 e não atribui efeito ao número de views.",
        },
        replicable=["Partir de um inventário cotidiano que se reduz.","Aumentar o pedido mantendo a mesma falta.","Usar absurdo sem copiar objetos, piadas ou linguagem ofensiva."],
        contingent=["Monólogo é apresentação adjacente, não esquete dialogada.","Transcrição automática contém ruído e censura.","Data e comentários ficaram não mensurados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala reaplica a falta de material em pedidos crescentes e um pedido absurdo","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_search_metadata_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260917-169",
        title="Restaurante que cobra taxa de desperdício",
        creator="Ray da resenha", identity="ray-da-resenha",
        url="https://www.youtube.com/watch?v=X8_pqGSeBbo",
        published=None, duration="PT3M25S",
        accessible=[
            "título", "criador", "descrição parcial indexada", "duração de 3 minutos e 25 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "629 visualizações indexadas em pesquisa pública",
            "primeira situação de taxa de desperdício e duas mudanças posteriores de premissa observáveis na transcrição",
        ],
        missing=MISSING_AV + [
            "data de publicação", "descrição integral", "curtidas", "contagem e amostra de comentários",
            "marcação editorial de capítulos ou esquetes", "baseline funcional contemporâneo",
        ],
        metrics={"viewsObserved":629,"likesObserved":None,"commentsObserved":None},
        cls=cls(
            presentations=["montagem","dialogo","esquete"], primary="humor",
            secondary=["storytelling","entretenimento"],
            mix=[{"family":"humor","percentage":55},{"family":"storytelling","percentage":30},{"family":"entretenimento","percentage":15}],
            objectives=["visualizacao"],
            topic="compilação de conflitos cotidianos iniciada por taxa de desperdício",
            segment="humor de situação cotidiana", subsegment="restaurante, benefício social e relacionamento",
            audience="público adulto de humor cotidiano",
            production="simple", scale="small", replicability="high",
            mechanisms=["identificacao","surpresa","humor"],
            hooks=["problema","conflito"], narrative=["situacao","progressao","virada"],
            evidence=[
                "Entre 0:00 e 1:07, a taxa de desperdício escala para ameaça de polícia.",
                "Em 1:08, a transcrição muda para comida azeda, com nova premissa.",
                "Em 2:11, muda novamente para aposentadoria e benefício social, sem ligação funcional com o restaurante.",
            ],
        ),
        comparison={"level":1,"group":"publicação de humor cotidiano cuja premissa titulada não é sustentada até o fim","referenceIds":["obs-20260917-166","obs-20260917-167"],"confidence":"high"},
        observations=[
            "A primeira situação possui escalada própria.",
            "A publicação abandona o conflito do título e concatena duas situações não relacionadas.",
            "Sem retenção ou teste de compreensão, a quebra não prova pior desempenho.",
        ],
        interpretations=[
            "Escalar uma cena local não basta para sustentar a progressão da publicação inteira.",
            "O caso delimita unidade editorial; é caso-limite, não contraexemplo causal.",
        ],
        scores={"gancho":84,"clareza":62,"relevancia":73,"desejo":68,"confianca":70,"retencao":"not_assessed","acao":"not_assessed","objecoes":58},
        lenses={
            "apressado":"Recebe rapidamente a taxa, mas encontra duas novas premissas sem aviso observável.",
            "analitico":"Consegue identificar três unidades, sem capítulos acessíveis.",
            "aspiracional":"Não há promessa aspiracional relevante.",
            "comunidade":"Situações populares podem gerar identificação, mas comentários não foram acessados.",
            "cetico":"Não confunde a mudança de premissa com prova de perda de retenção.",
        },
        replicable=["Manter cada publicação semanticamente unificada.","Se houver compilação, sinalizar unidades e transições."],
        contingent=["Não copiar situações, personagens ou alegações sobre benefícios públicos.","A ausência de capítulos pode ser limitação de cobertura.","Desempenho e reação permaneceram não medidos."],
        role="case_limit", evidence_level=1, eligible=False,
        claims=[
            {"claim":"a transcrição integral é suficiente para observar que a regra da cena inicial não é sustentada pela publicação inteira","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"há mudanças para duas premissas não relacionadas","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_search_metadata_and_full_automatic_transcript",
        comment_provenance=False,
    ),
    ref(
        id="obs-20260917-170",
        title="ninguém vende melhor do que o seu cliente",
        creator="Ricardo Date", identity="ricardo-date",
        url="https://www.youtube.com/watch?v=Rr-P-YwTSts",
        published=None, duration="PT55S", country="unknown",
        accessible=[
            "título", "criador", "descrição pública curta", "duração de 55 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "50.026 visualizações indexadas em pesquisa pública",
            "sequência verbal de recomendações no supermercado e revelação final de que a pessoa não trabalha ali",
        ],
        missing=MISSING_AV + [
            "país de origem confirmado", "data de publicação", "curtidas", "contagem e amostra de comentários",
            "marca, produto ou vínculo comercial confirmado", "baseline funcional contemporâneo",
        ],
        metrics={"viewsObserved":50026,"likesObserved":None,"commentsObserved":None},
        cls=cls(
            material="video_curto", presentations=["dialogo","dramatizacao"], primary="venda_indireta",
            secondary=["humor","demonstracao"],
            mix=[{"family":"venda_indireta","percentage":45},{"family":"humor","percentage":35},{"family":"demonstracao","percentage":20}],
            objectives=["apresentar_solucao","visualizacao","marca"],
            topic="cliente que recomenda produtos como se fosse atendente",
            segment="varejo alimentar", subsegment="supermercado",
            audience="consumidores e profissionais de varejo",
            awareness="consciente_solucao", production="simple", scale="small", replicability="high", duration="31_to_60s",
            mechanisms=["utilidade_pratica","surpresa","humor","confianca"],
            hooks=["identificacao"], narrative=["situacao","progressao","virada","conclusao"],
            evidence=[
                "Entre 0:06 e 0:36, uma pessoa oferece recomendações sucessivas sobre bolachas, frescos, peixe e receita.",
                "Entre 0:41 e 0:49, a outra agradece e descobre que a pessoa não trabalha no local.",
                "Título e fala sustentam o microresultado sem permitir identificar marca ou intenção comercial.",
            ],
            advertising="indeterminado", intent="indeterminada",
        ),
        comparison={"level":0,"group":"exploração controlada de micro-história de varejo; fora do grupo de esquetes-alvo","referenceIds":[],"confidence":"high"},
        observations=[
            "A fala constrói utilidade por recomendações e conclui com revelação de papel.",
            "Marca, produto patrocinado e cenas não ficaram acessíveis.",
            "A referência não foi usada para apoiar o padrão-alvo.",
        ],
        interpretations=[
            "Uma revelação pode fechar uma micro-história de marca sem esconder o assunto.",
            "Uma referência isolada gera observação, não hipótese ou padrão.",
        ],
        scores={"gancho":77,"clareza":82,"relevancia":76,"desejo":72,"confianca":68,"retencao":"not_assessed","acao":"not_assessed","objecoes":64},
        lenses={
            "apressado":"Recebe recomendações de compra antes da revelação.",
            "analitico":"Não consegue identificar marca, oferta ou prova de venda.",
            "aspiracional":"A promessa é ajuda cotidiana, não transformação.",
            "comunidade":"A inversão de papéis é reconhecível; comentários não foram acessados.",
            "cetico":"Trata intenção comercial e desempenho como indeterminados.",
        },
        replicable=["Dar utilidade antes da revelação.","Fechar com mudança de papel sem copiar diálogo ou produtos."],
        contingent=["Origem e intenção comercial não foram confirmadas.","Transcrição automática é ruidosa.","Views não demonstram venda, retenção ou eficácia."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"a fala oferece recomendações sucessivas e revela que a pessoa não é funcionária","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"o vídeo é publicidade ou gerou vendas","requiredModalities":["commercial_disclosure","conversion"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_search_metadata_description_and_full_automatic_transcript",
        comment_provenance=False,
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 030")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260917-166", "obs-20260917-167", "obs-20260917-168"]
new_case = "obs-20260917-169"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 6
pattern["supportingCount"] = 6
pattern["caseLimitCount"] = 2
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260917-166","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Regra de elogio é reaplicada como acusações crescentes até conflito conjugal e punição coletiva.","evidence":"Pesquisa pública, metadados indexados e transcrição pública integral em português.","limitations":["sem audiovisual, comentários ou retenção","produção complexa e fama são contingências"]},
    {"referenceId":"obs-20260917-167","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Atendimento apenas por telefone é reaplicado a recall e formulário até perda do produto e retorno circular.","evidence":"Pesquisa pública, metadados indexados e legenda pública integral em português.","limitations":["sem audiovisual ou reação da plateia","vídeo antigo sem baseline"]},
    {"referenceId":"obs-20260917-168","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Perda de material escolar escala de itens comuns a pedidos impossíveis, preservando a regra na fala.","evidence":"Pesquisa pública, metadados indexados e transcrição automática integral.","limitations":["monólogo adjacente, não esquete dialogada","transcrição ruidosa e sem data"]},
    {"referenceId":"obs-20260917-169","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"A primeira cena escala, mas a publicação abandona a premissa titulada e concatena duas situações sem ligação observável.","evidence":"Pesquisa pública, metadados indexados e transcrição automática integral.","limitations":["não mede efeito da quebra","ausência de capítulos pode ser limitação de cobertura"]},
])
pattern["limitations"] = [
    "Seis apoios formais vêm de seis criadores e seis fontes; demonstram recorrência estrutural, não riso, retenção, compartilhamento ou desempenho.",
    "Cinco apoios são esquetes dialogadas e um é monólogo funcionalmente adjacente de nível 2; a ampliação de apresentação exige revisão humana.",
    "Nenhum audiovisual, capa, áudio ouvido, texto na tela, atuação, montagem, ritmo ou retenção foi auditado neste lote.",
    "O segundo caso-limite mostra que uma cena pode escalar localmente e ainda perder unidade quando a publicação muda para premissas não relacionadas.",
    "Ainda não há contraexemplo genuíno com cobertura equivalente e métrica de compreensão, riso ou retenção.",
    "Popularidade, elenco, produção e idade são contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("RvoO_4400oY", "apoio forte, mas redundante com outro vídeo dos Barbixas selecionado"),
        ("BOtg6dGTnLc", "apoio forte, mas redundante com outro vídeo do Porta dos Fundos selecionado"),
        ("S_nNaLlyXc8", "apoio forte, mas redundante com Barbixas e produção ao vivo já coberta"),
        ("MPh7Eg7LBSA", "transcrição automática muito ruidosa e publicação extensa com várias situações"),
        ("3ptm3bJdaU0", "compilação de três premissas e alegações sensíveis sobre serviço público"),
        ("4TDZbu7xJHk", "mesma fonte de apoio já contada no padrão e compilação de tipos"),
        ("B8KtARMVh2Q", "transcrição pública desativada; cobertura insuficiente"),
        ("lq8IbhWxCEA", "monólogo de reclamação sem progressão comparável tão limpa quanto o selecionado"),
        ("eh39_LJdryo", "linguagem discriminatória e baixo valor transferível seguro"),
        ("ytDe2AwCQuo", "transcrição automática excessivamente ruidosa"),
        ("bgJR79rEC0Q", "mesmo criador de apoio já presente no padrão"),
        ("qIfrm6GSwLc", "mesmo criador de apoio selecionado neste lote"),
        ("R3WW_fmVQJU", "mesmo criador de apoio selecionado neste lote"),
        ("uFUfi9WDckM", "mesmo criador de apoio já presente no padrão"),
        ("dCZQv0Jyjn0", "mesmo criador de apoio selecionado e transcrição bloqueada durante a triagem"),
        ("L86T-_77Wi8", "origem internacional e transcrição bloqueada durante a triagem"),
        ("4AxuKXHfH0E", "cobertura insuficiente após bloqueio temporário da transcrição"),
        ("SCMlx2Pvr6o", "mesmo criador de apoio já presente no padrão"),
        ("7bp3YWXMpWo", "mesma fonte selecionada e transcrição bloqueada durante a triagem"),
        ("XVDm5Gc9VZI", "cobertura e comparabilidade inferiores às referências selecionadas"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 35,
    "referenceIds": [f"obs-20260917-{n}" for n in range(166, 171)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260917-170"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 4,
    "internationalReferences": 0,
    "unknownOriginReferences": 1,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["humor","storytelling","identificacao","demonstracao","venda_indireta","comunidade"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"os cinco downloads de mídia falharam porque os manifestos expiraram por timeout e não expuseram formato disponível; as cinco capas também expiraram após 12 segundos sem bytes","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":2,"fullAutomatic":3,"partialAutomatic":0,"none":0,"limitation":"transcrições substituem apenas a fala; as automáticas contêm erros e censura"},
    "commentsCoverage": {"countsOnly":0,"sampledReferences":0,"sampledComments":0,"limitation":"contagens e comentários não foram adquiridos; comunidade e recepção permanecem não mensuradas"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"datas, escalas, produções e idades heterogêneas impedem benchmark de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["escalada local não preserva unidade editorial quando a publicação muda para premissas não relacionadas"],
    "safetyFindings": ["linguagem ofensiva e estereótipos foram registrados como limitação, não ensinados","nenhuma fala ou personagem foi recomendado para cópia","popularidade e produção foram mantidas como contexto não causal"],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes acrescentam recorrência à tensão cotidiana escalada sob a mesma regra. O padrão passa de três para seis apoios e recebe um segundo caso-limite; permanece provisório, sem audiovisual, retenção, riso ou teste causal.",
    "nextTarget": "esquete brasileira curta de criador pequeno ou médio com audiovisual integral, premissa única, comentários e teste de compreensão; procurar um caso comparável em que a escalada abandone a regra ou torne a premissa menos clara",
    "limitations": ["Nenhum audiovisual, áudio ou capa foi adquirido.","Datas de três publicações, curtidas e comentários ficaram não mensurados.","Uma das três referências-alvo é monólogo funcionalmente adjacente, comparação de nível 2.","Nenhum resultado autoriza causalidade ou validação."],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
