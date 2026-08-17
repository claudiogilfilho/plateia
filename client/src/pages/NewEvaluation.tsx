import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { trpc } from "@/lib/trpc";
import { AlertCircle, ArrowLeft, FileText, Image, Instagram, Layers3, Link2, Loader2, UploadCloud, Video } from "lucide-react";
import { ChangeEvent, FormEvent, useState } from "react";
import { useLocation } from "wouter";

const types = [
  { value: "post", label: "Post", description: "Imagem única", icon: Image },
  { value: "carrossel", label: "Carrossel", description: "Sequência visual", icon: Layers3 },
  { value: "reel", label: "Reel", description: "Vídeo curto", icon: Video },
  { value: "copy", label: "Copy", description: "Texto e legenda", icon: FileText },
] as const;

type ContentType = (typeof types)[number]["value"];
type MediaInput = { fileName: string; mimeType: string; base64: string; preview: string };
type SourceMode = "upload" | "link";
type LinkKind = "direct_media" | "published_post";

export default function NewEvaluation() {
  const [, setLocation] = useLocation();
  const query = new URLSearchParams(window.location.search);
  const textOnlyComplement = query.get("complemento") === "legenda";
  const initialType = query.get("tipo");
  const [contentType, setContentType] = useState<ContentType>(() => types.some(type => type.value === initialType) ? initialType as ContentType : "post");
  const [contentText, setContentText] = useState("");
  const [product, setProduct] = useState("");
  const [objective, setObjective] = useState("");
  const [targetAudience, setTargetAudience] = useState("");
  const [media, setMedia] = useState<MediaInput | null>(null);
  const [sourceMode, setSourceMode] = useState<SourceMode>(() => textOnlyComplement || query.get("envio") === "link" ? "link" : "upload");
  const [sourceUrl, setSourceUrl] = useState(() => query.get("link") ?? "");
  const [linkKind, setLinkKind] = useState<LinkKind>(() => query.get("tipo-link") === "midia-direta" ? "direct_media" : "published_post");
  const [remoteMimeType, setRemoteMimeType] = useState<"image/jpeg" | "image/png" | "image/webp" | "video/mp4">("video/mp4");
  const [skipCaption, setSkipCaption] = useState(() => query.get("sem-legenda") === "1");
  const [materialError, setMaterialError] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const create = trpc.analyses.create.useMutation({
    onMutate: () => setSubmitted(true),
    onSuccess: ({ id }) => setLocation(`/analises/${id}`),
    onError: () => setSubmitted(false),
  });

  const onFile = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    setMaterialError("");
    if (!file) return;
    if (!/^(image\/(jpeg|png|webp)|video\/mp4)$/.test(file.type)) return setMaterialError("Use JPG, PNG, WEBP ou MP4.");
    if (file.size > 12 * 1024 * 1024) return setMaterialError("Nesta versão inicial, o arquivo deve ter até 12 MB.");
    const reader = new FileReader();
    reader.onload = () => setMedia({ fileName: file.name, mimeType: file.type, base64: String(reader.result), preview: URL.createObjectURL(file) });
    reader.readAsDataURL(file);
  };

  const changeType = (type: ContentType) => {
    if (textOnlyComplement) return;
    setContentType(type);
    setMaterialError("");
  };
  const chooseSource = (mode: SourceMode) => {
    setSourceMode(mode);
    setMaterialError("");
    if (mode === "link") setMedia(null);
  };
  const submit = (event: FormEvent) => {
    event.preventDefault();
    if ((contentType === "copy" || textOnlyComplement) && !contentText.trim()) return setMaterialError("Cole a legenda ou a copy para continuar.");
    if (!textOnlyComplement && contentType !== "copy" && sourceMode === "upload" && !media) return setMaterialError("Para post, carrossel ou Reel, envie a imagem ou o vídeo do material.");
    if (sourceMode === "link") {
      try {
        const parsed = new URL(sourceUrl);
        if (parsed.protocol !== "https:") throw new Error();
      } catch {
        return setMaterialError("Informe um link HTTPS público e completo.");
      }
    }
    create.mutate({
      contentType,
      contentText,
      product,
      objective,
      targetAudience,
      skipCaption,
      ...(sourceMode === "upload" && media ? { media: { fileName: media.fileName, mimeType: media.mimeType, base64: media.base64 } } : {}),
      ...(sourceMode === "link" ? { source: { url: sourceUrl.trim(), kind: linkKind, ...(linkKind === "direct_media" ? { mimeType: remoteMimeType } : {}) } } : {}),
    });
  };

  const materialInstruction = textOnlyComplement
    ? "O Instagram não disponibilizou capa nem legenda pública para este link. Cole somente a legenda ou a copy para receber uma leitura textual do conteúdo."
    : contentType === "copy"
      ? "Para uma copy, cole o texto no campo ao lado. Os demais campos são opcionais."
      : "Para post, carrossel ou Reel, a imagem, o vídeo ou um link público do material é obrigatório. Os demais campos são opcionais.";

  return <div className="mx-auto max-w-5xl pb-10">
    <button onClick={() => setLocation("/app")} className="mb-6 inline-flex items-center gap-2 rounded-md px-1 py-1 text-sm font-semibold text-violet-700 hover:text-violet-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-violet-500"><ArrowLeft className="h-4 w-4" /> Voltar ao painel</button>
    <div className="mb-8"><p className="text-xs font-bold uppercase tracking-[0.16em] text-violet-500">{textOnlyComplement ? "Complemento de leitura" : "Nova leitura"}</p><h1 className="mt-1 font-display text-4xl font-extrabold tracking-[-0.06em] text-[#2b1058]">{textOnlyComplement ? "Falta só a legenda." : "Entregue o material à sua Platéia."}</h1><p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">{materialInstruction}</p></div>
    <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
      <section className="space-y-6">
        {!textOnlyComplement && <div className="plateia-card p-6"><Label className="mb-3 block text-sm font-bold text-[#2b1058]">Tipo de conteúdo</Label><div className="grid grid-cols-2 gap-3">{types.map(type => { const Icon = type.icon; const active = type.value === contentType; return <button aria-pressed={active} type="button" key={type.value} onClick={() => changeType(type.value)} className={`rounded-2xl border p-3 text-left transition-all ${active ? "border-violet-500 bg-violet-50 shadow-sm" : "border-violet-100 bg-white hover:border-violet-300"}`}><Icon className={`mb-3 h-5 w-5 ${active ? "text-violet-700" : "text-slate-400"}`} /><p className="text-sm font-bold text-[#2b1058]">{type.label}</p><p className="mt-0.5 text-xs text-slate-500">{type.description}</p></button>; })}</div></div>}
        {textOnlyComplement ? <div className="rounded-2xl border border-amber-200 bg-amber-50 p-5"><div className="flex gap-3"><Instagram className="mt-0.5 h-5 w-5 shrink-0 text-amber-700" /><div><p className="text-sm font-bold text-amber-950">Link preservado</p><p className="mt-1 break-all text-xs leading-5 text-amber-900">{sourceUrl}</p><p className="mt-3 text-xs leading-5 text-amber-900">Neste passo, a Platéia solicitará somente o texto da legenda ou a copy. O material visual não é exigido.</p></div></div></div> : contentType !== "copy" && <VisualSourcePanel sourceMode={sourceMode} chooseSource={chooseSource} media={media} setMedia={setMedia} onFile={onFile} sourceUrl={sourceUrl} setSourceUrl={setSourceUrl} linkKind={linkKind} setLinkKind={setLinkKind} remoteMimeType={remoteMimeType} setRemoteMimeType={setRemoteMimeType} skipCaption={skipCaption} setSkipCaption={setSkipCaption} />}
        {materialError && <p role="alert" className="flex items-center gap-1.5 text-xs font-medium text-rose-600"><AlertCircle className="h-3.5 w-3.5" />{materialError}</p>}
      </section>
      <section className="space-y-6">
        {!textOnlyComplement && <div className="plateia-card p-6"><p className="mb-4 text-xs font-semibold leading-5 text-slate-500">Contexto opcional: quanto mais informação você fornecer, mais específica poderá ser a leitura.</p><ContextFields product={product} setProduct={setProduct} objective={objective} setObjective={setObjective} targetAudience={targetAudience} setTargetAudience={setTargetAudience} /></div>}
        {skipCaption && !textOnlyComplement ? <div className="rounded-2xl border border-violet-200 bg-violet-50 p-5"><p className="text-sm font-bold text-[#2b1058]">Leitura somente visual</p><p className="mt-1 text-xs leading-5 text-slate-600">A Platéia ignorará a legenda e não pontuará clareza textual, ação ou objeções ligadas à copy.</p></div> : <div className="plateia-card p-6"><Label htmlFor="content">Texto ou legenda {(contentType === "copy" || textOnlyComplement) ? <span className="text-rose-600">(obrigatório)</span> : <span className="font-normal text-slate-400">(opcional)</span>}</Label><Textarea id="content" value={contentText} onChange={event => { setContentText(event.target.value); setMaterialError(""); }} placeholder={textOnlyComplement ? "Cole a legenda ou a copy do post." : contentType === "copy" ? "Cole a copy que deseja avaliar." : "Cole o texto, roteiro ou legenda, se houver."} className="mt-2 min-h-44 border-violet-100 focus-visible:ring-violet-500" /></div>}
        <div className="rounded-2xl border border-[#ffdbd7] bg-[#fff7f5] p-4"><div className="flex gap-3"><Instagram className="mt-0.5 h-5 w-5 shrink-0 text-[#f15d50]" /><p className="text-xs leading-5 text-slate-600">A Platéia usa cinco lentes comportamentais para encontrar pontos fortes, riscos e recomendações de criação. A leitura é uma ferramenta de decisão, não uma previsão de resultado de mídia.</p></div></div>
        <Button type="submit" disabled={create.isPending} className="h-12 w-full bg-[#ff6f61] text-base font-bold text-white shadow-[0_12px_24px_-12px_rgba(255,111,97,0.75)] hover:bg-[#ee5e51]">{create.isPending ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" /> Sua Platéia está lendo…</> : <>{textOnlyComplement ? "Avaliar legenda" : "Iniciar avaliação"} <SparklesIcon /></>}</Button>
        {submitted && create.isPending && <p role="status" className="rounded-xl bg-violet-50 px-3 py-2 text-sm text-violet-700">Material recebido. A Platéia está preparando seu relatório.</p>}
        {create.error && <p role="alert" className="rounded-xl bg-rose-50 px-3 py-2 text-sm text-rose-700">{create.error.message}</p>}
      </section>
    </form>
  </div>;
}

