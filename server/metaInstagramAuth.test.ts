import { describe, expect, it } from "vitest";
import { buildInstagramAuthorizationUrl, decryptInstagramToken, encryptInstagramToken, exchangeInstagramAuthorizationCode } from "./metaInstagramAuth";

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

  it("exchanges the code using direct Instagram OAuth responses and resolves the professional account", async () => {
    const requestedUrls: string[] = [];
    const request: typeof fetch = async (input) => {
      const url = input instanceof URL ? input.toString() : input.toString();
      requestedUrls.push(url);
      if (url === "https://api.instagram.com/oauth/access_token") return new Response(JSON.stringify({ access_token: "short-token", user_id: "178900", permissions: "instagram_business_basic" }), { status: 200 });
      if (url.startsWith("https://graph.instagram.com/access_token")) return new Response(JSON.stringify({ access_token: "long-token", expires_in: 5_184_000 }), { status: 200 });
      if (url.startsWith("https://graph.instagram.com/v26.0/me")) return new Response(JSON.stringify({ user_id: "178900", username: "plateia_teste", account_type: "MEDIA_CREATOR" }), { status: 200 });
      return new Response("not found", { status: 404 });
    };

    const result = await exchangeInstagramAuthorizationCode(
      "authorization-code",
      "https://plateia.example.com/api/integrations/instagram/callback",
      { META_INSTAGRAM_APP_ID: "instagram-app-id", META_INSTAGRAM_APP_SECRET: "instagram-app-secret" },
      request,
    );

    expect(result).toEqual({ accessToken: "long-token", expiresIn: 5_184_000, instagramUserId: "178900", username: "plateia_teste", accountType: "creator", grantedScopes: "instagram_business_basic" });
    expect(requestedUrls).toHaveLength(3);
    expect(requestedUrls[1]).toContain("grant_type=ig_exchange_token");
    expect(requestedUrls[2]).toContain("fields=user_id%2Cusername%2Caccount_type");
  });
});
