import { describe, expect, it } from "vitest";
import { storagePut } from "./storage";

describe("MVP inline storage", () => {
  it("keeps an upload usable without an external storage service", async () => {
    const stored = await storagePut("plateia/teste.txt", Buffer.from("plateia"), "text/plain");
    expect(stored.key).toMatch(/^inline\//);
    expect(stored.url).toBe("data:text/plain;base64,cGxhdGVpYQ==");
  });
});
