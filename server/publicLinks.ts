const blockedHosts = new Set(["localhost", "0.0.0.0", "::1"]);
const instagramHosts = new Set(["instagram.com", "www.instagram.com", "m.instagram.com"]);

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

export function isInstagramPublicationUrl(value: string) {
  try {
    const url = new URL(value);
    const path = url.pathname.replace(/^\/+|\/+$/g, "");
    return instagramHosts.has(url.hostname.toLowerCase()) && /^(p|reel|reels|tv)\/[^/]+$/i.test(path);
  } catch {
    return false;
  }
}

function metaContent(html: string, property: string) {
  const escaped = property.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const propertyFirst = new RegExp(`<meta[^>]+(?:property|name)=["']${escaped}["'][^>]+content=["']([^"']+)["'][^>]*>`, "i");
  const contentFirst = new RegExp(`<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["']${escaped}["'][^>]*>`, "i");
  return html.match(propertyFirst)?.[1] ?? html.match(contentFirst)?.[1] ?? null;
}

function decodeHtml(value: string | null) {
  return value?.replace(/&amp;/g, "&").replace(/&#x27;/g, "'").replace(/&quot;/g, '"').trim() || null;
}

export type InstagramMaterial = { mediaUrl: string; mediaMimeType: "image/jpeg"; caption: string | null };

export async function resolveInstagramMaterial(sourceUrl: string): Promise<InstagramMaterial | null> {
  if (!isInstagramPublicationUrl(sourceUrl)) return null;
  const source = new URL(sourceUrl);
  const path = source.pathname.replace(/^\/+|\/+$/g, "");
  const embedUrl = `https://www.instagram.com/${path}/embed/captioned/`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8_000);

  try {
    const response = await fetch(embedUrl, {
      headers: { "user-agent": "Mozilla/5.0 (compatible; Plateia/1.0; +https://plateia.app)" },
      signal: controller.signal,
    });
    if (!response.ok) return null;
    const html = await response.text();
    const mediaUrl = decodeHtml(metaContent(html, "og:image"));
    if (!mediaUrl || !isAllowedPublicHttpsUrl(mediaUrl)) return null;
    const caption = decodeHtml(metaContent(html, "og:description"));
    return { mediaUrl, mediaMimeType: "image/jpeg", caption };
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

export const publicLinkMessage = "Use um link HTTPS público. Links locais, privados ou de rede interna não são aceitos.";
