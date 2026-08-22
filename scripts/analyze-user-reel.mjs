import { writeFile } from "node:fs/promises";
import { evaluateContent, validateAnalysisShape } from "../server/contentAnalysis.ts";
import { resolveInstagramMaterial } from "../server/publicLinks.ts";

const sourceUrl = "https://www.instagram.com/reel/DcGe0hCTe8l/?igsi=MjNkMTc4OHR6d3dv";
const material = await resolveInstagramMaterial(sourceUrl);
if (!material?.mediaUrl && !material?.caption) throw new Error("Nenhum material público foi capturado do Reel.");

const report = await evaluateContent({
  contentType: "reel",
  text: material?.caption ?? "",
  product: "",
  objective: "",
  targetAudience: "",
  mediaUrl: material?.mediaUrl ?? null,
  mediaMimeType: material?.mediaMimeType ?? null,
  sourceUrl,
  analysisScope: "standard",
});
validateAnalysisShape(report);

const result = {
  sourceUrl,
  reading: {
    hasPublicMedia: Boolean(material?.mediaUrl),
    mediaMimeType: material?.mediaMimeType ?? null,
    hasPublicCaption: Boolean(material?.caption),
  },
  report,
};
await writeFile("/home/ubuntu/plateia_user_reel_analysis.json", JSON.stringify(result, null, 2));
console.log(JSON.stringify({
  score: report.synthesis.overallScore,
  weightedAverage: report.synthesis.weightedAverage,
  divergence: report.synthesis.divergence,
  consumers: report.consumers.map(consumer => ({ name: consumer.name, score: consumer.overallScore })),
  recommendations: report.synthesis.recommendations,
}, null, 2));
