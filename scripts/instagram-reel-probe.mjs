import { writeFile } from "node:fs/promises";
import { resolveInstagramMaterial } from "../server/publicLinks.ts";

const sourceUrl = "https://www.instagram.com/reel/DcGe0hCTe8l/?igsi=MjNkMTc4OHR6d3dv";
const material = await resolveInstagramMaterial(sourceUrl);

if (!material?.mediaUrl && !material?.caption) {
  throw new Error("O Reel não expôs mídia nem legenda pública para a Platéia.");
}

const result = {
  sourceUrl,
  foundMedia: Boolean(material?.mediaUrl),
  mediaMimeType: material?.mediaMimeType ?? null,
  foundVideo: Boolean(material?.videoUrl),
  foundCoverImage: Boolean(material?.coverImageUrl),
  foundCaption: Boolean(material?.caption),
  captionLength: material?.caption?.length ?? 0,
};
await writeFile("/home/ubuntu/plateia_reel_probe_result.json", JSON.stringify(result, null, 2));
console.log(JSON.stringify(result, null, 2));
