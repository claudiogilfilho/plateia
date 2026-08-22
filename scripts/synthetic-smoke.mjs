import { writeFile } from "node:fs/promises";
import { evaluateContent, CONSUMERS, CRITERIA } from "../server/contentAnalysis.ts";

const cases = [
  {
    id: "copy-direta",
    input: {
      contentType: "copy",
      text: "Em 7 dias, organize sua rotina financeira com um plano simples. Baixe o guia gratuito e veja hoje onde seu dinheiro está escapando.",
      product: "Guia de organização financeira",
      objective: "Gerar cadastros",
      targetAudience: "Pessoas que querem organizar as finanças pessoais",
      analysisScope: "standard",
    },
  },
  {
    id: "reel-visual",
    input: {
      contentType: "reel",
      text: "",
      product: "Café especial de torra local",
      objective: "Aumentar desejo pelo produto",
      targetAudience: "Pessoas que apreciam cafés especiais",
      analysisScope: "visual_only",
    },
  },
  {
    id: "post-prova",
    input: {
      contentType: "post",
      text: "Antes de contratar, veja como funciona: diagnóstico, plano de ação e acompanhamento semanal. Sem promessas milagrosas; você recebe indicadores claros para decidir o próximo passo.",
      product: "Consultoria de posicionamento",
      objective: "Gerar conversas qualificadas",
      targetAudience: "Pequenas empresas em fase de crescimento",
      analysisScope: "standard",
    },
  },
];

function assertReport(caseId, report) {
  if (report.consumers.length !== CONSUMERS.length) throw new Error(`${caseId}: quantidade de consumidores inválida`);
  if (report.synthesis.recommendations.length !== 3) throw new Error(`${caseId}: recomendações inválidas`);
  const names = report.consumers.map(consumer => consumer.name);
  if (JSON.stringify(names) !== JSON.stringify(CONSUMERS)) throw new Error(`${caseId}: ordem de consumidores inválida`);
  for (const consumer of report.consumers) {
    for (const criterion of CRITERIA) {
      const score = consumer.criteria[criterion];
      if (!Number.isInteger(score) || score < 0 || score > 100) throw new Error(`${caseId}: critério inválido`);
    }
    if (!Number.isInteger(consumer.overallScore) || consumer.overallScore < 0 || consumer.overallScore > 100) throw new Error(`${caseId}: nota individual inválida`);
  }
  if (!Number.isInteger(report.synthesis.overallScore) || report.synthesis.overallScore < 0 || report.synthesis.overallScore > 100) throw new Error(`${caseId}: síntese inválida`);
}

const results = [];
for (const scenario of cases) {
  const report = await evaluateContent(scenario.input);
  assertReport(scenario.id, report);
  results.push({
    id: scenario.id,
    overallScore: report.synthesis.overallScore,
    weightedAverage: report.synthesis.weightedAverage,
    divergence: report.synthesis.divergence,
    consumers: report.consumers.map(consumer => ({ name: consumer.name, score: consumer.overallScore })),
    recommendations: report.synthesis.recommendations,
  });
}

await writeFile("/home/ubuntu/plateia_synthetic_smoke_results.json", JSON.stringify({ executedAt: new Date().toISOString(), results }, null, 2));
console.log(JSON.stringify({ passed: results.length, results }, null, 2));
