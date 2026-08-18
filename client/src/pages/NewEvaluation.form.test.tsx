import { cleanup, render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ mutate: vi.fn(), setLocation: vi.fn() }));

vi.mock("@/lib/trpc", () => ({
  trpc: { analyses: { create: { useMutation: () => ({ mutate: mocks.mutate, isPending: false, error: null }) } } },
}));

vi.mock("wouter", () => ({ useLocation: () => ["/avaliar", mocks.setLocation] }));

import NewEvaluation from "./NewEvaluation";

describe("NewEvaluation public-link form", () => {
  afterEach(cleanup);

  beforeEach(() => {
    mocks.mutate.mockReset();
    mocks.setLocation.mockReset();
    window.history.replaceState({}, "", "/avaliar");
  });

  async function submitPublicLink(caption: string) {
    const user = userEvent.setup();
    render(<NewEvaluation />);
    await user.click(screen.getAllByRole("button", { name: /usar link público/i })[0]);
    await user.type(screen.getByLabelText(/link público do material/i), "https://www.instagram.com/reel/exemplo/");
    if (caption) await user.type(screen.getByLabelText(/texto ou legenda/i), caption);
    await user.click(screen.getByRole("button", { name: /iniciar avaliação/i }));
  }

  it("submits a public link without a caption", async () => {
    await submitPublicLink("");
    await waitFor(() => expect(mocks.mutate).toHaveBeenCalledWith(expect.objectContaining({ contentText: "", source: { url: "https://www.instagram.com/reel/exemplo/", kind: "published_post" } })));
  });

  it("submits a public link and preserves an optional caption", async () => {
    await submitPublicLink("Legenda complementar.");
    await waitFor(() => expect(mocks.mutate).toHaveBeenCalledWith(expect.objectContaining({ contentText: "Legenda complementar.", source: { url: "https://www.instagram.com/reel/exemplo/", kind: "published_post" } })));
  });

  it("orients the user to upload the original file after an Instagram link without preview", () => {
    window.history.replaceState({}, "", "/avaliar?envio=upload&tipo=reel&retorno=instagram&link=https%3A%2F%2Fwww.instagram.com%2Freel%2Fexemplo%2F");
    render(<NewEvaluation />);

    expect(screen.getByText("Continuação do Reel")).not.toBeNull();
    expect(screen.getByRole("heading", { name: "Envie o arquivo original." })).not.toBeNull();
    expect(screen.getByText(/a legenda continua opcional/i)).not.toBeNull();
    expect(screen.getByRole("button", { name: /enviar arquivo/i }).getAttribute("aria-pressed")).toBe("true");
  });
});
