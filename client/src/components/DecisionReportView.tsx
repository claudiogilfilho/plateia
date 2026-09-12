import { Badge } from "@/components/ui/badge";
import { ArrowLeft, BrainCircuit, GitCompareArrows, ShieldCheck, Wrench } from "lucide-react";
import React from "react";
import { Link } from "wouter";

type Confidence = "low" | "medium" | "high";
type ScoreEvidence = { score: number | null; justification: string; evidence: string[]; confidence: Confidence };
type DecisionReport = {
  decisionSystemVersion: "1.0";
  operationalVerdict: "ready_to_publish" | "publish_after_adjustments" | "reevaluate" | "inconclusive";
  coverage?: { level: string; title: string; description: string };
  technicalTruth: Record<string, { status?: string; value?: unknown; limitation?: string }> & { limitations: string[] };
  blindAudit: {
    observedSummary: string; attentionAndRetention: ScoreEvidence; strengths: string[]; risks: string[]; limitations: string[]; frozenSha256: string;
    criteria: Array<ScoreEvidence & { name: string }>;
    lenses: Array<{ name: string; probableReaction: string; mainObjection: string; likelyAbandonmentMoment: string; reasonToContinue: string; likelyAction: string; confidence: Confidence }>;
    timeline: Array<{ stage: string; timeRange: string; observed: string; probableFunction: string; newInformation: string; reasonToContinue: string; estimatedAbandonmentRisk: "low" | "medium" | "high" | "not_assessed"; probableRiskCause: string; confidence: Confidence; specificCorrection: string; provenance: string }>;
    priorities: Array<{ timestampOrSection: string; observedProblem: string; probableMechanism: string; exactChange: string; component: string; intendedMetric: string; confidence: Confidence; humanValidationRequired: boolean }>;
    hookVariations: string[]; alternativeCta: string; editingGuidance: string; onScreenTextSuggestion: string; cutSuggestions: string[];
  };
  contextualAudit: { businessEffectiveness: ScoreEvidence; plateiaVerdict: string; alignment: string[]; incompatibilities: string[]; inventedOrUnsupportedInformation: string[]; missingInformation: string[]; uncommunicatedDifferentiators: string[]; limitations: string[]; confidence: Confidence };
  dualReading: { attentionAndRetention: ScoreEvidence; businessEffectiveness: ScoreEvidence };
  benchmark: { comparisonLevel: number; comparableReferenceCount: number; confidence: Confidence; limitation: string | null };
  comparison: null | { previousAnalysisId: number; previousBlindSha256: string; currentBlindSha256: string; changes: string[]; resolvedProblems: string[]; remainingRisks: string[]; scoreChanges: Array<{ dimension: string; before: number | null; after: number | null; reason: string }>; sideEffects: string[]; recommendedVersion: string; confidence: Confidence };
};

export function isDecisionReport(value: unknown): value is DecisionReport {
  return Boolean(value && typeof value === "object" && (value as { decisionSystemVersion?: unknown }).decisionSystemVersion === "1.0");
}

const verdictLabels = {
  ready_to_publish: "Pronto para publicar",
  publish_after_adjustments: "Publicar após ajustes",
  reevaluate: "Reavaliar",
  inconclusive: "Inconclusivo",
} as const;
const confidenceLabels = { low: "baixa", medium: "média", high: "alta" } as const;
const provenanceLabels: Record<string, string> = {
  measured_fact: "fato medido", ai_interpretation: "interpretação da IA", observatory_hypothesis: "hipótese do Observatório", unvalidated_prediction: "previsão não validada",
};
const riskStyles = { low: "bg-emerald-100 text-emerald-800", medium: "bg-amber-100 text-amber-900", high: "bg-rose-100 text-rose-800", not_assessed: "bg-slate-100 text-slate-600" } as const;

