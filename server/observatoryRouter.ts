import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { getEvaluationProviderStatus } from "./aiProvider";
import { createObservatoryReference, getObservatoryReferenceById, listActiveObservatoryPatterns, listObservatoryReferences, recordObservatoryHypotheses, updateObservatoryReferenceResult } from "./db";
import { analyzeObservatoryReference, buildObservatoryContext, type ObservatoryMaterialInput } from "./observatory";
import { isAllowedPublicHttpsUrl, isInstagramPublicationUrl, publicLinkMessage, resolveInstagramMaterial } from "./publicLinks";
import { storagePut } from "./storage";
import { assessViralityEvidence } from "./virality";
import { PATTERN_TYPES } from "../shared/plateiaTaxonomy";
import { adminProcedure, router } from "./_core/trpc";

const contentTypeSchema = z.enum(["post", "carrossel", "reel", "copy"]);
const mediaMimeSchema = z.enum(["image/jpeg", "image/png", "image/webp", "video/mp4"]);
const optionalText = (max: number) => z.string().max(max).optional().transform(value => value?.trim() ?? "");
const observatoryHypothesisSchema = z.object({
  name: z.string().trim().min(1).max(180),
  patternType: z.enum(PATTERN_TYPES),
  observation: z.string(),
  mechanism: z.string(),
  evidence: z.string(),
  conditions: z.array(z.string()).default([]),
  limitations: z.array(z.string()).default([]),
  confidence: z.enum(["low", "medium", "high"]),
  stage: z.enum(["observation", "hypothesis", "contradicted", "inconclusive"]),
});

const uploadSchema = z.object({
  fileName: z.string().min(1).max(160),
  mimeType: mediaMimeSchema,
  base64: z.string().min(16),
});

const sourceSchema = z.object({
  url: z.string().trim().max(2048).url().refine(isAllowedPublicHttpsUrl, publicLinkMessage),
  kind: z.enum(["direct_media", "published_post"]),
  mimeType: mediaMimeSchema.optional(),
}).superRefine((source, ctx) => {
  if (source.kind === "direct_media" && !source.mimeType) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["mimeType"], message: "Informe o formato da mídia direta." });
});

export const createObservatoryReferenceInputSchema = z.object({
  title: optionalText(240),
  creator: optionalText(160),
  contentType: contentTypeSchema,
  contentText: optionalText(10_000),
  segmentHint: optionalText(240),
  objectiveHint: optionalText(240),
  metrics: z.record(z.string(), z.union([z.number(), z.string(), z.null()])).optional(),
  media: uploadSchema.optional(),
  source: sourceSchema.optional(),
}).superRefine((input, ctx) => {
  if (input.contentType === "copy" && !input.contentText) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["contentText"], message: "Cole a copy que será ensinada ao Observatório." });
  if (input.contentType !== "copy" && !input.media && !input.source) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["media"], message: "Envie o material ou informe um link público." });
});

function safeFileName(fileName: string) {
  return fileName.toLowerCase().replace(/[^a-z0-9._-]/g, "-").replace(/-+/g, "-");
}

