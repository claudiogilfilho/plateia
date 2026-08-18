import { describe, expect, it } from "vitest";
import { validateEvaluationForm } from "./evaluationValidation";

describe("validateEvaluationForm", () => {
  const publicReel = {
    contentType: "reel" as const,
    sourceMode: "link" as const,
    hasMedia: false,
    sourceUrl: "https://www.instagram.com/reel/exemplo/",
  };

  it("accepts a public link with an empty optional caption", () => {
    expect(validateEvaluationForm({ ...publicReel, contentText: "" })).toBeNull();
  });

  it("also accepts a public link when an optional caption is supplied", () => {
    expect(validateEvaluationForm({ ...publicReel, contentText: "Legenda complementar." })).toBeNull();
  });
});
