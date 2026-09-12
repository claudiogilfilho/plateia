import { describe, expect, it } from "vitest";
import { parseProbeJson, parseSceneChanges, parseSilenceDetect, parseVolumeDetect, unavailableTechnicalTruth } from "./videoTechnicalAnalysis";

describe("verdade técnica determinística", () => {
  it("extrai duração, resolução, FPS, codec, tamanho e presença de áudio do ffprobe", () => {
    const parsed = parseProbeJson(JSON.stringify({
      streams: [
        { codec_type: "video", codec_name: "h264", width: 1080, height: 1920, avg_frame_rate: "30000/1001" },
        { codec_type: "audio", codec_name: "aac" },
      ],
      format: { duration: "12.345", size: "123456" },
    }), 1);
    expect(parsed).toMatchObject({ width: 1080, height: 1920, duration: 12.345, size: 123456 });
    expect(parsed.fps).toBeCloseTo(29.97, 2);
    expect(parsed.audio?.codec_name).toBe("aac");
  });

  it("interpreta volume, silêncios e mudanças de cena sem criar dados ausentes", () => {
    expect(parseVolumeDetect("mean_volume: -21.4 dB\nmax_volume: -2.0 dB")).toEqual({ meanDb: -21.4, peakDb: -2 });
    expect(parseSilenceDetect("silence_start: 1.25\nsilence_end: 2.75 | silence_duration: 1.50")).toEqual([{ startSeconds: 1.25, endSeconds: 2.75, durationSeconds: 1.5 }]);
    expect(parseSceneChanges("pts_time:0.50 pts_time:3.25")).toEqual([0.5, 3.25]);
    expect(parseSceneChanges("sem cenas")).toEqual([]);
  });

  it("marca URLs remotas como não avaliadas em vez de baixá-las", () => {
    const truth = unavailableTechnicalTruth("remote_media");
    expect(truth.durationSeconds.status).toBe("not_assessed");
    expect(truth.transcript.status).toBe("not_assessed");
    expect(truth.transcript.limitation).toContain("Transcrição");
    expect(truth.limitations.join(" ")).toContain("SSRF");
  });
});
