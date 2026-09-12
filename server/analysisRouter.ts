import { TRPCError } from "@trpc/server";
import { z } from "zod";
import { createAnalysis, getAnalysisByIdForUser, listAnalysesForUser, updateAnalysisResult } from "./db";
import { protectedProcedure, router } from "./_core/trpc";
import { storagePut } from "./storage";
import { isAllowedPublicHttpsUrl, isInstagramPublicationUrl, publicLinkMessage, resolveInstagramMaterial } from "./publicLinks";
import { buildObservatoryContext, type ObservatoryContext } from "./observatory";
import { analyzeUploadedMp4, unavailableTechnicalTruth, type VideoTechnicalTruth } from "./videoTechnicalAnalysis";
import { buildDecisionReport, compareDecisionReports, evaluateBlindDecision, evaluateContextualDecision, type BusinessDossier, type DecisionReport } from "./decisionSystem";

const contentTypeSchema = z.enum(["post", "carrossel", "reel", "copy"]);
const mediaMimeSchema = z.enum(["image/jpeg", "image/png", "image/webp", "video/mp4"]);
const optionalText = (max: number) => z.string().max(max).optional().transform(value => value?.trim() ?? "");
const visualOnlyExcludedCriteria = ["clareza", "ação", "objeções"] as const;

const uploadSchema = z.object({
  fileName: z.string().min(1).max(160),
  mimeType: z.string().regex(/^(image\/(jpeg|png|webp)|video\/mp4)$/),
  base64: z.string().min(16).max(17_000_000),
});

const remoteSourceSchema = z.object({
  url: z.string().trim().max(2048).url().refine(isAllowedPublicHttpsUrl, publicLinkMessage),
  kind: z.enum(["direct_media", "published_post"]),
  mimeType: mediaMimeSchema.optional(),
}).superRefine((source, ctx) => {
  if (source.kind === "direct_media" && !source.mimeType) ctx.addIssue({ code: z.ZodIssueCode.custom, path: ["mimeType"], message: "Informe se o link direto aponta para imagem ou vídeo." });
});

const businessDossierSchema = z.object({
  businessName: optionalText(200), segment: optionalText(200), subsegment: optionalText(200), productsOrServices: optionalText(1200),
  priorityAudience: optionalText(1000), painsAndDesires: optionalText(1200), offer: optionalText(1000), differentiators: optionalText(1200),
  positioning: optionalText(800), toneOfVoice: optionalText(500), availableProof: optionalText(1200), legalOrBrandRestrictions: optionalText(1200),
  campaignObjective: optionalText(600), funnelStage: optionalText(200), desiredAction: optionalText(400), platform: optionalText(100),
  distribution: z.enum(["organic", "paid", "not_informed"]).optional().default("not_informed"),
}).optional();

