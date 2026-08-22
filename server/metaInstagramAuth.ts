import { createCipheriv, createDecipheriv, createHash, randomBytes } from "crypto";
import { parse as parseCookieHeader } from "cookie";
import type { Express, Request, Response } from "express";
import { getInstagramConnectionForUser, saveInstagramConnectionForUser, updateInstagramConnectionStatus } from "./db";
import { isMetaInstagramConfigured } from "./instagramIntegration";
import { sdk } from "./_core/sdk";

const META_STATE_COOKIE = "plateia_meta_instagram_state";
const META_STATE_MAX_AGE_MS = 10 * 60 * 1000;
const CONSENT_VERSION = "2026-08-v1";
const INSTAGRAM_SCOPE = "instagram_business_basic";

type TokenExchangeResponse = { access_token?: string; user_id?: string; permissions?: string };
type LongLivedTokenResponse = { access_token?: string; expires_in?: number };
type InstagramIdentityResponse = { user_id?: string; username?: string; account_type?: string };

function getRequiredMetaCredentials(environment: Record<string, string | undefined> = process.env) {
  const appId = environment.META_INSTAGRAM_APP_ID?.trim();
  const appSecret = environment.META_INSTAGRAM_APP_SECRET?.trim();
  if (!appId || !appSecret) throw new Error("Meta Instagram não está configurado.");
  return { appId, appSecret };
}

function getRedirectUri(req: Request) {
  const forwardedProtocol = req.get("x-forwarded-proto")?.split(",")[0]?.trim();
  const protocol = forwardedProtocol || req.protocol;
  return `${protocol}://${req.get("host")}/api/integrations/instagram/callback`;
}

export function buildInstagramAuthorizationUrl({ appId, redirectUri, state }: { appId: string; redirectUri: string; state: string }) {
  const authorizeUrl = new URL("https://www.instagram.com/oauth/authorize");
  authorizeUrl.searchParams.set("client_id", appId);
  authorizeUrl.searchParams.set("redirect_uri", redirectUri);
  authorizeUrl.searchParams.set("response_type", "code");
  authorizeUrl.searchParams.set("force_reauth", "true");
  authorizeUrl.searchParams.set("scope", INSTAGRAM_SCOPE);
  authorizeUrl.searchParams.set("state", state);
  return authorizeUrl.toString();
}

function getClientRedirectPath(status: "connected" | "error") {
  return `/instagram?meta=${status}`;
}

function createTokenCipherKey() {
  const secret = process.env.JWT_SECRET?.trim();
  const metaSecret = process.env.META_INSTAGRAM_APP_SECRET?.trim();
  if (!secret || !metaSecret) throw new Error("Chave de proteção indisponível.");
  return createHash("sha256").update(`${secret}:${metaSecret}:plateia-instagram-token-v1`).digest();
}

export function encryptInstagramToken(accessToken: string) {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", createTokenCipherKey(), iv);
  const encrypted = Buffer.concat([cipher.update(accessToken, "utf8"), cipher.final()]);
  return ["v1", iv.toString("base64url"), cipher.getAuthTag().toString("base64url"), encrypted.toString("base64url")].join(".");
}

export function decryptInstagramToken(encryptedToken: string) {
  const [version, ivValue, tagValue, payload] = encryptedToken.split(".");
  if (version !== "v1" || !ivValue || !tagValue || !payload) throw new Error("Token protegido inválido.");
  const decipher = createDecipheriv("aes-256-gcm", createTokenCipherKey(), Buffer.from(ivValue, "base64url"));
  decipher.setAuthTag(Buffer.from(tagValue, "base64url"));
  return Buffer.concat([decipher.update(Buffer.from(payload, "base64url")), decipher.final()]).toString("utf8");
}

async function getAuthenticatedUser(req: Request) {
  try {
    return await sdk.authenticateRequest(req);
  } catch {
    return null;
  }
}

function clearStateCookie(res: Response) {
  res.clearCookie(META_STATE_COOKIE, { path: "/", secure: true, sameSite: "lax" });
}

function redirectWithError(req: Request, res: Response) {
  res.redirect(302, getClientRedirectPath("error"));
}

