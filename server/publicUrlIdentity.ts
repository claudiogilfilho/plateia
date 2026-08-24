const trackingParameters = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "fbclid", "gclid", "igshid", "si"];

export function canonicalPublicUrl(value: string) {
  try {
    const url = new URL(value);
    url.hostname = url.hostname.toLocaleLowerCase("pt-BR").replace(/^www\./, "");
    trackingParameters.forEach(parameter => url.searchParams.delete(parameter));
    url.hash = "";
    url.pathname = url.pathname.replace(/\/$/, "") || "/";
    url.searchParams.sort();
    return url.toString().replace(/\/$/, "");
  } catch {
    return value.trim().toLocaleLowerCase("pt-BR");
  }
}
