import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  createAnalysis: vi.fn(),
  updateAnalysisResult: vi.fn(),
  storagePut: vi.fn(),
  evaluateBlindDecision: vi.fn(),
  evaluateContextualDecision: vi.fn(),
  buildDecisionReport: vi.fn(),
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
vi.mock("./decisionSystem", () => ({
  evaluateBlindDecision: mocks.evaluateBlindDecision,
  evaluateContextualDecision: mocks.evaluateContextualDecision,
  buildDecisionReport: mocks.buildDecisionReport,
  compareDecisionReports: vi.fn(),
}));
vi.mock("./videoTechnicalAnalysis", () => ({
  analyzeUploadedMp4: vi.fn(),
  unavailableTechnicalTruth: vi.fn(() => ({ version: "1.0", source: "not_video", limitations: [] })),
}));
vi.mock("./observatory", () => ({ buildObservatoryContext: mocks.buildObservatoryContext }));
vi.mock("./publicLinks", () => ({
  isAllowedPublicHttpsUrl: () => true,
  isInstagramPublicationUrl: (url: string) => url.includes("instagram.com/reel/"),
  resolveInstagramMaterial: mocks.resolveInstagramMaterial,
  publicLinkMessage: "Link inválido",
}));

import { analysesRouter } from "./analysisRouter";