export async function exchangeInstagramAuthorizationCode(
  code: string,
  redirectUri: string,
  environment: Record<string, string | undefined> = process.env,
  request: typeof fetch = fetch,
) {
  const { appId, appSecret } = getRequiredMetaCredentials(environment);
  const exchangeBody = new URLSearchParams({ client_id: appId, client_secret: appSecret, grant_type: "authorization_code", redirect_uri: redirectUri, code });
  const exchangeResponse = await request("https://api.instagram.com/oauth/access_token", { method: "POST", body: exchangeBody });
  if (!exchangeResponse.ok) throw new Error("Não foi possível trocar o código Meta.");
  const exchanged = (await exchangeResponse.json()) as TokenExchangeResponse;
  const shortLivedToken = exchanged.access_token;
  if (!shortLivedToken) throw new Error("A Meta não retornou um token de autorização.");

  const longTokenUrl = new URL("https://graph.instagram.com/access_token");
  longTokenUrl.searchParams.set("grant_type", "ig_exchange_token");
  longTokenUrl.searchParams.set("client_secret", appSecret);
  longTokenUrl.searchParams.set("access_token", shortLivedToken);
  const longTokenResponse = await request(longTokenUrl);
  if (!longTokenResponse.ok) throw new Error("Não foi possível estender o token Meta.");
  const longLived = (await longTokenResponse.json()) as LongLivedTokenResponse;
  if (!longLived.access_token || !longLived.expires_in) throw new Error("A Meta não retornou um token de longa duração.");

  const meUrl = new URL("https://graph.instagram.com/v26.0/me");
  meUrl.searchParams.set("fields", "user_id,username,account_type");
  meUrl.searchParams.set("access_token", longLived.access_token);
  const identityResponse = await request(meUrl);
  if (!identityResponse.ok) throw new Error("Não foi possível ler a conta profissional autorizada.");
  const identity = (await identityResponse.json()) as InstagramIdentityResponse;
  if (!identity.user_id || !identity.username) throw new Error("A Meta não retornou a identidade da conta profissional.");

  return { accessToken: longLived.access_token, expiresIn: longLived.expires_in, instagramUserId: identity.user_id, username: identity.username, accountType: identity.account_type?.toUpperCase() === "MEDIA_CREATOR" ? "creator" as const : "business" as const, grantedScopes: INSTAGRAM_SCOPE };
}

export function registerMetaInstagramRoutes(app: Express) {
  app.get("/api/integrations/instagram/start", async (req, res) => {
    if (!isMetaInstagramConfigured()) return res.status(503).json({ error: "A integração Meta não está configurada." });
    const user = await getAuthenticatedUser(req);
    if (!user) return res.status(401).json({ error: "Autenticação necessária." });

    const state = randomBytes(32).toString("base64url");
    res.cookie(META_STATE_COOKIE, state, { httpOnly: true, secure: true, sameSite: "lax", maxAge: META_STATE_MAX_AGE_MS, path: "/" });

    const { appId } = getRequiredMetaCredentials();
    res.redirect(302, buildInstagramAuthorizationUrl({ appId, redirectUri: getRedirectUri(req), state }));
  });

  app.get("/api/integrations/instagram/callback", async (req, res) => {
    const code = typeof req.query.code === "string" ? req.query.code : undefined;
    const state = typeof req.query.state === "string" ? req.query.state : undefined;
    const expectedState = parseCookieHeader(req.headers.cookie ?? "")[META_STATE_COOKIE];
    const user = await getAuthenticatedUser(req);
    clearStateCookie(res);

    if (!user || !code || !state || state !== expectedState || req.query.error) return redirectWithError(req, res);
    try {
      const connection = await exchangeInstagramAuthorizationCode(code, getRedirectUri(req));
      await saveInstagramConnectionForUser(user.id, {
        instagramUserId: connection.instagramUserId,
        username: connection.username,
        accountType: connection.accountType,
        status: "connected",
        grantedScopes: connection.grantedScopes,
        accessTokenEncrypted: encryptInstagramToken(connection.accessToken),
        tokenExpiresAt: new Date(Date.now() + connection.expiresIn * 1000),
        consentVersion: CONSENT_VERSION,
        connectedAt: new Date(),
        revokedAt: null,
      });
      res.redirect(302, getClientRedirectPath("connected"));
    } catch (error) {
      console.error("[MetaInstagram] Callback failed", error instanceof Error ? error.message : "unknown error");
      redirectWithError(req, res);
    }
  });

  app.get("/api/integrations/instagram/media", async (req, res) => {
    const user = await getAuthenticatedUser(req);
    if (!user) return res.status(401).json({ error: "Autenticação necessária." });
    const connection = await getInstagramConnectionForUser(user.id);
    if (!connection?.accessTokenEncrypted || !connection.instagramUserId || connection.status !== "connected") return res.status(409).json({ error: "Nenhuma conta profissional conectada." });

    try {
      const mediaUrl = new URL(`https://graph.instagram.com/v26.0/${encodeURIComponent(connection.instagramUserId)}/media`);
      mediaUrl.searchParams.set("fields", "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp");
      mediaUrl.searchParams.set("access_token", decryptInstagramToken(connection.accessTokenEncrypted));
      const mediaResponse = await fetch(mediaUrl);
      if (mediaResponse.status === 401 || mediaResponse.status === 403) {
        await updateInstagramConnectionStatus(user.id, "expired");
        return res.status(401).json({ error: "A autorização do Instagram expirou. Reconecte a conta." });
      }
      if (!mediaResponse.ok) return res.status(502).json({ error: "Não foi possível ler as mídias conectadas agora." });
      const result = (await mediaResponse.json()) as { data?: unknown[] };
      res.json({ data: result.data ?? [] });
    } catch {
      res.status(502).json({ error: "Não foi possível ler as mídias conectadas agora." });
    }
  });
}
