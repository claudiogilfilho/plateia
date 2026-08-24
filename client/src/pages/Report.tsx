import { Badge } from "@/components/ui/badge";
import { trpc } from "@/lib/trpc";
import { parseReportJson } from "@/lib/reportParsing";
import { AlertTriangle, ArrowLeft, BrainCircuit, CheckCircle2, CircleAlert, ExternalLink, Lightbulb, Link2, Loader2, Target, UploadCloud } from "lucide-react";
import React, { type CSSProperties } from "react";
import { Link, useRoute, useSearch } from "wouter";

const criteria = ["gancho", "clareza", "relevância", "desejo", "confiança", "retenção", "ação", "objeções"] as const;
type Criterion = (typeof criteria)[number];
export type ReadingCoverage = { level: "complete" | "partial" | "requires_complement"; title: string; description: string; mode?: "visual_only" | "requires_visual"; excludedCriteria?: Criterion[] };
type ReportData = {
  consumers: Array<{ name: string; overallScore: number; reaction: string; criteria: Record<Criterion, number | null>; mainObjection: string }>;
  synthesis: { overallScore: number; weightedAverage: number; divergence: number; strengths: string[]; risks: string[]; recommendations: [string, string, string]; unassessedCriteria?: Criterion[] };
  coverage?: ReadingCoverage;
  observatory?: {
    promptVersion: string;
    classification: { materialFormat: string; primaryFamily: string; objectives: string[]; advertisingType?: string; commercialIntent?: string; mechanisms?: string[]; segment: string; confidence: "low" | "medium" | "high"; needsHumanReview: boolean };
    comparisons: Array<{ id: string | number; title: string; creator: string; similarity: number; comparisonLevel: 1 | 2 | 3 | 4; primaryFamily: string; segment: string }>;
    patterns: Array<{ id: string | number; name: string; stage: string; supportingCount: number; counterexampleCount: number; confidence: "low" | "medium" | "high"; mechanism: string }>;
    comparisonLevel: 1 | 2 | 3 | 4;
    benchmarkConfidence: "low" | "medium" | "high";
  } | null;
};

function isCompleteReport(value: ReportData | null): value is ReportData {
  return Boolean(value && Array.isArray(value.consumers) && value.consumers.length && value.synthesis && typeof value.synthesis.overallScore === "number");
}