function ContextFields({ product, setProduct, objective, setObjective, targetAudience, setTargetAudience }: { product: string; setProduct: (value: string) => void; objective: string; setObjective: (value: string) => void; targetAudience: string; setTargetAudience: (value: string) => void }) {
  return <div className="space-y-4"><div><Label htmlFor="product">Produto relacionado <span className="font-normal text-slate-400">(opcional)</span></Label><Input id="product" value={product} onChange={event => setProduct(event.target.value)} placeholder="Ex.: Consultoria de posicionamento" className="mt-2 h-11 border-violet-100 focus-visible:ring-violet-500" /></div><div><Label htmlFor="objective">Objetivo da publicação <span className="font-normal text-slate-400">(opcional)</span></Label><Input id="objective" value={objective} onChange={event => setObjective(event.target.value)} placeholder="Ex.: Gerar conversas qualificadas" className="mt-2 h-11 border-violet-100 focus-visible:ring-violet-500" /></div><div><Label htmlFor="audience">Público-alvo <span className="font-normal text-slate-400">(opcional)</span></Label><Textarea id="audience" value={targetAudience} onChange={event => setTargetAudience(event.target.value)} placeholder="Quem você deseja alcançar, quais dores ou desejos esse público tem?" className="mt-2 min-h-24 border-violet-100 focus-visible:ring-violet-500" /></div></div>;
}

