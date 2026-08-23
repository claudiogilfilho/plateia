import { useAuth } from "@/_core/hooks/useAuth";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { trpc } from "@/lib/trpc";
import { AlertCircle, BrainCircuit, CheckCircle2, ExternalLink, FileText, Image, Layers3, Loader2, UploadCloud, Video } from "lucide-react";
import { type ChangeEvent, type FormEvent, useState } from "react";

const contentTypes = [
  { value: "reel", label: "Reel", icon: Video },
  { value: "post", label: "Post", icon: Image },
  { value: "carrossel", label: "Carrossel", icon: Layers3 },
  { value: "copy", label: "Copy", icon: FileText },
] as const;

type ContentType = (typeof contentTypes)[number]["value"];
type SourceMode = "upload" | "link" | "copy";
type MediaInput = { fileName: string; mimeType: "image/jpeg" | "image/png" | "image/webp" | "video/mp4"; base64: string };
type Classification = { materialFormat?: string; presentationFormats?: string[]; primaryFamily?: string; objectives?: string[]; segment?: string; confidence?: string; needsHumanReview?: boolean };

function parseClassification(value: string | null): Classification | null {
  if (!value) return null;
  try {
    const parsed = JSON.parse(value) as unknown;
    return parsed && typeof parsed === "object" && !Array.isArray(parsed) ? parsed as Classification : null;
  } catch {
    return null;
  }
}

function humanize(value?: string) {
  return value ? value.replaceAll("_", " ") : "Ainda não classificado";
}