const blind = { observedSummary: "Leitura cega", priorities: [{}, {}, {}] };
const contextual = { plateiaVerdict: "inconclusive" };
const report = { decisionSystemVersion: "1.0", state: "completed" };

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
    mocks.evaluateBlindDecision.mockResolvedValue(blind);
    mocks.evaluateContextualDecision.mockResolvedValue(contextual);
    mocks.buildDecisionReport.mockImplementation((input: { coverage: unknown }) => ({ ...report, coverage: input.coverage }));
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: "Legenda pública" });
    mocks.buildObservatoryContext.mockRejectedValue(new Error("Observatório indisponível no teste legado"));
  });

  it("creates a copy evaluation with text only and optional context omitted", async () => {
    await expect(caller().create({ contentType: "copy", contentText: "Uma copy curta para avaliar.", product: "", objective: "", targetAudience: "" })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ contentType: "copy", contentText: "Uma copy curta para avaliar.", product: "", mediaUrl: null }));
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ contentType: "copy", text: "Uma copy curta para avaliar." }));
  });

  it("creates a visual evaluation with an uploaded image and no contextual fields", async () => {
    const png = Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), Buffer.alloc(16)]).toString("base64");
    await expect(caller().create({ contentType: "post", contentText: "", product: "", objective: "", targetAudience: "", media: { fileName: "post.png", mimeType: "image/png", base64: png } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.storagePut).toHaveBeenCalled();
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ contentType: "post", mediaUrl: "https://storage.example/test.png", mediaMimeType: "image/png" }));
  });

  it("creates an Instagram Reel evaluation from the public preview and caption", async () => {
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.resolveInstagramMaterial).toHaveBeenCalledWith("https://www.instagram.com/reel/C1Example/");
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ contentType: "reel", text: "Legenda pública", mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg" }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://www.instagram.com/reel/C1Example/" }));
  });

  it("continues visually when an Instagram preview exists but no public caption is available", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: null });
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ text: "", mediaUrl: "https://cdn.instagram.example/preview.jpg" }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://www.instagram.com/reel/C1Example/" }));
  });

  it("requests a visual file, not a caption, when Instagram hides the public preview", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue(null);
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "needs_content" });
    expect(mocks.evaluateBlindDecision).not.toHaveBeenCalled();
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "needs_content", expect.objectContaining({ coverage: expect.objectContaining({ level: "requires_complement", mode: "requires_visual", title: "Material visual necessário" }) }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://www.instagram.com/reel/C1Example/" }));
  });

  it("requests a visual file instead of a caption when visual-only was chosen and Instagram exposes no preview", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue(null);
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", skipCaption: true, source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "needs_content" });
    expect(mocks.evaluateBlindDecision).not.toHaveBeenCalled();
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "needs_content", expect.objectContaining({ coverage: expect.objectContaining({ mode: "requires_visual", title: "Material visual necessário" }) }));
  });

  it("requests the visual file when Instagram hides the preview even if the user supplied a caption", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue(null);
    await expect(caller().create({ contentType: "reel", contentText: "Legenda fornecida pelo usuário.", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "needs_content" });
    expect(mocks.evaluateBlindDecision).not.toHaveBeenCalled();
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "needs_content", expect.objectContaining({ coverage: expect.objectContaining({ level: "requires_complement", mode: "requires_visual" }) }));
  });

  it("preserves a captured caption but still requires visual material", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: null, mediaMimeType: null, caption: "Legenda captada do post" });
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "needs_content" });
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ contentText: "Legenda captada do post", mediaUrl: null }));
    expect(mocks.evaluateBlindDecision).not.toHaveBeenCalled();
  });

  it("continues with a visual-only reading when the user chooses not to evaluate the caption", async () => {
    mocks.resolveInstagramMaterial.mockResolvedValue({ mediaUrl: "https://cdn.instagram.example/preview.jpg", mediaMimeType: "image/jpeg", caption: "Legenda pública" });
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", skipCaption: true, source: { url: "https://www.instagram.com/reel/C1Example/", kind: "published_post" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ text: "", mediaUrl: "https://cdn.instagram.example/preview.jpg" }));
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "completed", expect.objectContaining({ coverage: expect.objectContaining({ mode: "visual_only", excludedCriteria: ["clareza", "ação", "objeções"] }) }));
  });

  it("discards user-provided text when the user explicitly selects visual-only reading", async () => {
    const png = Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), Buffer.alloc(16)]).toString("base64");
    await expect(caller().create({ contentType: "post", contentText: "Legenda que não deve entrar na análise.", product: "", objective: "", targetAudience: "", skipCaption: true, media: { fileName: "post.png", mimeType: "image/png", base64: png } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ text: "" }));
  });

  it("creates a visual-only reading for a direct media URL without requiring any caption", async () => {
    await expect(caller().create({ contentType: "reel", contentText: "", product: "", objective: "", targetAudience: "", skipCaption: true, source: { url: "https://cdn.example/video.mp4", kind: "direct_media", mimeType: "video/mp4" } })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.evaluateBlindDecision).toHaveBeenCalledWith(expect.objectContaining({ text: "", mediaUrl: "https://cdn.example/video.mp4", mediaMimeType: "video/mp4" }));
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "completed", expect.objectContaining({ coverage: expect.objectContaining({ mode: "visual_only" }) }));
    expect(mocks.createAnalysis).toHaveBeenCalledWith(expect.objectContaining({ sourceUrl: "https://cdn.example/video.mp4" }));
  });

  it("preserves the blind audit as inconclusive when the contextual stage is temporarily unavailable", async () => {
    mocks.evaluateContextualDecision.mockRejectedValueOnce(new Error("429"));
    await expect(caller().create({ contentType: "copy", contentText: "Uma copy curta para avaliar.", product: "", objective: "", targetAudience: "" })).resolves.toEqual({ id: 42, status: "completed" });
    expect(mocks.buildDecisionReport).toHaveBeenCalledWith(expect.objectContaining({ contextual: expect.objectContaining({ plateiaVerdict: "inconclusive" }) }));
    expect(mocks.updateAnalysisResult).toHaveBeenCalledWith(42, "completed", expect.objectContaining({ state: "completed_with_limitations" }));
  });

  it("rejects a file whose bytes do not match the declared MIME type", async () => {
    await expect(caller().create({ contentType: "post", contentText: "", product: "", objective: "", targetAudience: "", media: { fileName: "fake.png", mimeType: "image/png", base64: Buffer.from("not-a-png-file").toString("base64") } })).rejects.toThrow("não corresponde");
    expect(mocks.storagePut).not.toHaveBeenCalled();
  });
});
