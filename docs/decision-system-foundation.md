# Sistema de Decisão Criativa Pré-Publicação — fundação 1.0

Esta fundação aplica o Protocolo Platéia 2.1 ao relatório de decisão e preserva o Protocolo do Observatório 3.0 para memória, taxonomia e evidência científica.

## Ativado no código

- verdade técnica local de MP4 com `ffprobe`/FFmpeg: duração, resolução, proporção, FPS, codecs, tamanho, presença de áudio, volume, silêncios, mudanças de cena, duração média das cenas e cortes por minuto;
- leitura cega como única etapa que recebe a mídia;
- congelamento SHA-256 do relatório cego;
- auditoria contextual sem mídia, usando somente leitura congelada, verdade técnica e dossiê opcional;
- duas notas independentes: potencial de atenção e retenção e efetividade para o negócio;
- oito critérios com evidência, justificativa e confiança; ausência usa `null`, nunca zero;
- cinco lentes independentes, oito etapas temporais e linha do tempo de risco estimado;
- exatamente três prioridades estruturadas, além de hooks, CTA, montagem, texto e cortes quando pertinentes;
- comparação entre versões por análise anterior, sem sobrescrever o histórico;
- contrato de métricas pós-publicação vinculado à análise e à versão do vídeo, sem validação automática de hipótese;
- fila global de chamadas ao provedor, espera controlada por `Retry-After` e bloqueio de fallback pago;
- autenticação com falha segura em produção e validação de tamanho, MIME e assinatura do arquivo.

## Preparado, mas não ativado

- persistência e formulário manual das métricas pós-publicação;
- calibração por baseline, plataforma, mídia, duração, segmento, família criativa e objetivo;
- OCR temporal, transcrição local com timestamps, velocidade de fala, movimento, rosto, produto, logo, CTA visual, contraste e safe area;
- agregação estatística e revisão humana para evolução de hipóteses do Observatório.

Campos sem detector disponível permanecem explicitamente como `not_assessed`, com limitação registrada. Nenhum valor é simulado.

## Validação necessária antes de uso bloqueante

Três vídeos servem apenas para confirmar funcionamento. Uma decisão bloqueante exige de 12 a 20 vídeos com defeitos e resultados previamente conhecidos, revisão humana e comparação dos timestamps com o conteúdo real.

## Publicação

O repositório GitHub e o Site privado atualmente publicado usam bases técnicas distintas. Esta fundação não deve substituir silenciosamente o Site existente. A migração para o ambiente privado de publicação requer homologação específica, cópia controlada das funcionalidades e repetição de todos os testes com as variáveis de produção, sem expor segredos.
