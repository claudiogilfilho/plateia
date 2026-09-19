export function parseReportJson<T>(reportJson: string | null): T | null {
  if (!reportJson) return null;
  try {
    const parsed = JSON.parse(reportJson) as unknown;
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed as T : null;
  } catch {
    return null;
  }
}

export function getReportScore(reportJson: string | null) {
  const report = parseReportJson<{ synthesis?: { overallScore?: unknown } }>(reportJson);
  const score = report?.synthesis?.overallScore;
  return typeof score === "number" && Number.isFinite(score) ? score : null;
}
