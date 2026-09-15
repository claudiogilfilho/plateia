export type StructuredEvaluationRequest = {
  prompt: string;
  mediaUrl?: string | null;
  mediaMimeType?: string | null;
  responseFormat: unknown;
};

export type EvaluationProviderKind = "builtin" | "openai-compatible" | "bridge";

export interface EvaluationProvider {
  readonly id?: string;
  evaluate(request: StructuredEvaluationRequest): Promise<string>;
}

type FetchLike = typeof fetch;
type ProviderEnvironment = Record<string, string | undefined>;

export type OpenAICompatibleProviderConfig = {
  baseUrl: string;
  apiKey?: string;
  model: string;
  timeoutMs?: number;
  structuredOutput?: "json_schema" | "json_object" | "none";
  videoPart?: "file_url" | "video_url" | "unsupported";
  fetchImpl?: FetchLike;
  enforceFreeOnly?: boolean;
  freeQuotaStopConfirmed?: boolean;
};

export type BridgeProviderConfig = {
  endpoint: string;
  apiKey?: string;
  timeoutMs?: number;
  fetchImpl?: FetchLike;
};

export const builtInEvaluationProvider: EvaluationProvider = {
  id: "builtin-disabled",
  async evaluate() { throw new Error("O motor embutido legado está desativado pela política de custo zero."); },
};

function positiveInteger(value: string | undefined, fallback: number) {
  const parsed = Number(value);
  return Number.isInteger(parsed) && parsed > 0 ? parsed : fallback;
}

function chatCompletionsUrl(baseUrl: string) {
  const normalized = baseUrl.trim().replace(/\/+$/, "");
  if (/\/chat\/completions$/i.test(normalized)) return normalized;
  if (/\/v1$/i.test(normalized)) return `${normalized}/chat/completions`;
  return `${normalized}/v1/chat/completions`;
}

let providerQueue: Promise<void> = Promise.resolve();

async function withProviderQuotaLock<T>(task: () => Promise<T>) {
  const previous = providerQueue;
  let release!: () => void;
  providerQueue = new Promise<void>(resolve => { release = resolve; });
  await previous;
  try { return await task(); } finally { release(); }
}

function retryAfterMilliseconds(value: string | null) {
  if (!value) return 0;
  const seconds = Number(value);
  if (Number.isFinite(seconds)) return Math.max(0, Math.min(30_000, seconds * 1000));
  const date = Date.parse(value);
  return Number.isFinite(date) ? Math.max(0, Math.min(30_000, date - Date.now())) : 0;
}

async function postJson(fetchImpl: FetchLike, url: string, body: unknown, apiKey: string | undefined, timeoutMs: number) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await withProviderQuotaLock(async () => {
      for (let attempt = 0; attempt < 2; attempt += 1) {
        const response = await fetchImpl(url, {
          method: "POST",
          headers: {
            "content-type": "application/json",
            ...(apiKey ? { authorization: `Bearer ${apiKey}` } : {}),
          },
          body: JSON.stringify(body),
          signal: controller.signal,
        });
        const payload = await response.json().catch(() => null) as unknown;
        if (response.ok) return payload;
        if (response.status === 429 && attempt === 0) {
          const waitMs = retryAfterMilliseconds(response.headers.get("retry-after"));
          if (waitMs > 0) {
            await new Promise(resolve => setTimeout(resolve, waitMs));
            continue;
          }
        }
        const detail = payload && typeof payload === "object" && "error" in payload ? JSON.stringify((payload as { error: unknown }).error) : response.statusText;
        throw new Error(`O provedor de IA respondeu ${response.status}: ${detail || "erro sem detalhes"}.`);
      }
      throw new Error("O provedor gratuito permaneceu indisponível após Retry-After.");
    });
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") throw new Error(`O provedor de IA excedeu ${timeoutMs} ms.`);
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}

function contentFromProvider(payload: unknown) {
  if (typeof payload === "string" && payload.trim()) return payload;
  if (!payload || typeof payload !== "object") throw new Error("O provedor retornou uma resposta vazia.");
  const record = payload as Record<string, unknown>;
  for (const key of ["output", "content", "result"] as const) {
    if (typeof record[key] === "string" && record[key].trim()) return record[key];
  }
  const choices = Array.isArray(record.choices) ? record.choices : [];
  const first = choices[0] as { message?: { content?: unknown } } | undefined;
  const content = first?.message?.content;
  if (typeof content === "string" && content.trim()) return content;
  if (Array.isArray(content)) {
    const text = content.flatMap(part => part && typeof part === "object" && typeof (part as { text?: unknown }).text === "string" ? [(part as { text: string }).text] : []).join("\n").trim();
    if (text) return text;
  }
  throw new Error("O provedor não retornou conteúdo textual compatível com o contrato do Plateia.");
}

