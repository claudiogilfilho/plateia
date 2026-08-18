import { describe, expect, it } from "vitest";
import { buildAnalysisPayload } from "./NewEvaluation";

describe("buildAnalysisPayload", () => {
  const base = {
    contentType: "reel" as const,
    product: "",
    objective: "",
    targetAudience: "",
    skipCaption: false,
    sourceMode: "link" as const,
    sourceUrl: " https://www.instagram.com/reel/exemplo/ ",
    linkKind: "published_post" as const,
    remoteMimeType: "video/mp4" as const,
    media: null,
  };

  it("submits a public link with an empty optional caption", () => {
    const payload = buildAnalysisPayload({ ...base, contentText: "" });
    expect(payload.contentText).toBe("");
    expect(payload.source).toEqual({ url: "https://www.instagram.com/reel/exemplo/", kind: "published_post" });
  });

  it("preserves an optional caption in the submitted public-link payload", () => {
    const payload = buildAnalysisPayload({ ...base, contentText: "Legenda complementar." });
    expect(payload.contentText).toBe("Legenda complementar.");
    expect(payload.source?.url).toBe("https://www.instagram.com/reel/exemplo/");
  });
});
