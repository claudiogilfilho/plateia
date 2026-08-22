import { Badge } from "@/components/ui/badge";
import { trpc } from "@/lib/trpc";
import { ArrowRight, Clock3, Plus } from "lucide-react";
import React from "react";
import { Link } from "wouter";

const statusMap = { completed: { label: "Concluída", className: "bg-emerald-50 text-emerald-700 border-emerald-100" }, processing: { label: "Em avaliação", className: "bg-amber-50 text-amber-700 border-amber-100" }, needs_content: { label: "Complemento necessário", className: "bg-amber-50 text-amber-800 border-amber-200" }, failed: { label: "Não concluída", className: "bg-rose-50 text-rose-700 border-rose-100" } } as const;

export function getReportScore(reportJson: string | null) {
  if (!reportJson) return null;
  try {
    const score = JSON.parse(reportJson)?.synthesis?.overallScore;
    return typeof score === "number" && Number.isFinite(score) ? score : null;
  } catch {
    return null;
  }
}

export default function History() {
  const { data: analyses = [], isLoading, error } = trpc.analyses.list.useQuery();
  return <div className="mx-auto max-w-6xl pb-10"><div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Biblioteca</p><h1 className="mt-1 font-display text-4xl font-extrabold tracking-[-0.06em] text-[#2b1058]">Histórico de avaliações</h1><p className="mt-2 text-sm text-slate-600">Consulte materiais enviados e retome qualquer relatório quando precisar.</p></div><Link href="/avaliar" className="inline-flex h-10 items-center rounded-md bg-[#2b1058] px-4 text-sm font-semibold text-white transition-colors hover:bg-[#39166e] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500"><Plus className="mr-2 h-4 w-4" />Nova avaliação</Link></div><div className="plateia-card overflow-hidden">{error ? <div role="alert" className="p-8 text-sm text-rose-700">Não foi possível carregar o histórico agora. Atualize a página para tentar novamente.</div> : isLoading ? <div role="status" aria-busy="true" className="p-8 text-sm text-slate-500">Carregando histórico…</div> : analyses.length === 0 ? <div className="p-12 text-center"><Clock3 className="mx-auto mb-3 h-8 w-8 text-violet-300" /><p className="font-semibold text-[#2b1058]">Ainda não há avaliações.</p><p className="mt-1 text-sm text-slate-500">A sua biblioteca vai nascer após a primeira leitura.</p></div> : <><div className="hidden grid-cols-[minmax(0,1.1fr)_0.8fr_auto] gap-4 border-b border-violet-50 px-7 py-3 text-[11px] font-bold uppercase tracking-[0.12em] text-slate-400 sm:grid"><span>Material</span><span>Data</span><span>Status</span></div><div className="divide-y divide-violet-50">{analyses.map(item => <HistoryEntry key={item.id} item={item} />)}</div></>}</div></div>;
}

function HistoryEntry({ item }: { item: { id: number; status: keyof typeof statusMap; product: string | null; contentType: string; createdAt: Date; reportJson: string | null } }) {
  const status = statusMap[item.status];
  const score = getReportScore(item.reportJson);
  const title = item.product || `Avaliação de ${item.contentType}`;
  const date = new Date(item.createdAt).toLocaleDateString("pt-BR");
  return <Link href={`/analises/${item.id}`}><article className="group cursor-pointer px-5 py-4 transition-colors hover:bg-violet-50/45 sm:grid sm:grid-cols-[minmax(0,1.1fr)_0.8fr_auto] sm:items-center sm:gap-4 sm:px-7 sm:py-5"><div className="min-w-0"><p className="truncate font-semibold text-[#2b1058]">{title}</p><p className="mt-0.5 text-xs capitalize text-slate-500">{item.contentType}</p></div><div className="mt-3 flex items-center justify-between gap-3 sm:mt-0 sm:contents"><span className="text-xs text-slate-500 sm:text-sm">{date}</span><div className="flex min-w-0 items-center gap-2"><Badge variant="outline" className={`max-w-[calc(100vw-10rem)] truncate ${status.className}`}>{status.label}</Badge>{score !== null && <span className="text-sm font-extrabold text-[#2b1058]">{score}</span>}<ArrowRight className="h-4 w-4 shrink-0 text-slate-300 group-hover:text-violet-600" /></div></div></article></Link>;
}
