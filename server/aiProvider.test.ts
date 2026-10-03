import { afterEach, describe, expect, it, vi } from "vitest";
import { createBridgeProvider, createEvaluationProviderFromEnv, createOpenAICompatibleProvider, getEvaluationProviderStatus, resetEvaluationProvider } from "./aiProvider";

afterEach(() => resetEvaluationProvider());

const request = { prompt: "Avalie esta copy.", responseFormat: { type: "json_schema", json_schema: { name: "test", schema: { type: "object" } } } };

describe("provedores portáteis do Plateia", () => {
  it("falha de forma segura quando nenhum motor gratuito foi configurado", () => {
    expect(() => createEvaluationProviderFromEnv({})).toThrow("PLATEIA_AI_BASE_URL");
    expect(getEvaluationProviderStatus({})).toMatchObject({ provider: "openai-compatible", configured: false });
  });

  it("expõe capacidade de vídeo somente quando o transporte foi configurado", () => {
    const free = { PLATEIA_AI_PROVIDER: "openai-compatible", PLATEIA_AI_BASE_URL: "https://openrouter.ai/api/v1", PLATEIA_AI_API_KEY: "segredo", PLATEIA_AI_MODEL: "nvidia/test:free" };
    expect(getEvaluationProviderStatus(free)).toMatchObject({ configured: true, supportsImage: true, supportsVideo: false });
    expect(getEvaluationProviderStatus({ ...free, PLATEIA_AI_VIDEO_PART: "video_url" })).toMatchObject({ supportsVideo: true });
  });

  it("envia o contrato OpenAI-compatible sem depender de um SDK específico", async () => {
    const fetchImpl = vi.fn(async (_url: string | URL | Request, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body));
      expect(body).toMatchObject({ model: "modelo-teste", response_format: request.responseFormat });
      expect(body.messages[1].content[0]).toEqual({ type: "text", text: request.prompt });
      return new Response(JSON.stringify({ choices: [{ message: { content: "{\"ok\":true}" } }] }), { status: 200, headers: { "content-type": "application/json" } });
    }) as typeof fetch;
    const provider = createOpenAICompatibleProvider({ baseUrl: "https://ia.exemplo/v1", apiKey: "segredo", model: "modelo-teste", fetchImpl });
    await expect(provider.evaluate(request)).resolves.toBe("{\"ok\":true}");
    expect(fetchImpl).toHaveBeenCalledWith("https://ia.exemplo/v1/chat/completions", expect.objectContaining({ method: "POST" }));
  });

  it("não finge ter assistido vídeo quando o transporte não foi configurado", async () => {
    const provider = createOpenAICompatibleProvider({ baseUrl: "https://ia.exemplo", model: "modelo", fetchImpl: vi.fn() as typeof fetch });
    await expect(provider.evaluate({ ...request, mediaUrl: "https://cdn.exemplo/video.mp4", mediaMimeType: "video/mp4" })).rejects.toThrow("não está configurado para vídeo");
  });

  it("envia mídia e schema pela ponte neutra e aceita uma saída direta", async () => {
    const fetchImpl = vi.fn(async (_url: string | URL | Request, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body));
      expect(body).toMatchObject({ protocol: "plateia-evaluation/2.1", media: { url: "https://cdn.exemplo/post.jpg", mimeType: "image/jpeg" }, responseFormat: request.responseFormat });
      return new Response(JSON.stringify({ output: "{\"resultado\":\"ok\"}" }), { status: 200, headers: { "content-type": "application/json" } });
    }) as typeof fetch;
    const provider = createBridgeProvider({ endpoint: "https://ponte.exemplo/plateia", fetchImpl });
    await expect(provider.evaluate({ ...request, mediaUrl: "https://cdn.exemplo/post.jpg", mediaMimeType: "image/jpeg" })).resolves.toBe("{\"resultado\":\"ok\"}");
  });

  it("recusa uma configuração desconhecida", () => {
    expect(() => createEvaluationProviderFromEnv({ PLATEIA_AI_PROVIDER: "qualquer-coisa" })).toThrow("PLATEIA_AI_PROVIDER inválido");
  });

  it("não ativa uma ponte sem confirmação explícita de custo zero", () => {
    expect(() => createEvaluationProviderFromEnv({ PLATEIA_AI_PROVIDER: "bridge", PLATEIA_AI_BRIDGE_URL: "https://ponte.example" })).toThrow("PLATEIA_BRIDGE_FREE_ONLY");
  });

  it("bloqueia modelo pago do OpenRouter antes de qualquer chamada", () => {
    expect(() => createOpenAICompatibleProvider({ baseUrl: "https://openrouter.ai/api/v1", model: "modelo/pago", enforceFreeOnly: true })).toThrow("sufixo :free");
  });

  it("bloqueia DashScope quando a parada por cota gratuita não foi confirmada", () => {
    expect(() => createOpenAICompatibleProvider({ baseUrl: "https://ws.example.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1", model: "qwen-omni", enforceFreeOnly: true })).toThrow("parada automática");
  });

  it("impede fallback pago e define preço máximo zero no OpenRouter", async () => {
    const fetchImpl = vi.fn(async (_url: string | URL | Request, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body));
      expect(body.provider).toEqual({ allow_fallbacks: false, max_price: { prompt: 0, completion: 0 } });
      return new Response(JSON.stringify({ choices: [{ message: { content: "{\"ok\":true}" } }] }), { status: 200 });
    }) as typeof fetch;
    const provider = createOpenAICompatibleProvider({ baseUrl: "https://openrouter.ai/api/v1", model: "nvidia/test:free", enforceFreeOnly: true, fetchImpl });
    await expect(provider.evaluate(request)).resolves.toContain("ok");
  });

  it("respeita Retry-After uma vez antes de interromper a cota gratuita", async () => {
    const fetchImpl = vi.fn()
      .mockResolvedValueOnce(new Response(JSON.stringify({ error: "cota temporária" }), { status: 429, headers: { "retry-after": "0.001" } }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ choices: [{ message: { content: "{\"ok\":true}" } }] }), { status: 200 }));
    const provider = createOpenAICompatibleProvider({ baseUrl: "https://openrouter.ai/api/v1", model: "nvidia/test:free", enforceFreeOnly: true, fetchImpl });
    await expect(provider.evaluate(request)).resolves.toContain("ok");
    expect(fetchImpl).toHaveBeenCalledTimes(2);
  });
});
