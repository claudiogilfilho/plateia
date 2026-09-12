import { renderToStaticMarkup } from "react-dom/server";
import React from "react";
import { describe, expect, it } from "vitest";
import { CoverageNotice, getComplementAction, NeedsContentReport, requiresVisualComplement } from "./Report";

describe("CoverageNotice", () => {
  it("shows the coverage title and description for a partial reading", () => {
    const html = renderToStaticMarkup(<CoverageNotice coverage={{ level: "partial", title: "Leitura visual sem legenda", description: "Apenas critérios visuais foram usados." }} />);
    expect(html).toContain("Leitura visual sem legenda");
    expect(html).toContain("Apenas critérios visuais foram usados.");
  });

  it("does not show a notice for a complete reading", () => {
    const html = renderToStaticMarkup(<CoverageNotice coverage={{ level: "complete", title: "Leitura completa", description: "Todos os materiais disponíveis foram considerados." }} />);
    expect(html).toBe("");
  });

  it("directs a visual-only reading without preview to file upload, not caption entry", () => {
    expect(getComplementAction({ level: "requires_complement", mode: "requires_visual", title: "Material visual necessário", description: "Envie o arquivo." }, "reel", "https://instagram.com/reel/exemplo/")).toEqual({ heading: "O Instagram não liberou esse material.", label: "Escolher arquivo original", href: "/avaliar?envio=upload&tipo=reel&retorno=instagram&link=https%3A%2F%2Finstagram.com%2Freel%2Fexemplo%2F" });
  });

  it("renders the visual-material action instead of a caption request", () => {
    const html = renderToStaticMarkup(<NeedsContentReport contentType="reel" sourceUrl="https://instagram.com/reel/exemplo/" reportJson={JSON.stringify({ coverage: { level: "requires_complement", mode: "requires_visual", title: "Material visual necessário", description: "Envie o arquivo original." } })} />);
    expect(html).toContain("O Instagram não liberou esse material.");
    expect(html).toContain("Escolher arquivo original");
    expect(html).toContain("Tentar outro link público");
    expect(html).not.toContain("Adicionar legenda");
  });

  it("never treats an absent caption as a required action", () => {
    const action = getComplementAction(undefined, "reel", "https://www.instagram.com/reel/exemplo/");
    expect(action).toEqual({ heading: "O material visual não está disponível.", label: "Escolher arquivo original", href: "/avaliar?envio=upload&tipo=reel&retorno=instagram&link=https%3A%2F%2Fwww.instagram.com%2Freel%2Fexemplo%2F" });
  });

  it("intercepts legacy Instagram reports that were completed without visual media", () => {
    expect(requiresVisualComplement({ contentType: "reel", sourceKind: "published_post", sourceUrl: "https://www.instagram.com/reel/exemplo/", mediaUrl: null })).toBe(true);
    expect(requiresVisualComplement({ contentType: "reel", sourceKind: "published_post", sourceUrl: "https://www.instagram.com/reel/exemplo/", mediaUrl: "https://cdn.example/video.mp4" })).toBe(false);
  });
});
