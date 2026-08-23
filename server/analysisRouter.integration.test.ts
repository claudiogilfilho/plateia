import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  createAnalysis: vi.fn(),
  updateAnalysisResult: vi.fn(),
  storagePut: vi.fn(),
  evaluateContent: vi.fn(),
  applyVisualOnlyScope: vi.fn((value: unknown) => value),
  resolveInstagramMaterial: vi.fn(),
  buildObservatoryContext: vi.fn(),
}));

vi.mock("./db", () => ({
  createAnalysis: mocks.createAnalysis,
  getAnalysisByIdForUser: vi.fn(),
  listAnalysesForUser: vi.fn(),
  updateAnalysisResult: mocks.updateAnalysisResult,
}));
vi.mock("./storage", () => ({ storagePut: mocks.storagePut }));
vi.mock("./contentAnalysis", () => ({ evaluateContent: mocks.evaluateContent, applyVisualOnlyScope: mocks.applyVisualOnlyScope }));
vi.mock("./observatory", () => ({ buildObservatoryContext: mocks.buildObservatoryContext }));
vi.mock("./publicLinks", () => ({
  isAllowedPublicHttpsUrl: () => true,
  isInstagramPublicationUrl: (url: string) => url.includes("instagram.com/reel/"),
  resolveInstagramMaterial: mocks.resolveInstagramMaterial,
  publicLinkMessage: "Link inválido",
}));

import { analysesRouter } from "./analysisRouter";

const report = {
  consumers: [],
  synthesis: { overallScore: 70, weightedAverage: 70, divergence: 10, strengths: ["A"], risks: ["B"], recommendations: ["1", "2", "3"] },
};

const caller = () => analysesRouter.createCaller({
  user: { id: 7, openId: "test-user", name: "Teste", email: "teste@plateia.com", loginMethod: "test", role: "user", createdAt: new Date(), updatedAt: new Date(), lastSignedIn: new Date() },
  req: {} as never,
  res: {} as never,
});

describe("analyses.create integration", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mocks.createAnalysis.mockResolvedValue({ id: 42 });
    mocks.updateAnalysisResult.mockResolvedValue(undefined);
    mocks.storagePut.mockResolvedValue({ key: "plateia/test.png", url: "https://storage.example/test.png" });
    mocks.evaluateContent.mockResolvedValue(report);
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: "Legenda pública" });
    mocks.buildObservatoryContext.mockRejectedValue(new Error("Observatório indisponível no teste legado"));
  });

  it("creates a copy evaluation with text only and optional context omitted", async () => {
    await expect(caller().create({ contentType: "copy", contentText: "Uma copy curta para avaliar.", product: "", objective: "", targetAudience: "" })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ contentType: "copy", contentText: "Uma copy curta para avaliar.", product: "", mediaUrl: null }));
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ contentType: "copy", text: "Uma copy curta para avaliar." }));
  });

  it("creates a visual evaluation with an uploaded image and no contextual fields", async () => {
    await expect(caller().create({ contentType: "post", contentText: "", product: "", objective: "", targetAudience: "", media: { fileName: "post.png", mimeType: "image/png", base64: "a".repeat(24) } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.storagePut).toHaveBeenCalled();
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ contentType: "post", mediaUrl: "https://storage.example/test.png", mediaMimeType: "image/png" }));
  });

  it("creates an Instagram Reel evaluation from the public preview and caption", async () => {
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.resolveInstagramMaterial).toHaveBeenCalledWith("https://www.instagram.com/reel/C1Example/");
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ contentType: "reel", text: "Legenda pública", mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg" }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://www.instagram.com/reel/C1Example/" }));
  });

  it("continues visually when an Instagram preview exists but no public caption is available", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: null });
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ text: "", analysisScope: "visual_only", mediaUrl: "https://cdn.instagram.example/preview.jpg" }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://www.instagram.com/reel/C1Example/" }));
  });

  it("requests a visual file, not a caption, when Instagram hides the public preview", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue(null);
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "needs_content" });
    expect(mocks.evaluateContent).not.toHaveBeenCalled();
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "needs_content", expect.objectContaining({ coverage: expect.objectContaining({ level: "requires_complement", mode: "requires_visual", title: "Material visual necessário" }) }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://www.instagram.com/reel/C1Example/" }));
  });

  it("requests a visual file instead of a caption when visual-only was chosen and Instagram exposes no preview", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue(null);
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", skipCaption: true, source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "needs_content" });
    expect(mocks.evaluateContent).not.toHaveBeenCalled();
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "needs_content", expect.objectContaining({ coverage: expect.objectContaining({ mode: "requires_visual", title: "Material visual necessário" }) }));
  });

  it("continues with a partial text reading when Instagram hides the preview but the user supplied a caption", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue(null);
    await expect(caller().create({ contentType: "reel", contentText: "Legenda fornecida pelo usuário.", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ text: "Legenda fornecida pelo usuário.", mediaUrl: null }));
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "completed", expect.objectContaining({ coverage: expect.objectContaining({ level: "partial" }) }));
  });

  it("uses a caption captured from Instagram even when the visual preview is unavailable", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: null, mediaMimeType: null, caption: "Legenda captada do post" });
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ text: "Legenda captada do post", mediaUrl: null }));
  });

  it("continues with a visual-only reading when the user chooses not to evaluate the caption", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: "Legenda pública" });
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", skipCaption: true, source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ text: "", analysisScope: "visual_only", mediaUrl: "https://cdn.instagram.example/preview.jpg" }));
    expect(mocks.applyVisualOnlyScope).toHaveBeenCalledWith(report);
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "completed", expect.objectContaining({ coverage: expect.objectContaining({ mode: "visual_only", excludedCriteria: ["clareza", "ação", "objeções"] }) }));
  });

  it("discards user-provided text when the user explicitly selects visual-only reading", async () => {
    await expect(caller().create({ contentType: "post", contentText: "Legenda que não deve entrar na análise.", product: "", objective: "", targetAudience: "", skipCaption: true, media: { fileName: "post.png", mimeType: "image/png", base64: "a".repeat(24) } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ text: "", analysisScope: "visual_only" }));
  });

  it("creates a visual-only reading for a direct media URL without requiring any caption", async () => {
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", skipCaption: true, source: { url: "https://cdn.example/video.mp4", kind: "direct_media", mimeType: "video/mp4" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateContent).toHaveBeenCalledWith(expect.objectContaining({ text: "", analysisScope: "visual_only", mediaUrl: "https://cdn.example/video.mp4", mediaMimeType: "video/mp4" }));
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "completed", expect.objectContaining({ coverage: expect.objectContaining({ mode: "visual_only" }) }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://cdn.example/video.mp4" }));
  });
});