export const observatoryRouter = router({
  providerStatus: adminProcedure.query(() => getEvaluationProviderStatus()),
  list: adminProcedure.query(() => listObservatoryReferences()),
  patterns: adminProcedure.query(() => listActiveObservatoryPatterns()),
  get: adminProcedure.input(z.object({ id: z.number().int().positive() })).query(async ({ input }) => {
    const reference = await getObservatoryReferenceById(input.id);
    if (!reference) throw new TRPCError({ code: "NOT_FOUND", message: "Referência não encontrada." });
    return reference;
  }),
  create: adminProcedure.input(createObservatoryReferenceInputSchema).mutation(async ({ ctx, input }) => {
    let mediaUrl: string | null = null;
    let mediaKey: string | null = null;
    let mediaMimeType: string | null = null;
    let contentText = input.contentText;
    const sourceUrl = input.source?.url ?? null;
    const sourceKind: "upload" | "direct_media" | "published_post" | "copy" = input.contentType === "copy" ? "copy" : input.media ? "upload" : input.source?.kind ?? "copy";

    if (input.media) {
      const payload = input.media.base64.includes(",") ? input.media.base64.split(",")[1] : input.media.base64;
      const buffer = Buffer.from(payload, "base64");
      if (buffer.byteLength > 12 * 1024 * 1024) throw new TRPCError({ code: "PAYLOAD_TOO_LARGE", message: "Envie arquivos de até 12 MB nesta versão." });
      const stored = await storagePut(`plateia/observatory/${Date.now()}-${safeFileName(input.media.fileName)}`, buffer, input.media.mimeType);
      mediaUrl = stored.url;
      mediaKey = stored.key;
      mediaMimeType = input.media.mimeType;
    }

    if (!mediaUrl && input.source?.kind === "direct_media") {
      mediaUrl = input.source.url;
      mediaMimeType = input.source.mimeType ?? null;
    }

    if (!mediaUrl && input.source?.kind === "published_post") {
      if (!isInstagramPublicationUrl(input.source.url)) throw new TRPCError({ code: "BAD_REQUEST", message: "Nesta etapa, links de publicação são aceitos pelo Instagram. Para outras origens, use o link direto da mídia." });
      const material = await resolveInstagramMaterial(input.source.url);
      if (material) {
        mediaUrl = material.mediaUrl;
        mediaMimeType = material.mediaMimeType;
        if (!contentText && material.caption) contentText = material.caption;
      }
    }

    const created = await createObservatoryReference({
      createdByUserId: ctx.user.id,
      title: input.title || `Referência de ${input.contentType}`,
      creator: input.creator,
      contentType: input.contentType,
      sourceKind,
      sourceUrl,
      contentText,
      mediaUrl,
      mediaKey,
      mediaMimeType,
      segmentHint: input.segmentHint,
      objectiveHint: input.objectiveHint,
      metricsJson: input.metrics ? JSON.stringify(input.metrics) : null,
    });

    if (input.contentType !== "copy" && !mediaUrl && !contentText) {
      const limitation = { access: { completeness: "insufficient", dataQuality: "low", accessibleElements: ["link"], missingElements: ["imagem", "vídeo", "áudio", "transcrição", "legenda"], limitations: ["O link não disponibilizou material suficiente. Envie o arquivo original."] } };
      await updateObservatoryReferenceResult(created.id, "needs_content", null, limitation);
      return { id: created.id, status: "needs_content" as const };
    }

    const materialInput: ObservatoryMaterialInput = {
      contentType: input.contentType,
      text: contentText,
      segmentHint: input.segmentHint,
      objectiveHint: input.objectiveHint,
      sourceUrl,
      mediaUrl,
      mediaMimeType,
      metrics: input.metrics ?? null,
    };

    try {
      const context = await buildObservatoryContext(materialInput, created.id);
      const analysis = await analyzeObservatoryReference(materialInput, context);
      await updateObservatoryReferenceResult(created.id, "analyzed", context.classification, { ...analysis, comparison: context, viralityEvidence: assessViralityEvidence(input.metrics) });
      const hypotheses = z.array(observatoryHypothesisSchema).safeParse(analysis.hypotheses);
      if (hypotheses.success) {
        try {
          await recordObservatoryHypotheses(created.id, context.classification, hypotheses.data);
        } catch (patternError) {
          console.warn("[Observatório Platéia] Referência aprendida, mas a consolidação de padrões ficou pendente:", patternError instanceof Error ? patternError.message : "erro desconhecido");
        }
      }
      return { id: created.id, status: "analyzed" as const };
    } catch (error) {
      console.error("[Observatório Platéia] Falha na curadoria:", error);
      await updateObservatoryReferenceResult(created.id, "failed", null, null);
      throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: "O Observatório não conseguiu concluir esta leitura. A referência foi preservada para nova tentativa." });
    }
  }),
});
