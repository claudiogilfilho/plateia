#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-044.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]

NOW = "2026-10-03T11:12:38.000Z"
OBSERVED = "2026-10-03"
RUN_ID = "run-20261003-supervised-045"
PATTERN_ID = "pat-20260904-009"
BATCH_IDS = {f"obs-20261003-{n}" for n in range(241, 246)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

GROUP = "demonstração ou protótipo que mantém uma falha observável, nomeia uma variável ou limite e executa uma revisão rastreável"
MISSING_COMMON = MISSING_AV + [
    "teste representativo de compreensão ou confiança",
    "comparação causal controlada",
    "reprodução independente do resultado",
]

refs = [
    build_ref(
        id="obs-20261003-241",
        title="ELE EXPLODIU... então FIZEMOS OUTRO! DEU BOM?",
        creator="Manual do Mundo", identity="manual-do-mundo",
        url="https://www.youtube.com/watch?v=6VhEDnVy254",
        published="2026-06-16", duration="PT24M37S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 24 minutos e 37 segundos, 1.025.016 visualizações, 76.727 curtidas e 1.300 comentários indicados em 3 de outubro de 2026",
            "transcrição automática integral em português até 24 minutos e 38 segundos; fala acessível somente por substituição textual",
            "descrição e fala ligam a explosão do primeiro pião a desequilíbrio, rotação, estrutura de impressão 3D e gesso não totalmente curado; a segunda construção troca materiais, revê massa e é testada novamente",
            "vinte comentários públicos amostrados; perguntas e elogios não constituem teste de compreensão ou segurança",
        ],
        missing=MISSING_COMMON + ["medição instrumental das forças e da rotação", "auditoria visual da explosão e do teste final"],
        metrics={"viewsObserved":1025016,"likesObserved":76727,"commentsObserved":1300,"commentsSampled":20},
        classification=cls(
            material="video_longo", presentations=["demonstracao","bastidores","camera_direta"], primary="demonstracao",
            secondary=["transformacao","educativo"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"transformacao","percentage":30},{"family":"educativo","percentage":20}],
            objectives=["educar","visualizacao","confianca"],
            topic="reconstrução e teste de um pião gigante após falha estrutural", segment="ciência e engenharia maker", subsegment="rotação, materiais e prototipagem",
            audience="público geral interessado em ciência, construção e projetos maker", awareness="inconsciente",
            production="complex", scale="large", replicability="medium", duration="over_60s",
            mechanisms=["curiosidade","surpresa","confianca","recompensa"], hooks=["conflito","resultado_antecipado"],
            narrative=["problema","tentativa","mecanismo","progressao","virada","conclusao"], proof=["demonstracao","mecanismo_explicado"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "A descrição recupera o desfecho não planejado do primeiro pião e promete uma versão resistente e equilibrada.",
                "A fala relaciona a falha anterior a materiais, cura incompleta, desequilíbrio e rotação; essas relações permanecem hipóteses do criador, não ensaio causal.",
                "A revisão troca a casca e o preenchimento por camadas de MDF e EVA, revê a massa e descreve novo teste estável.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20261003-242","obs-20261003-243"],"confidence":"high"},
        observations=[
            "A falha anterior não é apagada: ela organiza a escolha de materiais, o balanceamento e o limite de velocidade da segunda versão.",
            "O criador distingue cálculo prévio, hipótese de causa e resultado declarado do novo teste.",
            "A escala, a oficina e a popularidade são contexto; não demonstram compreensão ou retenção.",
        ],
        interpretations=[
            "Preservar a falha e nomear o que foi alterado torna a revisão do protótipo rastreável na fala.",
            "Sem audiovisual e medição independente, não se conclui que cada variável causou a melhora.",
        ],
        scores={"gancho":94,"clareza":92,"relevancia":87,"desejo":82,"confianca":84,"retencao":"not_assessed","acao":68,"objecoes":79},
        lenses={
            "apressado":"Entende de imediato que houve explosão e uma segunda tentativa.",
            "analitico":"Consegue rastrear materiais, massa, equilíbrio e rotação, mas pede medições e controle de variáveis.",
            "aspiracional":"Vê uma falha convertida em projeto revisado.",
            "comunidade":"Comentários trazem perguntas e entusiasmo, sem teste representativo.",
            "cetico":"Separa a hipótese verbal sobre a causa de uma demonstração causal independente.",
        },
        replicable=["Recuperar a falha antes da nova tentativa.","Nomear materiais, limites e decisões alteradas.","Distinguir hipótese de causa do resultado do reteste."],
        contingent=["Projeto, oficina e orçamento são pouco replicáveis.","Hipóteses de causa não foram isoladas.","Audiovisual e retenção não foram observados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala liga a falha anterior a variáveis e registra uma revisão seguida de novo teste","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
    build_ref(
        id="obs-20261003-242",
        title="AGORA FOI! - Mudei TUDO, FUREI O PISTÃO e o TETO FUNCIONOU! - TETO POP UP PARA KOMBIHOME",
        creator="Philomena Estradeira", identity="philomena-estradeira",
        url="https://www.youtube.com/watch?v=VeWC1oA8hLA",
        published="2021-09-19", duration="PT15M48S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 15 minutos e 48 segundos, 25.004 visualizações, 1.970 curtidas e 75 comentários indicados em 3 de outubro de 2026",
            "transcrição automática integral em português até 15 minutos e 49 segundos; fala acessível somente por substituição textual e com alguns termos ruidosos",
            "descrição e fala registram teto que não fechava, testes de ângulo, identificação da força excessiva dos amortecedores, tentativa intermediária e substituição por suportes articulados de metal",
            "vinte comentários públicos amostrados; um comentário declara intenção de aplicar a ideia, sem confirmar execução",
        ],
        missing=MISSING_COMMON + ["cálculo estrutural independente", "auditoria visual do movimento, das travas e da segurança"],
        metrics={"viewsObserved":25004,"likesObserved":1970,"commentsObserved":75,"commentsSampled":20},
        classification=cls(
            material="video_longo", presentations=["demonstracao","bastidores","transformacao"], primary="transformacao",
            secondary=["demonstracao","storytelling"],
            mix=[{"family":"transformacao","percentage":45},{"family":"demonstracao","percentage":35},{"family":"storytelling","percentage":20}],
            objectives=["apresentar_solucao","educar","confianca"],
            topic="revisão do mecanismo de teto elevatório de uma Kombi", segment="faça você mesmo e construção veicular", subsegment="protótipo de teto pop-up",
            audience="pessoas construindo motorhomes e interessadas em soluções maker", awareness="consciente_solucao",
            production="intermediate", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","alivio","confianca","recompensa"], hooks=["resultado_antecipado","conflito"],
            narrative=["problema","tentativa","mecanismo","virada","transformacao","conclusao"], proof=["demonstracao","mecanismo_explicado"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "A descrição informa abandono da estrutura anterior e adoção de outro mecanismo.",
                "A fala diz que trocar o ângulo não resolveu e atribui o bloqueio à força e à geometria dos amortecedores.",
                "Uma unidade articulada é montada e testada antes de ser replicada; o funcionamento final é declarado na fala e no título.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20261003-241","obs-20261003-243"],"confidence":"medium"},
        observations=[
            "O vídeo preserva tentativas anteriores, elimina uma hipótese de ângulo e explica por que o amortecedor impedia o fechamento.",
            "O plano B é prototipado em uma peça antes da replicação, tornando a revisão rastreável na fala.",
            "Perfurar um amortecedor apesar do aviso de não perfurar é risco observável e não foi extraído como princípio replicável.",
        ],
        interpretations=[
            "Falha, diagnóstico e protótipo intermediário formam uma cadeia de revisão comparável ao alvo.",
            "O resultado declarado não substitui cálculo estrutural, teste de segurança ou auditoria visual.",
        ],
        scores={"gancho":90,"clareza":87,"relevancia":91,"desejo":79,"confianca":73,"retencao":"not_assessed","acao":70,"objecoes":67},
        lenses={
            "apressado":"Recebe cedo que o teto finalmente funcionará após mudanças.",
            "analitico":"Rastreia hipótese, força do amortecedor, plano B e protótipo; pede cálculo e ensaio de segurança.",
            "aspiracional":"Vê uma construção travada avançar por revisão concreta.",
            "comunidade":"Um comentário declara intenção de uso, mas não demonstra execução segura.",
            "cetico":"Rejeita a perfuração do amortecedor como conselho e exige validação estrutural.",
        },
        replicable=["Registrar as hipóteses já testadas.","Explicar por que o mecanismo anterior limitava o projeto.","Prototipar uma unidade antes de replicar."],
        contingent=["A solução física depende do veículo e da estrutura.","A perfuração do amortecedor não é recomendável.","Mídia, segurança e retenção não foram auditadas."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala liga falha, diagnóstico, mudança de mecanismo e teste do protótipo","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
    build_ref(
        id="obs-20261003-243",
        title="Carbon snake, bi-carb version, part 2 (including reaction equations)",
        creator="Science with Heen", identity="science-with-heen",
        url="https://www.youtube.com/watch?v=qmg9bwsmXKA",
        published="2021-04-10", duration="PT23M7S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 23 minutos e 7 segundos, 60 visualizações e uma curtida indicadas em 3 de outubro de 2026; contagem pública de comentários não mensurada",
            "transcrição automática integral em inglês até 23 minutos e 6 segundos; fala acessível somente por substituição textual",
            "descrição e fala identificam a segunda tentativa, a mudança da ordem entre combustível e mistura, o resultado melhor e as equações das reações",
            "nenhum comentário público foi retornado na coleta",
        ],
        missing=MISSING_COMMON + ["quantidades exatas e repetição controlada", "auditoria visual do crescimento da serpente", "métrica pública de comentários"],
        metrics={"viewsObserved":60,"likesObserved":1,"commentsObserved":"not_assessed","commentsSampled":0},
        classification=cls(
            material="video_longo", presentations=["demonstracao","tutorial","camera_direta"], primary="demonstracao",
            secondary=["educativo","explicativo"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":30},{"family":"explicativo","percentage":20}],
            objectives=["educar","confianca","visualizacao"],
            topic="segunda tentativa de serpente de carbono com bicarbonato", segment="ciência e educação", subsegment="química experimental",
            audience="estudantes e educadores interessados em reações químicas", awareness="consciente_solucao",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","confianca","recompensa"], hooks=["narrativo","problema"],
            narrative=["problema","tentativa","mecanismo","progressao","conclusao"], proof=["demonstracao","mecanismo_explicado","dado"],
            cta=[], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "A descrição declara que esta é a segunda tentativa e que funcionou melhor.",
                "A fala muda explicitamente a ordem: combustível na areia antes da mistura de açúcar e bicarbonato.",
                "Após o resultado declarado melhor, a fala explica decomposição, combustão e produção de gases por equações.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261003-241","obs-20261003-242"],"confidence":"high"},
        observations=[
            "A falha anterior é mantida como ponto de partida, uma variável operacional é alterada e o resultado comparativo é declarado.",
            "A explicação química vem depois da revisão do procedimento.",
            "Fogo e etanol exigem supervisão e controle; replicabilidade estrutural não é recomendação de execução doméstica.",
        ],
        interpretations=[
            "Nomear a única alteração principal antes do reteste torna a comparação especialmente rastreável.",
            "Uma tentativa melhor não isola causalidade sem quantidades, repetição e controle.",
        ],
        scores={"gancho":78,"clareza":94,"relevancia":88,"desejo":70,"confianca":86,"retencao":"not_assessed","acao":62,"objecoes":82},
        lenses={
            "apressado":"Entende pela descrição que é a segunda tentativa e houve melhora.",
            "analitico":"Encontra a variável alterada e equações, mas pede quantidades e repetição.",
            "aspiracional":"Vê uma falha convertida em explicação química.",
            "comunidade":"Nenhum comentário público foi retornado.",
            "cetico":"Aceita a rastreabilidade e rejeita causalidade sem controle.",
        },
        replicable=["Declarar que se trata de uma segunda tentativa.","Nomear a alteração operacional antes do reteste.","Explicar o mecanismo depois do resultado."],
        contingent=["Fogo e etanol exigem controle de segurança.","Uma única repetição não prova causalidade.","Audiovisual e retenção não foram observados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[
            {"claim":"a fala nomeia a ordem alterada, o resultado melhor e o mecanismo químico","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261003-244",
        title="Testei os experimentos mais virais do YouTube (deu ruim)",
        creator="Bia On", identity="bia-on",
        url="https://www.youtube.com/watch?v=Hs288TLlPgw",
        published="2026-04-12", duration="PT9M39S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 9 minutos e 39 segundos, 120 visualizações, 26 curtidas e 14 comentários indicados em 3 de outubro de 2026",
            "transcrição automática integral em português até 9 minutos e 41 segundos; fala acessível somente por substituição textual e com trechos ruidosos",
            "fala registra várias tentativas, resultados ausentes, vento como possível interferência em um teste e julgamentos de que desafios eram falsos",
            "todos os 14 comentários públicos retornados foram amostrados; elogios e pedidos não testam o procedimento",
        ],
        missing=MISSING_COMMON + ["procedimentos completos de cada teste", "controle das interferências", "auditoria visual dos resultados"],
        metrics={"viewsObserved":120,"likesObserved":26,"commentsObserved":14,"commentsSampled":14},
        classification=cls(
            material="video_longo", presentations=["reacao","demonstracao","montagem"], primary="reacao",
            secondary=["comparacao","entretenimento"],
            mix=[{"family":"reacao","percentage":45},{"family":"comparacao","percentage":30},{"family":"entretenimento","percentage":25}],
            objectives=["visualizacao","comentario"],
            topic="teste de experimentos virais", segment="entretenimento e ciência caseira", subsegment="checagem informal de desafios virais",
            audience="público jovem interessado em desafios e experimentos", awareness="inconsciente",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","surpresa","humor"], hooks=["promessa","conflito"],
            narrative=["promessa","tentativa","problema","progressao","cta"], proof=["demonstracao","ausencia_prova_necessaria"],
            cta=["seguir","comentar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "A fala repete testes e registra que alguns não produziram o efeito esperado.",
                "Vento é mencionado como possível interferência em um teste, mas não é controlado.",
                "O rótulo de falso aparece antes de isolar erro de execução, material, ambiente ou premissa.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20261003-241","obs-20261003-242","obs-20261003-243"],"confidence":"medium"},
        observations=[
            "A falha permanece na narrativa, mas as variáveis não são isoladas de modo rastreável.",
            "A possibilidade de vento ou erro de execução é reconhecida e depois substituída por julgamento amplo de falsidade.",
            "Chama, álcool e luva rasgada aparecem na fala; o conteúdo não foi tratado como instrução segura.",
        ],
        interpretations=[
            "É caso-limite, não contraexemplo: mostrar que algo falhou não basta para transformar a falha em explicação.",
            "Uma checagem informal precisa separar premissa falsa, erro de execução e interferência ambiental.",
        ],
        scores={"gancho":86,"clareza":69,"relevancia":76,"desejo":72,"confianca":43,"retencao":"not_assessed","acao":78,"objecoes":41},
        lenses={
            "apressado":"Entende a promessa de testar virais e ver falhas.",
            "analitico":"Não recebe controle suficiente para distinguir falsidade de execução ruim.",
            "aspiracional":"Vê tentativa e erro, mas pouco aprendizado transferível.",
            "comunidade":"Comentários celebram o vídeo; não corrigem ou reproduzem os testes.",
            "cetico":"Rejeita o rótulo de falso sem isolamento de alternativas.",
        },
        replicable=["Manter falhas reais em uma checagem.","Declarar possíveis interferências."],
        contingent=["O tom de reação é parte do entretenimento.","Procedimentos e resultados não foram auditados visualmente.","Comentários e métricas não provam acerto."],
        role="falsification_or_boundary", evidence_level=2, eligible=False,
        claims=[
            {"claim":"a fala registra tentativas, falhas e uma possível interferência","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"os experimentos virais eram falsos","requiredModalities":["controlled_reproduction","visual_result","materials_audit"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_complete_comment_sample",
    ),
    build_ref(
        id="obs-20261003-245",
        title="ROTINA DE UMA CIENTISTA NO JAPÃO: NEM TUDO DÁ CERTO",
        creator="Física e Afins", identity="fisica-e-afins",
        url="https://www.youtube.com/watch?v=V0x5C5mbNDA",
        published="2019-05-04", duration="PT19M10S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 19 minutos e 10 segundos, 2.475 visualizações, 306 curtidas e 27 comentários indicados em 3 de outubro de 2026",
            "transcrição automática integral em português até 19 minutos e 12 segundos; fala acessível somente por substituição textual e com muitos termos técnicos ruidosos",
            "relato falado de ajuste que não convergia, pausa, preparação de resumo, reunião de grupo, retorno ao problema e solução posterior descrita sem nomear o erro específico",
            "vinte comentários públicos amostrados; pedidos de vlogs técnicos e apoio não testam aprendizagem",
        ],
        missing=MISSING_COMMON + ["variável ou erro específico que resolveu o ajuste", "dados e código da pesquisa", "auditoria visual do trabalho"],
        metrics={"viewsObserved":2475,"likesObserved":306,"commentsObserved":27,"commentsSampled":20},
        classification=cls(
            material="video_longo", presentations=["bastidores","camera_direta","depoimento"], primary="storytelling",
            secondary=["identificacao","educativo"],
            mix=[{"family":"storytelling","percentage":45},{"family":"identificacao","percentage":35},{"family":"educativo","percentage":20}],
            objectives=["identificacao","comunidade","confianca"],
            topic="rotina de pesquisa com impasse e recuperação", segment="ciência e carreira acadêmica", subsegment="bastidores de pesquisa no Japão",
            audience="estudantes e pessoas interessadas em carreira científica", awareness="consciente_problema",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["identificacao","aproximacao","alivio","pertencimento"], hooks=["conflito","identificacao"],
            narrative=["situacao","problema","tentativa","virada","conclusao"], proof=["depoimento"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"nenhuma","name":"","confidence":"high"},
            evidence=[
                "A fala registra um ajuste que não funcionava e a decisão de mudar temporariamente de tarefa.",
                "Reunião de grupo, pausa e retorno aparecem como partes da rotina científica.",
                "A solução é atribuída a algo simples, mas o erro ou a variável não é nomeado de forma inteligível.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de storytelling sobre incerteza científica","referenceIds":[],"confidence":"medium"},
        observations=[
            "O conteúdo normaliza que pesquisa inclui impasses, pausas, ajuda e retomada.",
            "A causa da resolução não ficou acessível e, por isso, o vídeo não conta como apoio ao padrão de falha explicada.",
            "A experiência é própria e pública; não há relato privado identificável de terceiro ensinado.",
        ],
        interpretations=["A cobertura sustenta uma observação sobre bastidores científicos, sem nova hipótese transferível de desempenho."],
        scores={"gancho":83,"clareza":76,"relevancia":87,"desejo":68,"confianca":81,"retencao":"not_assessed","acao":59,"objecoes":73},
        lenses={
            "apressado":"Entende que a rotina inclui um problema que não se resolve de imediato.",
            "analitico":"Pede o erro específico, os dados e o procedimento ausentes.",
            "aspiracional":"Vê persistência sem idealização linear da ciência.",
            "comunidade":"Comentários pedem mais bastidores técnicos, sem medir aprendizagem.",
            "cetico":"Aceita o relato pessoal e evita transformá-lo em regra causal.",
        },
        replicable=["Mostrar impasse, pausa e retomada sem fabricar certeza.","Separar emoção, rotina e resultado técnico."],
        contingent=["O contexto de laboratório no Japão é pessoal.","A variável de resolução não ficou acessível.","Mídia e retenção não foram observadas."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a fala registra impasse, pausa, ajuda e resolução posterior","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
]

for item in refs:
    item["country"] = "INT" if item["id"] == "obs-20261003-243" else "BR"
    item["training"]["provenanceAndConsent"] = {
        "storyOrigin": "conteúdo editorial público do próprio canal; experiência própria ou demonstração pública",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhum relato privado identificável de terceiro foi ensinado"],
    }
    item["training"]["notRecommended"] = [
        "copiar frase, personagem, promessa, produto ou roteiro",
        "tratar visualizações, fama, comentários, escala ou orçamento como causa de desempenho",
        "repetir demonstrações com fogo, combustíveis, estruturas pesadas ou componentes pressurizados sem avaliação de segurança",
        "tratar uma tentativa melhor, depoimento ou rótulo de falso como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
    ]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 045")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20261003-241", "obs-20261003-242", "obs-20261003-243"]
new_case = "obs-20261003-244"
pattern["name"] = "Falha explicada e retestada como evidência do limite experimental"
pattern["statement"] = "Em demonstrações experimentais e protótipos, preservar a falha na progressão, ligá-la explicitamente a uma variável, interferência, limite ou hipótese verificável e registrar o que mudou no reteste torna a revisão do procedimento parte da explicação; dizer apenas que não funcionou ou que era falso sem controlar alternativas não basta, e efeitos sobre confiança, compreensão e retenção continuam não medidos."
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 8
pattern["supportingCount"] = 8
pattern["caseLimitCount"] = 3
pattern["creatorDiversityCount"] = 6
pattern["sourceDiversityCount"] = 6
pattern["conditions"] = [
    "família demonstração, transformação maker ou teste comparativo funcionalmente semelhante",
    "falha ou resultado inconclusivo preservado na progressão",
    "causa, variável, interferência, limite ou hipótese explicitada",
    "mudança do reteste descrita de forma rastreável quando houver nova tentativa",
    "ausência de conclusão fabricada ou rótulo de falsidade sem controle de alternativas",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20261003-241","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Explosão anterior é ligada a materiais, cura, equilíbrio e rotação; a segunda versão muda a estrutura e é retestada.","evidence":"Metadados, descrição integral, transcrição automática integral e 20 comentários amostrados.","limitations":["mesmo criador de apoios anteriores; hipóteses de causa sem isolamento e sem audiovisual"]},
    {"referenceId":"obs-20261003-242","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Ângulo é eliminado como explicação, força e geometria do amortecedor são nomeadas e um mecanismo articulado é prototipado antes da replicação.","evidence":"Metadados, descrição integral, transcrição automática integral e 20 comentários amostrados.","limitations":["segmento maker e risco de segurança; sem cálculo estrutural ou audiovisual"]},
    {"referenceId":"obs-20261003-243","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"A segunda tentativa muda a ordem entre combustível e mistura, declara resultado melhor e explica as reações.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["sem quantidades, repetição controlada ou audiovisual"]},
    {"referenceId":"obs-20261003-244","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"Falhas são mantidas, mas interferências e erros de execução não são controlados antes do rótulo de falsidade.","evidence":"Metadados, descrição integral, transcrição automática integral e 14 comentários amostrados.","limitations":["não conta como apoio nem contraexemplo de eficácia"]},
])
pattern["limitations"] = [
    "Oito apoios formais vêm de seis criadores; o novo lote traz três criadores independentes entre si, mas um deles já apoiava o padrão.",
    "Os segmentos variam entre ciência, prototipagem maker e química; a comparação é estrutural, com dois novos apoios de nível 2.",
    "Nenhum apoio possui retenção, teste representativo de compreensão ou comparação causal controlada.",
    "A evidência nova é textual; cenas, áudio ouvido, texto na tela, montagem, ritmo e segurança visual não foram auditados.",
    "O terceiro caso-limite mostra que manter a falha não basta: é necessário separar premissa falsa, erro de execução e interferência ambiental.",
    "O padrão permanece provisório e exige revisão humana ou experimento para qualquer validação.",
]

discarded = [
    {"url":"https://www.youtube.com/watch?v=8Z6uP2qfjC4","reason":"primeira versão do pião pertence ao mesmo criador; a segunda versão concentra falha, hipótese e reteste"},
    {"url":"https://www.youtube.com/watch?v=SqcJK9jtzoA","reason":"a transcrição é uma apresentação do canal, sem experimento analisável"},
    {"url":"https://www.youtube.com/watch?v=fDo4lPcSN2M","reason":"a slime dura é recuperada, mas o ingrediente corretivo não é nomeado na fala acessível"},
    {"url":"https://www.youtube.com/watch?v=I5GSiiw0DdI","reason":"a falha e várias suposições aparecem, mas nenhuma variável é isolada ou confirmada"},
    {"url":"https://www.youtube.com/watch?v=TcUX6eNT2j4","reason":"explica pontos de falha conceitualmente; menor prioridade que a demonstração direta selecionada"},
    {"url":"https://www.youtube.com/watch?v=nsnyl8llfH4","reason":"apresenta múltiplas soluções de queda de ovo; a falha não organiza o vídeo inteiro"},
    {"url":"https://www.youtube.com/watch?v=XyEaTVysMjk","reason":"transcrição curta e resultado inconclusivo, sem variável explicada"},
    {"url":"https://www.youtube.com/watch?v=YY3yMYn-4SI","reason":"transcrição indisponível e audiovisual não adquirido"},
    {"url":"https://www.youtube.com/watch?v=J2iGANe_Ov0","reason":"transcrição indisponível e audiovisual não adquirido"},
    {"url":"https://www.youtube.com/watch?v=gU7B8Dtcakw","reason":"transcrição indisponível e audiovisual não adquirido"},
    {"url":"https://www.youtube.com/watch?v=B0NhdLl60Rs","reason":"nenhuma transcrição foi encontrada e a mídia não foi adquirida"},
    {"url":"https://www.youtube.com/watch?v=3Yi_8XgOf_g","reason":"produção industrial complexa e menor comparabilidade de falha-reteste"},
    {"url":"https://www.youtube.com/watch?v=DKGDR7cF3dU","reason":"diagnóstico de fonte eletrônica e produto recebido; menor comparabilidade e origem internacional"},
    {"url":"https://www.youtube.com/watch?v=4b7ApLwhH7k","reason":"demonstração de sucesso sem falha organizada como evidência"},
    {"url":"https://www.youtube.com/watch?v=__8ueEt71ew","reason":"cinco testes de motor-foguete, porém sem falha explicada confirmada na triagem"},
    {"url":"https://www.youtube.com/watch?v=6Cj_7Xj5Lhg","reason":"comentário teórico sobre experimentos negativos, não demonstração individual comparável"},
    {"url":"https://www.youtube.com/watch?v=NblrD63p_xw","reason":"vídeo não reproduzível e sem transcrição adquirida"},
    {"url":"https://www.youtube.com/watch?v=bfGDReOdM5g","reason":"falha doméstica infantil sem cobertura suficiente para explicar a variável"},
    {"url":"https://www.youtube.com/watch?v=OVRvoGirqTo","reason":"desafio de objeto impossível, sem evidência suficiente de falha e revisão na triagem"},
    {"url":"https://www.youtube.com/watch?v=VukMAP_4NWA","reason":"conteúdo de segurança laboratorial não comparável a uma falha retestada"},
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 25,
    "referenceIds": [r["id"] for r in refs],
    "targetKnowledgeId": PATTERN_ID,
    "targetReferenceIds": new_supports,
    "falsificationOrBoundaryReferenceIds": [new_case],
    "controlledExplorationReferenceIds": ["obs-20261003-245"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 4,
    "internationalReferences": 1,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["demonstracao","transformacao","educativo","explicativo","reacao","comparacao","entretenimento","storytelling","identificacao"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "as cinco tentativas de vídeo falharam por formato indisponível e as cinco tentativas de capa produziram somente HTML de indisponibilidade de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, execução visual, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":0,
        "fullAutomatic":5,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":0,
        "limitation":"as cinco transcrições automáticas substituem somente a fala e podem errar termos; nenhuma cena, texto na tela ou áudio foi inferido delas",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":4,
        "sampledComments":74,
        "zeroReturnedReferences":1,
        "unavailableReferences":0,
        "limitation":"as amostras são públicas, pequenas e não representativas; elogio, pergunta ou intenção de reproduzir não foram tratados como aprendizagem ou execução",
    },
    "baselineCoverage": {
        "sampledProfiles":3,
        "contemporaneousBaselines":0,
        "limitation":"as próprias versões anteriores ou tentativas funcionam como comparadores internos, não como coorte contemporânea ou experimento causal",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["mostrar que algo falhou ou chamá-lo de falso sem controlar execução e interferência não transforma falha em explicação"],
    "safetyFindings": [
        "perfuração de amortecedor pressurizado, fogo, etanol e estruturas pesadas foram registrados como riscos e não como instruções replicáveis",
        "hipóteses de causa dos criadores não foram tratadas como causalidade demonstrada",
        "comentários, popularidade, escala e orçamento permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToBatch":3,"independentCreatorsAddedToPattern":2,"newHypotheses":0},
    "outcome": "Três criadores independentes entre si elevam de cinco para oito os apoios do padrão de falha explicada. Um caso-limite separa demonstração de falha de explicação controlada. O padrão permanece provisório.",
    "nextTarget": "demonstração brasileira recente e curta, de criador pequeno ou médio, com audiovisual integral, falha observável, uma variável alterada por vez, repetição controlada e teste de compreensão; priorizar um contraexemplo em que a explicação atribuída seja refutada pelo próprio resultado",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Cinco transcrições automáticas integrais substituem somente a fala e podem errar termos.",
        "Setenta e quatro comentários foram amostrados sem representatividade estatística.",
        "Não houve retenção, auditoria visual, teste de compreensão ou causalidade controlada.",
        "Um apoio novo repete um criador já presente no padrão; a diversidade total sobe de quatro para seis criadores.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
