# Platéia portátil

O protocolo do Platéia não depende mais do serviço de IA embutido. Há três superfícies complementares:

1. **Agent Skill** em `.agents/skills/plateia`: funciona em agentes compatíveis com o padrão aberto de skills. Inclui protocolo, taxonomias, contrato de relatório, memória JSON e extração de quadros de vídeo.
2. **Prompt independente** em `.agents/skills/plateia/references/portable-system-prompt.md`: pode ser usado como instrução de sistema em ambientes que não suportam skills.
3. **Adaptadores do aplicativo** em `server/aiProvider.ts`: permitem trocar o motor sem alterar o Observatório, as notas ou o relatório.

## Modos do aplicativo

### Motor embutido

É o padrão e preserva a configuração atual.

```env
PLATEIA_AI_PROVIDER=builtin
```

### API compatível com OpenAI

Serve para qualquer gateway ou modelo que implemente `POST /v1/chat/completions`.

```env
PLATEIA_AI_PROVIDER=openai-compatible
PLATEIA_AI_BASE_URL=https://provedor.exemplo/v1
PLATEIA_AI_API_KEY=configure-no-cofre-do-ambiente
PLATEIA_AI_MODEL=modelo-multimodal
PLATEIA_AI_STRUCTURED_OUTPUT=json_schema
PLATEIA_AI_VIDEO_PART=file_url
PLATEIA_AI_TIMEOUT_MS=90000
```

`PLATEIA_AI_STRUCTURED_OUTPUT` aceita `json_schema`, `json_object` ou `none`. `PLATEIA_AI_VIDEO_PART` aceita `file_url`, `video_url` ou fica sem suporte. Sem transporte de vídeo configurado, o adaptador interrompe a leitura em vez de fingir que assistiu.

### Ponte neutra

Use para Claude, Gemini, Bedrock, Vertex, modelos locais ou qualquer API que não siga o formato anterior. A ponte recebe um contrato estável e traduz para o provedor escolhido.

```env
PLATEIA_AI_PROVIDER=bridge
PLATEIA_AI_BRIDGE_URL=https://sua-ponte.exemplo/plateia/evaluate
PLATEIA_AI_API_KEY=configure-no-cofre-do-ambiente
PLATEIA_AI_TIMEOUT_MS=90000
```

Requisição:

```json
{
  "protocol": "plateia-evaluation/1.0",
  "prompt": "protocolo e material textual",
  "media": {
    "url": "https://url-assinada.exemplo/video.mp4",
    "mimeType": "video/mp4"
  },
  "responseFormat": {
    "type": "json_schema",
    "json_schema": {}
  }
}
```

Resposta aceita:

```json
{ "output": "{\"json\":\"estruturado\"}" }
```

Também são aceitos `content`, `result` ou o formato `choices[0].message.content`.

## Executar como skill

Pedidos típicos:

- “Use o Platéia para avaliar este Reel antes de eu publicar.”
- “Compare esta arte somente com referências educativas.”
- “Ensine este vídeo ao Observatório, mas não transforme uma observação em regra.”
- “Analise esta copy pelos cinco cérebros e dê três melhorias prioritárias.”

Quando um ambiente não lê vídeo nativamente, executar:

```bash
python3 .agents/skills/plateia/scripts/extract_video_frames.py video.mp4 --output ./quadros
```

Para memória portátil:

```bash
python3 .agents/skills/plateia/scripts/observatory_memory.py --db plateia-memory.json add --record referencia.json
python3 .agents/skills/plateia/scripts/observatory_memory.py --db plateia-memory.json search --classification classificacao.json
```

O arquivo `plateia-memory.json` pode acompanhar o projeto entre diferentes ambientes. Nenhuma chave de API deve ser colocada nele.
