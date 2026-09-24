#!/usr/bin/env python3
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "knowledge/observatory/plateia-memory.json"

# Rebuild the last approved checkpoint and reuse its schema helpers.
ns = runpy.run_path(str(Path(__file__).with_name("train-observatory-batch-034.py")))
memory = json.loads(DB.read_text(encoding="utf-8"))
make_ref = ns["make_ref"]
cls = ns["cls"]

NOW = "2026-09-21T11:14:01.000Z"
OBSERVED = "2026-09-21"
RUN_ID = "run-20260921-supervised-035"
HYPOTHESIS_ID = "hyp-20260827-029"
PATTERN_ID = "pat-20260921-015"
BATCH_IDS = {f"obs-20260921-{n}" for n in range(191, 196)}

make_ref.__globals__["NOW"] = NOW
make_ref.__globals__["OBSERVED"] = OBSERVED
memory["references"] = [r for r in memory["references"] if r.get("id") not in BATCH_IDS]
memory["trainingRuns"] = [r for r in memory["trainingRuns"] if r.get("id") != RUN_ID]
memory["patterns"] = [p for p in memory["patterns"] if p.get("id") != PATTERN_ID]

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
              consent=None):
    item = make_ref(
        id=id, title=title, creator=creator, identity=identity, url=url,
        published=published, duration=duration, accessible=accessible,
        missing=missing, metrics=metrics, cls=classification,
        comparison=comparison, observations=observations,
        interpretations=interpretations, scores=scores, lenses=lenses,
        replicable=replicable, contingent=contingent, role=role,
        evidence_level=evidence_level, eligible=eligible, claims=claims,
        source_type=source_type, comment_provenance=True,
    )
    item["country"] = "BR"
    item["training"]["provenanceAndConsent"] = consent or {
        "storyOrigin": "conteúdo editorial público do próprio criador",
        "consentStatus": "not_applicable",
        "identityProtection": "not_applicable",
        "evidence": ["nenhuma história privada identificável de terceiro foi ensinada"],
    }
    item["training"]["notRecommended"] = [
        "copiar pergunta, nome, frase, personagem ou roteiro",
        "expor a identidade de quem enviou uma dúvida sem necessidade e consentimento",
        "tratar comentário, visualização, fama, publicidade ou orçamento como prova causal",
        "inferir cena, áudio, texto na tela, edição, ritmo ou retenção sem mídia reproduzida",
        "confundir recorrência estrutural com aprendizagem ou desempenho comprovado",
    ]
    return item


GROUP = "tutorial brasileiro de Excel que parte de dúvida específica atribuída à audiência, usa recurso nativo e demonstra caminho e resultado na fala"

