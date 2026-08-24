---
name: plateia
description: Avaliar, comparar e melhorar vídeos, Reels, posts, carrosséis, artes e copies com o método Platéia; simular cinco lentes comportamentais; classificar conteúdo; ou ensinar referências ao Observatório. Usar quando o usuário mencionar Platéia, pedir avaliação antes de publicar, análise de conteúdo, treinamento por exemplos ou memória de padrões criativos.
---

# Platéia portátil

Executar o método independentemente do modelo hospedeiro. Tratar a IA como motor substituível e o protocolo, as taxonomias, a memória e as regras de evidência como o produto.

## Fluxo

1. Identificar o material efetivamente acessível: vídeo, imagem, carrossel, copy, legenda, áudio, transcrição, métricas e contexto declarado.
2. Para arquivo visual local, inspecionar diretamente. Para vídeo sem leitura nativa, executar `scripts/extract_video_frames.py` e inspecionar os quadros; não inferir o áudio sem transcrição.
3. Para link público, tentar abrir a publicação e registrar exatamente o que ficou acessível. Se houver somente capa ou legenda, fazer leitura parcial e explicar o limite.
4. Ler `references/protocol.md` e classificar o conteúdo antes de pontuar. Consultar `references/taxonomies.md` quando houver dúvida entre famílias ou mecanismos.
5. Se existir memória do Observatório, recuperar somente referências comparáveis. Executar `scripts/observatory_memory.py search` quando houver um arquivo de memória disponível.
6. Produzir a avaliação pelas cinco lentes e pelos oito critérios. Seguir `references/report-contract.md` para o formato.
7. Se o usuário disser “ensine”, “aprenda”, “guarde” ou equivalente, gerar uma ficha de referência e executar `scripts/observatory_memory.py add`. Não guardar automaticamente uma avaliação comum.

## Regras inegociáveis

- Separar observação, interpretação, hipótese, padrão, métrica e evidência experimental.
- Não tratar visualizações, comentários ou correlação como prova causal.
- Não inventar cena, fala, áudio, CTA, legenda, público, resultado, depoimento ou prova social.
- Não dar nota zero a algo inacessível; marcar como não avaliado.
- Comparar pela família, objetivo, segmento, apresentação, duração, público, consciência, produção e mecanismo — nunca apenas por ser Reel ou post.
- Manter independentes: cinco cérebros sintéticos, padrões do Observatório e futuros resultados experimentais do Freud.
- Uma referência isolada gera observação ou hipótese. Três apoios comparáveis e pelo menos dois criadores/fontes independentes podem gerar padrão provisório. Nunca validar automaticamente.
- Extrair princípios transferíveis; não copiar frase, personagem, bordão ou roteiro de terceiros.

## Cinco lentes

- O Apressado: interrupção, entendimento rápido e retenção inicial.
- O Analítico: lógica, clareza, especificidade, evidência e objeções.
- O Aspiracional: desejo, identidade, estética e transformação.
- O Influenciado pela Comunidade: identificação, pertencimento e confiança social autêntica.
- O Cético: exageros, ambiguidades, promessas e motivos para desconfiar.

## Entrega

Responder em português do Brasil. Liderar com o diagnóstico e as três decisões prioritárias. Indicar cobertura, confiança da classificação, grupo comparável e o que não pode ser concluído. Se o usuário pedir dados estruturados, usar o JSON descrito em `references/report-contract.md`.
