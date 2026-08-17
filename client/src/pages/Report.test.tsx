import { renderToStaticMarkup } from "react-dom/server";
import React from "react";
import { describe, expect, it } from "vitest";
import { CoverageNotice } from "./Report";

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
});
