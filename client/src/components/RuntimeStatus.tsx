import { Badge } from "@/components/ui/badge";
import { trpc } from "@/lib/trpc";
import { BrainCircuit, Database, ShieldCheck } from "lucide-react";
import React from "react";

export function useMvpStatus() {
  return trpc.system.mvpStatus.useQuery(undefined, { retry: false, refetchOnWindowFocus: false });
}

export function RuntimeStatus({ compact = false }: { compact?: boolean }) {
  const { data, isLoading } = useMvpStatus();
  if (isLoading || !data) return null;

  const ready = data.ready;
  return (
    <div className={`rounded-2xl border ${ready ? "border-emerald-100 bg-emerald-50/70" : "border-amber-200 bg-amber-50"} ${compact ? "p-4" : "p-5"}`} role={ready ? "status" : "alert"}>
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <div className={`grid h-9 w-9 shrink-0 place-items-center rounded-xl ${ready ? "bg-emerald-100 text-emerald-700" : "bg-amber-100 text-amber-700"}`}>
            <BrainCircuit className="h-4 w-4" />
          </div>
          <div>
            <p className="text-sm font-bold text-[#2b1058]">{ready ? "Platéia pronta para avaliar" : "Motor de IA ainda não conectado"}</p>
            <p className="mt-1 text-xs leading-5 text-slate-600">{data.ai.message}</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 pl-12 sm:pl-0">
          <Badge variant="outline" className="border-white bg-white/80 text-slate-600"><ShieldCheck className="mr-1 h-3 w-3" />{data.auth === "guest" ? "Acesso MVP" : "Conta protegida"}</Badge>
          <Badge variant="outline" className="border-white bg-white/80 text-slate-600"><Database className="mr-1 h-3 w-3" />{data.persistence === "memory" ? "Histórico temporário" : "Histórico persistente"}</Badge>
        </div>
      </div>
      {!ready && !compact && <p className="mt-3 border-t border-amber-200/70 pt-3 text-xs leading-5 text-amber-800">O aplicativo não produzirá notas fictícias. O administrador precisa configurar um dos adaptadores portáteis antes do primeiro teste.</p>}
    </div>
  );
}
