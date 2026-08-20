import type { InstagramConnection } from "../drizzle/schema";

type MetaCredentialValidation = {
  valid: boolean;
  reason?: "not_configured" | "request_failed" | "invalid_response";
};

export function isMetaInstagramConfigured(environment: Record<string, string | undefined> = process.env) {
  return Boolean(environment.META_INSTAGRAM_APP_ID?.trim() && environment.META_INSTAGRAM_APP_SECRET?.trim());
}

export async function validateMetaAppCredentials(
  environment: Record<string, string | undefined> = process.env,
  request: typeof fetch = fetch,
): Promise<MetaCredentialValidation> {
  const appId = environment.META_INSTAGRAM_APP_ID?.trim();
  const appSecret = environment.META_INSTAGRAM_APP_SECRET?.trim();
  if (!appId || !appSecret) return { valid: false, reason: "not_configured" };

  try {
    const body = new URLSearchParams({
      client_id: appId,
      client_secret: appSecret,
      grant_type: "authorization_code",
      redirect_uri: "https://credential-validation.invalid/instagram/callback",
      code: "credential-validation-probe",
    });
    const response = await request("https://api.instagram.com/oauth/access_token", { method: "POST", body });
    const payload = (await response.json()) as { error_type?: string; error_message?: string; error?: { message?: string } };
    if (response.ok) return { valid: true };

    const message = payload.error_message || payload.error?.message || "";
    if (payload.error_type === "OAuthException" && /code/i.test(message) && !/(client|secret)/i.test(message)) return { valid: true };
    return { valid: false, reason: "invalid_response" };
  } catch {
    return { valid: false, reason: "request_failed" };
  }
}

export function buildInstagramConnectionState(connection: InstagramConnection | undefined, configured = isMetaInstagramConfigured()) {
  if (!configured) return { configured: false, status: "ready" as const, connection: null, nextStep: "A integração está preparada. O administrador precisa cadastrar as credenciais do aplicativo Meta para liberar a conexão." };
  if (!connection) return { configured: true, status: "ready" as const, connection: null, nextStep: "Conecte sua conta profissional do Instagram para analisar mídias da sua própria conta." };
  return {
    configured: true,
    status: connection.status,
    connection: { username: connection.username, accountType: connection.accountType, connectedAt: connection.connectedAt, tokenExpiresAt: connection.tokenExpiresAt, revokedAt: connection.revokedAt },
    nextStep: connection.status === "connected" ? "Sua conta profissional está conectada." : "Reconecte sua conta profissional do Instagram para renovar a autorização.",
  };
}

export function buildRevokedInstagramConnectionPatch() {
  return { status: "revoked" as const, accessTokenEncrypted: null, tokenExpiresAt: null, revokedAt: new Date() };
}
