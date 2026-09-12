import { execFile } from "node:child_process";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

export type Confidence = "low" | "medium" | "high";
export type Assessed<T> =
  | { status: "measured"; value: T; confidence: Confidence; method: string }
  | { status: "not_assessed"; value: null; confidence: "low"; limitation: string };

export type VideoTechnicalTruth = {
  version: "1.0";
  source: "uploaded_mp4" | "remote_media" | "not_video";
  durationSeconds: Assessed<number>;
  resolution: Assessed<{ width: number; height: number }>;
  aspectRatio: Assessed<string>;
  framesPerSecond: Assessed<number>;
  videoCodec: Assessed<string>;
  fileSizeBytes: Assessed<number>;
  audioPresent: Assessed<boolean>;
  audioCodec: Assessed<string>;
  volume: Assessed<{ meanDb: number | null; peakDb: number | null }>;
  silenceIntervals: Assessed<Array<{ startSeconds: number; endSeconds: number; durationSeconds: number }>>;
  sceneChanges: Assessed<number[]>;
  averageSceneDurationSeconds: Assessed<number>;
  cutsPerMinute: Assessed<number>;
  motionVariation: Assessed<never>;
  transcript: Assessed<never>;
  onScreenText: Assessed<never>;
  faceProductLogoAndCta: Assessed<never>;
  speechSpeed: Assessed<never>;
  textDensityAndReadingTime: Assessed<never>;
  legibilityContrastSafeArea: Assessed<never>;
  limitations: string[];
};

const unavailable = (limitation: string): Assessed<never> => ({ status: "not_assessed", value: null, confidence: "low", limitation });
const measured = <T>(value: T, method: string, confidence: Confidence = "high"): Assessed<T> => ({ status: "measured", value, confidence, method });

function parseRate(value: unknown) {
  if (typeof value !== "string") return null;
  const parts = value.split("/");
  const numerator = Number(parts[0]);
  const denominator = Number(parts[1] ?? "1");
  if (!Number.isFinite(numerator) || !Number.isFinite(denominator) || denominator === 0) return null;
  return numerator / denominator;
}

function finiteNumber(value: unknown) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export function parseProbeJson(raw: string, fallbackSize: number) {
  const probe = JSON.parse(raw) as { streams?: Array<Record<string, unknown>>; format?: Record<string, unknown> };
  const streams = probe.streams ?? [];
  const video = streams.find(stream => stream.codec_type === "video");
  const audio = streams.find(stream => stream.codec_type === "audio");
  const width = finiteNumber(video?.width);
  const height = finiteNumber(video?.height);
  const duration = finiteNumber(probe.format?.duration) ?? finiteNumber(video?.duration);
  const fps = parseRate(video?.avg_frame_rate) ?? parseRate(video?.r_frame_rate);
  const size = finiteNumber(probe.format?.size) ?? fallbackSize;
  return { video, audio, width, height, duration, fps, size };
}

export function parseVolumeDetect(raw: string) {
  const mean = raw.match(/mean_volume:\s*(-?[\d.]+)\s*dB/i);
  const peak = raw.match(/max_volume:\s*(-?[\d.]+)\s*dB/i);
  return { meanDb: mean ? Number(mean[1]) : null, peakDb: peak ? Number(peak[1]) : null };
}

