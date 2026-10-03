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

function decodeHtml(value: string | null | undefined) {
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

function jsonObjectAfterKey(html: string, key: string) {
  const marker = `"${key}":`;
  const markerIndex = html.indexOf(marker);
  if (markerIndex < 0) return null;
  const start = html.indexOf("{", markerIndex + marker.length);
  if (start < 0) return null;

  let depth = 0;
  let quoted = false;
  let escaped = false;
  for (let index = start; index < html.length; index += 1) {
    const character = html[index];
    if (escaped) {
      escaped = false;
      continue;
    }
    if (character === "\\") {
      escaped = true;
      continue;
    }
    if (character === '"') {
      quoted = !quoted;
      continue;
    }
    if (quoted) continue;
    if (character === "{") depth += 1;
    if (character === "}") depth -= 1;
    if (depth === 0) {
      try {
        return JSON.parse(html.slice(start, index + 1)) as Record<string, unknown>;
      } catch {
        return null;
      }
    }
  }
  return null;
}

function contextJsonMedia(html: string) {
  const match = html.match(/"contextJSON":"((?:\\.|[^"\\])*)"/);
  if (!match) return null;
  try {
    const contextJson = JSON.parse(`"${match[1]}"`) as string;
    const parsed = JSON.parse(contextJson) as { gql_data?: { shortcode_media?: Record<string, unknown> } };
    return parsed.gql_data?.shortcode_media ?? null;
  } catch {
    return null;
  }
}

function structuredInstagramMaterial(html: string) {
  const media = jsonObjectAfterKey(html, "shortcode_media") ?? contextJsonMedia(html);
  if (!media) return null;
  const videoCandidate = typeof media.video_url === "string" ? decodeHtml(media.video_url) : null;
  const coverCandidate = typeof media.display_url === "string" ? decodeHtml(media.display_url) : typeof media.thumbnail_src === "string" ? decodeHtml(media.thumbnail_src) : null;
  const videoUrl = videoCandidate && isAllowedPublicHttpsUrl(videoCandidate) ? videoCandidate : null;
  const coverImageUrl = coverCandidate && isAllowedPublicHttpsUrl(coverCandidate) ? coverCandidate : null;
  const mediaUrl = videoUrl ?? coverImageUrl;
  const edgeCaption = media.edge_media_to_caption as { edges?: Array<{ node?: { text?: unknown } }> } | undefined;
  const structuredCaption = edgeCaption?.edges?.find(edge => typeof edge.node?.text === "string")?.node?.text;
  const caption = typeof structuredCaption === "string" && structuredCaption.trim() ? structuredCaption.trim() : null;
  if (!mediaUrl && !caption) return null;
  return { mediaUrl, mediaMimeType: videoUrl ? "video/mp4" as const : coverImageUrl ? "image/jpeg" as const : null, videoUrl, coverImageUrl, caption };
}

export type InstagramMaterial = { mediaUrl: string | null; mediaMimeType: "image/jpeg" | "video/mp4" | null; videoUrl: string | null; coverImageUrl: string | null; caption: string | null };

function instagramMaterialFromHtml(html: string): InstagramMaterial | null {
  const structured = structuredInstagramMaterial(html);
  const videoCandidate = [
    structured?.videoUrl,
    metaContent(html, "og:video:secure_url"),
    metaContent(html, "og:video:url"),
    metaContent(html, "og:video"),
    metaContent(html, "twitter:player:stream"),
  ].map(decodeHtml).find((candidate): candidate is string => Boolean(candidate && isAllowedPublicHttpsUrl(candidate))) ?? null;
  const coverCandidate = [
    structured?.coverImageUrl,
    metaContent(html, "og:image:secure_url"),
    metaContent(html, "og:image"),
    metaContent(html, "twitter:image"),
  ].map(decodeHtml).find((candidate): candidate is string => Boolean(candidate && isAllowedPublicHttpsUrl(candidate))) ?? null;
  const caption = structured?.caption ?? captionFromHtml(html);
  if (!videoCandidate && !coverCandidate && !caption) return null;
  return { mediaUrl: videoCandidate ?? coverCandidate, mediaMimeType: videoCandidate ? "video/mp4" : coverCandidate ? "image/jpeg" : null, videoUrl: videoCandidate, coverImageUrl: coverCandidate, caption };
}

function mergeInstagramMaterials(materials: Array<InstagramMaterial | null>): InstagramMaterial | null {
  const videoUrl = materials.find(material => material?.videoUrl)?.videoUrl ?? null;
  const coverImageUrl = materials.find(material => material?.coverImageUrl)?.coverImageUrl ?? null;
  const caption = materials.find(material => material?.caption)?.caption ?? null;
  if (!videoUrl && !coverImageUrl && !caption) return null;
  return { mediaUrl: videoUrl ?? coverImageUrl, mediaMimeType: videoUrl ? "video/mp4" : coverImageUrl ? "image/jpeg" : null, videoUrl, coverImageUrl, caption };
}

export async function resolveInstagramMaterial(sourceUrl: string): Promise<InstagramMaterial | null> {
  if (!isInstagramPublicationUrl(sourceUrl)) return null;
  const source = new URL(sourceUrl);
  const path = source.pathname.replace(/^\/+|\/+$/g, "");
  const canonicalPath = path.replace(/^reels\//i, "reel/");
  const candidateUrls = [`https://www.instagram.com/${canonicalPath}/embed/captioned/`, `https://www.instagram.com/${canonicalPath}/embed/`, `https://www.instagram.com/${canonicalPath}/`];
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 10_000);

  try {
    const attempts = await Promise.allSettled(candidateUrls.map(async url => {
      const response = await fetch(url, {
        headers: { accept: "text/html,application/xhtml+xml", "accept-language": "pt-BR,pt;q=0.9,en;q=0.7", "user-agent": "Mozilla/5.0 (compatible; Plateia/1.0; +https://plateia.app)" },
        redirect: "follow",
        signal: controller.signal,
      });
      if (!response.ok) return null;
      return instagramMaterialFromHtml(await response.text());
    }));
    return mergeInstagramMaterials(attempts.map(attempt => attempt.status === "fulfilled" ? attempt.value : null));
  } catch {
    return null;
  } finally {
    clearTimeout(timeout);
  }
}

export const publicLinkMessage = "Use um link HTTPS público. Links locais, privados ou de rede interna não são aceitos.";
