#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Rebuild the previous checkpoint and reuse the current schema helpers.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-030.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
classification = ns["classification"]
make_ref = ns["make_ref"]

NOW = "2026-09-18T11:25:09.000Z"
OBSERVED = "2026-09-18"
RUN_ID = "run-20260918-supervised-031"
PATTERN_ID = "pat-20260823-003"
BATCH_IDS = {f"obs-20260918-{n}" for n in range(171, 176)}

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
        production="unknown", scale="unknown", replicability="high", duration="over_60s",
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


def ref(**kwargs):
    item = make_ref(**kwargs)
    item["country"] = "BR"
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "conteúdo editorial público do próprio criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado identificável de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frases, analogias, personagens ou roteiro",
        "transformar percentuais gerais em prescrição financeira individual",
        "repetir promessa de riqueza, autoridade ou citação sem fonte verificável",
        "tratar comentários, visualizações, fama, mídia paga ou orçamento como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção",
    ]
    return item


refs = [
    ref(
        id="obs-20260918-171",
        title="Educação Financeira Básica: A REGRA DOS 3 FATORES",
        creator="Manual da Evolução", identity="manual-da-evolucao",
        url="https://www.youtube.com/watch?v=HSXcvFVtsdM",
        published="2024-08-08", duration="PT14M7S",
        accessible=[
            "título", "criador", "descrição pública", "data exata", "duração de 14 minutos e 7 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "504.033 visualizações, 23.817 curtidas e 358 comentários declarados nos metadados públicos",
            "amostra pública de 30 comentários", "sequência verbal dos três fatores financeiros",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "verificação externa dos percentuais e exemplos financeiros", "teste de compreensão"],
        metrics={"viewsObserved":504033,"likesObserved":23817,"commentsObserved":358},
        cls=cls(
            presentations=["camera_direta","tutorial"], primary="educativo",
            secondary=["autoridade_opiniao","demonstracao"],
            mix=[{"family":"educativo","percentage":70},{"family":"autoridade_opiniao","percentage":20},{"family":"demonstracao","percentage":10}],
            objectives=["educar","confianca","salvamento"],
            topic="três fatores para organizar finanças pessoais",
            segment="educação financeira", subsegment="orçamento e investimento para iniciantes",
            audience="adultos iniciantes que precisam organizar gastos, poupança e patrimônio",
            mechanisms=["aproximacao","alivio","confianca"], hooks=["problema","promessa"],
            narrative=["problema","promessa","progressao","mecanismo","conclusao"],
            proof=["mecanismo_explicado","tratamento_objecao"], cta=["outro_conteudo"],
            production="unknown", scale="medium", replicability="high",
            evidence=[
                "Entre 0:00 e 0:47, a fala anuncia três fatores e contextualiza a lacuna de educação financeira.",
                "Entre 0:47 e 4:14, organiza controle de gastos, faixas de comprometimento e objeções de renda e família.",
                "Entre 4:14 e 8:35, trata hábito de poupar, porcentagens graduais e aumento de renda.",
                "Entre 8:35 e 14:06, conecta patrimônio, reserva e investimento de longo prazo.",
            ],
        ),
        comparison={"level":1,"group":"explicador financeiro brasileiro de 10 a 30 minutos para iniciantes com problema explícito e caminho organizado","referenceIds":["obs-20260918-172","obs-20260918-173"],"confidence":"high"},
        observations=[
            "A fala define um mapa de três fatores antes de desenvolver o primeiro.",
            "Cada fator recebe exemplos, objeções e uma próxima ação verbalmente identificável.",
            "Comentários incluem dúvidas de aplicação a baixa renda, família e investimentos; não constituem teste de aprendizagem.",
        ],
        interpretations=[
            "O mapa finito torna problema e caminho rastreáveis na transcrição.",
            "Percentuais e produtos precisam de contexto individual; a recorrência estrutural não prova adequação financeira nem eficácia.",
        ],
        scores={"gancho":88,"clareza":94,"relevancia":89,"desejo":76,"confianca":82,"retencao":"not_assessed","acao":84,"objecoes":82},
        lenses={
            "apressado":"Recebe o assunto e os três fatores na abertura.",
            "analitico":"Consegue reconstruir a sequência e as ressalvas, mas não auditar todas as alegações.",
            "aspiracional":"A promessa é controle e progresso, não riqueza imediata.",
            "comunidade":"A amostra traz dúvidas práticas, sem representatividade estatística.",
            "cetico":"Desconta percentuais gerais, links afiliados e ausência de audiovisual e teste de resultado.",
        },
        replicable=["Nomear um mapa curto antes da explicação.","Tratar a objeção de renda antes de recomendar ação.","Separar controle, reserva e investimento sem copiar exemplos ou frases."],
        contingent=["Percentuais dependem de renda, custo de vida e composição familiar.","Livros e links afiliados são contexto comercial.","Comentários não demonstram aprendizagem ou desempenho."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"a fala explicita problema, mapa de três fatores e sequência de ações para iniciantes","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_full_automatic_transcript_and_30_public_comments",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260918-172",
        title="FAÇA ISSO SEMPRE QUE RECEBER SEU SALÁRIO | Como organizar suas finanças e guardar dinheiro?",
        creator="Bruno Perini - Você MAIS Rico", identity="bruno-perini-voce-mais-rico",
        url="https://www.youtube.com/watch?v=C67qPfI8_hg",
        published="2025-05-28", duration="PT21M12S",
        accessible=[
            "título", "criador", "descrição pública", "data exata", "duração de 21 minutos e 12 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "892.909 visualizações, 53.561 curtidas e 538 comentários declarados nos metadados públicos",
            "amostra pública de 30 comentários", "estrutura verbal de três promessas e orçamento em cinco fatias",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "verificação externa da simulação, depoimentos e produtos financeiros", "teste de compreensão"],
        metrics={"viewsObserved":892909,"likesObserved":53561,"commentsObserved":538},
        cls=cls(
            presentations=["camera_direta","tutorial","estudo_caso"], primary="educativo",
            secondary=["autoridade_opiniao","oferta_direta"],
            mix=[{"family":"educativo","percentage":65},{"family":"autoridade_opiniao","percentage":20},{"family":"oferta_direta","percentage":15}],
            objectives=["educar","autoridade","lead","venda"],
            topic="organização do salário, renda ativa e passiva e orçamento por categorias",
            segment="educação financeira", subsegment="orçamento e investimento para iniciantes",
            audience="adultos que querem guardar parte do salário e iniciar investimentos",
            mechanisms=["aproximacao","desejo","confianca","aversao_perda"], hooks=["problema","promessa"],
            narrative=["promessa","problema","mecanismo","progressao","prova","conclusao"],
            proof=["mecanismo_explicado","dado","depoimento"], cta=["clicar","comprar"],
            production="unknown", scale="large", replicability="medium",
            advertising="oferta_direta", intent="explicita",
            entity={"kind":"servico","name":"Viver de Renda, Finclass e Portfel","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:20, anuncia três entregas: armadilha, renda ativa/passiva e método.",
                "Entre 4:05 e 5:35, introduz o orçamento como guia e começa pela fatia de 15%.",
                "Entre 9:00 e 10:00, insere oferta extensa de cursos antes de retomar o orçamento.",
                "Entre 9:58 e 20:48, organiza 15%, 10%, 55%, 10% e 10%, com ressalvas por ocupação e renda.",
            ],
        ),
        comparison={"level":2,"group":"explicador financeiro brasileiro de 10 a 30 minutos para iniciantes com problema explícito e caminho organizado","referenceIds":["obs-20260918-171","obs-20260918-173"],"confidence":"high"},
        observations=[
            "A abertura promete um percurso finito e a fala conclui com um orçamento em cinco fatias.",
            "A oferta ocupa trecho intermediário; comentários amostrados registram tanto utilidade quanto objeção à interrupção comercial e à aplicabilidade para baixa renda.",
            "O próprio apresentador chama os percentuais de sugestão ajustável, não regra universal.",
        ],
        interpretations=[
            "O caminho organizado é rastreável, mas a venda no meio da explicação acrescenta uma objeção independente do conteúdo financeiro.",
            "É apoio estrutural de nível 2; não prova que o orçamento seja adequado a todo perfil ou que a oferta aumente conversão.",
        ],
        scores={"gancho":91,"clareza":90,"relevancia":86,"desejo":82,"confianca":75,"retencao":"not_assessed","acao":88,"objecoes":66},
        lenses={
            "apressado":"Recebe três entregas logo no começo, mas encontra uma oferta longa no meio.",
            "analitico":"Enxerga categorias e ressalvas; exige auditoria das simulações e produtos.",
            "aspiracional":"Liberdade financeira organiza o desejo, sem garantir resultado.",
            "comunidade":"Comentários expõem perfis de renda e família que pedem adaptação.",
            "cetico":"Questiona conflito comercial, depoimentos, seguro parceiro e generalização dos percentuais.",
        },
        replicable=["Anunciar entregas antes do desenvolvimento.","Organizar a solução em categorias que somam o todo.","Declarar que percentuais são ponto de partida ajustável."],
        contingent=["Oferta de cursos e seguro cria interesse comercial explícito.","Percentuais e ativos exigem adequação ao perfil e ao contexto.","Comentários são amostra não representativa."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"a fala explicita problema, três entregas e orçamento organizado antes da conclusão","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_full_automatic_transcript_and_30_public_comments",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260918-173",
        title="NOVO GUIA BÁSICO pra começar a investir com POUCO DINHEIRO! Saiba tudo em 10 minutos",
        creator="Me Poupe!", identity="me-poupe",
        url="https://www.youtube.com/watch?v=JtDrb2BPBf4",
        published="2025-06-16", duration="PT10M8S",
        accessible=[
            "título", "criador", "descrição pública", "data exata", "duração de 10 minutos e 8 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "238.679 visualizações, 17.042 curtidas e 293 comentários declarados nos metadados públicos",
            "amostra pública de 30 comentários", "perguntas de iniciante e comparação falada de alternativas",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "auditoria da simulação e da adequação dos produtos citados", "teste de compreensão"],
        metrics={"viewsObserved":238679,"likesObserved":17042,"commentsObserved":293},
        cls=cls(
            presentations=["camera_direta","tutorial","personagem_marca"], primary="educativo",
            secondary=["humor","demonstracao"],
            mix=[{"family":"educativo","percentage":65},{"family":"humor","percentage":20},{"family":"demonstracao","percentage":15}],
            objectives=["educar","comentario","compartilhamento","lead"],
            topic="primeiro investimento com pouco dinheiro",
            segment="educação financeira", subsegment="investimento para iniciantes",
            audience="adultos iniciantes com pouco ou nenhum valor disponível para investir",
            mechanisms=["aproximacao","humor","desejo","confianca"], hooks=["promessa","problema"],
            narrative=["promessa","progressao","situacao","prova","mecanismo","conclusao"],
            proof=["mecanismo_explicado","dado"], cta=["comentar","compartilhar","clicar"],
            production="unknown", scale="large", replicability="medium",
            advertising="geracao_de_leads", intent="explicita",
            entity={"kind":"produto","name":"Me Poupe+","confidence":"high"},
            evidence=[
                "Entre 0:00 e 1:03, declara nível básico e lista as perguntas que serão respondidas.",
                "Entre 1:36 e 2:47, define investimento e trata por que iniciantes não investem.",
                "Entre 4:49 e 8:18, usa exemplo de aportes e juros compostos para ordenar a decisão de começar cedo.",
                "Entre 8:28 e 9:47, apresenta critérios e opções para quem começa com pouco ou nada.",
            ],
        ),
        comparison={"level":1,"group":"explicador financeiro brasileiro de 10 a 30 minutos para iniciantes com problema explícito e caminho organizado","referenceIds":["obs-20260918-171","obs-20260918-172"],"confidence":"high"},
        observations=[
            "A promessa de nível básico e as perguntas do roteiro aparecem antes da primeira definição.",
            "A transcrição oferece conceito, comparação, simulação e próximo passo para pouco dinheiro.",
            "Comentários repetem o CTA e também pedem esclarecimentos sobre banco, idade e segurança; alguns corrigem indicação desatualizada.",
        ],
        interpretations=[
            "Perguntas explícitas funcionam como mapa semântico para o iniciante.",
            "A utilidade estrutural não valida produtos citados; atualização e revisão financeira continuam necessárias.",
        ],
        scores={"gancho":93,"clareza":91,"relevancia":90,"desejo":84,"confianca":72,"retencao":"not_assessed","acao":90,"objecoes":70},
        lenses={
            "apressado":"Recebe a promessa básica e as perguntas em menos de um minuto.",
            "analitico":"Consegue seguir definições e simulação, mas precisa revisar produtos e cálculo.",
            "aspiracional":"Começar com pouco sustenta desejo sem depender só de riqueza rápida.",
            "comunidade":"CTA produz repetição nos comentários, mas dúvidas persistem.",
            "cetico":"Rejeita produto citado sem atualização, simulação não auditada e linguagem absoluta.",
        },
        replicable=["Declarar para quem é a aula e quais dúvidas resolve.","Ordenar conceito, comparação e próximo passo.","Usar exemplo numérico com premissas explícitas e revisáveis."],
        contingent=["Produto digital e marca pessoal são interesses comerciais.","Instituições e taxas mudam com o tempo.","Comentários não medem compreensão ou segurança da decisão."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"a fala explicita problemas de iniciante, mapa de perguntas e caminho de decisão","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True}],
        source_type="youtube_public_metadata_full_automatic_transcript_and_30_public_comments",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260918-174",
        title="BILIONÁRIO REVELA: COMO USAR UM SALÁRIO MÍNIMO PARA FICAR RICO! - Dicas de um Bilionário",
        creator="Topo da Mente", identity="topo-da-mente",
        url="https://www.youtube.com/watch?v=dgkR1LtHFNw",
        published="2025-08-11", duration="PT25M29S",
        accessible=[
            "título", "criador", "descrição pública", "data exata", "duração de 25 minutos e 29 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "640.835 visualizações, 30.549 curtidas e aproximadamente 1.300 comentários nos metadados públicos",
            "amostra pública de 50 comentários", "promessa de riqueza, método de poupança e objeções públicas",
        ],
        missing=MISSING_AV + ["baseline funcional contemporâneo", "fonte primária para citações e casos atribuídos a Warren Buffett", "auditoria dos cálculos e da promessa de riqueza", "teste de compreensão"],
        metrics={"viewsObserved":640835,"likesObserved":30549,"commentsObserved":1300},
        cls=cls(
            presentations=["narracao_imagens","comentario","tutorial"], primary="inspiracao",
            secondary=["educativo","autoridade_opiniao"],
            mix=[{"family":"inspiracao","percentage":50},{"family":"educativo","percentage":30},{"family":"autoridade_opiniao","percentage":20}],
            objectives=["visualizacao","apresentar_solucao","educar"],
            topic="enriquecimento a partir de salário mínimo por hábitos e investimentos",
            segment="educação financeira", subsegment="mentalidade e investimento para baixa renda",
            audience="adultos de baixa renda buscando independência financeira",
            mechanisms=["desejo","aversao_perda","admiracao","medo"], hooks=["promessa","autoridade","conflito"],
            narrative=["problema","promessa","prova","progressao","situacao","conclusao"],
            proof=["autoridade_percebida","dado","alegacao_sem_prova"], cta=[],
            production="unknown", scale="medium", replicability="high",
            advertising="indeterminado", intent="indeterminada",
            evidence=[
                "Entre 0:00 e 3:28, atribui pobreza a método e mentalidade, usando Warren Buffett como autoridade.",
                "Entre 3:28 e 10:58, desenvolve separação automática, aportes pequenos e tempo.",
                "Entre 13:49 e 18:09, desloca a solução para cortes cotidianos e hábitos.",
                "Entre 18:09 e 25:09, acrescenta renda extra e visualização aspiracional sem fonte observável para os casos.",
                "Na amostra de 50 comentários, aparecem objeções à promessa, ao salário mínimo, ao prazo sugerido pela capa e à ausência de indicação concreta.",
            ],
        ),
        comparison={"level":1,"group":"explicador financeiro brasileiro de 10 a 30 minutos para iniciantes com promessa ampla e caminho organizado","referenceIds":["obs-20260918-171","obs-20260918-172","obs-20260918-173"],"confidence":"high"},
        observations=[
            "A fala oferece um caminho organizado, mas o título e a descrição prometem riqueza com salário mínimo e autoridade de bilionário.",
            "Atribuições, casos e citações não vieram acompanhados de fontes verificáveis na cobertura acessível.",
            "A amostra contém tanto identificação quanto múltiplas objeções explícitas à promessa e à aplicabilidade.",
        ],
        interpretations=[
            "Caminho claro não neutraliza custo de prova quando a promessa e a autoridade emprestada excedem a evidência acessível.",
            "É caso-limite, não contraexemplo causal: comentários são amostra e retenção, confiança e resultado não foram medidos.",
        ],
        scores={"gancho":94,"clareza":80,"relevancia":78,"desejo":93,"confianca":44,"retencao":"not_assessed","acao":76,"objecoes":38},
        lenses={
            "apressado":"Recebe promessa extrema e antagonismo social imediatamente.",
            "analitico":"Encontra método, mas não fontes para autoridade, casos e algumas contas.",
            "aspiracional":"Riqueza e liberdade concentram o desejo.",
            "comunidade":"Comentários dividem identificação e descrença; amostra não representa a audiência.",
            "cetico":"Questiona shaming, promessa, prazo, contexto do salário e citação sem fonte.",
        },
        replicable=["Converter problema em sequência concreta e gradual.","Explicitar premissas e limites dos exemplos numéricos."],
        contingent=["Título hiperbólico e autoridade emprestada elevam o custo de prova.","Contexto de salário mínimo e custo de vida varia.","Casos, citações e promessa não foram verificados."],
        role="case_limit", evidence_level=1, eligible=False,
        claims=[
            {"claim":"o conteúdo combina promessa ampla, autoridade emprestada e um caminho organizado","requiredModalities":["title","description","transcript"],"observedModalities":["title","description","transcript"],"sufficient":True},
            {"claim":"a promessa causa pior desempenho ou menor confiança","requiredModalities":["experiment","retention"],"observedModalities":["comments"],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_automatic_transcript_and_50_public_comments",
        comment_provenance=True,
    ),
    ref(
        id="obs-20260918-175",
        title="O CAMINHO MAIS RÁPIDO NÃO É O QUE PARECE!",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=alzphVrX3dU",
        published="2022-01-29", duration="PT15M17S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 15 minutos e 17 segundos",
            "transcrição automática integral em português com timestamps", "fala por substituição textual",
            "6.904.463 visualizações, 244.347 curtidas e aproximadamente 2.700 comentários nos metadados públicos",
            "pergunta, previsões, testes e explicações verbalmente observáveis",
        ],
        missing=MISSING_AV + ["amostra de comentários", "confirmação visual das rampas e resultados", "baseline funcional contemporâneo", "verificação independente da explicação matemática"],
        metrics={"viewsObserved":6904463,"likesObserved":244347,"commentsObserved":2700},
        cls=cls(
            presentations=["demonstracao","dialogo","tutorial"], primary="demonstracao",
            secondary=["educativo","curiosidade"],
            mix=[{"family":"demonstracao","percentage":60},{"family":"educativo","percentage":30},{"family":"curiosidade","percentage":10}],
            objectives=["educar","retencao","compartilhamento"],
            topic="braquistócrona, cicloide e tempo de descida",
            segment="divulgação científica", subsegment="física e matemática experimental",
            audience="público geral curioso sobre experimentos de movimento",
            mechanisms=["curiosidade","surpresa","recompensa","confianca"], hooks=["pergunta","afirmacao_contraintuitiva","promessa"],
            narrative=["problema","promessa","tentativa","prova","mecanismo","progressao","conclusao"],
            proof=["demonstracao","mecanismo_explicado"], cta=["outro_conteudo"],
            production="unknown", scale="large", replicability="medium",
            evidence=[
                "Entre 0:00 e 1:30, pergunta, palpite, primeiro teste e resultado são verbalmente identificáveis.",
                "Entre 1:30 e 4:26, novos formatos testam o limite da regra e preservam um palpite que falha.",
                "Entre 4:46 e 12:46, cicloide, braquistócrona e tautócrona organizam a progressão conceitual.",
                "Entre 12:46 e 14:26, imprecisão de construção, repetição e limite de atrito são reconhecidos na fala.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de demonstração científica; fora do grupo financeiro-alvo","referenceIds":[],"confidence":"high"},
        observations=[
            "A transcrição preserva pergunta, previsões, testes, correção e limite experimental.",
            "O resultado visual das corridas não foi visto; somente falas e descrição sustentam a progressão.",
            "A referência não foi usada para apoiar o padrão financeiro nem criou hipótese nova.",
        ],
        interpretations=[
            "Uma demonstração pode transformar erro de palpite em explicação quando a variável é nomeada.",
            "O caso é exploração controlada e não autoriza inferência sobre ritmo, retenção ou efeito visual.",
        ],
        scores={"gancho":90,"clareza":92,"relevancia":86,"desejo":78,"confianca":88,"retencao":"not_assessed","acao":72,"objecoes":86},
        lenses={
            "apressado":"Recebe pergunta e disputa entre reta e curva logo no início.",
            "analitico":"Consegue seguir hipóteses e limites na fala, sem confirmar visualmente os testes.",
            "aspiracional":"A recompensa é compreender uma solução contraintuitiva.",
            "comunidade":"Contagem de comentários existe, mas nenhuma amostra foi observada.",
            "cetico":"Aceita progressão verbal e exige vídeo e revisão técnica para resultado visual.",
        },
        replicable=["Antecipar a pergunta antes do aparato.","Preservar um palpite que falha e nomear a variável.","Separar resultado observado, explicação e limite experimental."],
        contingent=["Construção e medição exigem precisão técnica.","Produção do canal e escala de audiência não são replicáveis por padrão.","Resultados visuais não foram auditados."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"a fala organiza pergunta, previsões, testes, resultados declarados e limites","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"as bolinhas e rampas produziram exatamente os resultados visuais descritos","requiredModalities":["video"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_description_and_full_automatic_transcript",
        comment_provenance=False,
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 031")

memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20260918-171", "obs-20260918-172", "obs-20260918-173"]
new_case = "obs-20260918-174"
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 8
pattern["supportingCount"] = 8
pattern["caseLimitCount"] = 1
pattern["creatorDiversityCount"] = 8
pattern["sourceDiversityCount"] = 8
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20260918-171","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Três fatores organizam controle de gastos, hábito de poupar e administração do patrimônio, com objeções de renda e família.","evidence":"Metadados, descrição, transcrição automática integral e 30 comentários amostrados.","limitations":["sem audiovisual ou teste de compreensão","percentuais financeiros não auditados"]},
    {"referenceId":"obs-20260918-172","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Três entregas antecipadas conduzem a orçamento em cinco fatias; percentuais são apresentados como sugestão ajustável.","evidence":"Metadados, descrição, transcrição automática integral e 30 comentários amostrados.","limitations":["oferta comercial longa no meio","simulações, depoimentos e produtos não auditados"]},
    {"referenceId":"obs-20260918-173","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Perguntas de iniciante anunciam conceito, comparação, simulação e próximo passo para pouco dinheiro.","evidence":"Metadados, descrição, transcrição automática integral e 30 comentários amostrados.","limitations":["instituições e taxas mudam","sem audiovisual ou teste de compreensão"]},
    {"referenceId":"obs-20260918-174","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"Promessa de riqueza com salário mínimo e autoridade emprestada coexistem com caminho organizado; comentários expõem objeções à promessa e aplicabilidade.","evidence":"Metadados, descrição, transcrição automática integral e 50 comentários amostrados.","limitations":["comentários não são representativos","retenção, confiança e causalidade não medidas","fontes e cálculos não auditados"]},
])
pattern["limitations"] = [
    "Oito apoios formais vêm de oito criadores e oito fontes; demonstram recorrência estrutural, não relevância, aprendizagem, confiança, retenção ou resultado financeiro.",
    "Os três novos apoios possuem transcrição integral e 90 comentários amostrados, mas nenhum teste de compreensão ou baseline funcional contemporâneo.",
    "Percentuais, produtos, simulações e recomendações financeiras exigem adequação individual e revisão atual; estrutura clara não valida conselho financeiro.",
    "O primeiro caso-limite mostra que caminho organizado não elimina objeções quando promessa, prazo ou autoridade excedem a evidência acessível.",
    "Ofertas comerciais intermediárias e perfis de renda heterogêneos aparecem como fontes de objeção na amostra, sem prova de efeito causal.",
    "Nenhum audiovisual, capa, áudio ouvido, texto na tela, edição, ritmo ou retenção foi auditado neste lote.",
    "Popularidade, fama, produção e monetização são contexto, nunca prova causal.",
    "Validação exige revisão humana ou evidência experimental apropriada.",
]

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("in0XbfQEm2A", "conteúdo comparável, mas redundante com canal grande e sem vantagem de cobertura sobre os três escolhidos"),
        ("VLypOc9mdX8", "40 minutos; duração fora da condição de 10 a 30 minutos"),
        ("bidkGCz7eHM", "comparável, mas redundante com estrutura de organização já coberta"),
        ("EA2aFfOXPA8", "explicação macroeconômica, não caminho pessoal para iniciante"),
        ("iJJhlHQtGXo", "autoridade atribuída e promessa de riqueza com cobertura inferior ao caso-limite selecionado"),
        ("UMxSHX712qo", "palestra TED funcionalmente adjacente, mas fora da prioridade de criadores brasileiros da watchlist"),
        ("69l-iaw_Vz0", "finanças de pequeno negócio, público diferente"),
        ("4Z2Im13A_bw", "podcast de 95 minutos e múltiplos convidados; comparação de duração inadequada"),
        ("VyYB5WCI9rw", "36 minutos e reação a TikToks; formato e duração menos comparáveis"),
        ("zAJgVIOw6KU", "foco em instrumentos de renda fixa, não organização do problema pessoal"),
        ("8cPE9bOHXrw", "candidato replicável, mas redundante e com cobertura inferior aos selecionados"),
        ("HKnIAKdZHAs", "audiobook de 70 minutos e origem editorial pouco clara"),
        ("-3gtPazi79U", "foco em aprendizagem autônoma de investimento, não organização financeira básica"),
        ("7IrionoCYfk", "canal e origem com proveniência insuficiente na triagem"),
        ("SJ7-ImU4UYc", "planilha e captura de lead dominam a promessa; redundante com caminho organizado"),
        ("vknO2aLRhto", "lista de investimentos de 2026, dependente de contexto temporal"),
        ("ux3JFdRb5C0", "transformação pessoal e dívidas; duração acima do grupo comparável"),
        ("oLMxWL2w5PY", "orçamento doméstico comparável, mas publicado em 2023 e redundante com apoio mais recente"),
        ("_WLB4zeM__U", "curso completo de quase seis horas"),
        ("jYX23vniMOA", "vídeo de 59 segundos, insuficiente para comparação de 10 a 30 minutos"),
        ("p6jL2SBwkhA", "podcast de quase duas horas, público e apresentação divergentes"),
        ("Lxe4FAI-g6s", "exploração científica alternativa; risco elétrico e cobertura inferior ao caso selecionado"),
        ("W9AO7g2Cgdc", "exploração científica alternativa com foguete; produção e segurança menos replicáveis"),
        ("YzFGVZyAXKo", "exploração científica alternativa redundante"),
        ("H09iLSrkAiY", "colaboração e produção complexa reduzem replicabilidade"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 45,
    "referenceIds": [f"obs-20260918-{n}" for n in range(171, 176)],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20260918-175"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 2,
    "replicableReferences": 5,
    "creativeFamiliesObserved": ["educativo","autoridade_opiniao","demonstracao","humor","inspiracao","curiosidade","oferta_direta"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"os formatos públicos foram enumerados, mas as cinco aquisições de vídeo falharam por timeout ou HTTP 502; as cinco capas expiraram sem bytes","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":5,"partialAutomatic":0,"none":0,"limitation":"transcrições automáticas substituem apenas a fala e podem conter erros"},
    "commentsCoverage": {"countsOnly":1,"sampledReferences":4,"sampledComments":140,"limitation":"amostras públicas não são representativas e não medem aprendizagem, confiança ou desempenho"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"canais, datas, ofertas e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["caminho organizado não neutraliza objeções quando promessa, prazo ou autoridade excedem a evidência acessível"],
    "safetyFindings": [
        "alegações e recomendações financeiras não foram ensinadas como verdade nem prescrição individual",
        "autoridade, citações, casos e cálculos não verificados foram marcados como custo de prova",
        "comentários e métricas permaneceram contexto não causal",
        "nenhuma frase, analogia ou roteiro foi recomendado para cópia",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes acrescentam recorrência ao problema explícito seguido de caminho organizado em educação financeira para iniciantes. O padrão passa de cinco para oito apoios e recebe o primeiro caso-limite; permanece provisório e não valida conselho financeiro, confiança, aprendizagem, retenção ou desempenho.",
    "nextTarget": "explicador financeiro brasileiro de criador pequeno ou médio, com audiovisual integral, linguagem proporcional à renda, disclosure separado da aula e teste de compreensão; procurar um caso comparável em que o caminho seja claro, mas gere erro de aplicação ou decisão insegura",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "As cinco transcrições são automáticas e podem conter erros.",
        "Quatro amostras somam 140 comentários, sem representatividade estatística.",
        "Produtos, taxas, simulações, citações e recomendações financeiras não foram auditados.",
        "Nenhum resultado autoriza causalidade ou validação.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
