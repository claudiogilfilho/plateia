import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { createAnalysis, getAnalysisByIdForUser, listAnalysesForUser, updateAnalysisResult } from "./db";
import { applyVisualOnlyScope, evaluateContent } from "./contentAnalysis";
import { protectedProcedure, router } from "./_core/trpc";
import { storagePut } from "./storage";
import { isAllowedPublicHttpsUrl, isInstagramPublicationUrl, publicLinkMessage, resolveInstagramMaterial } from "./publicLinks";
import { buildObservatoryContext, type ObservatoryContext } from "./observatory";

const contentTypeSchema = z.enum(["post", "carrossel", "reel", "copy"]);
const mediaMimeSchema = z.enum(["image/jpeg", "image/png", "image/webp", "video/mp4"]);
const optionalText = (max: number) => z.string().max(max).optional().transform(value => value?.trim() ?? "");
const visualOnlyExcludedCriteria = ["clareza", "ação", "objeções"] as const;

const uploadSchema = z.object({
  fileName: z.string().min(1).max(160),
  mimeType: z.string().regex(/^(image\/(jpeg|png|webp)|video\/mp4)$/),
  base64: z.string().min(16),
});

const remoteSourceSchema = z.object({
  url: z.string().trim().max(2048).url().refine(isAllowedPublicHttpsUrl, publicLinkMessage),
  kind: z.enum(["direct_media", "published_post"]),
  mimeType: mediaMimeSchema.optional(),
}).superRefine((source, ctx) => {
  if (source.kind === "direct_media" && !source.mimeType) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["mimeType"], message: "Informe se o link direto aponta para imagem ou vídeo." });
});

export const createAnalysisInputSchema = z.object({
  contentType: contentTypeSchema,
  contentText: optionalText(10_000),
  product: optionalText(300),
  objective: optionalText(300),
  targetAudience: optionalText(600),
  media: uploadSchema.optional(),
  source: remoteSourceSchema.optional(),
  skipCaption: z.boolean().optional().default(false),
}).superRefine((input, ctx) => {
  if (input.contentType === "copy" && !input.contentText) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["contentText"], message: "Para avaliar uma copy, cole o texto do conteúdo." });
  if (input.contentType !== "copy" && !input.media && !input.source) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["media"], message: "Para post, carrossel ou Reel, envie um arquivo ou informe um link público do material." });
});

type ReadingCoverage = {
  level: "complete" | "partial" | "requires_complement";
  title: string;
  description: string;
  mode?: "visual_only" | "requires_visual";
  excludedCriteria?: readonly (typeof visualOnlyExcludedCriteria)[number][];
};

function visualOnlyCoverage(): ReadingCoverage {
  return {
    level: "partial",
    mode: "visual_only",
    excludedCriteria: visualOnlyExcludedCriteria,
    title: "Leitura visual sem legenda",
    description: "A Platéia avaliou somente os elementos visuais disponíveis. Clareza textual, ação e objeções ligadas à copy não entram na leitura consolidada.",
  };
}

function safeFileName(fileName: string) {
  return fileName.toLowerCase().replace(/[^a-z0-9._-]/g, "-").replace(/-+/g, "-");
}

