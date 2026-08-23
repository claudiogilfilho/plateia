import { afterEach, describe, expect, it, vi } from "vitest";
import { createBridgeProvider, createEvaluationProviderFromEnv, createOpenAICompatibleProvider, getEvaluationProviderStatus, resetEvaluationProvider } from "./aiProvider";

afterEach(() => resetEvaluationProvider());

const request = { prompt: "Avalie esta copy.", responseFormat: { type: "json_schema", json_schema: { name: "test", schema: { type: "object" } } } };

describe("provedores portáteis do Plateia", () => {
  it("configura o provedor embutido por padrão", () => {
    expect(createEvaluationProviderFromEnv({}).id).toBe("builtin");
    expect(getEvaluationProviderStatus({})).toMatchObject({ provider: "builtin", configured: false });
  });

  it("expõe capacidade de vídeo somente quando o transporte foi configurado", () => {
    expect(getEvaluationProviderStatus({ PLATEIA_AI_PROVIDER: "openai-compatible", PLATEIA_AI_BASE_URL: "https://ia.exemplo", PLATEIA_AI_MODEL: "modelo" })).toMatchObject({ configured: true, supportsImage: true, supportsVideo: false });
    expect(getEvaluationProviderStatus({ PLATEIA_AI_PROVIDER: "openai-compatible", PLATEIA_AI_BASE_URL: "https://ia.exemplo", PLATEIA_AI_MODEL: "modelo", PLATEIA_AI_VIDEO_PART: "video_url" })).toMatchObject({ supportsVideo: true });
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
      expect(body).toMatchObject({ protocol: "plateia-evaluation/1.0", media: { url: "https://cdn.exemplo/post.jpg", mimeType: "image/jpeg" }, responseFormat: request.responseFormat });
      return new Response(JSON.stringify({ output: "{\"resultado\":\"ok\"}" }), { status: 200, headers: { "content-type": "application/json" } });
    }) as typeof fetch;
    const provider = createBridgeProvider({ endpoint: "https://ponte.exemplo/plateia", fetchImpl });
    await expect(provider.evaluate({ ...request, mediaUrl: "https://cdn.exemplo/post.jpg", mediaMimeType: "image/jpeg" })).resolves.toBe("{\"resultado\":\"ok\"}");
  });

  it("recusa uma configuração desconhecida", () => {
    expect(() => createEvaluationProviderFromEnv({ PLATEIA_AI_PROVIDER: "qualquer-coisa" })).toThrow("PLATEIA_AI_PROVIDER inválido");
  });
});