export function DecisionReportView({ report, analysisId, title, context }: { report: DecisionReport; analysisId: number; title: string; context: string }) {
  const limitations = Array.from(new Set([...report.technicalTruth.limitations, ...report.blindAudit.limitations, ...report.contextualAudit.limitations]));
  return <div className="mx-auto max-w-7xl pb-14">
    <Link href="/historico" className="mb-5 inline-flex items-center gap-2 text-sm font-bold text-violet-700"><ArrowLeft className="h-4 w-4" /> Voltar ao histórico</Link>
    <header className="overflow-hidden rounded-[1.75rem] bg-[#2b1058] p-6 text-white sm:p-9">
      <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between"><div><div className="flex flex-wrap gap-2"><Badge className="bg-white/10 text-white hover:bg-white/10">Decisão criativa pré-publicação</Badge><Badge className="bg-violet-400/20 text-violet-100 hover:bg-violet-400/20">Protocolo 2.1</Badge></div><h1 className="mt-4 font-display text-3xl font-extrabold tracking-[-0.05em] sm:text-5xl">{title}</h1>{context && <p className="mt-3 max-w-3xl text-sm leading-6 text-violet-100">{context}</p>}</div><div className="rounded-2xl bg-white/10 p-4 lg:max-w-xs"><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-200">Veredito operacional</p><p className="mt-1 text-2xl font-extrabold">{verdictLabels[report.operationalVerdict]}</p><p className="mt-2 text-xs leading-5 text-violet-100">É um parecer do Platéia, não autorização final nem previsão de resultado.</p></div></div>
    </header>

    {report.coverage && <section className="mt-5 rounded-2xl border border-violet-100 bg-white p-5"><p className="text-xs font-bold uppercase tracking-[0.14em] text-violet-600">Cobertura da análise</p><h2 className="mt-1 font-bold text-[#2b1058]">{report.coverage.title}</h2><p className="mt-1 text-sm leading-6 text-slate-600">{report.coverage.description}</p></section>}

    <section className="mt-5 grid gap-4 sm:grid-cols-2">
      <ScoreCard label="Potencial de atenção e retenção" value={report.dualReading.attentionAndRetention} note="Tendência estrutural estimada; não é retenção real." />
      <ScoreCard label="Efetividade para o negócio" value={report.dualReading.businessEffectiveness} note="Depende da qualidade do dossiê informado." />
    </section>

    <section className="mt-5 grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
      <div className="plateia-card p-5 sm:p-7"><p className="section-kicker">Etapa 1 · leitura cega congelada</p><h2 className="section-title">O que o conteúdo efetivamente comunicou</h2><p className="mt-4 text-sm leading-7 text-slate-700">{report.blindAudit.observedSummary}</p><p className="mt-4 break-all text-[11px] text-slate-400">SHA-256: {report.blindAudit.frozenSha256}</p></div>
      <div className="plateia-card p-5 sm:p-7"><p className="section-kicker">Etapa 2 · adequação ao negócio</p><h2 className="section-title">Comparação sem rever o vídeo</h2><p className="mt-4 text-sm leading-6 text-slate-700">{report.contextualAudit.businessEffectiveness.justification}</p><p className="mt-3 text-xs font-bold text-violet-700">Confiança {confidenceLabels[report.contextualAudit.confidence]} · plateiaVerdict: {report.contextualAudit.plateiaVerdict}</p>{report.contextualAudit.missingInformation.length > 0 && <MiniList title="Não foi possível concluir" items={report.contextualAudit.missingInformation} tone="amber" />}</div>
    </section>

    <section className="mt-5 plateia-card p-5 sm:p-7"><p className="section-kicker">Oito critérios</p><h2 className="section-title">Nota, evidência e confiança</h2><div className="mt-5 grid gap-3 md:grid-cols-2">{report.blindAudit.criteria.map(item => <details key={item.name} className="rounded-2xl border border-violet-100 p-4"><summary className="flex cursor-pointer list-none items-center justify-between gap-3"><span className="font-bold capitalize text-[#2b1058]">{item.name}</span><span className="rounded-lg bg-violet-50 px-2.5 py-1 text-sm font-extrabold text-violet-700">{item.score === null ? "não avaliado" : `${item.score}/100`}</span></summary><p className="mt-3 text-sm leading-6 text-slate-600">{item.justification}</p><Evidence items={item.evidence} confidence={item.confidence} /></details>)}</div></section>

    <section className="mt-5 plateia-card p-5 sm:p-7"><p className="section-kicker">Cinco lentes comportamentais</p><h2 className="section-title">Reações independentes</h2><div className="mt-5 grid gap-3">{report.blindAudit.lenses.map(lens => <details key={lens.name} className="rounded-2xl border border-violet-100 p-4 open:bg-violet-50/40"><summary className="cursor-pointer list-none font-bold text-[#2b1058]">{lens.name} <span className="ml-2 text-xs font-medium text-slate-500">confiança {confidenceLabels[lens.confidence]}</span></summary><div className="mt-3 grid gap-3 text-sm leading-6 text-slate-600 sm:grid-cols-2"><p><strong>Reação:</strong> {lens.probableReaction}</p><p><strong>Objeção:</strong> {lens.mainObjection}</p><p><strong>Possível abandono:</strong> {lens.likelyAbandonmentMoment}</p><p><strong>Motivo para continuar:</strong> {lens.reasonToContinue}</p><p className="sm:col-span-2"><strong>Ação provável:</strong> {lens.likelyAction}</p></div></details>)}</div></section>

    <section className="mt-5 plateia-card p-5 sm:p-7"><p className="section-kicker">Linha do tempo de risco de retenção</p><h2 className="section-title">Sinais temporais, sem fingir uma curva real</h2><p className="mt-2 text-sm leading-6 text-slate-600">Cada trecho identifica sua origem e confiança. Risco estimado não equivale a retenção medida.</p><div className="mt-5 space-y-3">{report.blindAudit.timeline.map((item, index) => <article key={`${item.stage}-${index}`} className="relative rounded-2xl border border-violet-100 p-4 sm:pl-20"><div className="mb-3 sm:absolute sm:left-4 sm:top-4"><span className="rounded-lg bg-[#2b1058] px-2 py-1 text-xs font-bold text-white">{item.timeRange}</span></div><div className="flex flex-wrap items-center gap-2"><h3 className="font-bold text-[#2b1058]">{item.stage}</h3><span className={`rounded-full px-2 py-0.5 text-[11px] font-bold ${riskStyles[item.estimatedAbandonmentRisk]}`}>risco {item.estimatedAbandonmentRisk.replace("not_assessed", "não avaliado")}</span><span className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] text-slate-600">{provenanceLabels[item.provenance] ?? item.provenance} · confiança {confidenceLabels[item.confidence]}</span></div><p className="mt-2 text-sm leading-6 text-slate-700"><strong>Observado:</strong> {item.observed}</p><div className="mt-2 grid gap-2 text-xs leading-5 text-slate-600 sm:grid-cols-2"><p><strong>Função provável:</strong> {item.probableFunction}</p><p><strong>Informação nova:</strong> {item.newInformation}</p><p><strong>Motivo para continuar:</strong> {item.reasonToContinue}</p><p><strong>Causa do risco:</strong> {item.probableRiskCause}</p></div>{item.specificCorrection && <p className="mt-3 rounded-xl bg-violet-50 p-3 text-xs leading-5 text-violet-900"><strong>Correção:</strong> {item.specificCorrection}</p>}</article>)}</div></section>

    <section className="mt-5 overflow-hidden rounded-[1.75rem] bg-[#ff6f61] p-5 text-white sm:p-7"><div className="flex items-center gap-2"><Wrench className="h-5 w-5" /><p className="text-xs font-bold uppercase tracking-[0.14em] text-white/80">Exatamente três correções prioritárias</p></div><div className="mt-5 grid gap-4 lg:grid-cols-3">{report.blindAudit.priorities.map((item, index) => <article key={index} className="rounded-2xl bg-white/12 p-4"><p className="text-xs font-bold text-white/75">{index + 1} · {item.timestampOrSection} · {item.component}</p><h3 className="mt-2 font-bold">{item.observedProblem}</h3><p className="mt-2 text-sm leading-6 text-white/90">{item.exactChange}</p><p className="mt-3 text-xs leading-5 text-white/80"><strong>Mecanismo:</strong> {item.probableMechanism}<br /><strong>Objetivo da mudança:</strong> {item.intendedMetric}<br /><strong>Confiança:</strong> {confidenceLabels[item.confidence]}{item.humanValidationRequired ? " · requer validação humana" : ""}</p></article>)}</div></section>

    <section className="mt-5 grid gap-5 lg:grid-cols-2"><div className="plateia-card p-5 sm:p-7"><p className="section-kicker">Variações executáveis</p><h2 className="section-title">Instruções para a próxima versão</h2><MiniList title="Hooks" items={report.blindAudit.hookVariations} /><MiniList title="CTA alternativo" items={report.blindAudit.alternativeCta ? [report.blindAudit.alternativeCta] : []} /><MiniList title="Montagem e cortes" items={[report.blindAudit.editingGuidance, ...report.blindAudit.cutSuggestions].filter(Boolean)} /><MiniList title="Texto na tela" items={report.blindAudit.onScreenTextSuggestion ? [report.blindAudit.onScreenTextSuggestion] : []} /></div><div className="plateia-card p-5 sm:p-7"><p className="section-kicker">Verdade técnica</p><h2 className="section-title">O que foi medido do arquivo</h2><TechnicalTruth truth={report.technicalTruth} /><p className="mt-4 text-xs leading-5 text-slate-500">Campos sem detector aparecem como não avaliados; a IA não preenche medições ausentes.</p></div></section>

    <section className="mt-5 grid gap-5 lg:grid-cols-2"><div className="plateia-card p-5 sm:p-7"><div className="flex items-center gap-2 text-violet-700"><BrainCircuit className="h-5 w-5" /><p className="section-kicker">Observatório</p></div><h2 className="section-title">Benchmark comparável</h2><p className="mt-3 text-sm leading-6 text-slate-600">Nível {report.benchmark.comparisonLevel} · {report.benchmark.comparableReferenceCount} referências comparáveis · confiança {confidenceLabels[report.benchmark.confidence]}.</p>{report.benchmark.limitation && <p className="mt-3 rounded-xl bg-amber-50 p-3 text-xs leading-5 text-amber-900">{report.benchmark.limitation}</p>}</div><div className="plateia-card p-5 sm:p-7"><div className="flex items-center gap-2 text-emerald-700"><ShieldCheck className="h-5 w-5" /><p className="section-kicker">Limitações e confiança</p></div><h2 className="section-title">O que este relatório não afirma</h2><MiniList title="Limitações declaradas" items={limitations.length ? limitations : ["Nenhuma limitação adicional foi registrada."]} tone="amber" /><p className="mt-4 text-xs leading-5 text-slate-500">O relatório não prevê visualizações, não mede retenção real e não valida automaticamente hipóteses do Observatório.</p></div></section>

    {report.comparison && <Comparison comparison={report.comparison} />}
    <div className="mt-6 flex flex-col gap-3 sm:flex-row"><Link href={`/avaliar?compararCom=${analysisId}`} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[#2b1058] px-5 text-sm font-bold text-white"><GitCompareArrows className="h-4 w-4" /> Enviar versão corrigida</Link><Link href="/avaliar" className="inline-flex min-h-12 items-center justify-center rounded-xl border border-violet-200 px-5 text-sm font-bold text-violet-800">Nova avaliação independente</Link></div>
  </div>;
}

function ScoreCard({ label, value, note }: { label: string; value: ScoreEvidence; note: string }) {
  return <article className="plateia-card p-5 sm:p-6"><p className="text-xs font-bold uppercase tracking-[0.14em] text-violet-600">{label}</p><div className="mt-3 flex items-start gap-4"><span className="min-w-20 text-4xl font-extrabold tracking-[-0.05em] text-[#2b1058]">{value.score === null ? "—" : value.score}</span><div><p className="text-sm leading-6 text-slate-700">{value.justification}</p><p className="mt-2 text-xs text-slate-500">Confiança {confidenceLabels[value.confidence]}. {note}</p></div></div></article>;
}

function Evidence({ items, confidence }: { items: string[]; confidence: Confidence }) { return <div className="mt-3 rounded-xl bg-slate-50 p-3 text-xs leading-5 text-slate-600"><strong>Evidência observável:</strong> {items.length ? items.join("; ") : "não disponível"}. <strong>Confiança:</strong> {confidenceLabels[confidence]}.</div>; }
function MiniList({ title, items, tone = "violet" }: { title: string; items: string[]; tone?: "violet" | "amber" }) { if (!items.length) return null; return <div className={`mt-4 rounded-xl p-3 ${tone === "amber" ? "bg-amber-50 text-amber-900" : "bg-violet-50 text-violet-900"}`}><p className="text-xs font-bold uppercase tracking-[0.12em]">{title}</p><ul className="mt-2 space-y-1 text-xs leading-5">{items.map((item, index) => <li key={index}>• {item}</li>)}</ul></div>; }

function TechnicalTruth({ truth }: { truth: DecisionReport["technicalTruth"] }) {
  const fields: Array<[string, string]> = [["durationSeconds", "Duração"], ["resolution", "Resolução"], ["aspectRatio", "Proporção"], ["framesPerSecond", "FPS"], ["videoCodec", "Codec"], ["fileSizeBytes", "Tamanho"], ["audioPresent", "Áudio"], ["volume", "Volume"], ["silenceIntervals", "Silêncios"], ["sceneChanges", "Mudanças de cena"], ["averageSceneDurationSeconds", "Duração média das cenas"], ["cutsPerMinute", "Cortes por minuto"]];
  return <dl className="mt-4 grid gap-2 text-xs sm:grid-cols-2">{fields.map(([key, label]) => { const field = truth[key]; return <div key={key} className="rounded-xl bg-slate-50 p-3"><dt className="font-bold text-slate-500">{label}</dt><dd className="mt-1 break-words text-[#2b1058]">{field?.status === "measured" ? formatValue(field.value, key) : "não avaliado"}</dd></div>; })}</dl>;
}
function formatValue(value: unknown, key: string) {
  if (key === "fileSizeBytes" && typeof value === "number") return `${(value / 1024 / 1024).toFixed(2)} MB`;
  if (typeof value === "boolean") return value ? "presente" : "ausente";
  if (typeof value === "number") return String(value);
  if (Array.isArray(value)) return value.length ? value.map(item => typeof item === "number" ? `${item}s` : JSON.stringify(item)).join(", ") : "nenhum detectado";
  if (value && typeof value === "object") return Object.values(value as Record<string, unknown>).join(" × ");
  return String(value ?? "não avaliado");
}

function Comparison({ comparison }: { comparison: NonNullable<DecisionReport["comparison"]> }) {
  return <section className="mt-5 plateia-card p-5 sm:p-7"><div className="flex items-center gap-2 text-violet-700"><GitCompareArrows className="h-5 w-5" /><p className="section-kicker">Comparação com a versão #{comparison.previousAnalysisId}</p></div><h2 className="section-title">O que mudou sem sobrescrever o histórico</h2><div className="mt-5 grid gap-4 lg:grid-cols-3"><MiniList title="Mudanças" items={comparison.changes} /><MiniList title="Problemas resolvidos" items={comparison.resolvedProblems} /><MiniList title="Riscos restantes" items={comparison.remainingRisks} tone="amber" /></div><p className="mt-4 text-sm font-bold text-[#2b1058]">Versão recomendada: {comparison.recommendedVersion === "current" ? "atual" : comparison.recommendedVersion === "previous" ? "anterior" : "decisão inconclusiva"} · confiança {confidenceLabels[comparison.confidence]}</p>{comparison.sideEffects.length > 0 && <MiniList title="Possíveis efeitos colaterais" items={comparison.sideEffects} tone="amber" />}</section>;
}
