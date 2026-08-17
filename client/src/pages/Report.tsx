import { Badge } from "@/components/ui/badge";
import { trpc } from "@/lib/trpc";
import { AlertTriangle, ArrowLeft, CheckCircle2, CircleAlert, ExternalLink, Lightbulb, Loader2, Target } from "lucide-react";
import type { CSSProperties } from "react";
import { Link, useRoute } from "wouter";

const criteria = ["gancho", "clareza", "relevância", "desejo", "confiança", "retenção", "ação", "objeções"] as const;
type Criterion = (typeof criteria)[number];
type ReportData = {
  consumers: Array<{ name: string; overallScore: number; reaction: string; criteria: Record<Criterion, number>; mainObjection: string }>;
  synthesis: { overallScore: number; weightedAverage: number; divergence: number; strengths: string[]; risks: string[]; recommendations: [string, string, string] };
};

export default function Report() {
  const [, params] = useRoute("/analises/:id");
  const id = Number(params?.id);
  const { data: analysis, isLoading, error } = trpc.analyses.get.useQuery({ id }, { enabled: Number.isFinite(id), retry: false });

  if (isLoading) return <div className="grid min-h-[55vh] place-items-center"><Loader2 className="h-7 w-7 animate-spin text-violet-600" /></div>;
  if (error) return <div role="alert" className="mx-auto mt-16 max-w-xl rounded-2xl border border-rose-100 bg-rose-50 p-6 text-center text-rose-700">Não foi possível carregar este relatório agora. Volte ao histórico e tente novamente.</div>;
  if (!analysis) return <div className="p-8 text-slate-600">Avaliação não encontrada.</div>;
  if (analysis.status === "failed") return <FailedReport />;
  if (!analysis.reportJson) return <div className="mx-auto max-w-xl pt-16 text-center"><Loader2 className="mx-auto mb-4 h-9 w-9 animate-spin text-violet-600" /><h1 className="font-display text-3xl font-extrabold text-[#2b1058]">A Platéia está lendo seu material.</h1><p className="mt-2 text-slate-600">O relatório aparecerá aqui assim que a avaliação for concluída.</p></div>;

  const report = JSON.parse(analysis.reportJson) as ReportData;
  const avgByCriterion = Object.fromEntries(criteria.map(key => [key, Math.round(report.consumers.reduce((sum, consumer) => sum + consumer.criteria[key], 0) / report.consumers.length)])) as Record<Criterion, number>;

  return <div className="mx-auto max-w-7xl pb-12">
    <Link href="/historico" className="mb-6 inline-flex items-center gap-2 rounded-md px-1 py-1 text-sm font-semibold text-violet-700 hover:text-violet-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500"><ArrowLeft className="h-4 w-4" /> Voltar ao histórico</Link>
    <section className="relative overflow-hidden rounded-[2rem] bg-[#2b1058] px-6 py-8 text-white sm:px-10">
      <div className="absolute -right-14 -top-14 h-56 w-56 rounded-full bg-[#ff6f61]/30 blur-3xl" />
      <div className="relative grid gap-8 md:grid-cols-[1fr_auto] md:items-center">
        <div>
          <Badge className="border-violet-400/25 bg-white/10 text-violet-100 hover:bg-white/10">Relatório de avaliação</Badge>
          <h1 className="mt-4 font-display text-4xl font-extrabold tracking-[-0.06em] sm:text-5xl">{analysis.product}</h1>
          <p className="mt-3 max-w-2xl text-sm leading-6 text-violet-100">{analysis.objective} · Público: {analysis.targetAudience}</p>
          {analysis.sourceUrl && <a href={analysis.sourceUrl} target="_blank" rel="noreferrer" className="mt-4 inline-flex items-center gap-2 rounded-md border border-white/20 bg-white/10 px-3 py-2 text-xs font-bold text-white transition-colors hover:bg-white/15 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white"><ExternalLink className="h-3.5 w-3.5" /> Abrir material de origem</a>}
        </div>
        <div className="flex items-center gap-4">
          <div className="score-orb" style={{ "--score": report.synthesis.overallScore } as CSSProperties}><div><strong>{report.synthesis.overallScore}</strong><span>/100</span></div></div>
          <div><p className="text-sm font-bold">Nota geral</p><p className="mt-1 text-xs text-violet-200">Leitura consolidada da Platéia</p></div>
        </div>
      </div>
    </section>
    <section className="mt-6 grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
      <div className="space-y-6">
        <div className="plateia-card p-6 sm:p-7">
          <div className="flex items-center justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Painel de critérios</p><h2 className="mt-1 font-display text-2xl font-extrabold tracking-[-0.045em] text-[#2b1058]">O que o material comunica</h2></div><span className="rounded-xl bg-violet-50 px-3 py-2 text-xs font-bold text-violet-700">Média {report.synthesis.weightedAverage}</span></div>
          <div className="mt-7 space-y-4">{criteria.map(key => <ScoreBar key={key} label={key} score={avgByCriterion[key]} />)}</div>
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