function VisualSourcePanel({ sourceMode, chooseSource, media, setMedia, onFile, sourceUrl, setSourceUrl, linkKind, setLinkKind, remoteMimeType, setRemoteMimeType, skipCaption, setSkipCaption }: { sourceMode: SourceMode; chooseSource: (mode: SourceMode) => void; media: MediaInput | null; setMedia: (media: MediaInput | null) => void; onFile: (event: ChangeEvent<HTMLInputElement>) => void; sourceUrl: string; setSourceUrl: (value: string) => void; linkKind: LinkKind; setLinkKind: (value: LinkKind) => void; remoteMimeType: "image/jpeg" | "image/png" | "image/webp" | "video/mp4"; setRemoteMimeType: (value: "image/jpeg" | "image/png" | "image/webp" | "video/mp4") => void; skipCaption: boolean; setSkipCaption: (value: boolean) => void }) {
  return <div className="plateia-card p-6"><Label className="mb-3 block text-sm font-bold text-[#2b1058]">Material visual <span className="text-rose-600">(obrigatório)</span></Label><div className="grid grid-cols-2 gap-3"><button type="button" aria-pressed={sourceMode === "upload"} onClick={() => chooseSource("upload")} className={`rounded-2xl border p-3 text-left transition-all ${sourceMode === "upload" ? "border-violet-500 bg-violet-50 shadow-sm" : "border-violet-100 bg-white hover:border-violet-300"}`}><UploadCloud className={`mb-2 h-5 w-5 ${sourceMode === "upload" ? "text-violet-700" : "text-slate-400"}`} /><p className="text-sm font-bold text-[#2b1058]">Enviar arquivo</p><p className="mt-0.5 text-xs text-slate-500">Imagem ou vídeo do dispositivo</p></button><button type="button" aria-pressed={sourceMode === "link"} onClick={() => chooseSource("link")} className={`rounded-2xl border p-3 text-left transition-all ${sourceMode === "link" ? "border-violet-500 bg-violet-50 shadow-sm" : "border-violet-100 bg-white hover:border-violet-300"}`}><Link2 className={`mb-2 h-5 w-5 ${sourceMode === "link" ? "text-violet-700" : "text-slate-400"}`} /><p className="text-sm font-bold text-[#2b1058]">Usar link público</p><p className="mt-0.5 text-xs text-slate-500">Instagram ou arquivo em nuvem</p></button></div>{sourceMode === "upload" ? <div className="mt-4">{media ? <div className="flex items-center gap-3 rounded-2xl border border-violet-100 bg-violet-50/50 p-3">{media.mimeType.startsWith("image/") ? <img src={media.preview} alt="Prévia enviada" className="h-12 w-12 rounded-xl object-cover" /> : <div className="grid h-12 w-12 place-items-center rounded-xl bg-[#2b1058] text-white"><Video className="h-5 w-5" /></div>}<div className="min-w-0 flex-1"><p className="truncate text-sm font-semibold text-[#2b1058]">{media.fileName}</p><p className="text-xs text-slate-500">Pronto para leitura</p></div><button type="button" onClick={() => setMedia(null)} className="rounded-md px-1 py-1 text-xs font-bold text-rose-600 hover:text-rose-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-rose-500">Remover</button></div> : <label className="flex min-h-36 cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-violet-200 bg-violet-50/35 px-4 text-center transition-colors hover:border-violet-400 hover:bg-violet-50"><UploadCloud className="mb-3 h-7 w-7 text-violet-600" /><p className="text-sm font-bold text-[#2b1058]">Envie a imagem ou o vídeo</p><p className="mt-1 text-xs text-slate-500">JPG, PNG, WEBP ou MP4 · até 12 MB</p><input aria-label="Selecionar arquivo de mídia" type="file" className="sr-only" accept="image/jpeg,image/png,image/webp,video/mp4" onChange={onFile} /></label>}</div> : <div className="mt-4 space-y-3 rounded-2xl border border-violet-100 bg-violet-50/35 p-4"><div><Label htmlFor="sourceUrl">Link público do material</Label><Input id="sourceUrl" type="url" required value={sourceUrl} onChange={event => setSourceUrl(event.target.value)} placeholder="https://…" className="mt-2 h-11 border-violet-100 bg-white focus-visible:ring-violet-500" /></div><div><Label htmlFor="linkKind">Tipo de link</Label><select id="linkKind" value={linkKind} onChange={event => { const nextKind = event.target.value as LinkKind; setLinkKind(nextKind); if (nextKind !== "published_post") setSkipCaption(false); }} className="mt-2 h-11 w-full rounded-md border border-violet-100 bg-white px-3 text-sm text-[#2b1058] outline-none focus:ring-2 focus:ring-violet-500"><option value="published_post">Post ou Reel público do Instagram</option><option value="direct_media">Arquivo direto em nuvem</option></select></div>{linkKind === "direct_media" ? <div><Label htmlFor="remoteMimeType">Formato do arquivo no link</Label><select id="remoteMimeType" value={remoteMimeType} onChange={event => setRemoteMimeType(event.target.value as typeof remoteMimeType)} className="mt-2 h-11 w-full rounded-md border border-violet-100 bg-white px-3 text-sm text-[#2b1058] outline-none focus:ring-2 focus:ring-violet-500"><option value="video/mp4">Vídeo MP4</option><option value="image/jpeg">Imagem JPG</option><option value="image/png">Imagem PNG</option><option value="image/webp">Imagem WEBP</option></select></div> : <><p className="text-xs leading-5 text-slate-600">A Platéia tenta ler a capa e a legenda pública disponíveis. Para uma leitura somente visual, deixe a legenda fora da avaliação.</p><label className="flex cursor-pointer items-start gap-3 rounded-xl border border-violet-200 bg-white px-3 py-3 text-xs leading-5 text-slate-700"><input type="checkbox" checked={skipCaption} onChange={event => setSkipCaption(event.target.checked)} className="mt-0.5 h-4 w-4 rounded border-violet-300 text-violet-700 focus:ring-violet-500" /><span><strong className="text-[#2b1058]">Analisar somente o visual</strong><br />Não considerar nem pontuar a legenda, a chamada textual ou objeções relacionadas à copy.</span></label></>}<p className="text-xs leading-5 text-violet-700">Use links HTTPS públicos. Em Google Drive, Dropbox ou similares, use um link que permita abrir ou baixar o arquivo sem login.</p></div>}</div>;
}

function SparklesIcon() { return <span className="ml-2 text-lg leading-none">✦</span>; }