function openAIUserContent(request: StructuredEvaluationRequest, videoPart: NonNullable<OpenAICompatibleProviderConfig["videoPart"]>) {
  const content: Array<Record<string, unknown>> = [{ type: "text", text: request.prompt }];
  if (request.mediaUrl && request.mediaMimeType?.startsWith("image/")) {
    content.push({ type: "image_url", image_url: { url: request.mediaUrl, detail: "high" } });
  }
  if (request.mediaUrl && request.mediaMimeType?.startsWith("video/")) {
    if (videoPart === "unsupported") throw new Error("Este adaptador não está configurado para vídeo. Use PLATEIA_AI_VIDEO_PART=file_url ou video_url, ou conecte uma ponte multimodal.");
    content.push(videoPart === "file_url"
      ? { type: "file_url", file_url: { url: request.mediaUrl, mime_type: request.mediaMimeType } }
      : { type: "video_url", video_url: { url: request.mediaUrl } });
  }
  return content;
}

export function createOpenAICompatibleProvider(config: OpenAICompatibleProviderConfig): EvaluationProvider {
  const fetchImpl = config.fetchImpl ?? fetch;
  const timeoutMs = config.timeoutMs ?? 90_000;
  const structuredOutput = config.structuredOutput ?? "json_schema";
  const videoPart = config.videoPart ?? "unsupported";
  if (!config.baseUrl.trim()) throw new Error("PLATEIA_AI_BASE_URL é obrigatória para o modo openai-compatible.");
  if (!config.model.trim()) throw new Error("PLATEIA_AI_MODEL é obrigatório para o modo openai-compatible.");
  const host = new URL(config.baseUrl).hostname.toLowerCase();
  const openRouter = host === "openrouter.ai" || host.endsWith(".openrouter.ai");
  const dashScope = host.endsWith(".aliyuncs.com") || host.endsWith(".alibabacloud.com");
  if (config.enforceFreeOnly && openRouter && !config.model.endsWith(":free")) throw new Error("Modelo bloqueado: o OpenRouter só pode usar modelos com sufixo :free no Platéia.");
  if (config.enforceFreeOnly && dashScope && !config.freeQuotaStopConfirmed) throw new Error("DashScope bloqueado: ative e confirme a parada automática ao esgotar a cota gratuita.");
  if (config.enforceFreeOnly && !openRouter && !dashScope) throw new Error("Provedor bloqueado: não há garantia configurada de cota exclusivamente gratuita.");
  return {
    id: "openai-compatible",
    async evaluate(request) {
      const responseFormat = structuredOutput === "json_schema" ? request.responseFormat : structuredOutput === "json_object" ? { type: "json_object" } : undefined;
      const payload = await postJson(fetchImpl, chatCompletionsUrl(config.baseUrl), {
        model: config.model,
        messages: [
          { role: "system", content: "Execute o protocolo do Plateia. Retorne somente JSON compatível com o esquema solicitado e não invente elementos ausentes." },
          { role: "user", content: openAIUserContent(request, videoPart) },
        ],
        max_tokens: 6000,
        ...(openRouter && config.enforceFreeOnly ? { provider: { allow_fallbacks: false, max_price: { prompt: 0, completion: 0 } } } : {}),
        ...(responseFormat ? { response_format: responseFormat } : {}),
      }, config.apiKey, timeoutMs);
      return contentFromProvider(payload);
    },
  };
}

export function createBridgeProvider(config: BridgeProviderConfig): EvaluationProvider {
  const fetchImpl = config.fetchImpl ?? fetch;
  const timeoutMs = config.timeoutMs ?? 90_000;
  if (!config.endpoint.trim()) throw new Error("PLATEIA_AI_BRIDGE_URL é obrigatória para o modo bridge.");
  return {
    id: "bridge",
    async evaluate(request) {
      const payload = await postJson(fetchImpl, config.endpoint, {
        protocol: "plateia-evaluation/2.1",
        prompt: request.prompt,
        media: request.mediaUrl ? { url: request.mediaUrl, mimeType: request.mediaMimeType ?? "application/octet-stream" } : null,
        responseFormat: request.responseFormat,
      }, config.apiKey, timeoutMs);
      return contentFromProvider(payload);
    },
  };
}