export const createAnalysisInputSchema = z.object({
  contentType: contentTypeSchema,
  contentText: optionalText(10_000),
  product: optionalText(300),
  objective: optionalText(300),
  targetAudience: optionalText(600),
  media: uploadSchema.optional(),
  source: remoteSourceSchema.optional(),
  skipCaption: z.boolean().optional().default(false),
  businessDossier: businessDossierSchema,
  previousAnalysisId: z.number().int().positive().optional(),
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

export function hasExpectedMediaSignature(buffer: Buffer, mimeType: string) {
  if (mimeType === "video/mp4") return buffer.length >= 12 && buffer.subarray(4, 8).toString("ascii") === "ftyp";
  if (mimeType === "image/jpeg") return buffer.length >= 3 && buffer[0] === 0xff && buffer[1] === 0xd8 && buffer[2] === 0xff;
  if (mimeType === "image/png") return buffer.length >= 8 && buffer.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
  if (mimeType === "image/webp") return buffer.length >= 12 && buffer.subarray(0, 4).toString("ascii") === "RIFF" && buffer.subarray(8, 12).toString("ascii") === "WEBP";
  return false;
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
    let uploadedTechnicalTruth: VideoTechnicalTruth | null = null;
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
      if (!hasExpectedMediaSignature(buffer, input.media.mimeType)) throw new TRPCError({ code: "BAD_REQUEST", message: "O conteúdo do arquivo não corresponde ao formato informado." });
      if (input.media.mimeType === "video/mp4") {
        uploadedTechnicalTruth = await analyzeUploadedMp4(buffer);
        if (uploadedTechnicalTruth.videoCodec.status !== "measured") throw new TRPCError({ code: "BAD_REQUEST", message: "O MP4 não contém uma faixa de vídeo válida ou não pôde ser lido." });
      }
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
      }
      if (!mediaUrl) {
        coverage = {
          level: "requires_complement",
          mode: "requires_visual",
          title: "Material visual necessário",
          description: contentText ? "A legenda ficou acessível, mas o Instagram não disponibilizou imagem ou vídeo público para este link. Ela não será pontuada sozinha: envie o arquivo original para a Platéia avaliar o conteúdo." : "O Instagram não disponibilizou capa, imagem ou vídeo público para este link. Envie o arquivo original para a Platéia avaliar o conteúdo visual; a legenda continua opcional.",
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
      let technicalTruth: VideoTechnicalTruth = mediaMimeType === "video/mp4"
        ? unavailableTechnicalTruth(mediaUrl?.startsWith("data:") ? "uploaded_mp4" : "remote_media")
        : unavailableTechnicalTruth("not_video");
      if (uploadedTechnicalTruth) technicalTruth = uploadedTechnicalTruth;

      let observatoryContext: ObservatoryContext | null = null;
      try {
        observatoryContext = await buildObservatoryContext({
          contentType: input.contentType,
          text: contentText,
          segmentHint: "",
          objectiveHint: "",
          sourceUrl,
          mediaUrl,
          mediaMimeType,
          metrics: null,
        });
      } catch (observatoryError) {
        console.warn("[Platéia] Observatório indisponível; seguindo com avaliação estrutural:", observatoryError instanceof Error ? observatoryError.message : "erro desconhecido");
      }

      const blind = await evaluateBlindDecision({
        contentType: input.contentType,
        text: contentText,
        mediaUrl,
        mediaMimeType,
        technicalTruth,
        observatoryContext,
      });

      const dossier: BusinessDossier = {
        ...input.businessDossier,
        productsOrServices: input.businessDossier?.productsOrServices || input.product,
        priorityAudience: input.businessDossier?.priorityAudience || input.targetAudience,
        campaignObjective: input.businessDossier?.campaignObjective || input.objective,
      };
      let contextual;
      try {
        contextual = await evaluateContextualDecision({ blind, technicalTruth, dossier });
      } catch (contextualError) {
        console.warn("[Platéia] Auditoria contextual indisponível; preservando leitura cega congelada:", contextualError instanceof Error ? contextualError.message : "erro desconhecido");
        contextual = {
          businessEffectiveness: { score: null, justification: "A adequação ao negócio não pôde ser concluída nesta execução.", evidence: [], confidence: "low" as const },
          plateiaVerdict: "inconclusive" as const,
          alignment: [], incompatibilities: [], inventedOrUnsupportedInformation: [],
          missingInformation: ["Auditoria contextual indisponível; a leitura cega não representa aprovação."],
          uncommunicatedDifferentiators: [], limitations: ["Falha temporária na segunda etapa; tente reavaliar sem reenviar ou reinterpretar este relatório como aprovação."], confidence: "low" as const,
        };
      }
      let report = buildDecisionReport({ blind, contextual, technicalTruth, coverage, observatory: observatoryContext });
      if (contextual.plateiaVerdict === "inconclusive" && contextual.limitations?.some(item => item.includes("Falha temporária"))) report = { ...report, state: "completed_with_limitations" };

      if (input.previousAnalysisId) {
        const previous = await getAnalysisByIdForUser(input.previousAnalysisId, ctx.user.id);
        if (!previous?.reportJson) throw new TRPCError({ code: "BAD_REQUEST", message: "A versão anterior não foi encontrada no seu histórico." });
        const previousReport = JSON.parse(previous.reportJson) as DecisionReport;
        if (previousReport.decisionSystemVersion === "1.0") {
          const comparison = compareDecisionReports(input.previousAnalysisId, previousReport, report);
          report = { ...report, comparison };
        }
      }

      await updateAnalysisResult(created.id, "completed", report);
      return { id: created.id, status: "completed" as const };
    } catch (error) {
      await updateAnalysisResult(created.id, "failed", null);
      console.error("[Platéia] Falha na avaliação:", error);
      throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: "A Platéia não conseguiu finalizar a leitura agora. Tente novamente em instantes." });
    }
  }),
});
