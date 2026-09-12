type BrandMarkProps = {
  compact?: boolean;
  dark?: boolean;
};

export function BrandMark({ compact = false, dark = false }: BrandMarkProps) {
  return (
    <div className="flex items-center gap-2.5">
      <svg
        viewBox="0 0 48 48"
        role="img"
        aria-label="Símbolo da Platéia"
        className="h-9 w-9 shrink-0 rounded-xl drop-shadow-[0_8px_12px_rgba(43,16,88,0.16)]"
      >
        <rect width="48" height="48" rx="15" fill={dark ? "#ffffff" : "#2b1058"} />
        <path d="M12 28c5-8 19-8 24 0" fill="none" stroke="#ff6f61" strokeWidth="4" strokeLinecap="round" />
        <path d="M16 20c3-5 13-5 16 0" fill="none" stroke={dark ? "#2b1058" : "#ffffff"} strokeWidth="3.5" strokeLinecap="round" />
        <circle cx="15" cy="34" r="2.2" fill={dark ? "#2b1058" : "#ffffff"} />
        <circle cx="24" cy="34" r="2.2" fill="#ff6f61" />
        <circle cx="33" cy="34" r="2.2" fill={dark ? "#2b1058" : "#ffffff"} />
      </svg>
      {!compact && (
        <div className="leading-none">
          <p className={`font-display text-xl font-extrabold tracking-[-0.055em] ${dark ? "text-white" : "text-[#29104e]"}`}>Platéia</p>
          <p className={`mt-1 text-[9px] font-bold uppercase tracking-[0.18em] ${dark ? "text-violet-200" : "text-violet-500"}`}>inteligência de conteúdo</p>
        </div>
      )}
    </div>
  );
}
