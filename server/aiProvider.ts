import { invokeLLM, listLLMModels } from "./_core/llm";

export type StructuredEvaluationRequest = {
  prompt: string;
  mediaUrl?: string | null;
  mediaMimeType?: string | null;
  responseFormat: unknown;
};

export interface EvaluationProvider {
  evaluate(request: StructuredEvaluationRequest): Promise<string>;
}

async function selectInitialModel() {
  const { data: models } = await listLLMModels();
  return models.find(item => item.id === "gemini-3-flash-preview")?.id ?? models.find(item => item.id === "gpt-5-mini")?.id ?? models[0]?.id;
}

export const builtInEvaluationProvider: EvaluationProvider = {
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

let activeProvider: EvaluationProvider = builtInEvaluationProvider;

export function setEvaluationProvider(provider: EvaluationProvider) {
  activeProvider = provider;
}

export function evaluateWithProvider(request: StructuredEvaluationRequest) {
  return activeProvider.evaluate(request);
}
