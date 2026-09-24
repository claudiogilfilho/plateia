import { beforeEach, describe, expect, it } from "vitest";
import {
  memoryCreateAnalysis,
  memoryGetAnalysis,
  memoryListAnalyses,
  memoryUpdateAnalysisResult,
  resetMemoryRepository,
} from "./memoryRepository";

describe("temporary MVP repository", () => {
  beforeEach(resetMemoryRepository);

  it("preserves an analysis through create, update, list and detail", () => {
    const created = memoryCreateAnalysis({
      userId: 1,
      contentType: "copy",
      contentText: "Uma copy real para avaliar.",
      product: "",
      objective: "",
      targetAudience: "",
      mediaUrl: null,
      mediaKey: null,
      mediaMimeType: null,
      sourceUrl: null,
      sourceKind: null,
      sourceMediaMimeType: null,
    });

    memoryUpdateAnalysisResult(created.id, "completed", { synthesis: { overallScore: 81 } });

    expect(memoryListAnalyses(1)).toHaveLength(1);
    expect(memoryGetAnalysis(created.id, 1)).toMatchObject({ status: "completed", reportJson: expect.stringContaining("81") });
    expect(memoryGetAnalysis(created.id, 2)).toBeUndefined();
  });
});
