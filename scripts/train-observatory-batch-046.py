#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-045.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
build_ref = ns["build_ref"]
cls = ns["cls"]
MISSING_AV = ns["MISSING_AV"]

NOW = "2026-10-04T11:37:14.000Z"
OBSERVED = "2026-10-04"
RUN_ID = "run-20261004-supervised-046"
PATTERN_ID = "pat-20260824-005"
BATCH_IDS = {f"obs-20261004-{n}" for n in range(246, 251)}

build_ref.__globals__["NOW"] = NOW
build_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]

GROUP = "microtutorial de Canva que nomeia a ferramenta e delimita um único recurso, problema ou microresultado antes de demonstrar o caminho"
MISSING_COMMON = MISSING_AV + [
    "métrica de retenção",
    "teste representativo de compreensão ou execução",
    "comparação causal controlada",
]

refs = [
    build_ref(
        id="obs-20261004-246",
        title="Como DESFOCAR ou SUAVIZAR as BORDAS de uma IMAGEM no CANVA em 41 S",
        creator="Facil e Rapido", identity="facil-e-rapido",
        url="https://www.youtube.com/watch?v=DSNy8aXVxGY",
        published="2026-04-07", duration="PT42S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 42 segundos, 1.340 visualizações, nove curtidas e zero comentários indicados em 4 de outubro de 2026",
            "transcrição automática integral em português até 42,5 segundos; fala acessível somente por substituição textual",
            "título, descrição e fala delimitam uma imagem, o problema das bordas e o microresultado de desfocar ou suavizar no Canva",
            "nenhum comentário público foi retornado",
        ],
        missing=MISSING_COMMON + ["auditoria visual do desfoque", "versão e plano do Canva usados"],
        metrics={"viewsObserved":1340,"likesObserved":9,"commentsObserved":0,"commentsSampled":0},
        classification=cls(
            material="video_curto", presentations=["tutorial","tela_gravada","demonstracao"], primary="demonstracao",
            secondary=["educativo","explicativo"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":30},{"family":"explicativo","percentage":20}],
            objectives=["educar","salvamento","apresentar_solucao"],
            topic="suavizar bordas de imagem no Canva", segment="Canva e design para redes sociais", subsegment="edição de imagens",
            audience="iniciantes no Canva e criadores de conteúdo", awareness="consciente_problema",
            production="simple", scale="small", replicability="high", duration="31_to_60s",
            mechanisms=["recompensa","curiosidade","confianca"], hooks=["problema","promessa"],
            narrative=["problema","mecanismo","progressao","conclusao"], proof=["demonstracao"],
            cta=["seguir","comentar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"produto","name":"Canva","confidence":"high"},
            evidence=[
                "O título nomeia Canva, objeto, operação e duração prometida.",
                "A fala começa pelo problema e localiza a edição da imagem antes de descrever ajustes.",
                "O resultado visual foi declarado, mas não observado.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261004-247","obs-20261004-248"],"confidence":"high"},
        observations=[
            "A embalagem reduz a promessa a um único objeto e uma única alteração no Canva.",
            "A fala confirma um caminho direto de seleção, edição e ajuste para o microresultado declarado.",
            "A velocidade prometida não foi tratada como evidência de aprendizagem ou execução correta.",
        ],
        interpretations=[
            "Ferramenta, objeto e microresultado tornam a promessa semanticamente delimitada antes da reprodução.",
            "Sem a tela, não se confirma a posição atual dos controles nem a qualidade do acabamento.",
        ],
        scores={"gancho":89,"clareza":95,"relevancia":90,"desejo":78,"confianca":78,"retencao":"not_assessed","acao":73,"objecoes":76},
        lenses={
            "apressado":"Entende ferramenta, problema e resultado diretamente pelo título.",
            "analitico":"Rastreia a sequência falada, mas pede tela e versão do Canva.",
            "aspiracional":"Vê uma melhoria visual pequena e imediatamente aplicável.",
            "comunidade":"Nenhum comentário público foi retornado.",
            "cetico":"Não confunde a duração curta com prova de facilidade ou aprendizagem.",
        },
        replicable=["Nomear ferramenta, objeto e transformação no título.","Manter um único microresultado por tutorial.","Ligar a promessa a uma sequência curta na fala."],
        contingent=["A interface pode mudar entre versões e planos.","O acabamento visual não foi observado.","Retenção e execução permanecem não medidas."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"o título delimita Canva, imagem e suavização de bordas, e a fala descreve o caminho","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True}],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261004-247",
        title="Create Transparent Text Effect in Canva – Easy Canva Tutorial",
        creator="Webon", identity="webon",
        url="https://www.youtube.com/watch?v=X_4iYZlvkQ4",
        published="2025-03-17", duration="PT2M3S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 2 minutos e 3 segundos, 67.309 visualizações, 1.361 curtidas e 83 comentários indicados em 4 de outubro de 2026",
            "transcrição automática integral em inglês até 2 minutos e 5 segundos; fala acessível somente por substituição textual",
            "descrição e fala delimitam texto transparente no Canva, criação do texto, escolha de fonte, duplicação e composição do efeito",
            "vinte comentários públicos amostrados; dúvidas sobre fundo, mesclagem e controles movidos não constituem teste representativo",
        ],
        missing=MISSING_COMMON + ["auditoria visual da transparência", "teste atual da interface e dos modos de mesclagem"],
        metrics={"viewsObserved":67309,"likesObserved":1361,"commentsObserved":83,"commentsSampled":20},
        classification=cls(
            material="video_curto", presentations=["tutorial","tela_gravada","demonstracao"], primary="demonstracao",
            secondary=["educativo","transformacao"],
            mix=[{"family":"demonstracao","percentage":50},{"family":"educativo","percentage":30},{"family":"transformacao","percentage":20}],
            objectives=["educar","salvamento","visualizacao"],
            topic="efeito de texto transparente no Canva", segment="Canva e design para redes sociais", subsegment="tipografia e composição",
            audience="iniciantes em design e criadores de conteúdo", awareness="consciente_solucao",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["recompensa","desejo","confianca"], hooks=["promessa","resultado_antecipado"],
            narrative=["promessa","mecanismo","progressao","conclusao"], proof=["demonstracao"],
            cta=["seguir"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"produto","name":"Canva","confidence":"high"},
            evidence=[
                "O título nomeia o efeito e o Canva sem depender de adjetivo genérico.",
                "A fala descreve criação e formatação do texto e composição do efeito.",
                "Comentários registram dúvidas de execução e possível mudança de interface; o autor responde que o controle ainda existe em outra área.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261004-246","obs-20261004-248"],"confidence":"high"},
        observations=[
            "A promessa textual contém ferramenta e efeito específico; a fala apresenta uma rota correspondente.",
            "Comentários mostram que clareza da promessa não elimina dependência de versão, plano ou localização de controles.",
            "Popularidade e elogios foram mantidos como contexto, não como prova de execução.",
        ],
        interpretations=[
            "O apoio é estrutural: embalagem e fala estão alinhadas com um único microresultado.",
            "Objeções sobre interface refinam a necessidade de declarar versão ou rota alternativa.",
        ],
        scores={"gancho":87,"clareza":93,"relevancia":88,"desejo":83,"confianca":76,"retencao":"not_assessed","acao":74,"objecoes":70},
        lenses={
            "apressado":"Identifica Canva e o efeito transparente pelo título.",
            "analitico":"Encontra passos falados, mas pede interface atual e teste de exportação.",
            "aspiracional":"Percebe um acabamento tipográfico aplicável a posts e capas.",
            "comunidade":"Comentários revelam dúvidas específicas; não provam execução bem-sucedida da audiência.",
            "cetico":"Nota dependência de versão e não usa métricas como validação.",
        },
        replicable=["Nomear o efeito visual sem superlativo vazio.","Fazer a fala corresponder ao microresultado prometido.","Antecipar diferenças de interface quando conhecidas."],
        contingent=["Controles podem mudar de lugar.","Comentários não medem taxa de sucesso.","Resultado visual e retenção não foram observados."],
        role="target_support", evidence_level=1, eligible=True,
        claims=[{"claim":"o título delimita o efeito transparente e a fala descreve uma rota correspondente no Canva","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True}],
        source_type="youtube_public_watch_metadata_full_description_full_automatic_transcript_and_20_public_comments",
    ),
    build_ref(
        id="obs-20261004-248",
        title="NOVA Ferramenta do Canva: Crie IMAGENS com Inteligência Artificial (Tutorial ‘Pede pro Canva’)",
        creator="Dicas do Raffa", identity="dicas-do-raffa",
        url="https://www.youtube.com/watch?v=TkJ6UAWD36w",
        published="2025-11-18", duration="PT3M46S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 3 minutos e 46 segundos, 87 visualizações, seis curtidas e um comentário indicados em 4 de outubro de 2026",
            "legenda humana integral em português e transcrição automática integral até 3 minutos e 47 segundos; fala acessível somente por texto",
            "descrição e fala identificam Pede pro Canva, geração de imagem por texto e refinamento de maçã verde para maçã amarela sem fundo",
            "o único comentário retornado é do próprio canal e divulga outros vídeos; não mede aprendizagem",
        ],
        missing=MISSING_COMMON + ["auditoria visual das imagens geradas", "disponibilidade atual por plano, conta e região"],
        metrics={"viewsObserved":87,"likesObserved":6,"commentsObserved":1,"commentsSampled":1},
        classification=cls(
            material="video_longo", presentations=["tutorial","tela_gravada","demonstracao"], primary="demonstracao",
            secondary=["educativo","comparacao"],
            mix=[{"family":"demonstracao","percentage":45},{"family":"educativo","percentage":35},{"family":"comparacao","percentage":20}],
            objectives=["educar","apresentar_solucao","autoridade"],
            topic="gerar e refinar imagem por prompt no Canva", segment="Canva e design para redes sociais", subsegment="inteligência artificial generativa",
            audience="usuários do Canva interessados em gerar elementos por texto", awareness="consciente_solucao",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["curiosidade","recompensa","confianca"], hooks=["novidade","promessa"],
            narrative=["promessa","tentativa","progressao","conclusao"], proof=["demonstracao","mecanismo_explicado"],
            cta=["seguir"], advertising="editorial_organico", intent="implicita",
            entity={"kind":"produto","name":"Canva","confidence":"high"},
            evidence=[
                "Título e descrição nomeiam o Canva, o recurso de IA e o resultado de criar imagens.",
                "A descrição registra um pedido vago e um segundo pedido com cor e remoção de fundo.",
                "O canal declara links de afiliados e possibilidade de comissão sem custo adicional.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20261004-246","obs-20261004-247"],"confidence":"medium"},
        observations=[
            "Ferramenta, recurso e microresultado são identificáveis antes da reprodução.",
            "O refinamento do prompt transforma a explicação em uma pequena comparação de entrada e resultado declarado.",
            "Duração maior e disponibilidade variável tornam o apoio menos comparável aos microtutoriais abaixo de três minutos.",
        ],
        interpretations=[
            "O caso apoia a clareza da promessa, com menor força de comparabilidade por duração e dependência de rollout.",
            "Disclosure comercial é contexto de confiança, não evidência de qualidade ou eficácia.",
        ],
        scores={"gancho":85,"clareza":92,"relevancia":86,"desejo":80,"confianca":78,"retencao":"not_assessed","acao":69,"objecoes":72},
        lenses={
            "apressado":"Entende que verá geração de imagem por IA dentro do Canva.",
            "analitico":"Rastreia dois prompts, mas pede tela e disponibilidade atual.",
            "aspiracional":"Vê possibilidade de criar elementos personalizados sem banco de imagens.",
            "comunidade":"O único comentário é autopromoção do canal.",
            "cetico":"Mantém rollout, plano e vínculo de afiliado como limites explícitos.",
        },
        replicable=["Nomear o recurso e o microresultado.","Comparar pedido vago e pedido refinado.","Declarar vínculo de afiliado."],
        contingent=["A ferramenta pode variar por plano, conta e região.","O vídeo é mais longo que o núcleo comparável.","Qualidade visual e retenção não foram observadas."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[{"claim":"título, descrição e fala ligam a ferramenta de IA a geração e refinamento de imagem","requiredModalities":["title","description","transcript"],"observedModalities":["title","description","transcript"],"sufficient":True}],
        source_type="youtube_public_watch_metadata_full_description_full_human_caption_full_automatic_transcript_and_one_public_comment",
    ),
    build_ref(
        id="obs-20261004-249",
        title="Como FAZER e EDITAR VÍDEOS no CANVA em 63 S",
        creator="Facil e Rapido", identity="facil-e-rapido",
        url="https://www.youtube.com/watch?v=ux3IaKWaT9w",
        published="2026-03-23", duration="PT1M3S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 1 minuto e 3 segundos, 11 visualizações, uma curtida e zero comentários indicados em 4 de outubro de 2026",
            "transcrição automática integral em português até 59,4 segundos; fala acessível somente por substituição textual",
            "descrição promete criar e editar vídeos para vários usos; a fala percorre formato de vídeo, modelo e edição, sem reduzir a promessa a um único microresultado",
            "nenhum comentário público foi retornado",
        ],
        missing=MISSING_COMMON + ["um microresultado único e verificável", "auditoria visual do projeto e do resultado"],
        metrics={"viewsObserved":11,"likesObserved":1,"commentsObserved":0,"commentsSampled":0},
        classification=cls(
            material="video_curto", presentations=["tutorial","tela_gravada","demonstracao"], primary="educativo",
            secondary=["demonstracao","explicativo"],
            mix=[{"family":"educativo","percentage":45},{"family":"demonstracao","percentage":35},{"family":"explicativo","percentage":20}],
            objectives=["educar","apresentar_solucao"],
            topic="criar e editar vídeos no Canva", segment="Canva e design para redes sociais", subsegment="edição de vídeo para iniciantes",
            audience="iniciantes que desejam produzir vídeos no Canva", awareness="consciente_solucao",
            production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["recompensa","aproximacao"], hooks=["promessa"],
            narrative=["promessa","mecanismo","progressao","cta"], proof=["demonstracao"],
            cta=["seguir","comentar"], advertising="editorial_organico", intent="ausente",
            entity={"kind":"produto","name":"Canva","confidence":"high"},
            evidence=[
                "O título nomeia Canva e duração, mas agrega os verbos fazer e editar vídeos.",
                "A descrição amplia a entrega para redes sociais, YouTube e apresentações, com textos, efeitos e organização.",
                "A fala apresenta uma visão inicial do formato de vídeo e da edição, não um único resultado delimitado.",
            ],
        ),
        comparison={"level":1,"group":GROUP,"referenceIds":["obs-20261004-246","obs-20261004-247","obs-20261004-248"],"confidence":"high"},
        observations=[
            "Ferramenta e tema são claros, porém a promessa combina criação, edição, modelos, textos e efeitos.",
            "A cobertura sustenta um tutorial introdutório amplo, não um microresultado único.",
            "O caso delimita o padrão sem provar que promessa ampla reduz compreensão ou desempenho.",
        ],
        interpretations=["É caso-limite, não contraexemplo: clareza de ferramenta e assunto não equivale a especificidade de microresultado."],
        scores={"gancho":77,"clareza":68,"relevancia":82,"desejo":73,"confianca":70,"retencao":"not_assessed","acao":66,"objecoes":58},
        lenses={
            "apressado":"Entende Canva e vídeo, mas não qual resultado específico receberá.",
            "analitico":"Vê uma introdução ampla demais para verificar uma única entrega.",
            "aspiracional":"Percebe acesso rápido à produção de vídeos.",
            "comunidade":"Nenhum comentário público foi retornado.",
            "cetico":"Questiona a promessa de cobrir criação e edição completas em 63 segundos.",
        },
        replicable=["Nomear a ferramenta e o domínio geral."],
        contingent=["A promessa reúne tarefas demais.","Não existe microresultado central único.","A tela e a execução não foram observadas."],
        role="falsification_or_boundary", evidence_level=1, eligible=False,
        claims=[
            {"claim":"o título e a fala identificam Canva e edição de vídeo","requiredModalities":["title","transcript"],"observedModalities":["title","transcript"],"sufficient":True},
            {"claim":"há um único microresultado central","requiredModalities":["title","description","transcript","specific_microresult"],"observedModalities":["title","description","transcript"],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_full_automatic_transcript",
    ),
    build_ref(
        id="obs-20261004-250",
        title="Nosso Canto | Marina Sena - Feira de Mangaio",
        creator="Sebrae", identity="sebrae",
        url="https://www.youtube.com/watch?v=dmbEpCGKDEM",
        published="2026-07-18", duration="PT3M24S",
        accessible=[
            "título, criador, descrição pública integral e data exata",
            "duração pública de 3 minutos e 24 segundos, 16.434.567 visualizações, 15.878 curtidas e 608 comentários indicados em 4 de outubro de 2026",
            "descrição oficial apresenta Nosso Canto como iniciativa que usa música para mostrar histórias, desafios, conquistas e identidade de quem empreende, e situa a edição no Ver-o-Peso",
            "vinte comentários públicos amostrados; elogios à música e uma objeção sobre representação cultural não constituem avaliação representativa",
        ],
        missing=MISSING_COMMON + [
            "vídeo, imagem, fala ou legenda utilizável",
            "transcrição da música ou de depoimentos",
            "identificação e consentimento dos empreendedores retratados",
            "auditoria das histórias, cenas e representação cultural",
        ],
        metrics={"viewsObserved":16434567,"likesObserved":15878,"commentsObserved":608,"commentsSampled":20},
        classification=cls(
            material="video_longo", presentations=["institucional","montagem"], primary="institucional",
            secondary=["storytelling","posicionamento_marca"],
            mix=[{"family":"institucional","percentage":45},{"family":"storytelling","percentage":35},{"family":"posicionamento_marca","percentage":20}],
            objectives=["marca","identificacao","comunidade"],
            topic="empreendedorismo e identidade local apresentados por música", segment="institucional e empreendedorismo", subsegment="campanha cultural do Sebrae",
            audience="público brasileiro interessado em cultura e empreendedorismo", awareness="inconsciente",
            production="complex", scale="large", replicability="low", duration="over_60s",
            mechanisms=["identificacao","pertencimento","admiracao"], hooks=["identificacao","autoridade"],
            narrative=["situacao","promessa","conclusao"], proof=["alegacao_sem_prova"],
            cta=[], advertising="institucional", intent="implicita",
            entity={"kind":"marca","name":"Sebrae","confidence":"high"},
            evidence=[
                "A descrição declara uma série que liga música a histórias de empreendedores em diferentes lugares do Brasil.",
                "Esta edição é situada no Ver-o-Peso e associa Marina Sena à canção Feira de Mangaio.",
                "Um comentário da amostra questiona a adequação da representação cultural; é objeção individual, não conclusão coletiva.",
            ],
        ),
        comparison={"level":4,"group":"exploração controlada de storytelling institucional musical sobre empreendedorismo","referenceIds":[],"confidence":"low"},
        observations=[
            "A cobertura sustenta apenas a proposta editorial declarada: conectar música, território e empreendedorismo.",
            "A execução narrativa, as pessoas retratadas e a adequação cultural não foram observadas.",
            "Popularidade, artista conhecida e escala de produção não foram tratadas como prova causal.",
        ],
        interpretations=["A combinação de marca, música e território é uma exploração contextual; não gera hipótese nova sem audiovisual e procedência das histórias."],
        scores={"gancho":82,"clareza":84,"relevancia":79,"desejo":75,"confianca":65,"retencao":"not_assessed","acao":"not_assessed","objecoes":55},
        lenses={
            "apressado":"O título identifica série, artista e canção, mas não explicita a história individual.",
            "analitico":"Pede audiovisual, protagonistas, consentimento e ligação entre narrativa e objetivo institucional.",
            "aspiracional":"A descrição associa identidade local, música e transformação pelo empreendedorismo.",
            "comunidade":"Comentários mostram entusiasmo e uma objeção cultural isolada.",
            "cetico":"Não aceita fama, visualizações ou campanha institucional como prova de representação adequada.",
        },
        replicable=["Declarar território, tema e propósito editorial da série.","Separar proposta institucional de prova de impacto."],
        contingent=["Artista, música e escala são pouco replicáveis.","Histórias e consentimento não ficaram acessíveis.","Sem audiovisual não se ensinam cenas, montagem ou ritmo."],
        role="controlled_exploration", evidence_level=4, eligible=False,
        claims=[
            {"claim":"a descrição oficial enquadra a iniciativa como encontro entre música, território e histórias de empreendedorismo","requiredModalities":["description"],"observedModalities":["description"],"sufficient":True},
            {"claim":"o vídeo representa adequadamente o território e as pessoas","requiredModalities":["video","story_provenance","consent"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_watch_metadata_full_description_and_20_public_comments_no_transcript",
    ),
]

for item in refs:
    item["country"] = "INT" if item["id"] == "obs-20261004-247" else "BR"
    if item["id"] == "obs-20261004-250":
        item["training"]["provenanceAndConsent"] = {
            "storyOrigin":"descrição oficial declara histórias de pessoas empreendedoras no Ver-o-Peso, sem identificar os protagonistas na modalidade acessível",
            "consentStatus":"not_documented",
            "identityProtection":"not_assessed",
            "evidence":["descrição oficial e comentários públicos; sem vídeo, fala, legenda ou documentos de consentimento"],
        }
    else:
        item["training"]["provenanceAndConsent"] = {
            "storyOrigin":"tutorial público do próprio canal; nenhum relato privado identificável de terceiro foi ensinado",
            "consentStatus":"not_applicable",
            "identityProtection":"not_applicable",
            "evidence":["conteúdo instrucional público"],
        }
    item["training"]["notRecommended"] = [
        "copiar frase, identidade visual, personagem, música ou roteiro",
        "tratar visualizações, fama, comentários, tendência, mídia ou orçamento como causa de desempenho",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
        "ensinar controles atuais do Canva sem verificar versão, plano, conta e região",
        "tratar histórias de terceiros como autorizadas sem procedência e consentimento documentados",
    ]

existing_urls = {r.get("url") for r in memory["references"]}
if len({r["url"] for r in refs}) != 5 or any(r["url"] in existing_urls for r in refs):
    raise RuntimeError("duplicate URL in batch 046")
memory["references"].extend(refs)

pattern = next(p for p in memory["patterns"] if p["id"] == PATTERN_ID)
new_supports = ["obs-20261004-246", "obs-20261004-247", "obs-20261004-248"]
new_case = "obs-20261004-249"
pattern["name"] = "Canva, microresultado e caminho rastreável em microtutorial"
pattern["statement"] = "Em microtutoriais de Canva, nomear a ferramenta e delimitar um único recurso, objeto, problema ou microresultado no título torna a promessa semanticamente rastreável; quando a fala confirma um caminho correspondente, embalagem e entrega declarada podem ser comparadas. Verbos amplos como criar e editar, superlativos sem objeto ou dependências de versão, plano e interface não declaradas elevam o ônus de prova; efeitos sobre compreensão, execução e retenção permanecem não medidos."
pattern["supportReferenceIds"] = [x for x in pattern.get("supportReferenceIds", []) if x not in BATCH_IDS] + new_supports
pattern["caseLimitReferenceIds"] = [x for x in pattern.get("caseLimitReferenceIds", []) if x not in BATCH_IDS] + [new_case]
pattern["comparableSupportCount"] = 11
pattern["supportingCount"] = 11
pattern["caseLimitCount"] = 5
pattern["creatorDiversityCount"] = 11
pattern["sourceDiversityCount"] = 11
pattern["conditions"] = [
    "tutorial compacto de Canva ou formato funcionalmente equivalente",
    "Canva nomeado na embalagem",
    "um recurso, objeto, problema ou microresultado central delimitado",
    "fala ou legenda confirma um caminho correspondente quando o apoio inclui entrega",
    "versão, plano, conta ou região tratados como dependências quando observados",
    "adjetivo genérico, promessa ampla ou nome da ferramenta isolado não bastam",
]
pattern["evidence"] = [e for e in pattern.get("evidence", []) if e.get("referenceId") not in BATCH_IDS]
pattern["evidence"].extend([
    {"referenceId":"obs-20261004-246","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Título delimita Canva, imagem e suavização de bordas; a fala descreve um caminho correspondente.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["sem audiovisual, versão do Canva, retenção ou teste de execução"]},
    {"referenceId":"obs-20261004-247","role":"support","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"high","observation":"Título nomeia o efeito de texto transparente e a fala apresenta uma rota correspondente; comentários expõem dúvidas de interface.","evidence":"Metadados, descrição integral, transcrição automática integral e vinte comentários amostrados.","limitations":["sem audiovisual; controles podem ter mudado"]},
    {"referenceId":"obs-20261004-248","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Título, descrição e fala ligam Pede pro Canva à geração e ao refinamento de uma imagem por prompt.","evidence":"Metadados, descrição integral, legenda humana integral, transcrição automática integral e um comentário.","limitations":["duração maior; disponibilidade por plano, conta e região não revalidada"]},
    {"referenceId":"obs-20261004-249","role":"case_limit","comparisonLevel":1,"requiredEvidenceObserved":False,"confidence":"high","observation":"Canva e vídeo são claros, mas criar e editar reúnem várias operações sem um microresultado central único.","evidence":"Metadados, descrição integral e transcrição automática integral.","limitations":["não conta como apoio nem contraexemplo de desempenho"]},
])
pattern["limitations"] = [
    "Onze apoios formais vêm de onze criadores e fontes independentes, mas apenas um novo apoio tem menos de sessenta segundos.",
    "Um apoio novo é em inglês e outro excede três minutos; a comparação de nível 2 foi usada quando duração ou contexto divergiram.",
    "Cinco casos-limite mostram que nomear Canva, usar superlativo ou prometer criação e edição amplas não substitui um microresultado delimitado.",
    "Comentários expõem dependência de interface, mas não medem taxa de sucesso ou compreensão.",
    "Nenhum apoio possui audiovisual auditado, retenção, teste representativo de execução ou comparação causal.",
    "O padrão permanece provisório e exige revisão humana ou experimento para qualquer validação.",
]

discarded = [
    {"url":"https://www.youtube.com/watch?v=UOgU6ED0W-0","reason":"microresultado específico, porém publicado em 2022 e com menor prioridade que candidatos mais recentes"},
    {"url":"https://www.youtube.com/watch?v=IDPgXowzs50","reason":"apoio potencial antigo; menor prioridade temporal"},
    {"url":"https://www.youtube.com/watch?v=Wx29H9GyMUI","reason":"apoio potencial antigo; menor prioridade temporal"},
    {"url":"https://www.youtube.com/watch?v=ouoyq3Wn144","reason":"transcrição automática contém apenas música e não confirma o procedimento"},
    {"url":"https://www.youtube.com/watch?v=pdn9ieiCal4","reason":"configuração de idioma é clara, mas menos comparável ao microresultado visual selecionado"},
    {"url":"https://www.youtube.com/watch?v=FEd1V6IqL_w","reason":"transcrição automática contém apenas música e o audiovisual não foi adquirido"},
    {"url":"https://www.youtube.com/watch?v=VEQ3fWKDu-g","reason":"transcrição automática ruidosa e audiovisual não adquirido"},
    {"url":"https://www.youtube.com/watch?v=SZsT6KIS2rY","reason":"procedimento acessível, mas duração e antiguidade reduzem a prioridade"},
    {"url":"https://www.youtube.com/watch?v=86gVNGUaT14","reason":"transcrição automática contém essencialmente música e o audiovisual não foi adquirido"},
    {"url":"https://www.youtube.com/watch?v=l8_W-a8cmFs","reason":"apoio potencial antigo e mais longo que o núcleo comparável"},
    {"url":"https://www.youtube.com/watch?v=DH1WJMRD16o","reason":"procedimento acessível, porém vídeo mais longo e antigo"},
    {"url":"https://www.youtube.com/watch?v=1k7eAKc_7HU","reason":"publicação recente, mas duração de cinco minutos e dez segundos excede o microtutorial prioritário"},
    {"url":"https://www.youtube.com/watch?v=-y_TT3FvtWY","reason":"procedimento acessível, mas vídeo longo e de criador já presente na triagem"},
    {"url":"https://www.youtube.com/watch?v=QgAfjclrCg0","reason":"procedimento acessível, mas duração longa e baixa comparabilidade"},
    {"url":"https://www.youtube.com/watch?v=-t9LJHgNZI4","reason":"procedimento acessível, mas publicação antiga e vídeo longo"},
    {"url":"https://www.youtube.com/watch?v=Cd42mGyZXyQ","reason":"procedimento acessível, porém mais longo e antigo que os apoios selecionados"},
    {"url":"https://www.youtube.com/watch?v=CjP-eLGixVw","reason":"campanha institucional com descrição acessível, mas publicação de 2024; exploração mais recente selecionada"},
    {"url":"https://www.youtube.com/watch?v=BJeBS2Wyb2k","reason":"sem transcrição adquirida e publicação antiga"},
    {"url":"https://www.youtube.com/watch?v=lO0fExkJyJg","reason":"sem transcrição adquirida e descrição menos informativa para exploração"},
    {"url":"https://www.youtube.com/watch?v=3GtHW1yAQ48","reason":"vídeo indisponível"},
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
    "controlledExplorationReferenceIds": ["obs-20261004-250"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 4,
    "internationalReferences": 1,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 4,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["demonstracao","educativo","explicativo","transformacao","comparacao","institucional","storytelling","posicionamento_marca"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {
        "attempted": True,
        "succeeded": 0,
        "failure": "as cinco tentativas de vídeo falharam por formato indisponível e as cinco tentativas de capa produziram somente HTML de indisponibilidade de 195 bytes",
        "effect": "imagem em movimento, capa, áudio ouvido, texto na tela, execução visual, edição, ritmo e retenção ficaram não mensurados",
    },
    "transcriptCoverage": {
        "fullHumanOrCreatorProvided":1,
        "fullAutomatic":4,
        "partialHumanOrCreatorProvided":0,
        "partialAutomatic":0,
        "none":1,
        "limitation":"quatro transcrições automáticas substituem somente a fala; uma delas também possui legenda humana integral. A exploração institucional não teve fala ou legenda adquirida e foi limitada à descrição.",
    },
    "commentsCoverage": {
        "countsOnly":0,
        "sampledReferences":3,
        "sampledComments":41,
        "zeroReturnedReferences":2,
        "unavailableReferences":0,
        "limitation":"as amostras são públicas, pequenas e não representativas; dúvidas, elogios e objeções não foram tratados como aprendizagem, execução ou opinião coletiva",
    },
    "baselineCoverage": {
        "sampledProfiles":3,
        "contemporaneousBaselines":0,
        "limitation":"não houve coorte contemporânea, teste de compreensão ou experimento causal",
    },
    "patternsCreated": [],
    "patternsStrengthened": [PATTERN_ID],
    "patternsRefined": [PATTERN_ID],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["nomear Canva e prometer fazer e editar vídeos ainda é amplo demais quando nenhum microresultado central organiza a entrega"],
    "safetyFindings": [
        "controles e recursos do Canva não foram ensinados como atuais sem verificar versão, plano, conta e região",
        "histórias institucionais de terceiros não foram tratadas como autorizadas sem procedência e consentimento documentados",
        "comentários, popularidade, artista, mídia e orçamento permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, edição, ritmo ou retenção foi inventado",
        "Observatório, cérebros sintéticos e futuro Freud permaneceram separados",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToBatch":4,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores novos elevam de oito para onze os apoios do padrão de microtutorial do Canva. Um caso-limite separa assunto amplo de microresultado delimitado. O padrão permanece provisório.",
    "nextTarget": "microtutorial brasileiro recente de Canva, com audiovisual integral, interface e plano declarados, um único microresultado e teste de execução; priorizar um contraexemplo em que título específico leve a procedimento ausente, desatualizado ou incapaz de produzir o resultado",
    "limitations": [
        "Nenhum vídeo, áudio ou capa utilizável foi adquirido.",
        "Quatro transcrições automáticas integrais substituem somente a fala e podem errar termos; uma delas também tem legenda humana integral.",
        "A exploração institucional ficou limitada à descrição, metadados e vinte comentários.",
        "Quarenta e um comentários foram amostrados sem representatividade estatística.",
        "Não houve retenção, auditoria visual, teste de compreensão, teste de execução ou causalidade controlada.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"strengthenedPattern":PATTERN_ID}, ensure_ascii=False))
