const blockedHosts = new Set(["localhost", "0.0.0.0", "::1"]);

export function isAllowedPublicHttpsUrl(value: string) {
  try {
    const url = new URL(value);
    const host = url.hostname.toLowerCase();
    if (url.protocol !== "https:") return false;
    if (blockedHosts.has(host) || host.endsWith(".local") || host.endsWith(".internal") || host.endsWith(".localhost")) return false;
    if (/^(127|10)\./.test(host) || /^192\.168\./.test(host) || /^172\.(1[6-9]|2\d|3[0-1])\./.test(host)) return false;
    return true;
  } catch {
    return false;
  }
}

export const publicLinkMessage = "Use um link HTTPS público. Links locais, privados ou de rede interna não são aceitos.";
