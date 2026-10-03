# Observatório Platéia — taxonomia e evidência v3

## Decisão de arquitetura

A taxonomia v3 é multiaxial. Ela separa o recipiente (Reel, TikTok, Short), o formato material, a apresentação, a família criativa, o objetivo, o tema editorial, o produto/serviço anunciado, a intenção e o tipo de publicidade. Também registra público, consciência, produção, escala do criador, replicabilidade, ritmo, ganchos, narrativa, mecanismos, provas, CTA e distribuição.

Uma publicação não recebe um rótulo forte sem evidência. Campos incertos permanecem `indeterminado` ou `unknown`, com alternativas, ausências e revisão humana. Conteúdo híbrido recebe mistura funcional, em vez de ser forçado a uma única família.

## Referências pesquisadas

- [IAB Tech Lab Content Taxonomy](https://iabtechlab.com/standards/content-taxonomy/): taxonomia de assunto do conteúdo. A v3 separa o assunto editorial da oferta anunciada e guarda um código IAB opcional, nunca inferido à força.
- [IAB Tech Lab Ad Product Taxonomy](https://iabtechlab.com/standards/ad-product-taxonomy/): base para separar o produto/serviço promovido do tema ao redor dele.
- [Google Ads — ABCD para criativos em vídeo](https://support.google.com/google-ads/answer/14783551?hl=pt-BR): atenção, marca, conexão e direção ajudam a decompor abertura, identificação, prova e CTA.
- [TikTok Creative Codes](https://ads.tiktok.com/business/en-US/creative-codes): estrutura gancho–corpo–fechamento e integração de som, movimento e edição.
- [TikTok Video Insights](https://ads.tiktok.com/help/article/video-insights): análise por quadros-chave, comentários e benchmark de indústria, sem confundir correlação com causa.
- [Meta — anúncios em Reels](https://www.facebook.com/business/ads/facebook-instagram-reels-ads): o contexto de veiculação, área segura, áudio e testes A/B são tratados separadamente da qualidade criativa observada.
- [YouTube Analytics](https://support.google.com/youtube/answer/9002587): alcance, engajamento, retenção e desempenho típico exigem contexto do canal e do vídeo.
- [Berger & Milkman, Journal of Marketing Research](https://doi.org/10.1509/jmr.10.0353): ativação emocional, surpresa e utilidade prática são hipóteses transferíveis; proeminência e distribuição são confundidores.
- [Google Research — recomendação de próximo vídeo](https://research.google/pubs/recommending-what-video-to-watch-next-a-multitask-ranking-system/): desempenho e recomendação são multiobjetivo e sujeitos a viés de seleção.

## Viralidade: regra operacional

“Viral” não é uma família criativa nem uma explicação causal. A v3 separa cinco resultados: alcance relativo, compartilhamento, retenção/conclusão, conversão e velocidade. Visualizações absolutas isoladas não classificam viralidade.

Quando houver denominadores verificáveis, o motor calcula taxas seguras e compara com a mediana histórica do próprio perfil e uma coorte funcional. Sem baseline, janela, distribuição orgânica/paga e métricas compatíveis, o resultado é `indeterminate`. Toda classificação de desempenho inclui limitações e `causalClaimAllowed: false`.

## Promoção de padrões

- uma referência: observação;
- dois apoios: hipótese apoiada;
- três ou mais apoios realmente comparáveis, com pelo menos dois criadores/fontes independentes: padrão provisório;
- revisão humana ou experimento: validado experimentalmente;
- contraexemplos e contradições ficam preservados.

Os cinco cérebros sintéticos, o Observatório e o futuro Freud permanecem fontes separadas no relatório e na memória.

## Migração

O script `scripts/migrate-observatory-taxonomy-v3.mjs` é idempotente. Ele preserva a classificação antiga em `reference.migration.legacyClassification`, não remove referências nem URLs e gera `knowledge/observatory/migrations/taxonomy-v3-report.json`. A reversão integral também permanece disponível pelo histórico Git.
