const trackingParameters = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid", "gclid", "igshid", "si", "feature"];

export function canonicalPublicUrl(value: string) {
  try {
    const url = new URL(value.trim());
    url.protocol = "https:";
    url.hostname = url.hostname.toLocaleLowerCase("pt-BR").replace(/^www\./, "");
    trackingParameters.forEach(parameter => url.searchParams.delete(parameter));
    url.hash = "";

    if (url.hostname === "youtu.be" && url.pathname.replace(/^\//, "")) {
      const videoId = url.pathname.replace(/^\//, "").split("/")[0];
      url.hostname = "youtube.com";
      url.pathname = "/watch";
      url.search = "";
      url.searchParams.set("v", videoId);
    }
    if (url.hostname === "m.youtube.com") url.hostname = "youtube.com";
    const short = url.hostname === "youtube.com" ? url.pathname.match(/^\/shorts\/([^/]+)\/?$/) : null;
    if (short) {
      url.pathname = "/watch";
      url.search = "";
      url.searchParams.set("v", short[1]);
    }

    url.pathname = url.pathname.replace(/\/+$/, "") || "/";
    url.searchParams.sort();
    return url.toString().replace(/\/$/, "");
  } catch {
    return value.trim().toLocaleLowerCase("pt-BR");
  }
}