export const analysesRouter = router({
  list: protectedProcedure.query(async ({ ctx }) => listAnalysesForUser(ctx.user.id)),

  get: protectedProcedure.input(z.object({ id: z.number().int().positive() })).query(async ({ ctx, input }) => {
    const analysis = await getAnalysisByIdForUser(input.id, ctx.user.id);
    if (!analysis) throw new TRPCError({ code: "NOT_FOUND", message: "Avaliação não encontrada." });
    return analysis;
  }),

  create: protectedProcedure.input(createAnalysisInputSchema).mutation(async ({ ctx, input }) => {
    let mediaUrl: string | null = null;
    let mediaKey: string | null = null;
    let mediaMimeType: string | null = null;
    let contentText = input.skipCaption ? "" : input.contentText;
    const sourceUrl = input.source?.url ?? null;
    const sourceKind = input.source?.kind ?? null;
    const sourceMediaMimeType = input.source?.mimeType ?? null;
    let coverage: ReadingCoverage = {
      level: "complete",
      title: "Leitura completa",
      description: input.contentType === "copy" ? "A Platéia avaliou o texto enviado." : "A Platéia avaliou o material visual enviado.",
    };

    if (input.media) {
      const payload = input.media.base64.includes(",") ? input.media.base64.split(",")[1] : input.media.base64;
      const buffer = Buffer.from(payload, "base64");
      if (buffer.byteLength > 12 * 1024 * 1024) throw new TRPCError({ code: "PAYLOAD_TOO_LARGE", message: "Envie arquivos de até 12 MB nesta versão inicial." });
      const stored = await storagePut(`plateia/${ctx.user.id}/${Date.now()}-${safeFileName(input.media.fileName)}`, buffer, input.media.mimeType);
      mediaUrl = stored.url;
      mediaKey = stored.key;
      mediaMimeType = input.media.mimeType;
    }

    if (!mediaUrl && input.source?.kind === "direct_media") {
      mediaUrl = input.source.url;
      mediaMimeType = input.source.mimeType ?? null;
    }

    if (!mediaUrl && input.source?.kind === "published_post") {
      if (!isInstagramPublicationUrl(input.source.url)) throw new TRPCError({ code: "BAD_REQUEST", message: "Por enquanto, links de posts publicados são suportados no Instagram. Para outras redes, envie o arquivo ou use um link direto da mídia." });
      const instagram = await resolveInstagramMaterial(input.source.url);
      coverage = {
        level: "partial",
        title: "Leitura parcial do Instagram",
        description: "A Platéia considera apenas a capa e a legenda pública disponíveis. Para analisar cenas, ritmo e áudio do Reel, envie o MP4.",
      };
      if (instagram) {
        mediaUrl = instagram.mediaUrl;
        mediaMimeType = instagram.mediaMimeType;
        if (!input.skipCaption && !contentText && instagram.caption) contentText = instagram.caption;
      } else if (!contentText) {
        coverage = {
          level: "requires_complement",
          mode: "requires_visual",
          title: "Material visual necessário",
          description: "O Instagram não disponibilizou capa, imagem ou vídeo público para este link. Envie o arquivo original para a Platéia avaliar o conteúdo visual; a legenda continua opcional.",
        };
      } else {
        coverage = {
          level: "partial",
          title: "Leitura parcial pela legenda",
          description: "O Instagram não liberou a prévia visual; a Platéia avaliou somente o texto informado. Envie o MP4 para uma leitura visual completa.",
        };
      }
      if (mediaUrl && (input.skipCaption || !contentText)) coverage = visualOnlyCoverage();
    }

    if (input.contentType !== "copy" && mediaUrl && (input.skipCaption || !contentText) && coverage.level === "complete") coverage = visualOnlyCoverage();

    if (input.contentType !== "copy" && !mediaUrl && !contentText && coverage.level !== "requires_complement") throw new TRPCError({ code: "BAD_REQUEST", message: "A Platéia precisa de uma imagem, vídeo, carrossel ou texto de complemento para avaliar esse conteúdo." });

    const created = await createAnalysis({
      userId: ctx.user.id,
      contentType: input.contentType,
      contentText,
      product: input.product,
      objective: input.objective,
      targetAudience: input.targetAudience,
      mediaUrl,
      mediaKey,
      mediaMimeType,
      sourceUrl,
      sourceKind,
      sourceMediaMimeType,
    });

    if (coverage.level === "requires_complement") {
      await updateAnalysisResult(created.id, "needs_content", { coverage });
      return { id: created.id, status: "needs_content" as const };
    }

    try {
      let observatoryContext: ObservatoryContext | null = null;
      try {
        observatoryContext = await buildObservatoryContext({
          contentType: input.contentType,
          text: contentText,
          segmentHint: input.product,
          objectiveHint: input.objective,
          sourceUrl,
          mediaUrl,
          mediaMimeType,
          metrics: null,
        });
      } catch (observatoryError) {
        console.warn("[Platéia] Observatório indisponível; seguindo com avaliação estrutural:", observatoryError instanceof Error ? observatoryError.message : "erro desconhecido");
      }
      const evaluation = await evaluateContent({
        contentType: input.contentType,
        text: contentText,
        product: input.product,
        objective: input.objective,
        targetAudience: input.targetAudience,
        mediaUrl,
        mediaMimeType,
        sourceUrl,
        analysisScope: coverage.mode === "visual_only" ? "visual_only" : "standard",
        observatoryContext,
      });
      const scopedEvaluation = coverage.mode === "visual_only"
        ? observatoryContext ? applyVisualOnlyScope(evaluation, observatoryContext.classification) : applyVisualOnlyScope(evaluation)
        : evaluation;
      await updateAnalysisResult(created.id, "completed", { ...scopedEvaluation, coverage, observatory: observatoryContext });
      return { id: created.id, status: "completed" as const };
    } catch (error) {
      await updateAnalysisResult(created.id, "failed", null);
      console.error("[Platéia] Falha na avaliação:", error);
      throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: "A Platéia não conseguiu finalizar a leitura agora. Tente novamente em instantes." });
    }
  }),
});
