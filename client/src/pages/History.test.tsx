import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import { Router } from "wouter";

const queryState = vi.hoisted(() => ({ data: [{ id: 1, status: "completed", product: "Material de teste com nome longo", contentType: "reel", createdAt: new Date("2026-08-20T12:00:00Z"), reportJson: "{json inválido" }], isLoading: false, error: null }));

vi.mock("@/lib/trpc", () => ({ trpc: { analyses: { list: { useQuery: () => queryState } } } }));

import History, { getReportScore } from "./History";

function renderHistory() {
  return renderToStaticMarkup(<Router hook={() => ["/historico", () => undefined]}><History /></Router>);
}

describe("History", () => {
  it("does not break the library when a persisted report is malformed", () => {
    expect(getReportScore("{json inválido")).toBeNull();
    const html = renderHistory();
    expect(html).toContain("Material de teste com nome longo");
    expect(html).toContain("Concluída");
  });

  it("keeps the mobile entry metadata grouped below the material title", () => {
    const html = renderHistory();
    expect(html).toContain("sm:grid");
    expect(html).toContain("mt-3 flex items-center justify-between");
    expect(html).toContain("max-w-[calc(100vw-10rem)]");
  });
});
