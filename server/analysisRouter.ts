import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { createAnalysis, getAnalysisByIdForUser, listAnalysesForUser, updateAnalysisResult } from "./db";
import { evaluateContent } from "./contentAnalysis";
import { protectedProcedure, router } from "./_core/trpc";
import { storagePut } from "./storage";
import { isAllowedPublicHttpsUrl, publicLinkMessage } from "./publicLinks";

const contentTypeSchema = z.enum(["post", "carrossel", "reel", "copy"]);

const uploadSchema = z.object({
  fileName: z.string().min(1).max(160),
  mimeType: z.string().regex(/^(image\/(jpeg|png|webp)|video\/mp4)$/),
  base64: z.string().min(16),
});

const remoteSourceSchema = z.object({
  url: z.string().trim().max(2048).url().refine(isAllowedPublicHttpsUrl, publicLinkMessage),
  kind: z.enum(["direct_media", "published_post"]),
  mimeType: z.enum(["image/jpeg", "image/png", "image/webp", "video/mp4"]).optional(),
}).superRefine((source, ctx) => {
  if (source.kind === "direct_media" && !source.mimeType) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["mimeType"], message: "Informe se o link direto aponta para imagem ou vídeo." });
  }
});

const createSchema = z.object({
  contentType: contentTypeSchema,
  contentText: z.string().max(10000).default(""),
  product: z.string().min(2).max(300),
  objective: z.string().min(2).max(300),
  targetAudience: z.string().min(2).max(600),
  media: uploadSchema.optional(),
  source: remoteSourceSchema.optional(),
}).superRefine((input, ctx) => {
  if (!input.media && !input.source && !input.contentText.trim()) {
    ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["contentText"], message: "Envie um arquivo, informe um link público ou adicione o texto do conteúdo." });
  }
});

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

  create: protectedProcedure.input(createSchema).mutation(async ({ ctx, input }) => {
    let mediaUrl: string | null = null;
    let mediaKey: string | null = null;
    let mediaMimeType: string | null = null;
    const sourceUrl = input.source?.url ?? null;
    const sourceKind = input.source?.kind ?? null;
    const sourceMediaMimeType = input.source?.mimeType ?? null;

    if (input.media) {
      const payload = input.media.base64.includes(",") ? input.media.base64.split(",")[1] : input.media.base64;
      const buffer = Buffer.from(payload, "base64");
      if (buffer.byteLength > 12 * 1024 * 1024) {
        throw new TRPCError({ code: "PAYLOAD_TOO_LARGE", message: "Envie arquivos de até 12 MB nesta versão inicial." });
      }
      const key = `plateia/${ctx.user.id}/${Date.now()}-${safeFileName(input.media.fileName)}`;
      const stored = await storagePut(key, buffer, input.media.mimeType);
      mediaUrl = stored.url;
      mediaKey = stored.key;
      mediaMimeType = input.media.mimeType;
    }

    if (!mediaUrl && input.source?.kind === "direct_media") {
      mediaUrl = input.source.url;
      mediaMimeType = input.source.mimeType ?? null;
    }

    const created = await createAnalysis({
      userId: ctx.user.id,
      contentType: input.contentType,
      contentText: input.contentText,
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

    try {
      const evaluation = await evaluateContent({
        contentType: input.contentType,
        text: input.contentText,
        product: input.product,
        objective: input.objective,
        targetAudience: input.targetAudience,
        mediaUrl,
        mediaMimeType,
        sourceUrl,
      });
      await updateAnalysisResult(created.id, "completed", evaluation);
      return { id: created.id, status: "completed" as const };
    } catch (error) {
      await updateAnalysisResult(created.id, "failed", null);
      console.error("[Platéia] Falha na avaliação:", error);
      throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: "Não foi possível concluir a avaliação agora. Tente novamente em instantes." });
    }
  }),
});
