import { getInstagramConnectionForUser, revokeInstagramConnectionForUser } from "./db";
import { buildInstagramConnectionState } from "./instagramIntegration";
import { protectedProcedure, router } from "./_core/trpc";

export const instagramRouter = router({
  connection: protectedProcedure.query(async ({ ctx }) => buildInstagramConnectionState(await getInstagramConnectionForUser(ctx.user.id))),
  revoke: protectedProcedure.mutation(async ({ ctx }) => {
    await revokeInstagramConnectionForUser(ctx.user.id);
    return { success: true } as const;
  }),
});
