import { describe, expect, it } from "vitest";
import { buildInstagramConnectionState, buildRevokedInstagramConnectionPatch, isMetaInstagramConfigured, validateMetaAppCredentials } from "./instagramIntegration";

describe("instagram integration preparation", () => {
  it("requires both Meta app credentials before enabling a connection", () => {
    expect(isMetaInstagramConfigured({ META_INSTAGRAM_APP_ID: "id" })).toBe(false);
    expect(isMetaInstagramConfigured({ META_INSTAGRAM_APP_ID: "id", META_INSTAGRAM_APP_SECRET: "secret" })).toBe(true);
  });

  it("keeps the connection state in preparation until Meta credentials exist", () => {
    expect(buildInstagramConnectionState(undefined, false)).toMatchObject({ configured: false, status: "ready", connection: null });
  });

  it("removes the token and records revocation when a user disconnects", () => {
    const patch = buildRevokedInstagramConnectionPatch();
    expect(patch.status).toBe("revoked");
    expect(patch.accessTokenEncrypted).toBeNull();
    expect(patch.tokenExpiresAt).toBeNull();
    expect(patch.revokedAt).toBeInstanceOf(Date);
  });

  const hasSuppliedMetaCredentials = isMetaInstagramConfigured();
  it.skipIf(!hasSuppliedMetaCredentials)("validates the supplied Instagram App credentials with a discarded OAuth authorization-code probe", async () => {
    const result = await validateMetaAppCredentials();
    expect(result.valid).toBe(true);
  }, 15_000);
});