export default function Report() {
  const [, params] = useRoute("/analises/:id");
  const id = Number(params?.id);
  const search = useSearch();
  const { data: analysis, isLoading, error } = trpc.analyses.get.useQuery({ id }, { enabled: Number.isFinite(id), retry: false });
  const previewRequiresVisual = import.meta.env.DEV && new URLSearchParams(search).get("preview") === "requires_visual";
  const previewCaptionMissing = import.meta.env.DEV && new URLSearchParams(search).get("preview") === "caption_missing";

  if (previewRequiresVisual) return <NeedsContentReport contentType="reel" sourceUrl="https://www.instagram.com/reel/exemplo/" reportJson={JSON.stringify({ coverage: { level: "requires_complement", mode: "requires_visual", title: "Material visual necessário", description: "Você escolheu uma leitura somente visual, mas o Instagram não disponibilizou capa, imagem ou vídeo público para este link. Envie o arquivo original para continuar sem legenda." } })} />;
  if (previewCaptionMissing) return <NeedsContentReport contentType="reel" sourceUrl="https://www.instagram.com/reel/exemplo/" reportJson={JSON.stringify({ coverage: { level: "requires_complement", mode: "requires_visual", title: "Material visual necessário", description: "O Instagram não disponibilizou imagem ou vídeo público para este link. Envie o arquivo para a Platéia avaliar o conteúdo visual; a legenda é opcional." } })} />;

  if (isLoading) return <div className="grid min-h-[55vh] place-items-center"><Loader2 className="h-7 w-7 animate-spin text-violet-600" /></div>;
  if (error) return <div role="alert" className="mx-auto mt-16 max-w-xl rounded-2xl border border-rose-100 bg-rose-50 p-6 text-center text-rose-700">Não foi possível carregar este relatório agora. Volte ao histórico e tente novamente.</div>;
  if (!analysis) return <div className="p-8 text-slate-600">Avaliação não encontrada.</div>;
  if (analysis.status === "failed") return <FailedReport />;
  if (analysis.status === "needs_content") return <NeedsContentReport contentType={analysis.contentType} sourceUrl={analysis.sourceUrl} reportJson={analysis.reportJson} />;
  if (!analysis.reportJson) return <div className="mx-auto max-w-xl pt-16 text-center"><Loader2 className="mx-auto mb-4 h-9 w-9 animate-spin text-violet-600" /><h1 className="font-display text-3xl font-extrabold text-[#2b1058]">A Platéia está lendo seu material.</h1><p className="mt-2 text-slate-600">O relatório aparecerá aqui assim que a avaliação for concluída.</p></div>;

  const report = parseReportJson<ReportData>(analysis.reportJson);
  if (!isCompleteReport(report)) return <InvalidReport />;
  const reportTitle = analysis.product || `Avaliação de ${analysis.contentType}`;
  const reportContext = [analysis.objective && `Objetivo: ${analysis.objective}`, analysis.targetAudience && `Público: ${analysis.targetAudience}`].filter(Boolean).join(" · ");
  const excludedCriteria = Array.from(new Set([...(report.coverage?.excludedCriteria ?? []), ...(report.synthesis.unassessedCriteria ?? [])]));
  const assessedCriteria = criteria.filter(key => !excludedCriteria.includes(key));
  const avgByCriterion = Object.fromEntries(assessedCriteria.flatMap(key => {
    const scores = report.consumers.map(consumer => consumer.criteria[key]).filter((score): score is number => score !== null);
    return scores.length ? [[key, Math.round(scores.reduce((sum, score) => sum + score, 0) / scores.length)]] : [];
  })) as Partial<Record<Criterion, number>>;

  return <div className="mx-auto max-w-7xl pb-12">
    <Link href="/historico" className="mb-6 inline-flex items-center gap-2 rounded-md px-1 py-1 text-sm font-semibold text-violet-700 hover:text-violet-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500"><ArrowLeft className="h-4 w-4" /> Voltar ao histórico</Link>
    <section className="relative overflow-hidden rounded-[2rem] bg-[#2b1058] px-6 py-8 text-white sm:px-10">
      <div className="absolute -right-14 -top-14 h-56 w-56 rounded-full bg-[#ff6f61]/30 blur-3xl" />
      <div className="relative grid gap-8 md:grid-cols-[1fr_auto] md:items-center">
        <div>
          <Badge className="border-violet-400/25 bg-white/10 text-violet-100 hover:bg-white/10">Relatório de avaliação</Badge>{report.coverage?.level === "partial" && <Badge className="ml-2 border-amber-200/30 bg-amber-300/15 text-amber-100 hover:bg-amber-300/15">Leitura parcial</Badge>}
          <h1 className="mt-4 font-display text-4xl font-extrabold tracking-[-0.06em] sm:text-5xl">{reportTitle}</h1>
          {reportContext && <p className="mt-3 max-w-2xl text-sm leading-6 text-violet-100">{reportContext}</p>}
          {analysis.sourceUrl && <a href={analysis.sourceUrl} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/10 px-3 py-2 text-xs font-bold text-white transition-colors hover:bg-white/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"><ExternalLink className="h-3.5 w-3.5" /> Abrir material de origem</a>}
        </div>
        <div className="flex items-center gap-4">
          <div className="score-orb" style={{ "--score": report.synthesis.overallScore } as CSSProperties}><div><strong>{report.synthesis.overallScore}</strong><span>/100</span></div></div>
          <div><p className="text-sm font-bold">Nota geral</p><p className="mt-1 text-xs text-violet-200">Leitura consolidada da Platéia</p></div>
        </div>
      </div>
    </section>
    <CoverageNotice coverage={report.coverage} />
    <ObservatoryNotice observatory={report.observatory} />
    <section className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
      <div className="space-y-6">
        <div className="plateia-card p-6 sm:p-7">
          <div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Painel de critérios</p><h2 className="mt-1 font-display text-2xl font-extrabold tracking-[-0.045em] text-[#2b1058]">O que o material comunica</h2></div><span className="rounded-xl bg-violet-50 px-3 py-2 text-xs font-bold text-violet-700">Média {report.synthesis.weightedAverage}</span></div>
          <div className="mt-7 space-y-4">{criteria.map(key => excludedCriteria.includes(key) ? <ExcludedScore key={key} label={key} /> : <ScoreBar key={key} label={key} score={avgByCriterion[key] ?? 0} />)}</div>
        </div>
        <div className="plateia-card p-6 sm:p-7">
          <div className="flex items-center gap-3"><div className="grid h-10 w-10 place-items-center rounded-xl bg-[#fff1ef] text-[#f15d50]"><Target className="h-5 w-5" /></div><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Leitura por perfil</p><h2 className="font-display text-2xl font-extrabold tracking-[-0.045em] text-[#2b1058]">Cinco reações, uma decisão melhor.</h2></div></div>
          <div className="mt-6 grid gap-3">{report.consumers.map(consumer => <ConsumerCard key={consumer.name} consumer={consumer} />)}</div>
        </div>
      </div>
      <aside className="space-y-6">
        <InsightList tone="success" title="Pontos fortes" items={report.synthesis.strengths} />
        <InsightList tone="risk" title="Riscos percebidos" items={report.synthesis.risks} />
        <div className="overflow-hidden rounded-[1.6rem] bg-[#ff6f61] p-6 text-white shadow-[0_18px_35px_-20px_rgba(255,111,97,0.9)]"><div className="flex items-center gap-2"><Lightbulb className="h-5 w-5" /><p className="text-xs font-bold uppercase tracking-[0.16em] text-white/80">Prioridade de melhoria</p></div><h2 className="mt-2 font-display text-2xl font-extrabold tracking-[-0.045em]">As próximas três decisões.</h2><ol className="mt-5 space-y-4">{report.synthesis.recommendations.map((item, index) => <li key={index} className="flex gap-3"><span className="grid h-6 w-6 shrink-0 place-items-center rounded-full bg-white/20 text-xs font-extrabold">{index + 1}</span><p className="text-sm leading-5 text-white">{item}</p></li>)}</ol></div>
        <div className="rounded-2xl border border-violet-100 bg-violet-50/55 p-5"><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Divergência entre perfis</p><p className="mt-2 font-display text-3xl font-extrabold tracking-[-0.06em] text-[#2b1058]">{report.synthesis.divergence}<span className="ml-1 text-sm tracking-normal text-slate-500">/100</span></p><p className="mt-2 text-xs leading-5 text-slate-600">{report.synthesis.divergence > 30 ? "Os perfis reagiram de modo bastante diferente. Vale observar para quem a mensagem é mais forte." : "Os perfis tiveram uma leitura relativamente alinhada do material."}</p></div>
      </aside>
    </section>
  </div>;
}

function FailedReport() {
  return <div className="mx-auto max-w-xl pt-16 text-center"><CircleAlert className="mx-auto mb-4 h-10 w-10 text-rose-500" /><h1 className="font-display text-3xl font-extrabold text-[#2b1058]">Essa leitura não foi concluída.</h1><p className="mt-2 text-slate-600">Tente enviar o material novamente. Nenhum relatório parcial foi salvo.</p><Link href="/avaliar" className="mt-6 inline-flex h-10 items-center rounded-md bg-[#2b1058] px-4 text-sm font-semibold text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500">Nova avaliação</Link></div>;
}

function InvalidReport() {
  return <div role="alert" className="mx-auto max-w-xl rounded-2xl border border-rose-100 bg-rose-50 p-6 text-center text-rose-700"><CircleAlert className="mx-auto mb-3 h-8 w-8" /><p className="font-bold">Este relatório está incompleto.</p><p className="mt-1 text-sm">Volte ao histórico e tente uma nova avaliação. A tela foi protegida para não interromper o restante do aplicativo.</p></div>;
}

export function NeedsContentReport({ contentType, sourceUrl, reportJson }: { contentType: string; sourceUrl: string | null; reportJson: string | null }) {
  const coverage = parseReportJson<Pick<ReportData, "coverage">>(reportJson)?.coverage;
  const action = getComplementAction(coverage, contentType, sourceUrl);
  return <section className="mx-auto max-w-2xl py-3 sm:py-12"><div className="rounded-[1.75rem] border border-violet-100 bg-white px-6 py-8 text-center shadow-[0_20px_45px_-36px_rgba(43,16,88,0.45)] sm:px-10 sm:py-10"><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-amber-50 text-amber-500"><CircleAlert className="h-7 w-7" /></div><p className="mt-5 text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Link público indisponível</p><h1 className="mt-2 font-display text-3xl font-extrabold tracking-[-0.055em] text-[#2b1058] sm:text-4xl">{action.heading}</h1><p className="mx-auto mt-4 max-w-lg text-base leading-7 text-slate-600">{coverage?.description || "O Instagram não disponibilizou a prévia deste conteúdo. Para continuar agora, envie o arquivo original; a legenda permanece opcional."}</p><div className="mx-auto mt-6 max-w-md rounded-2xl border border-violet-100 bg-violet-50/65 p-4 text-left"><div className="flex gap-3"><UploadCloud className="mt-0.5 h-5 w-5 shrink-0 text-violet-700" /><div><p className="text-sm font-bold text-[#2b1058]">Você não precisa recomeçar.</p><p className="mt-1 text-xs leading-5 text-slate-600">Abra o vídeo ou a imagem original no celular e envie-o na próxima tela. MP4, JPG, PNG ou WEBP de até 12 MB.</p></div></div></div><a href={action.href} className="mt-6 inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[#2b1058] px-5 text-base font-bold text-white shadow-[0_14px_28px_-18px_rgba(43,16,88,0.85)] transition-transform hover:bg-[#401d7b] active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 sm:w-auto"><UploadCloud className="h-5 w-5" />{action.label}</a>{sourceUrl && <a href={getRetryLink(contentType, sourceUrl)} className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-violet-700 hover:text-violet-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500"><Link2 className="h-4 w-4" />Tentar outro link público</a>}</div></section>;
}

function humanize(value: string) {
  return value.replaceAll("_", " ");
}

function ObservatoryNotice({ observatory }: { observatory?: ReportData["observatory"] }) {
  if (!observatory) return null;
  const { classification, comparisons, patterns = [] } = observatory;
  const levelLabels = { 1: "mesma família, objetivo e segmento", 2: "mesma família e objetivo", 3: "mecanismo semelhante", 4: "sem equivalente confiável" } as const;
  const confidenceLabels = { low: "baixa", medium: "média", high: "alta" } as const;
  return <section className="mt-6 rounded-2xl border border-violet-100 bg-violet-50/55 p-5 sm:p-6"><div className="flex items-start gap-3"><div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[#2b1058] text-white"><BrainCircuit className="h-5 w-5" /></div><div className="min-w-0 flex-1"><div className="flex flex-wrap items-center gap-2"><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-600">Contexto do Observatório</p><Badge variant="outline" className="border-violet-200 bg-white text-violet-700">Confiança {confidenceLabels[observatory.benchmarkConfidence]}</Badge></div><h2 className="mt-1 font-display text-xl font-extrabold text-[#2b1058] capitalize">{humanize(classification.primaryFamily)} · {classification.segment}</h2><p className="mt-2 text-sm leading-6 text-slate-600">A avaliação identificou este material como <strong>{humanize(classification.materialFormat)}</strong>, com objetivo provável de <strong>{classification.objectives.map(humanize).join(", ")}</strong>{classification.advertisingType ? <> e publicidade <strong>{humanize(classification.advertisingType)}</strong></> : null}. A comparação usada foi de nível {observatory.comparisonLevel}: {levelLabels[observatory.comparisonLevel]}.</p>{comparisons.length ? <><p className="mt-2 text-xs leading-5 text-slate-500">Base comparável: {comparisons.length} {comparisons.length === 1 ? "referência curada" : "referências curadas"}; {patterns.length} {patterns.length === 1 ? "padrão provisório relevante" : "padrões provisórios relevantes"}. O Observatório informa contexto; os cinco cérebros sintéticos continuam independentes.</p><p className="mt-2 text-xs leading-5 text-slate-500"><strong>Referências que influenciaram a comparação:</strong> {comparisons.slice(0, 3).map(item => `${item.title} — ${item.creator}`).join("; ")}.</p>{patterns.length ? <p className="mt-1 text-xs leading-5 text-slate-500"><strong>Padrões usados:</strong> {patterns.slice(0, 3).map(item => item.name).join("; ")}.</p> : null}</> : <p className="mt-2 text-xs leading-5 text-amber-700">Ainda não há referência suficientemente semelhante. A nota foi calculada pelos critérios estruturais e não foi tratada como benchmark de categoria.</p>}</div></div></section>;
}

export function getComplementAction(coverage: ReadingCoverage | undefined, contentType: string, sourceUrl: string | null) {
  const params = new URLSearchParams({ envio: "upload", tipo: contentType, retorno: "instagram" });
  if (sourceUrl) params.set("link", sourceUrl);
  if (coverage?.mode === "requires_visual") return { heading: "O Instagram não liberou esse material.", label: "Escolher arquivo original", href: `/avaliar?${params.toString()}` };
  return { heading: "O material visual não está disponível.", label: "Escolher arquivo original", href: `/avaliar?${params.toString()}` };
}

function getRetryLink(contentType: string, sourceUrl: string) {
  return `/avaliar?${new URLSearchParams({ envio: "link", tipo: contentType, link: sourceUrl, "tipo-link": "post-publicado" }).toString()}`;
}

export function CoverageNotice({ coverage }: { coverage?: ReadingCoverage }) {
  if (coverage?.level !== "partial") return null;
  return <div role="note" className="mt-6 flex gap-3 rounded-2xl border border-amber-200 bg-amber-50 px-5 py-4 text-amber-950"><CircleAlert className="mt-0.5 h-5 w-5 shrink-0 text-amber-700" /><div><p className="text-sm font-bold">{coverage.title}</p><p className="mt-1 text-sm leading-6 text-amber-900">{coverage.description}</p></div></div>;
}

function ConsumerCard({ consumer }: { consumer: ReportData["consumers"][number] }) {
  return <details className="group rounded-2xl border border-violet-100 bg-white px-4 py-3 open:bg-violet-50/45"><summary className="flex cursor-pointer list-none items-center gap-3 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500"><div className="grid h-9 w-9 place-items-center rounded-xl bg-[#2b1058] text-sm font-extrabold text-white">{consumer.overallScore}</div><div className="min-w-0 flex-1"><p className="font-bold text-[#2b1058]">{consumer.name}</p><p className="truncate text-xs text-slate-500">{consumer.reaction}</p></div><span className="text-xs font-semibold text-violet-600">Abrir</span></summary><div className="mt-4 border-t border-violet-100 pt-4"><p className="text-sm leading-6 text-slate-600">{consumer.reaction}</p><p className="mt-3 rounded-xl bg-white px-3 py-2 text-xs leading-5 text-slate-600"><strong className="text-[#2b1058]">Objeção central:</strong> {consumer.mainObjection}</p></div></details>;
}

function InsightList({ tone, title, items }: { tone: "success" | "risk"; title: string; items: string[] }) {
  const success = tone === "success";
  return <div className="plateia-card p-6"><div className={`flex items-center gap-2 ${success ? "text-emerald-700" : "text-amber-700"}`}>{success ? <CheckCircle2 className="h-5 w-5" /> : <AlertTriangle className="h-5 w-5" />}<p className="text-xs font-bold uppercase tracking-[0.16em]">{title}</p></div><div className="mt-4 space-y-3">{items.map((item, index) => <p key={index} className={`rounded-xl px-3 py-3 text-sm leading-5 ${success ? "bg-emerald-50 text-emerald-800" : "bg-amber-50 text-amber-800"}`}>{item}</p>)}</div></div>;
}

function ScoreBar({ label, score }: { label: string; score: number }) {
  return <div><div className="mb-1.5 flex items-center justify-between"><span className="capitalize text-sm font-semibold text-[#2b1058]">{label}</span><span className="text-xs font-bold text-violet-700">{score}</span></div><div className="h-2 overflow-hidden rounded-full bg-violet-100"><div className="h-full rounded-full bg-gradient-to-r from-[#4c2385] to-[#ff6f61]" style={{ width: `${score}%` }} /></div></div>;
}

function ExcludedScore({ label }: { label: string }) {
  return <div><div className="mb-1.5 flex items-center justify-between"><span className="capitalize text-sm font-semibold text-slate-500">{label}</span><span className="text-xs font-bold text-slate-400">não avaliado</span></div><div className="h-2 rounded-full bg-slate-100" /></div>;
}
