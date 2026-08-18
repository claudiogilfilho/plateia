export type EvaluationContentType = "post" | "carrossel" | "reel" | "copy";

export function validateEvaluationForm(input: {
  contentType: EvaluationContentType;
  sourceMode: "upload" | "link";
  hasMedia: boolean;
  sourceUrl: string;
  contentText: string;
}): string | null {
  if (input.contentType === "copy" && !input.contentText.trim()) return "Cole a copy para continuar.";
  if (input.contentType !== "copy" && input.sourceMode === "upload" && !input.hasMedia) return "Para post, carrossel ou Reel, envie a imagem ou o vídeo do material.";
  if (input.sourceMode === "link") {
    try {
      const parsed = new URL(input.sourceUrl);
      if (parsed.protocol !== "https:") throw new Error();
    } catch {
      return "Informe um link HTTPS público e completo.";
    }
  }
  return null;
}