refs = [
    build_ref(
        id="obs-20260921-191",
        title="Resposta a Duvidas Inscritos - (Excel com cara de Menus de Sistema)",
        creator="Excel com Joabe Souza", identity="excel-com-joabe-souza",
        url="https://www.youtube.com/watch?v=V0OUkOQoZ9o",
        published="2022-08-07", duration="PT5M45S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 5 minutos e 45 segundos",
            "transcrição automática integral em português com 134 segmentos e timestamps", "fala por substituição textual",
            "466 visualizações, 38 curtidas e 5 comentários declarados", "amostra integral dos 5 comentários públicos retornados",
            "pergunta do inscrito reproduzida na descrição e na fala", "recurso nativo Visual Basic e eventos da pasta de trabalho nomeados na transcrição",
            "procedimento e teste final declarados na fala",
        ],
        missing=MISSING_AV + ["identidade e consentimento verificáveis do autor da pergunta", "teste de execução pelo espectador", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":466,"likesObserved":38,"commentsObserved":5},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"demonstracao","percentage":30},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="fechamento automático de submenu em planilha com aparência de sistema",
            segment="software e produtividade", subsegment="automação em Excel e VBA", audience="usuários de Excel que constroem interfaces e automações",
            awareness="consciente_problema", production="simple", scale="medium", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","confianca"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","seguir"],
            evidence=[
                "Entre 0:07 e 0:26, a fala apresenta a rotina de responder dúvidas publicadas no canal.",
                "Entre 0:27 e 0:48, identifica a pergunta sobre fechar automaticamente um submenu.",
                "A partir de 1:14, a transcrição registra o uso do Visual Basic e de eventos nativos; entre 3:49 e 5:22, registra teste e resultado declarado.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260921-192","obs-20260921-193"],"confidence":"high"},
        observations=[
            "Descrição e abertura preservam a pergunta concreta antes de nomear o caminho técnico.",
            "A transcrição conecta problema, recurso nativo, etapas e teste final; a execução visual não foi observada.",
            "Cinco comentários foram lidos, incluindo duas respostas do criador; não houve teste de aprendizagem.",
        ],
        interpretations=[
            "A dúvida atribuída torna o caso de uso rastreável e o recurso padrão reduz, na fala, a necessidade de ferramenta adicional.",
            "Recorrência e métricas não provam maior relevância, retenção ou aprendizagem.",
        ],
        scores={"gancho":86,"clareza":92,"relevancia":91,"desejo":80,"confianca":81,"retencao":"not_assessed","acao":85,"objecoes":84},
        lenses={
            "apressado":"Reconhece a dúvida e o resultado esperado antes do procedimento.",
            "analitico":"Consegue reconstruir recurso, eventos e teste, mas precisa ver a tela para auditar a execução.",
            "aspiracional":"Vê uma interface mais automática como ganho de acabamento.",
            "comunidade":"A pergunta enviada vira pauta e recebe resposta pública.",
            "cetico":"Exige consentimento, arquivo e teste próprio antes de aceitar a entrega como reproduzida.",
        },
        replicable=["Abrir com uma dúvida pública específica.","Nomear cedo o recurso nativo que resolve o problema.","Demonstrar passos e testar o resultado sem copiar a pergunta ou o roteiro."],
        contingent=["A transcrição automática pode conter erros.","O resultado visual não foi confirmado.","A identidade e o consentimento de quem perguntou não foram auditados."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"o tutorial parte de dúvida específica atribuída a inscrito","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"recurso nativo, procedimento e resultado declarado aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_5_public_comments",
        consent={"storyOrigin":"pergunta pública de inscrito reproduzida pelo criador","consentStatus":"public_submission_but_reuse_consent_not_audited","identityProtection":"nome do autor não reproduzido nesta ficha","evidence":["a descrição e a fala atribuem a origem à audiência; autorização específica não foi acessada"]},
    ),
    build_ref(
        id="obs-20260921-192",
        title="Como conectar CAIXA de LISTAGEM com GRÁFICO no EXCEL - Respondendo Dúvidas dos INSCRITOS",
        creator="Excel com William Oliveira", identity="excel-com-william-oliveira",
        url="https://www.youtube.com/watch?v=yKuRVbXvdK4",
        published="2021-05-28", duration="PT10M6S",
        accessible=[
            "título", "criador", "descrição pública integral com link para arquivo auxiliar", "data exata", "duração de 10 minutos e 6 segundos",
            "transcrição automática integral em português com 255 segmentos e timestamps", "fala por substituição textual",
            "1.456 visualizações, 57 curtidas e 4 comentários declarados", "amostra integral dos 4 comentários públicos retornados",
            "pergunta recebida pelo Instagram reproduzida na fala", "funções nativas TEXTO, SOMASE, LIN e NÃO.DISP nomeadas",
            "procedimento e teste declarados na transcrição",
        ],
        missing=MISSING_AV + ["consentimento verificável do autor da pergunta", "teste de compreensão", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":1456,"likesObserved":57,"commentsObserved":4},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":55},{"family":"demonstracao","percentage":30},{"family":"comunidade","percentage":15}],
            objectives=["educar","comunidade","confianca","comentario"], topic="conexão entre caixa de listagem e gráfico no Excel",
            segment="software e produtividade", subsegment="dashboards e fórmulas em Excel", audience="usuários de Excel que montam dashboards interativos",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","aproximacao","reciprocidade","confianca"], hooks=["pergunta","problema"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","seguir"],
            evidence=[
                "Entre 0:00 e 0:25, a fala atribui a pauta a uma pergunta recebida no Instagram e formula o problema da caixa de listagem ligada ao gráfico.",
                "A partir de 1:20, a transcrição registra a construção com funções nativas; o teste e o resultado declarado aparecem na segunda metade.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260921-191","obs-20260921-193"],"confidence":"high"},
        observations=[
            "O título sinaliza que a pauta responde à audiência; a abertura torna a dúvida específica e a origem reconhecíveis.",
            "Funções padrão, passos e teste aparecem na transcrição; caixa de listagem e gráfico não foram vistos.",
            "Os quatro comentários retornados são majoritariamente troca entre canais e não medem aprendizagem.",
        ],
        interpretations=[
            "A sequência pergunta atribuída, recurso nativo e teste constitui resposta rastreável sem depender de plugin na fala.",
            "O arquivo auxiliar melhora auditabilidade potencial, mas não foi executado neste lote.",
        ],
        scores={"gancho":88,"clareza":93,"relevancia":91,"desejo":81,"confianca":83,"retencao":"not_assessed","acao":84,"objecoes":85},
        lenses={
            "apressado":"Título e abertura entregam a pergunta e o objeto técnico.",
            "analitico":"Reconstrói funções e teste pela transcrição, mas precisa do arquivo e da tela.",
            "aspiracional":"Visualiza um dashboard mais interativo como resultado.",
            "comunidade":"Uma pergunta de rede social vira aula pública.",
            "cetico":"Não confunde link de arquivo e resultado falado com execução auditada.",
        },
        replicable=["Atribuir a pergunta sem expor dados desnecessários.","Traduzir a dúvida em um problema técnico delimitado.","Usar recurso nativo e testar o resultado."],
        contingent=["A pergunta veio de outra plataforma e o consentimento não foi auditado.","Transcrição automática pode conter erros.","Não houve reprodução do arquivo nem do vídeo."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"a fala parte de pergunta específica recebida da audiência","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
            {"claim":"funções nativas, passos e teste são identificáveis na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_4_public_comments",
        consent={"storyOrigin":"pergunta pública ou semipública recebida pelo Instagram e reproduzida pelo criador","consentStatus":"public_social_question_but_reuse_consent_not_audited","identityProtection":"identidade do autor omitida nesta ficha","evidence":["a fala atribui a origem ao Instagram; autorização específica não foi acessada"]},
    ),
    build_ref(
        id="obs-20260921-193",
        title="Checklist no Excel sem a Caixa de Seleção (Caixa de Flag)",
        creator="O Canal do Rodi", identity="o-canal-do-rodi",
        url="https://www.youtube.com/watch?v=8zTgKHpCt0k",
        published="2022-12-01", duration="PT7M45S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 7 minutos e 45 segundos",
            "transcrição automática integral em português com 185 segmentos e timestamps", "fala por substituição textual",
            "1.042 visualizações, 40 curtidas e 10 comentários declarados", "amostra integral dos 10 comentários públicos retornados",
            "pergunta e solução do inscrito atribuídas na descrição e na fala", "fórmula e caixa de seleção nativa nomeadas na transcrição",
            "comentário do autor da dúvida agradecendo os créditos e resposta do criador",
        ],
        missing=MISSING_AV + ["termos formais de autorização", "teste de compreensão", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":1042,"likesObserved":40,"commentsObserved":10},
        classification=cls(
            presentations=["tutorial","tela_gravada","comentario"], primary="educativo",
            secondary=["demonstracao","comunidade"],
            mix=[{"family":"educativo","percentage":50},{"family":"demonstracao","percentage":30},{"family":"comunidade","percentage":20}],
            objectives=["educar","comunidade","confianca","comentario"], topic="checklist automático no Excel ligado ao preenchimento de data",
            segment="software e produtividade", subsegment="fórmulas e controles em Excel", audience="usuários de Excel que automatizam controles e checklists",
            awareness="consciente_problema", production="simple", scale="small", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","reciprocidade","pertencimento","confianca"], hooks=["pergunta","problema"],
            narrative=["problema","virada","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado","depoimento"], cta=["comentar","seguir","clicar"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"treinamento e links de Office divulgados pelo canal","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:25, a fala identifica a pergunta do inscrito sobre marcar uma flag automaticamente após inserir uma data.",
                "Entre 0:25 e 0:48, o criador declara que não conhecia a solução, recebeu a contribuição e a complementou.",
                "Entre 2:06 e 7:31, a transcrição registra comportamento final, fórmula, controle nativo e agradecimento ao inscrito.",
                "Na amostra integral, o autor da pergunta agradece os créditos e o criador responde.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260921-191","obs-20260921-192"],"confidence":"high"},
        observations=[
            "Pergunta, contribuição do inscrito e complemento do criador são explicitados antes do passo a passo.",
            "A transcrição nomeia fórmula e controle nativo e declara o resultado; a tela não foi vista.",
            "A troca pública sobre créditos oferece evidência de procedência e reconhecimento, sem equivaler a termo formal de autorização.",
        ],
        interpretations=[
            "Além de pauta, a dúvida funciona como colaboração reconhecida, fortalecendo rastreabilidade comunitária.",
            "Oferta de curso e afiliados é contexto comercial, não prova de confiança, aprendizagem ou conversão.",
        ],
        scores={"gancho":88,"clareza":92,"relevancia":90,"desejo":80,"confianca":87,"retencao":"not_assessed","acao":86,"objecoes":86},
        lenses={
            "apressado":"Entende o gatilho e o resultado do checklist na abertura.",
            "analitico":"Vê origem, fórmula e teste na fala, com crédito público ao colaborador.",
            "aspiracional":"O checklist automático representa ganho concreto de fluidez.",
            "comunidade":"A solução circula entre inscrito e canal, com reconhecimento público.",
            "cetico":"Separa crédito público de consentimento formal e exige auditoria visual.",
        },
        replicable=["Creditar a origem da dúvida ou solução.","Admitir o que não se sabia e delimitar o complemento próprio.","Ensinar o recurso nativo e testar o resultado."],
        contingent=["Identidade de terceiro exige cuidado mesmo em comentário público.","A oferta e afiliados podem afetar percepção.","A execução visual não foi observada."],
        role="target_support", evidence_level=2, eligible=True,
        claims=[
            {"claim":"pergunta e contribuição do inscrito são publicamente atribuídas","requiredModalities":["description","transcript","comments"],"observedModalities":["description","transcript","comments"],"sufficient":True},
            {"claim":"recurso padrão, procedimento e resultado declarado aparecem na fala","requiredModalities":["transcript"],"observedModalities":["transcript"],"sufficient":True},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_10_public_comments",
        consent={"storyOrigin":"pergunta e solução compartilhadas por inscrito em interação pública","consentStatus":"public_comment_and_explicit_acknowledgment","identityProtection":"nome não necessário ao princípio transferível","evidence":["o autor agradece publicamente os créditos na amostra de comentários; termos formais não foram acessados"]},
    ),
    build_ref(
        id="obs-20260921-194",
        title="Aprenda Função SE de uma VEZ no EXCEL",
        creator="Curso de Excel Online", identity="curso-de-excel-online",
        url="https://www.youtube.com/watch?v=SgrCNtopz9I",
        published="2020-01-07", duration="PT16M26S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 16 minutos e 26 segundos",
            "transcrição automática integral em português com 354 segmentos e timestamps", "fala por substituição textual",
            "74.894 visualizações, 3.549 curtidas e 52 comentários declarados", "amostra pública limitada de 30 comentários",
            "três exemplos e a função SE nativa descritos na descrição e na fala",
        ],
        missing=MISSING_AV + ["pergunta específica atribuída a uma pessoa ou comentário", "procedência de uma dúvida real individual", "teste de compreensão", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":74894,"likesObserved":3549,"commentsObserved":52},
        classification=cls(
            presentations=["tutorial","tela_gravada","camera_direta"], primary="educativo",
            secondary=["demonstracao","autoridade_opiniao"],
            mix=[{"family":"educativo","percentage":60},{"family":"demonstracao","percentage":30},{"family":"autoridade_opiniao","percentage":10}],
            objectives=["educar","confianca","lead","comentario"], topic="uso da função SE em três exemplos de Excel",
            segment="software e produtividade", subsegment="fórmulas básicas em Excel", audience="iniciantes que têm dificuldade com lógica condicional",
            awareness="consciente_problema", production="simple", scale="large", replicability="high", duration="over_60s",
            mechanisms=["utilidade_pratica","autoridade","alivio"], hooks=["problema","promessa"],
            narrative=["problema","promessa","progressao","prova","conclusao"], proof=["demonstracao","mecanismo_explicado"], cta=["comentar","clicar","seguir"],
            advertising="oferta_direta", intent="explicita", entity={"kind":"servico","name":"curso de Excel do canal","confidence":"high"},
            evidence=[
                "Entre 0:00 e 0:32, a fala apresenta a função SE como muito pesquisada e diz genericamente que muitas pessoas ainda têm dúvidas.",
                "A descrição e o restante da transcrição organizam três exemplos com recurso nativo.",
                "Nenhuma pergunta individual, origem pública ou autor de dúvida aparece na cobertura adquirida.",
            ],
        ),
        comparison={"level":2,"group":GROUP,"referenceIds":["obs-20260921-191","obs-20260921-192","obs-20260921-193"],"confidence":"high"},
        observations=[
            "O tutorial usa função nativa, exemplos e procedimento, mas inicia por demanda genérica de muitas pessoas.",
            "Amostra de 30 comentários contém elogios e novas dúvidas; não demonstra que uma delas originou o vídeo.",
            "Ausência de dúvida atribuída delimita o mecanismo-alvo, mas não prova menor utilidade ou desempenho.",
        ],
        interpretations=[
            "Dizer que o tema é muito pedido não equivale a mostrar procedência de uma pergunta concreta.",
            "É caso-limite, não contraexemplo: o tutorial pode funcionar por outras razões não medidas.",
        ],
        scores={"gancho":82,"clareza":91,"relevancia":84,"desejo":77,"confianca":78,"retencao":"not_assessed","acao":82,"objecoes":76},
        lenses={
            "apressado":"Reconhece função e promessa, mas não uma situação de usuário específica.",
            "analitico":"Recebe exemplos e lógica, sem origem rastreável da dúvida.",
            "aspiracional":"A promessa é dominar uma função muito pedida.",
            "comunidade":"Há comentários com perguntas, mas não procedência da pauta.",
            "cetico":"Não transforma demanda genérica ou métricas em prova do mecanismo.",
        },
        replicable=["Organizar exemplos progressivos de uma função nativa.","Distinguir demanda geral de pergunta atribuída.","Não alegar origem comunitária sem evidência."],
        contingent=["É um tutorial genérico, não resposta individual rastreável.","A transcrição automática pode conter erros.","Audiovisual e aprendizagem não foram avaliados."],
        role="case_limit", evidence_level=2, eligible=False,
        claims=[
            {"claim":"recurso nativo e exemplos são observáveis na fala e descrição","requiredModalities":["description","transcript"],"observedModalities":["description","transcript"],"sufficient":True},
            {"claim":"o vídeo nasce de uma dúvida específica atribuída à audiência","requiredModalities":["description","transcript","comments"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_full_automatic_transcript_and_30_of_52_public_comments",
    ),
    build_ref(
        id="obs-20260921-195",
        title="DUOLINGO ANIME: O Teste Final (Ep. 1 Dublado) | O Teste Beta Começa",
        creator="Duolingo Brasil", identity="duolingo-brasil",
        url="https://www.youtube.com/watch?v=XSMV2H9Weic",
        published="2026-02-09", duration="PT2M3S",
        accessible=[
            "título", "criador", "descrição pública integral", "data exata", "duração de 2 minutos e 3 segundos",
            "legenda humana oficial em português do Brasil com 28 segmentos e timestamps, retornada somente até cerca de 1 minuto e 4 segundos", "fala por substituição textual parcial",
            "613.355 visualizações, 28.999 curtidas e 1.400 comentários declarados", "amostra pública limitada de 30 comentários",
            "premissa de teste beta, aplicativo imersivo e ameaça de manter a chama acesa presentes na legenda parcial",
        ],
        missing=MISSING_AV + ["legenda ou transcrição do trecho final de aproximadamente 59 segundos", "desfecho narrativo integral", "baseline funcional contemporâneo"],
        metrics={"viewsObserved":613355,"likesObserved":28999,"commentsObserved":1400},
        classification=cls(
            presentations=["animacao","narracao_imagens","institucional"], primary="storytelling",
            secondary=["entretenimento","institucional"],
            mix=[{"family":"storytelling","percentage":50},{"family":"entretenimento","percentage":30},{"family":"institucional","percentage":20}],
            objectives=["marca","visualizacao","compartilhamento","retencao"], topic="ficção animada sobre um teste beta imersivo do aplicativo Duolingo",
            segment="educação de idiomas e entretenimento de marca", subsegment="anime institucional seriado", audience="usuários e fãs do Duolingo e de animação",
            awareness="consciente_produto", production="complex", scale="large", replicability="low", duration="over_60s",
            mechanisms=["curiosidade","tensao","pertencimento","antecipacao"], hooks=["narrativo","conflito"],
            narrative=["situacao","conflito","virada","risco","continuidade_serial"], proof=[], cta=["clicar","seguir","proxima_parte"],
            advertising="conteudo_de_marca", intent="explicita", entity={"kind":"marca","name":"Duolingo","confidence":"high"},
            evidence=[
                "A descrição oficial identifica o primeiro episódio e promove o curso de japonês.",
                "Entre 0:00 e 0:35, a legenda oficial estabelece personagens desorientados e a revelação de que estão no aplicativo.",
                "Entre 0:35 e 1:04, a legenda apresenta o teste beta imersivo e a regra de não deixar a chama apagar.",
                "A legenda retornada termina por volta de 1:04, embora o vídeo tenha 2:03; o desfecho não foi ensinado.",
            ],
        ),
        comparison={"level":0,"group":"exploração controlada de storytelling animado de marca, fora do grupo-alvo de tutoriais de software","referenceIds":[],"confidence":"high"},
        observations=[
            "Descrição e legenda oficial parcial permitem identificar premissa, marca e ameaça narrativa.",
            "A cobertura textual não alcança o minuto final e nenhum quadro ou áudio foi adquirido.",
            "Comentários amostrados fazem referências a personagens e cenas, mas não substituem observação audiovisual.",
        ],
        interpretations=[
            "A tradução de um produto educacional em conflito ficcional merece exploração futura, sem gerar hipótese neste lote.",
            "Escala, fandom e métricas são contexto, não prova de retenção, afinidade ou conversão.",
        ],
        scores={"gancho":90,"clareza":83,"relevancia":82,"desejo":86,"confianca":72,"retencao":"not_assessed","acao":68,"objecoes":60},
        lenses={
            "apressado":"Recebe episódio, teste beta e conflito na embalagem e legenda inicial.",
            "analitico":"Entende a regra narrativa, mas não tem o desfecho nem o audiovisual.",
            "aspiracional":"A imersão transforma aprendizagem de idioma em aventura.",
            "comunidade":"Comentários mostram reconhecimento de personagens, sem representar o público.",
            "cetico":"Desconta campanha de marca, cobertura parcial e ausência de cenas.",
        },
        replicable=["Converter uma regra de produto em conflito narrativo abstrato.","Apresentar situação, regra e risco cedo.","Separar exploração de marca de prova de eficácia educacional."],
        contingent=["Anime e propriedade intelectual da marca não são replicáveis diretamente.","A legenda oficial está temporalmente incompleta.","Nenhuma cena, voz ou montagem foi observada."],
        role="controlled_exploration", evidence_level=0, eligible=False,
        claims=[
            {"claim":"descrição e legenda parcial estabelecem teste beta e regra da chama","requiredModalities":["description","captions"],"observedModalities":["description","captions"],"sufficient":True},
            {"claim":"o arco narrativo e o desfecho completos foram observados","requiredModalities":["video","captions"],"observedModalities":[],"sufficient":False},
        ],
        source_type="youtube_public_metadata_full_description_partial_official_human_ptbr_captions_and_30_of_1400_public_comments",
    ),
]

existing_urls = {r["url"] for r in memory["references"]}
new_urls = [r["url"] for r in refs]
if len(new_urls) != len(set(new_urls)) or any(u in existing_urls for u in new_urls):
    raise RuntimeError("duplicate URL in batch 035")
memory["references"].extend(refs)

hypothesis = next(h for h in memory["hypotheses"] if h["id"] == HYPOTHESIS_ID)
hypothesis["supportReferenceIds"] = [x for x in hypothesis.get("supportReferenceIds", []) if x not in BATCH_IDS] + [
    "obs-20260921-191", "obs-20260921-192", "obs-20260921-193"
]
hypothesis["status"] = "promoted_to_provisional"
hypothesis["promotedPatternId"] = PATTERN_ID
hypothesis["reasonNotPromoted"] = None

memory["patterns"].append({
    "id": PATTERN_ID,
    "status": "provisional",
    "statement": "Em tutoriais de software, explicitar uma dúvida atribuída a um usuário, localizar o recurso nativo que a resolve e demonstrar passos e resultado torna problema, caminho e resposta rastreáveis; efeitos sobre aprendizagem, retenção e participação não foram medidos.",
    "mechanism": ["utilidade_pratica","aproximacao","reciprocidade","confianca"],
    "conditions": [
        "dúvida específica com procedência pública registrada",
        "problema funcional delimitado antes do passo a passo",
        "recurso padrão ou nativo nomeado",
        "procedimento e resultado identificáveis em evidência direta",
        "identidade e consentimento tratados proporcionalmente",
    ],
    "supportReferenceIds": ["obs-20260921-191","obs-20260921-192","obs-20260921-193"],
    "comparableSupportCount": 3,
    "comparisonLevel": 2,
    "confidence": "medium",
    "limitations": [
        "Os três apoios formais são tutoriais antigos de Excel e não autorizam generalização para todo software ou formato.",
        "Há um precursor em Affinity by Canva, mas ele não foi contado entre os três apoios formais por ter menor cobertura e contexto diferente.",
        "Nenhum audiovisual, ritmo, retenção, baseline, execução pelo espectador ou teste de compreensão foi adquirido.",
        "Atribuição pública não substitui consentimento formal para reutilizar identidade ou história.",
        "O caso-limite mostra que demanda genérica e recurso nativo não equivalem a uma dúvida individual rastreável.",
        "Transcrições automáticas podem conter erros e não autorizam copiar frases ou perguntas.",
        "Popularidade, escala, oferta e comentários são contexto, nunca prova causal.",
        "Validação exige revisão humana ou evidência experimental apropriada.",
    ],
    "validation": "requires_human_or_experimental_evidence",
    "stage": "provisional",
    "name": "Dúvida real convertida em tutorial nativo",
    "creativeFamily": "família educativo",
    "objective": "clareza, relevância e resposta comunitária",
    "segment": "tutorial de software",
    "supportingCount": 3,
    "counterexampleCount": 0,
    "evidence": [
        {"referenceId":"obs-20260921-191","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta de inscrito, recurso nativo, procedimento e teste final aparecem em descrição e fala.","evidence":"Metadados, descrição integral, transcrição automática integral e cinco comentários.","limitations":["sem audiovisual, consentimento auditado ou teste de aprendizagem"]},
        {"referenceId":"obs-20260921-192","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta recebida no Instagram é convertida em problema técnico, funções nativas e teste.","evidence":"Metadados, descrição integral, transcrição automática integral e quatro comentários.","limitations":["sem audiovisual, consentimento auditado ou execução do arquivo"]},
        {"referenceId":"obs-20260921-193","role":"support","comparisonLevel":2,"requiredEvidenceObserved":True,"confidence":"high","observation":"Pergunta e solução do inscrito são creditadas antes de fórmula, controle nativo e resultado declarado.","evidence":"Metadados, descrição integral, transcrição automática integral e dez comentários, incluindo reconhecimento público dos créditos.","limitations":["sem audiovisual, termo formal de autorização ou teste de aprendizagem"]},
        {"referenceId":"obs-20260921-194","role":"case_limit","comparisonLevel":2,"requiredEvidenceObserved":False,"confidence":"high","observation":"O tutorial usa função nativa e exemplos, mas a origem da dúvida permanece genérica e não atribuída.","evidence":"Metadados, descrição integral, transcrição automática integral e 30 de 52 comentários.","limitations":["não é contraexemplo de desempenho"]},
        {"referenceId":"obs-20260827-060","role":"precursor","comparisonLevel":1,"requiredEvidenceObserved":True,"confidence":"medium","observation":"Uma pergunta de seguidor antecede solução com recurso padrão no Affinity by Canva.","evidence":"Ficha anterior com trecho inicial de transcrição.","limitations":["cobertura menor e contexto diferente; não contado como apoio formal"]},
    ],
    "taxonomyVersion": "1.1",
    "creatorDiversityCount": 3,
    "sourceDiversityCount": 3,
    "patternType": "compreensao",
    "caseLimitReferenceIds": ["obs-20260921-194"],
    "caseLimitCount": 1,
    "counterexampleReferenceIds": [],
})

discarded = [
    {"url": f"https://www.youtube.com/watch?v={video_id}", "reason": reason}
    for video_id, reason in [
        ("ci0wOcvW_YU", "apoio comparável, mas redundante depois de três criadores independentes selecionados"),
        ("1AN6WfxtvxQ", "pergunta de inscrito observável, porém redundante com o grupo final de Excel"),
        ("GHozZrPVk0I", "compilação de várias dúvidas no Canva com menor comparabilidade a um único problema"),
        ("WdN0lDneAo0", "mesma criadora e formato de perguntas múltiplas, sem ganho de independência"),
        ("NnDLgz-b7gU", "candidato comparável, mas redundante por tema e formato"),
        ("R4AH6oDNI0o", "candidato longo e redundante após fechar três apoios"),
        ("fVMTMkMAOFM", "candidato comparável, mas sem ganho informativo sobre o limite"),
    ]
]

memory["trainingRuns"].append({
    "id": RUN_ID,
    "executedAt": NOW,
    "batchPolicyVersion": "1.1",
    "requestedBatchSize": 5,
    "candidatesFound": 123,
    "referenceIds": [f"obs-20260921-{n}" for n in range(191, 196)],
    "targetKnowledgeId": HYPOTHESIS_ID,
    "targetReferenceIds": ["obs-20260921-191","obs-20260921-192","obs-20260921-193"],
    "falsificationOrBoundaryReferenceIds": ["obs-20260921-194"],
    "controlledExplorationReferenceIds": ["obs-20260921-195"],
    "discarded": discarded,
    "analyzed": 5,
    "brazilianReferences": 5,
    "internationalReferences": 0,
    "unknownOriginReferences": 0,
    "smallOrMediumCreatorReferences": 3,
    "replicableReferences": 4,
    "creativeFamiliesObserved": ["educativo","demonstracao","comunidade","storytelling","entretenimento","institucional","autoridade_opiniao"],
    "coverageSummary": {"complete":0,"partial":5,"insufficient":0},
    "audiovisualAcquisition": {"attempted":True,"succeeded":0,"failure":"os cinco downloads de mídia falharam por timeout, resposta 502 ou formato indisponível; cinco tentativas diretas de capa também expiraram","effect":"imagem em movimento, capa, áudio ouvido, texto na tela, atuação, edição, ritmo e retenção ficaram não mensurados"},
    "transcriptCoverage": {"fullHumanOrCreatorProvided":0,"fullAutomatic":4,"partialHumanOrCreatorProvided":1,"partialAutomatic":0,"none":0,"limitation":"quatro transcrições automáticas substituem somente a fala; a legenda humana oficial da exploração cobre aparentemente só 28 segmentos até cerca de 1:04 de um vídeo de 2:03"},
    "commentsCoverage": {"countsOnly":0,"sampledReferences":5,"sampledComments":79,"limitation":"duas amostras foram limitadas a 30 comentários; comentários públicos não são representativos nem teste de compreensão"},
    "baselineCoverage": {"sampledProfiles":0,"contemporaneousBaselines":0,"limitation":"datas, canais, temas, durações e escalas diferentes impedem benchmark causal de desempenho"},
    "patternsCreated": [PATTERN_ID],
    "patternsStrengthened": [],
    "patternsRefined": [],
    "hypothesesCreated": [],
    "hypothesesStrengthened": [HYPOTHESIS_ID],
    "validatedPatternsCreated": 0,
    "contradictionsFound": [],
    "caseLimitsFound": ["dizer que muitas pessoas têm dúvidas não equivale a mostrar uma pergunta específica e atribuída"],
    "safetyFindings": [
        "identidade de quem enviou pergunta foi omitida quando não necessária ao princípio",
        "atribuição pública não foi confundida com consentimento formal",
        "ofertas, popularidade, marca, orçamento e comentários permaneceram contexto não causal",
        "nenhuma cena, áudio, texto na tela, edição, ritmo, retenção, frase ou roteiro foi inventado",
        "a legenda parcial do anime não foi tratada como cobertura do arco completo",
    ],
    "evidenceGateSummary": {"targetSupportsEligible":3,"targetSupportsRejected":0,"boundaryCases":1,"explorationReferences":1,"duplicateUrls":0,"independentCreatorsAddedToPattern":3,"newHypotheses":0},
    "outcome": "Três criadores independentes sustentam a passagem de dúvida atribuída para recurso nativo, passos e resultado declarado. A hipótese foi promovida a padrão provisório; o caso genérico delimita procedência, sem provar menor desempenho.",
    "nextTarget": "tutorial brasileiro recente e curto de software, de criador pequeno ou médio, com audiovisual integral, pergunta anonimizada ou consentida, recurso nativo e teste de execução ou compreensão; buscar também resposta que exija ferramenta externa paga ou cuja pergunta não tenha procedência",
    "limitations": [
        "Nenhum audiovisual, áudio ou capa foi adquirido.",
        "Quatro transcrições são automáticas; a legenda humana da exploração ficou temporalmente parcial.",
        "Foram amostrados 79 comentários em cinco publicações; as amostras não são representativas.",
        "Os três apoios formais são antigos e restritos a Excel.",
        "Não houve baseline, retenção, replay, teste de execução, compreensão ou causalidade.",
        "Nenhum resultado autoriza validação; revisão humana ou evidência experimental continua necessária.",
    ],
})

memory["updatedAt"] = NOW
DB.write_text(json.dumps(memory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"references":len(memory["references"]),"patterns":len(memory["patterns"]),"hypotheses":len(memory["hypotheses"]),"runs":len(memory["trainingRuns"]),"createdPattern":PATTERN_ID}, ensure_ascii=False))
