import { BrandMark } from "@/components/BrandMark";
import { Badge } from "@/components/ui/badge";
import { trpc } from "@/lib/trpc";
import { getReportScore } from "@/lib/reportParsing";
import { ArrowRight, BarChart3, Clock3, FileCheck2, Plus, Sparkles } from "lucide-react";
import { Link } from "wouter";
import { RuntimeStatus } from "@/components/RuntimeStatus";

const statusMap = {
  completed: { label: "Concluída", className: "bg-emerald-50 text-emerald-700 border-emerald-100" },
  processing: { label: "Em avaliação", className: "bg-amber-50 text-amber-700 border-amber-100" },
  needs_content: { label: "Complemento necessário", className: "bg-amber-50 text-amber-800 border-amber-200" },
  failed: { label: "Não concluída", className: "bg-rose-50 text-rose-700 border-rose-100" },
} as const;

export default function Dashboard() {
  const { data: analyses = [], isLoading, error } = trpc.analyses.list.useQuery();
  const completed = analyses.filter(item => item.status === "completed").length;
  const processing = analyses.filter(item => item.status === "processing").length;

  return (
    <div className="mx-auto max-w-7xl space-y-8 pb-10">
      <section className="relative overflow-hidden rounded-[2rem] bg-[#2b1058] px-6 py-8 text-white shadow-[0_22px_60px_-24px_rgba(43,16,88,0.55)] sm:px-10 sm:py-10">
        <div className="absolute -right-20 -top-24 h-72 w-72 rounded-full bg-[#ff6f61]/25 blur-3xl" />
        <div className="absolute bottom-0 right-20 h-36 w-36 rounded-full border border-violet-300/20" />
        <div className="relative grid gap-8 lg:grid-cols-[1.35fr_0.65fr] lg:items-end">
          <div>
            <div className="mb-5 flex items-center gap-2 text-xs font-bold uppercase tracking-[0.18em] text-violet-200">
              <Sparkles className="h-4 w-4 text-[#ff978d]" />
              Painel de leitura
            </div>
            <h1 className="font-display max-w-xl text-4xl font-extrabold tracking-[-0.06em] sm:text-5xl">Antes de publicar, escute a sua Platéia.</h1>
            <p className="mt-4 max-w-xl text-sm leading-6 text-violet-100 sm:text-base">Envie um conteúdo e receba uma leitura estruturada de atenção, clareza, desejo, confiança e ação por cinco lentes comportamentais.</p>
            <Link href="/avaliar" className="mt-7 inline-flex h-11 items-center rounded-md bg-[#ff6f61] px-6 text-sm font-bold text-white shadow-sm transition-colors hover:bg-[#f15d50] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-offset-2 focus-visible:ring-offset-[#2b1058]">Nova avaliação <ArrowRight className="ml-2 h-4 w-4" /></Link>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-2xl border border-white/10 bg-white/10 p-4 backdrop-blur-sm"><p className="text-3xl font-extrabold">{isLoading ? "—" : analyses.length}</p><p className="mt-1 text-xs text-violet-200">materiais enviados</p></div>
            <div className="rounded-2xl border border-white/10 bg-white/10 p-4 backdrop-blur-sm"><p className="text-3xl font-extrabold">{isLoading ? "—" : completed}</p><p className="mt-1 text-xs text-violet-200">leituras concluídas</p></div>
          </div>
        </div>
      </section>

      <RuntimeStatus />

      <section className="grid gap-4 md:grid-cols-3">
        <MetricCard icon={FileCheck2} label="Avaliações concluídas" value={isLoading ? "—" : String(completed)} accent="bg-violet-100 text-violet-700" />
        <MetricCard icon={Clock3} label="Em avaliação" value={isLoading ? "—" : String(processing)} accent="bg-amber-100 text-amber-700" />
        <MetricCard icon={BarChart3} label="Lentes de análise" value="5" accent="bg-coral-100 text-[#e9594c]" />
      </section>

      <section className="plateia-card overflow-hidden">
        <div className="flex items-center justify-between px-6 pb-5 pt-6 sm:px-7">
          <div><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Histórico recente</p><h2 className="mt-1 font-display text-2xl font-extrabold tracking-[-0.045em] text-[#2b1058]">Suas últimas leituras</h2></div>
          <Link href="/historico" className="hidden items-center rounded-md px-3 py-2 text-sm font-semibold text-violet-700 transition-colors hover:bg-violet-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500 sm:inline-flex">Ver histórico <ArrowRight className="ml-1.5 h-4 w-4" /></Link>
        </div>
        {isLoading ? (
          <div role="status" aria-busy="true" className="mx-6 mb-6 rounded-2xl border border-violet-100 bg-violet-50/55 px-5 py-10 text-center text-sm text-violet-700 sm:mx-7">Carregando as leituras da sua Platéia…</div>
        ) : error ? (
          <div role="alert" className="mx-6 mb-6 rounded-2xl border border-rose-100 bg-rose-50 px-5 py-5 text-sm text-rose-700 sm:mx-7">Não foi possível carregar o histórico agora. Atualize a página para tentar novamente.</div>
        ) : analyses.length === 0 && !isLoading ? (
          <div className="mx-6 mb-6 rounded-2xl border border-dashed border-violet-200 bg-violet-50/55 px-5 py-10 text-center sm:mx-7"><div className="mx-auto mb-3 grid h-11 w-11 place-items-center rounded-2xl bg-white text-violet-600 shadow-sm"><Plus className="h-5 w-5" /></div><p className="font-semibold text-[#2b1058]">Sua Platéia está pronta para a primeira leitura.</p><p className="mx-auto mt-1 max-w-md text-sm leading-6 text-slate-500">Envie um post, carrossel, Reel ou copy e descubra o que vale reforçar antes da publicação.</p><Link href="/avaliar" className="mt-5 inline-flex h-10 items-center rounded-md bg-[#2b1058] px-4 text-sm font-semibold text-white transition-colors hover:bg-[#39166e] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500">Enviar conteúdo</Link></div>
        ) : (
          <div className="divide-y divide-violet-50 border-t border-violet-50">
            {analyses.slice(0, 5).map(item => {
              const score = getReportScore(item.reportJson);
              const status = statusMap[item.status];
              return <Link key={item.id} href={`/analises/${item.id}`}><div className="group flex cursor-pointer items-center gap-4 px-6 py-4 transition-colors hover:bg-violet-50/50 sm:px-7"><div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[#f3efff] text-sm font-extrabold text-violet-700">{item.contentType.slice(0, 1).toUpperCase()}</div><div className="min-w-0 flex-1"><p className="truncate font-semibold text-[#2b1058]">{item.product || `Avaliação de ${item.contentType}`}</p><p className="mt-0.5 text-xs text-slate-500">{item.contentType} · {new Date(item.createdAt).toLocaleDateString("pt-BR")}</p></div><Badge variant="outline" className={status.className}>{status.label}</Badge>{score !== null && <div className="hidden h-9 min-w-9 place-items-center rounded-full bg-[#2b1058] px-2 text-sm font-extrabold text-white sm:grid">{score}</div>}<ArrowRight className="h-4 w-4 text-slate-300 transition-transform group-hover:translate-x-1 group-hover:text-violet-600" /></div></Link>;
            })}
          </div>
        )}
      </section>
    </div>
  );
}

function MetricCard({ icon: Icon, label, value, accent }: { icon: typeof FileCheck2; label: string; value: string; accent: string }) {
  return <div className="plateia-card p-5"><div className={`mb-5 grid h-10 w-10 place-items-center rounded-xl ${accent}`}><Icon className="h-5 w-5" /></div><p className="font-display text-3xl font-extrabold tracking-[-0.06em] text-[#2b1058]">{value}</p><p className="mt-1 text-sm text-slate-500">{label}</p></div>;
}
