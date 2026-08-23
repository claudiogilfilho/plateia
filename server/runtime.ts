import type { User } from "../drizzle/schema";

type RuntimeEnvironment = Record<string, string | undefined>;

export type PlateiaAuthMode = "guest" | "oauth";

function isTruthy(value: string | undefined) {
  return ["1", "true", "yes", "on"].includes((value ?? "").trim().toLowerCase());
}

export function getAuthMode(environment: RuntimeEnvironment = process.env): PlateiaAuthMode {
  const explicit = environment.PLATEIA_AUTH_MODE?.trim().toLowerCase();
  if (explicit === "guest" || explicit === "oauth") return explicit;
  return environment.OAUTH_SERVER_URL && environment.VITE_APP_ID && environment.JWT_SECRET ? "oauth" : "guest";
}

export function getGuestUser(environment: RuntimeEnvironment = process.env): User {
  const now = new Date(0);
  return {
    id: 1,
    openId: "plateia-mvp-guest",
    name: environment.PLATEIA_GUEST_NAME?.trim() || "Visitante do Platéia",
    email: null,
    loginMethod: "guest",
    role: isTruthy(environment.PLATEIA_GUEST_ADMIN) ? "admin" : "user",
    createdAt: now,
    updatedAt: now,
    lastSignedIn: now,
  };
}

export function getRuntimeStorageMode(environment: RuntimeEnvironment = process.env) {
  return environment.BUILT_IN_FORGE_API_URL && environment.BUILT_IN_FORGE_API_KEY ? "remote" as const : "inline" as const;
}

export function getRuntimePersistenceMode(environment: RuntimeEnvironment = process.env) {
  return environment.DATABASE_URL ? "mysql" as const : "memory" as const;
}
