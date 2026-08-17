type BrandMarkProps = {
  compact?: boolean;
  dark?: boolean;
};

const logoUrl = "/manus-storage/plateia-logo_76c2d10e.png";

export function BrandMark({ compact = false, dark = false }: BrandMarkProps) {
  return (
    <div className="flex items-center gap-2.5">
      <img src={logoUrl} alt="Símbolo da Platéia" className="h-9 w-9 rounded-xl object-cover" />
      {!compact && (
        <div className="leading-none">
          <p className={`font-display text-xl font-extrabold tracking-[-0.055em] ${dark ? "text-white" : "text-[#29104e]"}`}>Platéia</p>
          <p className={`mt-1 text-[9px] font-bold uppercase tracking-[0.18em] ${dark ? "text-violet-200" : "text-violet-500"}`}>inteligência de conteúdo</p>
        </div>
      )}
    </div>
  );
}