export function createEvaluationProviderFromEnv(environment: ProviderEnvironment = process.env): EvaluationProvider {
  const kind = (environment.PLATEIA_AI_PROVIDER || "openai-compatible").trim().toLowerCase() as EvaluationProviderKind;
  if (kind === "builtin") throw new Error("O motor embutido legado está desativado: ele não oferece garantia de uso exclusivamente gratuito.");
  if (kind === "openai-compatible") {
    const structured = environment.PLATEIA_AI_STRUCTURED_OUTPUT;
    const video = environment.PLATEIA_AI_VIDEO_PART;
    return createOpenAICompatibleProvider({
      baseUrl: environment.PLATEIA_AI_BASE_URL || (environment.OPENROUTER_API_KEY ? "https://openrouter.ai/api/v1" : ""),
      apiKey: environment.PLATEIA_AI_API_KEY || environment.OPENROUTER_API_KEY || environment.DASHSCOPE_API_KEY,
      model: environment.PLATEIA_AI_MODEL || (environment.OPENROUTER_API_KEY ? "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free" : ""),
      timeoutMs: positiveInteger(environment.PLATEIA_AI_TIMEOUT_MS, 90_000),
      structuredOutput: structured === "none" || structured === "json_object" ? structured : "json_schema",
      videoPart: video === "file_url" || video === "video_url" ? video : "unsupported",
      enforceFreeOnly: true,
      freeQuotaStopConfirmed: environment.DASHSCOPE_FREE_ONLY === "true",
    });
  }
  if (kind === "bridge") {
    if (environment.PLATEIA_BRIDGE_FREE_ONLY !== "true") throw new Error("Ponte bloqueada: confirme PLATEIA_BRIDGE_FREE_ONLY=true somente quando não houver cobrança nem fallback pago.");
    return createBridgeProvider({
      endpoint: environment.PLATEIA_AI_BRIDGE_URL || "",
      apiKey: environment.PLATEIA_AI_API_KEY,
      timeoutMs: positiveInteger(environment.PLATEIA_AI_TIMEOUT_MS, 90_000),
    });
  }
  throw new Error(`PLATEIA_AI_PROVIDER inválido: ${kind}. Use openai-compatible ou bridge.`);
}

let providerOverride: EvaluationProvider | null = null;
let environmentProvider: EvaluationProvider | null = null;

export function setEvaluationProvider(provider: EvaluationProvider) {
  providerOverride = provider;
}

export function resetEvaluationProvider() {
  providerOverride = null;
  environmentProvider = null;
}

export function evaluateWithProvider(request: StructuredEvaluationRequest) {
  if (providerOverride) return providerOverride.evaluate(request);
  environmentProvider ??= createEvaluationProviderFromEnv();
  return environmentProvider.evaluate(request);
}

export function getEvaluationProviderStatus(environment: ProviderEnvironment = process.env) {
  const kind = (environment.PLATEIA_AI_PROVIDER || "openai-compatible").trim().toLowerCase();
  if (kind === "builtin") {
    return {
      provider: "builtin",
      configured: false,
      supportsImage: false,
      supportsVideo: false,
      portableProtocol: "plateia-evaluation/2.1",
      message: "Motor embutido legado bloqueado pela política de custo zero.",
    } as const;
  }
  if (kind === "openai-compatible") {
    const baseUrl = environment.PLATEIA_AI_BASE_URL || (environment.OPENROUTER_API_KEY ? "https://openrouter.ai/api/v1" : "");
    const model = environment.PLATEIA_AI_MODEL || (environment.OPENROUTER_API_KEY ? "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free" : "");
    const openRouter = baseUrl.includes("openrouter.ai");
    const dashScope = baseUrl.includes("aliyuncs.com") || baseUrl.includes("alibabacloud.com");
    const freeOnly = openRouter ? model.endsWith(":free") : dashScope ? environment.DASHSCOPE_FREE_ONLY === "true" : false;
    const configured = Boolean(baseUrl && model && freeOnly && (environment.PLATEIA_AI_API_KEY || environment.OPENROUTER_API_KEY || environment.DASHSCOPE_API_KEY));
    const supportsVideo = configured && ["file_url", "video_url"].includes(environment.PLATEIA_AI_VIDEO_PART || "");
    return {
      provider: "openai-compatible",
      configured,
      supportsImage: configured,
      supportsVideo,
      portableProtocol: "plateia-evaluation/2.1",
      message: configured ? supportsVideo ? "Motor gratuito compatível pronto para imagem e vídeo, sem fallback pago." : "Motor gratuito pronto para texto e imagem; vídeo exige transporte multimodal." : "Informe a URL, a chave e um modelo comprovadamente gratuito.",
    } as const;
  }
  if (kind === "bridge") {
    const configured = Boolean(environment.PLATEIA_AI_BRIDGE_URL && environment.PLATEIA_BRIDGE_FREE_ONLY === "true");
    return {
      provider: "bridge",
      configured,
      supportsImage: configured,
      supportsVideo: configured,
      portableProtocol: "plateia-evaluation/2.1",
      message: configured ? "Ponte multimodal gratuita pronta." : "Informe a ponte e confirme a política de custo zero.",
    } as const;
  }
  return {
    provider: kind,
    configured: false,
    supportsImage: false,
    supportsVideo: false,
    portableProtocol: "plateia-evaluation/2.1",
    message: "O provedor de IA configurado não é reconhecido.",
  } as const;
}
