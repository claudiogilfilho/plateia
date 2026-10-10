import { describe, expect, it } from "vitest";
import { getAuthMode, getGuestUser, getRuntimePersistenceMode, getRuntimeStorageMode } from "./runtime";

describe("Plateia MVP runtime", () => {
  it("starts in guest, memory and inline modes without external services", () => {
    expect(getAuthMode({})).toBe("guest");
    expect(getRuntimePersistenceMode({})).toBe("memory");
    expect(getRuntimeStorageMode({})).toBe("inline");
  });

  it("uses OAuth automatically only when its required configuration exists", () => {
    expect(getAuthMode({ OAUTH_SERVER_URL: "https://auth.example", VITE_APP_ID: "plateia", JWT_SECRET: "secret" })).toBe("oauth");
    expect(getAuthMode({ PLATEIA_AUTH_MODE: "guest", OAUTH_SERVER_URL: "https://auth.example", VITE_APP_ID: "plateia", JWT_SECRET: "secret" })).toBe("guest");
  });

  it("does not grant admin privileges to the public MVP guest by default", () => {
    expect(getGuestUser({}).role).toBe("user");
    expect(getGuestUser({ PLATEIA_GUEST_ADMIN: "true" }).role).toBe("admin");
  });

  it("fails closed in production when private authentication is missing", () => {
    expect(() => getAuthMode({ NODE_ENV: "production" })).toThrow("não inicia em produção");
    expect(() => getAuthMode({ NODE_ENV: "production", PLATEIA_AUTH_MODE: "guest" })).toThrow("bloqueado em produção");
    expect(getAuthMode({ NODE_ENV: "production", PLATEIA_AUTH_MODE: "oauth", OAUTH_SERVER_URL: "https://auth.example", VITE_APP_ID: "plateia", JWT_SECRET: "secret" })).toBe("oauth");
  });
});
