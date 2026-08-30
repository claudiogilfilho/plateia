# Platéia MVP

O Platéia avalia vídeos, Reels, posts, carrosséis, artes e copies antes da publicação. O método classifica o material, aplica cinco lentes comportamentais, calcula oito critérios compatíveis com a cobertura realmente disponível e entrega exatamente três decisões prioritárias.

## Fluxo essencial

1. Abra o painel sem cadastro no modo MVP.
2. Envie um arquivo, uma copy ou um link público.
3. O Platéia registra a cobertura efetivamente acessível.
4. Um motor de IA configurado executa o protocolo portátil.
5. O relatório entra no histórico da sessão.

O aplicativo não cria notas de demonstração quando não existe motor de IA. Nesse caso, a interface informa que o adaptador precisa ser conectado.

## Rodar localmente

```bash
cp .env.example .env
pnpm install
pnpm dev
```

Preencha no `.env` um dos três adaptadores descritos em [docs/plateia-portable.md](docs/plateia-portable.md). Sem `DATABASE_URL`, o histórico funciona em memória e é apagado quando o servidor reinicia. Sem armazenamento externo, uploads usam dados inline, adequados somente para teste controlado.

## Limites do MVP

- A conexão oficial com Instagram é opcional; upload, copy e link público continuam sendo as entradas principais.
- Link público pode oferecer somente capa ou legenda. O relatório informa quando a leitura é parcial.
- Vídeo só é considerado assistido quando o adaptador realmente suporta transporte multimodal.
- Observatório, cinco cérebros sintéticos e futuros dados do Freud permanecem como fontes independentes.
- Para produção multiusuário, configure OAuth, banco e armazenamento persistente.

## Estado verificável do Observatório

- Taxonomia atual: v3.0; política de evidência: v1.1.
- Corpus portátil: 75 referências públicas com URLs únicas.
- Conhecimento consolidado: sete padrões provisórios, 33 hipóteses observadas e nenhum padrão validado automaticamente.
- O treinamento usa busca concentrada: três referências para um alvo existente, uma tentativa de falsificação ou limite e uma exploração controlada.
- Apoio só é contado quando o mecanismo está observado, a comparação é nível 1 ou 2 e a confiança é média ou alta; caso-limite não é contraexemplo.
- O comando `pnpm observatory:verify:v3` audita enums, cardinalidades, URLs, contagens, apoios e diversidade de criadores. O corpus pode crescer sem exigir a troca de um número fixo no verificador.
- Referências com cobertura parcial continuam marcadas para revisão humana; ausência de mídia, áudio, transcrição ou métricas não é convertida em nota zero nem em certeza classificatória.
