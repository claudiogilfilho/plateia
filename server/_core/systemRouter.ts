import { z } from "zod";
import { notifyOwner } from "./notification";
import { adminProcedure, publicProcedure, router } from "./trpc";
import { getEvaluationProviderStatus } from "../aiProvider";
import { getAuthMode, getRuntimePersistenceMode, getRuntimeStorageMode } from "../runtime";

export const systemRouter = router({
  health: publicProcedure
    .input(
      z.object({
        timestamp: z.number().min(0, "timestamp cannot be negative"),
      })
    )
    .query(() => ({
      ok: true,
    })),

  mvpStatus: publicProcedure.query(() => {
    const ai = getEvaluationProviderStatus();
    return {
      ready: ai.configured,
      auth: getAuthMode(),
      persistence: getRuntimePersistenceMode(),
      storage: getRuntimeStorageMode(),
      ai,
    };
  }),

  notifyOwner: adminProcedure
    .input(
      z.object({
        title: z.string().min(1, "title is required"),
        content: z.string().min(1, "content is required"),
      })
    )
    .mutation(async ({ input }) => {
      const delivered = await notifyOwner(input);
      return {
        success: delivered,
      } as const;
    }),
});
