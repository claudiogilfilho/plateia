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
  return value?.replace(/&amp;/g, "&").replace(/&#x27;/g, "'").replace(/&quot;/g, '"').replace(/&#39;/g, "'").trim() || null;
}

function jsonLdCaption(html: string) {
  const scripts = Array.from(html.matchAll(/<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi));
  for (const script of scripts) {
    try {
      const parsed = JSON.parse(script[1]) as Record<string, unknown>;
      const candidates = [parsed.caption, parsed.description, parsed.articleBody];
      const caption = candidates.find(value => typeof value === "string" && value.trim());
      if (typeof caption === "string") return caption.trim();
    } catch {
      // A página pode conter dados estruturados incompletos; os metadados seguem como fallback.
    }
  }
  return null;
}

function captionFromHtml(html: string) {
  const candidates = [
    metaContent(html, "og:description"),
    metaContent(html, "twitter:description"),
    metaContent(html, "description"),
    jsonLdCaption(html),
  ];
  return candidates.map(decodeHtml).find((caption): caption is string => Boolean(caption)) ?? null;
}

export type InstagramMaterial = { mediaUrl: string | null; mediaMimeType: "image/jpeg" | null; caption: string | null };

export async function resolveInstagramMaterial(sourceUrl: string): Promise<InstagramMaterial | null> {
  if (!isInstagramPublicationUrl(sourceUrl)) return null;
  const source = new URL(sourceUrl);
  const path = source.pathname.replace(/^\/+|\/+$/g, "");
  const canonicalPath = path.replace(/^reels\//i, "reel/");
  const embedUrl = `https://www.instagram.com/${canonicalPath}/embed/captioned/`;
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8_000);

  try {
    const response = await fetch(embedUrl, {
      headers: { "user-agent": "Mozilla/5.0 (compatible; Plateia/1.0; +https://plateia.app)" },
      signal: controller.signal,
    });
    if (!response.ok) return null;
    const html = await response.text();
    const candidateMediaUrl = decodeHtml(metaContent(html, "og:image"));
    const mediaUrl = candidateMediaUrl && isAllowedPublicHttpsUrl(candidateMediaUrl) ? candidateMediaUrl : null;
    const caption = captionFromHtml(html);
    if (!mediaUrl && !caption) return null;
    return { mediaUrl, mediaMimeType: mediaUrl ? "image/jpeg" : null, caption };
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

export const publicLinkMessage = "Use um link HTTPS público. Links locais, privados ou de rede interna não são aceitos.";
