import { invokeLLM, listLLMModels } from "./_core/llm";

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
};

export type BridgeProviderConfig = {
  endpoint: string;
  apiKey?: string;
  timeoutMs?: number;
  fetchImpl?: FetchLike;
};

async function selectInitialModel() {
  const { data: models } = await listLLMModels();
  return models.find(item => item.id === "gemini-3-flash-preview")?.id ?? models.find(item => item.id === "gpt-5-mini")?.id ?? models[0]?.id;
}

export const builtInEvaluationProvider: EvaluationProvider = {
  id: "builtin",
  async evaluate(request) {
    const model = await selectInitialModel();
    if (!model) throw new Error("Nenhum modelo de IA está disponível para a avaliação.");

    const content: Array<Record<string, unknown>> = [{ type: "text", text: request.prompt }];
    if (request.mediaUrl && request.mediaMimeType?.startsWith("image/")) {
      content.push({ type: "image_url", image_url: { url: request.mediaUrl, detail: "high" } });
    }
    if (request.mediaUrl && request.mediaMimeType?.startsWith("video/")) {
      content.push({ type: "file_url", file_url: { url: request.mediaUrl, mime_type: "video/mp4" } });
    }

    const response = await invokeLLM({
      model,
      messages: [
        { role: "system", content: "Você produz avaliações estruturadas para criadores e marcas. Retorne somente JSON compatível com o esquema solicitado." },
        { role: "user", content: content as never },
      ],
      response_format: request.responseFormat as never,
      max_tokens: 6000,
    });
    const raw = response.choices[0]?.message?.content;
    if (!raw || typeof raw !== "string") throw new Error("A IA não retornou uma avaliação válida.");
    return raw;
  },
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

async function postJson(fetchImpl: FetchLike, url: string, body: unknown, apiKey: string | undefined, timeoutMs: number) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
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
    if (!response.ok) {
      const detail = payload && typeof payload === "object" && "error" in payload ? JSON.stringify((payload as { error: unknown }).error) : response.statusText;
      throw new Error(`O provedor de IA respondeu ${response.status}: ${detail || "erro sem detalhes"}.`);
    }
    return payload;
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
        protocol: "plateia-evaluation/1.0",
        prompt: request.prompt,
        media: request.mediaUrl ? { url: request.mediaUrl, mimeType: request.mediaMimeType ?? "application/octet-stream" } : null,
        responseFormat: request.responseFormat,
      }, config.apiKey, timeoutMs);
      return contentFromProvider(payload);
    },
  };
}

export function createEvaluationProviderFromEnv(environment: ProviderEnvironment = process.env): EvaluationProvider {
  const kind = (environment.PLATEIA_AI_PROVIDER || "builtin").trim().toLowerCase() as EvaluationProviderKind;
  if (kind === "builtin") return builtInEvaluationProvider;
  if (kind === "openai-compatible") {
    const structured = environment.PLATEIA_AI_STRUCTURED_OUTPUT;
    const video = environment.PLATEIA_AI_VIDEO_PART;
    return createOpenAICompatibleProvider({
      baseUrl: environment.PLATEIA_AI_BASE_URL || "",
      apiKey: environment.PLATEIA_AI_API_KEY,
      model: environment.PLATEIA_AI_MODEL || "",
      timeoutMs: positiveInteger(environment.PLATEIA_AI_TIMEOUT_MS, 90_000),
      structuredOutput: structured === "none" || structured === "json_object" ? structured : "json_schema",
      videoPart: video === "file_url" || video === "video_url" ? video : "unsupported",
    });
  }
  if (kind === "bridge") {
    return createBridgeProvider({
      endpoint: environment.PLATEIA_AI_BRIDGE_URL || "",
      apiKey: environment.PLATEIA_AI_API_KEY,
      timeoutMs: positiveInteger(environment.PLATEIA_AI_TIMEOUT_MS, 90_000),
    });
  }
  throw new Error(`PLATEIA_AI_PROVIDER inválido: ${kind}. Use builtin, openai-compatible ou bridge.`);
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
  environmentProvider ??= createEvaluationProviderFromEnv();
  return (providerOverride ?? environmentProvider).evaluate(request);
}

export function getEvaluationProviderStatus(environment: ProviderEnvironment = process.env) {
  const kind = (environment.PLATEIA_AI_PROVIDER || "builtin").trim().toLowerCase();
  if (kind === "builtin") {
    const configured = Boolean(environment.BUILT_IN_FORGE_API_URL && environment.BUILT_IN_FORGE_API_KEY);
    return {
      provider: "builtin",
      configured,
      supportsImage: configured,
      supportsVideo: configured,
      portableProtocol: "plateia-evaluation/1.0",
      message: configured ? "Motor de IA embutido pronto." : "Configure um motor de IA para iniciar avaliações.",
    } as const;
  }
  if (kind === "openai-compatible") {
    const configured = Boolean(environment.PLATEIA_AI_BASE_URL && environment.PLATEIA_AI_MODEL);
    const supportsVideo = configured && ["file_url", "video_url"].includes(environment.PLATEIA_AI_VIDEO_PART || "");
    return {
      provider: "openai-compatible",
      configured,
      supportsImage: configured,
      supportsVideo,
      portableProtocol: "plateia-evaluation/1.0",
      message: configured ? supportsVideo ? "Motor compatível pronto para imagem e vídeo." : "Motor pronto para texto e imagem; vídeo exige transporte multimodal." : "Informe a URL e o modelo do provedor compatível.",
    } as const;
  }
  if (kind === "bridge") {
    const configured = Boolean(environment.PLATEIA_AI_BRIDGE_URL);
    return {
      provider: "bridge",
      configured,
      supportsImage: configured,
      supportsVideo: configured,
      portableProtocol: "plateia-evaluation/1.0",
      message: configured ? "Ponte multimodal pronta." : "Informe o endereço da ponte de IA.",
    } as const;
  }
  return {
    provider: kind,
    configured: false,
    supportsImage: false,
    supportsVideo: false,
    portableProtocol: "plateia-evaluation/1.0",
    message: "O provedor de IA configurado não é reconhecido.",
  } as const;
}