export default function Observatory() {
  const { user } = useAuth();
  const utils = trpc.useUtils();
  const { data: references = [], isLoading, error } = trpc.observatory.list.useQuery(undefined, { enabled: user?.role === "admin", retry: false });
  const { data: providerStatus } = trpc.observatory.providerStatus.useQuery(undefined, { enabled: user?.role === "admin", retry: false });
  const [contentType, setContentType] = useState<ContentType>("reel");
  const [sourceMode, setSourceMode] = useState<SourceMode>("link");
  const [title, setTitle] = useState("");
  const [creator, setCreator] = useState("");
  const [contentText, setContentText] = useState("");
  const [sourceUrl, setSourceUrl] = useState("");
  const [linkKind, setLinkKind] = useState<"published_post" | "direct_media">("published_post");
  const [remoteMimeType, setRemoteMimeType] = useState<MediaInput["mimeType"]>("video/mp4");
  const [segmentHint, setSegmentHint] = useState("");
  const [objectiveHint, setObjectiveHint] = useState("");
  const [views, setViews] = useState("");
  const [comments, setComments] = useState("");
  const [media, setMedia] = useState<MediaInput | null>(null);
  const [formError, setFormError] = useState("");
  const create = trpc.observatory.create.useMutation({
    onSuccess: async () => {
      await utils.observatory.list.invalidate();
      setTitle(""); setCreator(""); setContentText(""); setSourceUrl(""); setMedia(null); setViews(""); setComments("");
    },
  });

  if (user?.role !== "admin") return <div role="alert" className="mx-auto max-w-xl rounded-2xl border border-amber-200 bg-amber-50 p-6 text-sm leading-6 text-amber-900"><strong>Área interna.</strong> O Observatório é acessível apenas à equipe administradora da Platéia.</div>;

  const changeType = (next: ContentType) => {
    setContentType(next);
    setSourceMode(next === "copy" ? "copy" : sourceMode === "copy" ? "link" : sourceMode);
    setFormError("");
  };
  const onFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setFormError("");
    if (!file) return;
    if (!/^(image\/(jpeg|png|webp)|video\/mp4)$/.test(file.type)) return setFormError("Use JPG, PNG, WEBP ou MP4.");
    if (file.size > 12 * 1024 * 1024) return setFormError("O arquivo deve ter até 12 MB.");
    const reader = new FileReader();
    reader.onload = () => setMedia({ fileName: file.name, mimeType: file.type as MediaInput["mimeType"], base64: String(reader.result) });
    reader.readAsDataURL(file);
  };
  const submit = (event: FormEvent) => {
    event.preventDefault();
    setFormError("");
    if (contentType === "copy" && !contentText.trim()) return setFormError("Cole a copy que será ensinada ao Observatório.");
    if (contentType !== "copy" && sourceMode === "upload" && !media) return setFormError("Selecione o arquivo público de referência.");
    if (contentType !== "copy" && sourceMode === "link" && !sourceUrl.trim()) return setFormError("Informe o link público da referência.");
    create.mutate({
      title, creator, contentType, contentText, segmentHint, objectiveHint,
      ...(views || comments ? { metrics: { ...(views ? { views } : {}), ...(comments ? { comments } : {}) } } : {}),
      ...(sourceMode === "upload" && media ? { media } : {}),
      ...(sourceMode === "link" ? { source: { url: sourceUrl.trim(), kind: linkKind, ...(linkKind === "direct_media" ? { mimeType: remoteMimeType } : {}) } } : {}),
    });
  };

  return <div className="mx-auto max-w-7xl pb-12">
    <section className="overflow-hidden rounded-[2rem] bg-[#2b1058] px-7 py-8 text-white sm:px-10">
      <div className="flex items-start gap-4"><div className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-white/10 text-[#ff978d]"><BrainCircuit className="h-6 w-6" /></div><div><div className="flex flex-wrap gap-2"><Badge className="border-white/15 bg-white/10 text-violet-100 hover:bg-white/10">Uso interno · Prompt v2.0</Badge>{providerStatus && <Badge className="border-white/15 bg-white/10 text-violet-100 hover:bg-white/10">IA: {providerStatus.provider}</Badge>}</div><h1 className="mt-3 font-display text-4xl font-extrabold tracking-[-0.055em]">Observatório Platéia</h1><p className="mt-3 max-w-3xl text-sm leading-6 text-violet-100">Ensine por exemplos públicos com procedência. Cada material é classificado automaticamente e comparado apenas com referências estruturalmente semelhantes.</p></div></div>
    </section>

    <div className="mt-6 grid gap-6 xl:grid-cols-[0.92fr_1.08fr]">
      <form onSubmit={submit} className="plateia-card space-y-5 p-6 sm:p-7">
        <div><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Nova referência</p><h2 className="mt-1 font-display text-2xl font-extrabold text-[#2b1058]">Adicionar material exemplar</h2></div>
        <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">{contentTypes.map(item => { const Icon = item.icon; const active = item.value === contentType; return <button key={item.value} type="button" aria-pressed={active} onClick={() => changeType(item.value)} className={`rounded-xl border p-3 text-left ${active ? "border-violet-500 bg-violet-50" : "border-violet-100"}`}><Icon className={`mb-2 h-4 w-4 ${active ? "text-violet-700" : "text-slate-400"}`} /><span className="text-xs font-bold text-[#2b1058]">{item.label}</span></button>; })}</div>
        <div className="grid gap-4 sm:grid-cols-2"><div><Label htmlFor="obs-title">Título interno</Label><Input id="obs-title" value={title} onChange={event => setTitle(event.target.value)} placeholder="Ex.: Gancho de curiosidade" className="mt-2" /></div><div><Label htmlFor="obs-creator">Perfil ou criador</Label><Input id="obs-creator" value={creator} onChange={event => setCreator(event.target.value)} placeholder="Ex.: @perfil" className="mt-2" /></div></div>
        {contentType !== "copy" && <div><Label>Origem do material</Label><div className="mt-2 grid grid-cols-2 gap-2"><button type="button" onClick={() => setSourceMode("link")} className={`rounded-xl border p-3 text-sm font-bold ${sourceMode === "link" ? "border-violet-500 bg-violet-50 text-violet-800" : "border-violet-100 text-slate-600"}`}>Link público</button><button type="button" onClick={() => setSourceMode("upload")} className={`rounded-xl border p-3 text-sm font-bold ${sourceMode === "upload" ? "border-violet-500 bg-violet-50 text-violet-800" : "border-violet-100 text-slate-600"}`}>Enviar arquivo</button></div></div>}
        {contentType !== "copy" && sourceMode === "link" && <div className="space-y-3 rounded-2xl bg-violet-50/55 p-4"><div><Label htmlFor="obs-url">URL pública</Label><Input id="obs-url" type="url" value={sourceUrl} onChange={event => setSourceUrl(event.target.value)} placeholder="https://…" className="mt-2 bg-white" /></div><div className="grid gap-3 sm:grid-cols-2"><select aria-label="Tipo do link" value={linkKind} onChange={event => setLinkKind(event.target.value as typeof linkKind)} className="h-10 rounded-md border border-violet-100 bg-white px-3 text-sm"><option value="published_post">Publicação do Instagram</option><option value="direct_media">Link direto da mídia</option></select>{linkKind === "direct_media" && <select aria-label="Formato da mídia" value={remoteMimeType} onChange={event => setRemoteMimeType(event.target.value as MediaInput["mimeType"])} className="h-10 rounded-md border border-violet-100 bg-white px-3 text-sm"><option value="video/mp4">Vídeo MP4</option><option value="image/jpeg">Imagem JPG</option><option value="image/png">Imagem PNG</option><option value="image/webp">Imagem WEBP</option></select>}</div></div>}
        {contentType !== "copy" && sourceMode === "upload" && <label className="flex min-h-28 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-violet-200 bg-violet-50/35 p-4 text-center"><UploadCloud className="mb-2 h-6 w-6 text-violet-600" /><span className="text-sm font-bold text-[#2b1058]">{media?.fileName || "Selecionar mídia"}</span><span className="mt-1 text-xs text-slate-500">JPG, PNG, WEBP ou MP4 · até 12 MB</span><input type="file" className="sr-only" accept="image/jpeg,image/png,image/webp,video/mp4" onChange={onFile} /></label>}
        <div><Label htmlFor="obs-text">{contentType === "copy" ? "Copy" : "Legenda, roteiro ou transcrição"}</Label><Textarea id="obs-text" value={contentText} onChange={event => setContentText(event.target.value)} placeholder={contentType === "copy" ? "Cole o texto completo." : "Opcional, mas melhora a leitura multimodal."} className="mt-2 min-h-28" /></div>
        <div className="grid gap-4 sm:grid-cols-2"><div><Label htmlFor="obs-segment">Segmento sugerido</Label><Input id="obs-segment" value={segmentHint} onChange={event => setSegmentHint(event.target.value)} placeholder="Ex.: estética" className="mt-2" /></div><div><Label htmlFor="obs-objective">Objetivo sugerido</Label><Input id="obs-objective" value={objectiveHint} onChange={event => setObjectiveHint(event.target.value)} placeholder="Ex.: autoridade" className="mt-2" /></div></div>
        <div className="grid gap-4 sm:grid-cols-2"><div><Label htmlFor="obs-views">Visualizações observadas</Label><Input id="obs-views" inputMode="numeric" value={views} onChange={event => setViews(event.target.value)} placeholder="Opcional" className="mt-2" /></div><div><Label htmlFor="obs-comments">Comentários observados</Label><Input id="obs-comments" inputMode="numeric" value={comments} onChange={event => setComments(event.target.value)} placeholder="Opcional" className="mt-2" /></div></div>
        <p className="text-xs leading-5 text-slate-500">Métricas são contexto observado, não prova isolada de causa. O sistema registra limitações e explicações alternativas.</p>
        {formError && <p role="alert" className="flex items-center gap-2 text-sm text-rose-700"><AlertCircle className="h-4 w-4" />{formError}</p>}
        {create.error && <p role="alert" className="rounded-xl bg-rose-50 p-3 text-sm text-rose-700">{create.error.message}</p>}
        {create.isSuccess && <p role="status" className="flex items-center gap-2 rounded-xl bg-emerald-50 p-3 text-sm text-emerald-700"><CheckCircle2 className="h-4 w-4" />Referência classificada e incorporada à memória.</p>}
        <Button type="submit" disabled={create.isPending} className="h-11 w-full bg-[#ff6f61] font-bold text-white hover:bg-[#ee5e51]">{create.isPending ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Analisando referência…</> : "Ensinar ao Observatório"}</Button>
      </form>

      <section className="plateia-card overflow-hidden">
        <div className="border-b border-violet-50 px-6 py-5"><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">Memória curada</p><h2 className="mt-1 font-display text-2xl font-extrabold text-[#2b1058]">Referências aprendidas</h2></div>
        {isLoading ? <div className="grid min-h-52 place-items-center"><Loader2 className="h-6 w-6 animate-spin text-violet-600" /></div> : error ? <p role="alert" className="p-6 text-sm text-rose-700">Não foi possível carregar o Observatório.</p> : references.length === 0 ? <div className="p-10 text-center text-sm text-slate-500">A memória ainda está vazia. Adicione a primeira referência exemplar.</div> : <div className="divide-y divide-violet-50">{references.map(reference => {
          const classification = parseClassification(reference.classificationJson);
          return <article key={reference.id} className="p-5 sm:p-6"><div className="flex items-start justify-between gap-4"><div className="min-w-0"><div className="flex flex-wrap items-center gap-2"><h3 className="truncate font-bold text-[#2b1058]">{reference.title}</h3><Badge variant="outline" className={reference.status === "analyzed" ? "border-emerald-200 bg-emerald-50 text-emerald-700" : reference.status === "failed" ? "border-rose-200 bg-rose-50 text-rose-700" : "border-amber-200 bg-amber-50 text-amber-700"}>{reference.status === "analyzed" ? "Aprendida" : reference.status === "needs_content" ? "Precisa do arquivo" : reference.status === "failed" ? "Falhou" : "Processando"}</Badge></div><p className="mt-1 text-xs text-slate-500">{reference.creator || "Criador não informado"} · {new Date(reference.createdAt).toLocaleDateString("pt-BR")}</p></div>{reference.sourceUrl && <a href={reference.sourceUrl} target="_blank" rel="noreferrer" aria-label="Abrir referência pública" className="rounded-lg p-2 text-violet-600 hover:bg-violet-50"><ExternalLink className="h-4 w-4" /></a>}</div>{classification && <div className="mt-4 flex flex-wrap gap-2"><span className="rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700">{humanize(classification.primaryFamily)}</span><span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">{humanize(classification.materialFormat)}</span><span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600">{classification.segment || "segmento indeterminado"}</span></div>}{classification?.objectives?.length ? <p className="mt-3 text-xs leading-5 text-slate-600"><strong>Objetivos:</strong> {classification.objectives.map(humanize).join(", ")}</p> : null}{classification?.needsHumanReview && <p className="mt-2 text-xs font-semibold text-amber-700">Classificação marcada para revisão humana.</p>}</article>;
        })}</div>}
      </section>
    </div>
  </div>;
}
