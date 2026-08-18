import type { InstagramConnection } from "../drizzle/schema";

export function isMetaInstagramConfigured(environment: Record<string, string | undefined> = process.env) {
  return Boolean(environment.META_INSTAGRAM_APP_ID?.trim() && environment.META_INSTAGRAM_APP_SECRET?.trim());
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
