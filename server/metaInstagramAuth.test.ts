import { describe, expect, it } from "vitest";
import { buildInstagramAuthorizationUrl, decryptInstagramToken, encryptInstagramToken } from "./metaInstagramAuth";

describe("Meta Instagram authorization helpers", () => {
  it("builds an authorization URL with the minimum read-only scope and a state value", () => {
    const url = new URL(buildInstagramAuthorizationUrl({
      appId: "1059740836503946",
      redirectUri: "https://plateia.example.com/api/integrations/instagram/callback",
      state: "csrf-state",
    }));

    expect(url.origin + url.pathname).toBe("https://www.instagram.com/oauth/authorize");
    expect(url.searchParams.get("client_id")).toBe("1059740836503946");
    expect(url.searchParams.get("redirect_uri")).toBe("https://plateia.example.com/api/integrations/instagram/callback");
    expect(url.searchParams.get("response_type")).toBe("code");
    expect(url.searchParams.get("force_reauth")).toBe("true");
    expect(url.searchParams.get("scope")).toBe("instagram_business_basic");
    expect(url.searchParams.get("state")).toBe("csrf-state");
  });

  it.skipIf(!process.env.META_INSTAGRAM_APP_SECRET || !process.env.JWT_SECRET)("encrypts the authorized access token before it can be persisted", () => {
    const encrypted = encryptInstagramToken("test-instagram-access-token");
    expect(encrypted).not.toContain("test-instagram-access-token");
    expect(decryptInstagramToken(encrypted)).toBe("test-instagram-access-token");
  });
});
