#!/usr/bin/env python3
"""Portable JSON memory for Platéia references and evidence-gated patterns."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_PARAMETERS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term",
    "fbclid", "gclid", "igshid", "si", "feature",
}
COUNTABLE_ROLES = {"support", "counterexample"}


def empty_memory() -> dict:
    return {"protocol": "plateia-memory/1.0", "references": [], "patterns": [], "hypotheses": []}


def load(path: Path) -> dict:
    if not path.exists():
        return empty_memory()
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("protocol") != "plateia-memory/1.0":
        raise SystemExit("Arquivo de memória incompatível.")
    value.setdefault("references", [])
    value.setdefault("patterns", [])
    value.setdefault("hypotheses", [])
    return value


def save(path: Path, memory: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{json.dumps(memory, ensure_ascii=False, indent=2)}\n", encoding="utf-8")


def normalized(value: str) -> str:
    raw = unicodedata.normalize("NFD", str(value or ""))
    raw = "".join(char for char in raw if unicodedata.category(char) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", raw).strip()


def canonical_url(value: str) -> str:
    try:
        parsed = urlsplit(str(value).strip())
        host = parsed.hostname.lower() if parsed.hostname else ""
        host = re.sub(r"^www\.", "", host)
        path = re.sub(r"/$", "", parsed.path) or "/"
        query = [(key, item) for key, item in parse_qsl(parsed.query, keep_blank_values=True) if key.lower() not in TRACKING_PARAMETERS]
        if host == "youtu.be" and path.strip("/"):
            host, path, query = "youtube.com", "/watch", [("v", path.strip("/"))]
        short = re.fullmatch(r"/shorts/([^/]+)", path)
        if host in {"youtube.com", "m.youtube.com"} and short:
            host, path, query = "youtube.com", "/watch", [("v", short.group(1))]
        if host == "m.youtube.com":
            host = "youtube.com"
        query.sort()
        return urlunsplit((parsed.scheme.lower() or "https", host, path, urlencode(query), "")).rstrip("/")
    except Exception:
        return normalized(value)


def clean_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def overlap(left: list[str], right: list[str]) -> bool:
    unknown = {"", "indeterminado", "indeterminada", "unknown", "not_applicable"}
    return bool((set(left) - unknown) & (set(right) - unknown))


def similarity(target: dict, candidate: dict) -> int:
    score = 0
    if target.get("primaryFamily") == candidate.get("primaryFamily") and target.get("primaryFamily") not in {None, "indeterminado"}:
        score += 30
    if overlap([target.get("primaryFamily", ""), *target.get("secondaryFamilies", [])], [candidate.get("primaryFamily", ""), *candidate.get("secondaryFamilies", [])]):
        score += 10
    if overlap(target.get("objectives", []), candidate.get("objectives", [])):
        score += 18
    if normalized(target.get("segment", "")) and normalized(target.get("segment", "")) == normalized(candidate.get("segment", "")):
        score += 15
    if overlap(target.get("presentationFormats", []), candidate.get("presentationFormats", [])):
        score += 8
    if target.get("materialFormat") == candidate.get("materialFormat") and target.get("materialFormat") not in {None, "indeterminado"}:
        score += 6
    if target.get("awarenessStage") == candidate.get("awarenessStage") and target.get("awarenessStage") not in {None, "indeterminado"}:
        score += 4
    if target.get("productionLevel") == candidate.get("productionLevel") and target.get("productionLevel") not in {None, "unknown"}:
        score += 3
    if target.get("durationBand") == candidate.get("durationBand") and target.get("durationBand") not in {None, "unknown"}:
        score += 3
    if target.get("pace") == candidate.get("pace") and target.get("pace") not in {None, "unknown"}:
        score += 3
    if overlap(target.get("mechanisms", []), candidate.get("mechanisms", [])):
        score += 10
    return min(100, score)


def level(target: dict, candidate: dict, score: int) -> int:
    same_family = target.get("primaryFamily") == candidate.get("primaryFamily") and target.get("primaryFamily") not in {None, "indeterminado"}
    same_objective = overlap(target.get("objectives", []), candidate.get("objectives", []))
    same_segment = normalized(target.get("segment", "")) == normalized(candidate.get("segment", "")) and bool(normalized(target.get("segment", "")))
    if same_family and same_objective and same_segment and score >= 65:
        return 1
    if same_family and same_objective and score >= 48:
        return 2
    if overlap(target.get("mechanisms", []), candidate.get("mechanisms", [])) and score >= 25:
        return 3
    return 4


def source_identity(reference: dict) -> str:
    explicit = normalized(reference.get("sourceIdentity", ""))
    creator = normalized(reference.get("creator", ""))
    return explicit or creator or canonical_url(reference.get("url", ""))


def normalize_hypothesis(raw) -> dict | None:
    if isinstance(raw, str):
        statement = raw.strip()
        return {"name": statement, "statement": statement, "evidenceRole": "context", "requiredEvidenceObserved": False, "comparisonLevel": 4, "confidence": "low"} if statement else None
    if not isinstance(raw, dict):
        return None
    value = dict(raw)
    value["name"] = str(value.get("name") or value.get("statement") or "").strip()
    value["evidenceRole"] = str(value.get("evidenceRole") or value.get("role") or ("counterexample" if value.get("stage") == "contradicted" else "context")).strip()
    value["comparisonLevel"] = int(value.get("comparisonLevel") or 4)
    value["requiredEvidenceObserved"] = value.get("requiredEvidenceObserved") is True
    value["confidence"] = str(value.get("confidence") or "low")
    return value if value["name"] else None


def evidence_eligible(hypothesis: dict) -> bool:
    return (
        hypothesis.get("evidenceRole") in COUNTABLE_ROLES
        and hypothesis.get("comparisonLevel") in {1, 2}
        and hypothesis.get("requiredEvidenceObserved") is True
        and hypothesis.get("confidence") in {"medium", "high"}
    )


def pattern_stage(pattern: dict, references_by_id: dict[str, dict]) -> tuple[str, str, int, int]:
    support_ids = list(dict.fromkeys(clean_list(pattern.get("supportReferenceIds"))))
    counter_ids = list(dict.fromkeys(clean_list(pattern.get("counterexampleReferenceIds"))))
    creators = {normalized(references_by_id[item].get("creator", "")) for item in support_ids if item in references_by_id and normalized(references_by_id[item].get("creator", ""))}
    sources = {source_identity(references_by_id[item]) for item in support_ids if item in references_by_id and source_identity(references_by_id[item])}
    existing = pattern.get("stage") or pattern.get("status")
    if existing in {"experimentally_validated", "validated"}:
        return "experimentally_validated", "high", len(creators), len(sources)
    if len(counter_ids) >= len(support_ids) and len(counter_ids) >= 2:
        return "contradicted", "low", len(creators), len(sources)
    if len(support_ids) >= 3 and len(creators) >= 2 and len(sources) >= 2:
        confidence = "high" if len(support_ids) >= 5 and not counter_ids else "medium"
        return "provisional", confidence, len(creators), len(sources)
    if len(support_ids) >= 2:
        return "supported_hypothesis", "low", len(creators), len(sources)
    if len(support_ids) == 1:
        return "observation", "low", len(creators), len(sources)
    return ("inconclusive" if counter_ids else "hypothesis"), "low", len(creators), len(sources)


def refresh_pattern(pattern: dict, references_by_id: dict[str, dict]) -> None:
    for key in ["supportReferenceIds", "counterexampleReferenceIds", "caseLimitReferenceIds"]:
        pattern[key] = list(dict.fromkeys(clean_list(pattern.get(key))))
    support = set(pattern["supportReferenceIds"])
    counter = set(pattern["counterexampleReferenceIds"])
    limits = set(pattern["caseLimitReferenceIds"])
    pattern["counterexampleReferenceIds"] = [item for item in pattern["counterexampleReferenceIds"] if item not in support]
    counter = set(pattern["counterexampleReferenceIds"])
    pattern["caseLimitReferenceIds"] = [item for item in pattern["caseLimitReferenceIds"] if item not in support and item not in counter]
    pattern["supportingCount"] = len(pattern["supportReferenceIds"])
    pattern["counterexampleCount"] = len(pattern["counterexampleReferenceIds"])
    pattern["caseLimitCount"] = len(pattern["caseLimitReferenceIds"])
    stage, confidence, creators, sources = pattern_stage(pattern, references_by_id)
    pattern["stage"] = stage
    pattern["status"] = stage
    pattern["confidence"] = confidence
    pattern["creatorDiversityCount"] = creators
    pattern["sourceDiversityCount"] = sources


def locate_pattern(memory: dict, hypothesis: dict, classification: dict) -> dict | None:
    target_id = str(hypothesis.get("targetPatternId") or hypothesis.get("patternId") or "").strip()
    if target_id:
        return next((item for item in memory["patterns"] if str(item.get("id")) == target_id), None)
    pattern_key = normalized(hypothesis.get("patternKey", ""))
    if pattern_key:
        return next((item for item in memory["patterns"] if normalized(item.get("patternKey", "")) == pattern_key), None)
    return None


def evidence_record(reference: dict, hypothesis: dict) -> dict:
    return {
        "referenceId": reference["id"],
        "role": hypothesis.get("evidenceRole"),
        "comparisonLevel": hypothesis.get("comparisonLevel"),
        "requiredEvidenceObserved": hypothesis.get("requiredEvidenceObserved"),
        "observation": hypothesis.get("observation", ""),
        "evidence": hypothesis.get("evidence", ""),
        "limitations": clean_list(hypothesis.get("limitations")),
    }


def apply_evidence(pattern: dict, reference: dict, hypothesis: dict, references_by_id: dict[str, dict]) -> None:
    reference_id = str(reference["id"])
    role = hypothesis.get("evidenceRole")
    for key in ["supportReferenceIds", "counterexampleReferenceIds", "caseLimitReferenceIds"]:
        pattern[key] = [item for item in clean_list(pattern.get(key)) if item != reference_id]
    if evidence_eligible(hypothesis) and role == "support":
        pattern["supportReferenceIds"].append(reference_id)
    elif evidence_eligible(hypothesis) and role == "counterexample":
        pattern["counterexampleReferenceIds"].append(reference_id)
    elif role == "case_limit":
        pattern["caseLimitReferenceIds"].append(reference_id)
    previous = [item for item in pattern.get("evidence", []) if str(item.get("referenceId")) != reference_id]
    pattern["evidence"] = [*previous, evidence_record(reference, hypothesis)][-50:]
    refresh_pattern(pattern, references_by_id)


def create_pattern(reference: dict, hypothesis: dict, classification: dict) -> dict:
    objective = (classification.get("objectives") or ["indeterminado"])[0]
    pattern_key = normalized(hypothesis.get("patternKey") or hypothesis.get("name"))
    return {
        "id": str(uuid.uuid4()),
        "patternKey": pattern_key,
        "name": hypothesis["name"],
        "statement": hypothesis.get("statement") or hypothesis["name"],
        "creativeFamily": classification.get("primaryFamily", "indeterminado"),
        "objective": objective,
        "segment": classification.get("segment", "indeterminado"),
        "mechanism": clean_list(hypothesis.get("mechanism")) if isinstance(hypothesis.get("mechanism"), list) else [str(hypothesis.get("mechanism") or "").strip()] if hypothesis.get("mechanism") else [],
        "patternType": hypothesis.get("patternType", "outro"),
        "supportReferenceIds": [],
        "counterexampleReferenceIds": [],
        "caseLimitReferenceIds": [],
        "supportingCount": 0,
        "counterexampleCount": 0,
        "caseLimitCount": 0,
        "stage": "observation",
        "status": "observation",
        "confidence": "low",
        "evidence": [],
        "validation": "requires_human_or_experimental_evidence",
    }


def consolidate(memory: dict, reference: dict) -> None:
    classification = reference.get("classification", {})
    references_by_id = {str(item.get("id")): item for item in memory["references"] if item.get("id") is not None}
    raw_hypotheses = reference.get("training", {}).get("hypotheses", [])
    for raw in raw_hypotheses[:5]:
        hypothesis = normalize_hypothesis(raw)
        if not hypothesis:
            continue
        pattern = locate_pattern(memory, hypothesis, classification)
        if pattern is None:
            if not (evidence_eligible(hypothesis) and hypothesis.get("evidenceRole") == "support"):
                continue
            pattern = create_pattern(reference, hypothesis, classification)
            memory["patterns"].append(pattern)
        apply_evidence(pattern, reference, hypothesis, references_by_id)


def command_add(args: argparse.Namespace) -> dict:
    memory = load(args.db)
    record = json.loads(args.record.read_text(encoding="utf-8"))
    record.setdefault("id", str(uuid.uuid4()))
    record.setdefault("createdAt", datetime.now(timezone.utc).isoformat())
    if not isinstance(record.get("classification"), dict):
        raise SystemExit("A referência precisa de classification.")
    if any(str(item.get("id")) == str(record["id"]) for item in memory["references"]):
        raise SystemExit("Já existe uma referência com este id.")
    url = canonical_url(record.get("url", ""))
    if not url:
        raise SystemExit("A referência precisa de URL pública individual.")
    if any(canonical_url(item.get("url", "")) == url for item in memory["references"]):
        raise SystemExit("Já existe uma referência com esta URL canônica.")
    memory["references"].append(record)
    consolidate(memory, record)
    memory["updatedAt"] = datetime.now(timezone.utc).isoformat()
    save(args.db, memory)
    return {"status": "added", "id": record["id"], "references": len(memory["references"]), "patterns": len(memory["patterns"])}


def command_search(args: argparse.Namespace) -> dict:
    memory = load(args.db)
    target = json.loads(args.classification.read_text(encoding="utf-8"))
    matches = []
    for reference in memory["references"]:
        candidate = reference.get("classification", {})
        score = similarity(target, candidate)
        comparison_level = level(target, candidate, score)
        if comparison_level < 4:
            matches.append({"id": reference.get("id"), "title": reference.get("title", ""), "creator": reference.get("creator", ""), "similarity": score, "comparisonLevel": comparison_level, "classification": candidate, "replicable": reference.get("training", {}).get("replicable", [])[:3]})
    matches.sort(key=lambda item: (item["comparisonLevel"], -item["similarity"]))
    return {"protocol": memory["protocol"], "matches": matches[: args.limit]}


def command_candidates(args: argparse.Namespace) -> dict:
    memory = load(args.db)
    candidates = []
    for pattern in memory["patterns"]:
        stage = pattern.get("stage") or pattern.get("status")
        if stage not in {"observation", "hypothesis", "supported_hypothesis", "provisional"}:
            continue
        support = int(pattern.get("supportingCount") or 0)
        counter = int(pattern.get("counterexampleCount") or 0)
        priority = 0 if stage == "supported_hypothesis" and support == 2 else 1 if support == 1 else 2 if stage == "provisional" and counter == 0 else 3
        candidates.append({"id": pattern.get("id"), "statement": pattern.get("statement") or pattern.get("name"), "stage": stage, "supportingCount": support, "counterexampleCount": counter, "caseLimitCount": int(pattern.get("caseLimitCount") or 0), "creativeFamily": pattern.get("creativeFamily"), "objective": pattern.get("objective"), "segment": pattern.get("segment"), "priority": priority})
    pattern_ids = {str(item.get("id")) for item in memory["patterns"]}
    refs = {str(item.get("id")): item for item in memory["references"]}
    for hypothesis in memory.get("hypotheses", []):
        if str(hypothesis.get("id")) in pattern_ids:
            continue
        support_ids = clean_list(hypothesis.get("supportReferenceIds"))
        first = refs.get(support_ids[0], {}) if support_ids else {}
        classification = first.get("classification", {})
        support = len(set(support_ids))
        candidates.append({"id": hypothesis.get("id"), "statement": hypothesis.get("statement"), "stage": "supported_hypothesis" if support >= 2 else "observation", "supportingCount": support, "counterexampleCount": 0, "caseLimitCount": 0, "creativeFamily": classification.get("primaryFamily"), "objective": (classification.get("objectives") or [None])[0], "segment": classification.get("segment"), "priority": 0 if support == 2 else 1})
    candidates.sort(key=lambda item: (item["priority"], -item["supportingCount"], str(item.get("id"))))
    return {"protocol": memory["protocol"], "candidates": candidates[: args.limit]}


def command_audit(args: argparse.Namespace) -> dict:
    memory = load(args.db)
    issues = []
    seen_urls = {}
    references_by_id = {str(item.get("id")): item for item in memory["references"]}
    for reference in memory["references"]:
        key = canonical_url(reference.get("url", ""))
        if key in seen_urls:
            issues.append(f"duplicateUrl:{seen_urls[key]}:{reference.get('id')}")
        seen_urls[key] = reference.get("id")
    for pattern in memory["patterns"]:
        pattern_id = pattern.get("id")
        support = set(clean_list(pattern.get("supportReferenceIds")))
        counter = set(clean_list(pattern.get("counterexampleReferenceIds")))
        limits = set(clean_list(pattern.get("caseLimitReferenceIds")))
        if support & counter or support & limits or counter & limits:
            issues.append(f"overlappingEvidenceRoles:{pattern_id}")
        if int(pattern.get("supportingCount") or 0) != len(support):
            issues.append(f"supportingCount:{pattern_id}")
        if int(pattern.get("counterexampleCount") or 0) != len(counter):
            issues.append(f"counterexampleCount:{pattern_id}")
        if int(pattern.get("caseLimitCount") or 0) != len(limits):
            issues.append(f"caseLimitCount:{pattern_id}")
        if any(item not in references_by_id for item in support | counter | limits):
            issues.append(f"unknownReference:{pattern_id}")
    return {"ok": not issues, "issues": issues, "references": len(memory["references"]), "patterns": len(memory["patterns"])}


def command_stats(args: argparse.Namespace) -> dict:
    memory = load(args.db)
    stages = ["observation", "hypothesis", "supported_hypothesis", "provisional", "experimentally_validated", "contradicted", "inconclusive", "archived"]
    return {"protocol": memory["protocol"], "references": len(memory["references"]), "hypotheses": len(memory.get("hypotheses", [])), "patterns": {stage: sum(1 for item in memory["patterns"] if (item.get("stage") or item.get("status")) == stage) for stage in stages}, "caseLimits": sum(int(item.get("caseLimitCount") or 0) for item in memory["patterns"])}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--record", type=Path, required=True)
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--classification", type=Path, required=True)
    search_parser.add_argument("--limit", type=int, default=8)
    candidates_parser = subparsers.add_parser("candidates")
    candidates_parser.add_argument("--limit", type=int, default=12)
    subparsers.add_parser("stats")
    subparsers.add_parser("audit")
    args = parser.parse_args()

    if args.command == "add":
        result = command_add(args)
    elif args.command == "search":
        result = command_search(args)
    elif args.command == "candidates":
        result = command_candidates(args)
    elif args.command == "audit":
        result = command_audit(args)
    else:
        result = command_stats(args)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