export function parseSilenceDetect(raw: string) {
  const starts = Array.from(raw.matchAll(/silence_start:\s*([\d.]+)/g), match => Number(match[1]));
  const ends = Array.from(raw.matchAll(/silence_end:\s*([\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)/g));
  return ends.map((match, index) => ({
    startSeconds: starts[index] ?? Math.max(0, Number(match[1]) - Number(match[2])),
    endSeconds: Number(match[1]),
    durationSeconds: Number(match[2]),
  }));
}

export function parseSceneChanges(raw: string) {
  return Array.from(raw.matchAll(/pts_time:([\d.]+)/g), match => Number(match[1])).filter(Number.isFinite);
}

async function run(binary: string, args: string[], timeout: number) {
  return execFileAsync(binary, args, { timeout, maxBuffer: 8 * 1024 * 1024 });
}

function baseTruth(source: VideoTechnicalTruth["source"], fileSize: number): VideoTechnicalTruth {
  const localOnly = "Detector determinístico não executado neste ambiente ou para esta origem.";
  return {
    version: "1.0",
    source,
    durationSeconds: unavailable(localOnly),
    resolution: unavailable(localOnly),
    aspectRatio: unavailable(localOnly),
    framesPerSecond: unavailable(localOnly),
    videoCodec: unavailable(localOnly),
    fileSizeBytes: fileSize ? measured(fileSize, "tamanho do upload") : unavailable("Tamanho não disponível para mídia remota."),
    audioPresent: unavailable(localOnly),
    audioCodec: unavailable(localOnly),
    volume: unavailable("Medição de volume requer faixa de áudio local acessível ao FFmpeg."),
    silenceIntervals: unavailable("Detecção de silêncio requer faixa de áudio local acessível ao FFmpeg."),
    sceneChanges: unavailable("Detecção de mudanças de cena requer MP4 local e FFmpeg."),
    averageSceneDurationSeconds: unavailable("Sem mudanças de cena medidas."),
    cutsPerMinute: unavailable("Sem mudanças de cena e duração medidas."),
    motionVariation: unavailable("Detector de movimento ainda não está disponível; a IA não deve inventar este dado."),
    transcript: unavailable("Transcrição com timestamps depende de um transcritor configurado e não foi executada."),
    onScreenText: unavailable("OCR temporal ainda não está disponível e não foi simulado."),
    faceProductLogoAndCta: unavailable("Detectores de rosto, produto, logo e CTA visual ainda não estão disponíveis."),
    speechSpeed: unavailable("Sem transcrição temporal não é possível medir velocidade de fala."),
    textDensityAndReadingTime: unavailable("Sem OCR temporal não é possível medir densidade ou tempo de leitura."),
    legibilityContrastSafeArea: unavailable("Auditoria determinística de contraste, safe area e sobreposição ainda não está disponível."),
    limitations: [],
  };
}

export function unavailableTechnicalTruth(source: VideoTechnicalTruth["source"] = "remote_media") {
  const result = baseTruth(source, 0);
  result.limitations.push("A verdade técnica integral só é extraída do MP4 enviado diretamente; URLs remotas não são baixadas pelo servidor para evitar SSRF e vazamento de dados.");
  return result;
}

export async function analyzeUploadedMp4(buffer: Buffer): Promise<VideoTechnicalTruth> {
  const result = baseTruth("uploaded_mp4", buffer.byteLength);
  const directory = await mkdtemp(join(tmpdir(), "plateia-video-"));
  const file = join(directory, "material.mp4");
  try {
    await writeFile(file, buffer, { mode: 0o600 });
    const probeResult = await run("ffprobe", ["-v", "error", "-show_format", "-show_streams", "-of", "json", file], 20_000);
    const probe = parseProbeJson(probeResult.stdout, buffer.byteLength);
    if (!probe.video) throw new Error("O arquivo não contém uma faixa de vídeo reconhecível.");

    if (probe.duration !== null) result.durationSeconds = measured(Number(probe.duration.toFixed(3)), "ffprobe");
    if (probe.width !== null && probe.height !== null) {
      result.resolution = measured({ width: probe.width, height: probe.height }, "ffprobe");
      const divisor = greatestCommonDivisor(probe.width, probe.height);
      result.aspectRatio = measured(`${probe.width / divisor}:${probe.height / divisor}`, "ffprobe");
    }
    if (probe.fps !== null) result.framesPerSecond = measured(Number(probe.fps.toFixed(3)), "ffprobe");
    if (typeof probe.video.codec_name === "string") result.videoCodec = measured(probe.video.codec_name, "ffprobe");
    result.fileSizeBytes = measured(probe.size, "ffprobe");
    result.audioPresent = measured(Boolean(probe.audio), "ffprobe");
    if (typeof probe.audio?.codec_name === "string") result.audioCodec = measured(probe.audio.codec_name, "ffprobe");

    if (probe.audio) {
      const [volumeResult, silenceResult] = await Promise.allSettled([
        run("ffmpeg", ["-hide_banner", "-i", file, "-af", "volumedetect", "-f", "null", "-"], 25_000),
        run("ffmpeg", ["-hide_banner", "-i", file, "-af", "silencedetect=noise=-35dB:d=0.35", "-f", "null", "-"], 25_000),
      ]);
      if (volumeResult.status === "fulfilled") result.volume = measured(parseVolumeDetect(volumeResult.value.stderr), "FFmpeg volumedetect", "medium");
      else result.limitations.push("O FFmpeg não concluiu a medição de volume.");
      if (silenceResult.status === "fulfilled") result.silenceIntervals = measured(parseSilenceDetect(silenceResult.value.stderr), "FFmpeg silencedetect", "medium");
      else result.limitations.push("O FFmpeg não concluiu a detecção de silêncio.");
    }

    try {
      const scenesResult = await run("ffmpeg", ["-hide_banner", "-i", file, "-vf", "select=gt(scene\\,0.35),showinfo", "-an", "-f", "null", "-"], 35_000);
      const scenes = parseSceneChanges(scenesResult.stderr);
      result.sceneChanges = measured(scenes, "FFmpeg scene threshold 0.35", "medium");
      if (probe.duration !== null && probe.duration > 0) {
        result.averageSceneDurationSeconds = measured(Number((probe.duration / (scenes.length + 1)).toFixed(3)), "duração / segmentos detectados", "medium");
        result.cutsPerMinute = measured(Number(((scenes.length / probe.duration) * 60).toFixed(2)), "mudanças de cena / minuto", "medium");
      }
    } catch {
      result.limitations.push("O FFmpeg não concluiu a detecção de mudanças de cena.");
    }
  } catch (error) {
    result.limitations.push(error instanceof Error ? error.message : "Falha técnica não identificada.");
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
  return result;
}

function greatestCommonDivisor(a: number, b: number): number {
  let left = Math.abs(Math.round(a));
  let right = Math.abs(Math.round(b));
  while (right) [left, right] = [right, left % right];
  return left || 1;
}
