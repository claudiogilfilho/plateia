export type ViralityAssessment = {
  status: "indeterminate" | "above_creator_baseline" | "breakout_relative_to_cohort" | "high_shareability" | "strong_retention" | "strong_conversion";
  confidence: "low" | "medium" | "high";
  observedRates: Record<string, number>;
  observations: string[];
  limitations: string[];
  causalClaimAllowed: false;
};

function finite(value: unknown) {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value !== "string") return null;
  const compact = value.trim().toLocaleLowerCase("pt-BR").replace(/\s/g, "");
  const multiplier = compact.endsWith("mi") ? 1_000_000 : compact.endsWith("mil") ? 1_000 : 1;
  const normalized = compact.replace(/(?:mi|mil)$/, "").replace(/\.(?=\d{3}(?:\D|$))/g, "").replace(",", ".");
  const number = Number(normalized);
  return Number.isFinite(number) ? number * multiplier : null;
}

export function safeRate(numerator: unknown, denominator: unknown) {
  const top = finite(numerator);
  const bottom = finite(denominator);
  if (top === null || bottom === null || bottom <= 0 || top < 0) return null;
  return top / bottom;
}

export function assessViralityEvidence(metrics: Record<string, unknown> | null | undefined): ViralityAssessment {
  const views = finite(metrics?.views ?? metrics?.viewsObserved);
  const shares = finite(metrics?.shares ?? metrics?.sharesObserved);
  const saves = finite(metrics?.saves ?? metrics?.savesObserved);
  const completions = finite(metrics?.completions);
  const clicks = finite(metrics?.clicks);
  const conversions = finite(metrics?.conversions);
  const creatorMedianViews = finite(metrics?.creatorMedianViews);
  const cohortMedianViews = finite(metrics?.cohortMedianViews);
  const observedRates: Record<string, number> = {};
  const observations: string[] = [];
  const limitations = ["Desempenho observado não demonstra qual elemento criativo causou o resultado."];
  const rateEntries = [
    ["shareRate", safeRate(shares, views)], ["saveRate", safeRate(saves, views)], ["completionRate", safeRate(completions, views)],
    ["clickRate", safeRate(clicks, views)], ["conversionRate", safeRate(conversions, clicks)],
  ] as const;
  for (const [name, value] of rateEntries) if (value !== null) observedRates[name] = value;
  if (views !== null && creatorMedianViews !== null && creatorMedianViews > 0) observedRates.creatorBaselineRatio = views / creatorMedianViews;
  if (views !== null && cohortMedianViews !== null && cohortMedianViews > 0) observedRates.cohortRatio = views / cohortMedianViews;

  let status: ViralityAssessment["status"] = "indeterminate";
  if ((observedRates.conversionRate ?? 0) >= 0.05) status = "strong_conversion";
  else if ((observedRates.completionRate ?? 0) >= 0.7) status = "strong_retention";
  else if ((observedRates.shareRate ?? 0) >= 0.02) status = "high_shareability";
  else if ((observedRates.cohortRatio ?? 0) >= 3) status = "breakout_relative_to_cohort";
  else if ((observedRates.creatorBaselineRatio ?? 0) >= 3) status = "above_creator_baseline";

  if (status === "indeterminate") limitations.push("Faltam baseline do próprio perfil, coorte funcional, denominadores ou métricas de retenção/ação para classificar desempenho relativo.");
  else observations.push(`Há evidência descritiva compatível com ${status.replaceAll("_", " ")}; isso não é uma explicação causal de viralidade.`);
  if (!metrics || metrics.organicPaid === undefined) limitations.push("Distribuição orgânica, paga ou mista não foi informada.");
  if (!metrics?.observedAt) limitations.push("Janela e data de observação não foram informadas.");
  return { status, confidence: status === "indeterminate" ? "low" : Object.keys(observedRates).length >= 3 ? "medium" : "low", observedRates, observations, limitations, causalClaimAllowed: false };
}
