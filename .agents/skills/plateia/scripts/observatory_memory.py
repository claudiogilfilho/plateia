#!/usr/bin/env python3
"""Portable JSON memory for Platéia references and provisional patterns."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path


def empty_memory() -> dict:
    return {"protocol": "plateia-memory/1.0", "references": [], "patterns": []}


def load(path: Path) -> dict:
    if not path.exists():
        return empty_memory()
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("protocol") != "plateia-memory/1.0":
        raise SystemExit("Arquivo de memória incompatível.")
    value.setdefault("references", [])
    value.setdefault("patterns", [])
    return value


def save(path: Path, memory: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")


def normalized(value: str) -> str:
    raw = unicodedata.normalize("NFD", value or "")
    raw = "".join(char for char in raw if unicodedata.category(char) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", " ", raw).strip()


def overlap(left: list[str], right: list[str]) -> bool:
    return bool(set(left) & set(right))


def similarity(target: dict, candidate: dict) -> int:
    score = 0
    if target.get("primaryFamily") == candidate.get("primaryFamily"):
        score += 30
    if overlap([target.get("primaryFamily", ""), *target.get("secondaryFamilies", [])], [candidate.get("primaryFamily", ""), *candidate.get("secondaryFamilies", [])]):
        score += 10
    if overlap(target.get("objectives", []), candidate.get("objectives", [])):
        score += 18
    if normalized(target.get("segment", "")) == normalized(candidate.get("segment", "")):
        score += 15
    if overlap(target.get("presentationFormats", []), candidate.get("presentationFormats", [])):
        score += 8
    if target.get("materialFormat") == candidate.get("materialFormat"):
        score += 6
    if target.get("awarenessStage") == candidate.get("awarenessStage"):
        score += 4
    if target.get("productionLevel") == candidate.get("productionLevel"):
        score += 3
    if target.get("durationBand") == candidate.get("durationBand"):
        score += 3
    if target.get("pace") == candidate.get("pace"):
        score += 3
    if overlap(target.get("mechanisms", []), candidate.get("mechanisms", [])):
        score += 10
    return min(100, score)


def level(target: dict, candidate: dict, score: int) -> int:
    same_family = target.get("primaryFamily") == candidate.get("primaryFamily")
    same_objective = overlap(target.get("objectives", []), candidate.get("objectives", []))
    same_segment = normalized(target.get("segment", "")) == normalized(candidate.get("segment", ""))
    if same_family and same_objective and same_segment and score >= 65:
        return 1
    if same_family and same_objective and score >= 48:
        return 2
    if overlap(target.get("mechanisms", []), candidate.get("mechanisms", [])) and score >= 25:
        return 3
    return 4


def consolidate(memory: dict, reference: dict) -> None:
    classification = reference.get("classification", {})
    objective = (classification.get("objectives") or ["indeterminado"])[0]
    for hypothesis in reference.get("training", {}).get("hypotheses", [])[:5]:
        name = str(hypothesis.get("name", "")).strip()
        if not name:
            continue
        fingerprint = "|".join(normalized(item) for item in [name, classification.get("primaryFamily", ""), objective, classification.get("segment", "")])
        pattern = next((item for item in memory["patterns"] if item.get("fingerprint") == fingerprint), None)
        contradicted = hypothesis.get("stage") == "contradicted"
        evidence = {"referenceId": reference["id"], "observation": hypothesis.get("observation", ""), "evidence": hypothesis.get("evidence", ""), "limitations": hypothesis.get("limitations", [])}
        if pattern is None:
            pattern = {"id": str(uuid.uuid4()), "fingerprint": fingerprint, "name": name, "creativeFamily": classification.get("primaryFamily", ""), "objective": objective, "segment": classification.get("segment", ""), "mechanism": hypothesis.get("mechanism", ""), "stage": "contradicted" if contradicted else "observation", "supportingCount": 0 if contradicted else 1, "counterexampleCount": 1 if contradicted else 0, "confidence": "low", "evidence": [evidence]}
            memory["patterns"].append(pattern)
            continue
        pattern["supportingCount"] += 0 if contradicted else 1
        pattern["counterexampleCount"] += 1 if contradicted else 0
        pattern["evidence"] = [*pattern.get("evidence", []), evidence][-20:]
        if pattern["counterexampleCount"] >= pattern["supportingCount"] and pattern["counterexampleCount"] >= 2:
            pattern["stage"], pattern["confidence"] = "contradicted", "low"
        elif pattern.get("stage") == "validated":
            pattern["confidence"] = "high"
        elif pattern["supportingCount"] >= 3:
            pattern["stage"] = "provisional"
            pattern["confidence"] = "high" if pattern["supportingCount"] >= 5 else "medium"
        else:
            pattern["stage"], pattern["confidence"] = "hypothesis", "low"


def command_add(args: argparse.Namespace) -> dict:
    memory = load(args.db)
    record = json.loads(args.record.read_text(encoding="utf-8"))
    record.setdefault("id", str(uuid.uuid4()))
    record.setdefault("createdAt", datetime.now(timezone.utc).isoformat())
    if not isinstance(record.get("classification"), dict):
        raise SystemExit("A referência precisa de classification.")
    if any(item.get("id") == record["id"] for item in memory["references"]):
        raise SystemExit("Já existe uma referência com este id.")
    memory["references"].append(record)
    consolidate(memory, record)
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, required=True)
    subparsers = parser.add_subparsers(dest="command", required=True)
    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--record", type=Path, required=True)
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--classification", type=Path, required=True)
    search_parser.add_argument("--limit", type=int, default=8)
    subparsers.add_parser("stats")
    args = parser.parse_args()

    if args.command == "add":
        result = command_add(args)
    elif args.command == "search":
        result = command_search(args)
    else:
        memory = load(args.db)
        result = {"protocol": memory["protocol"], "references": len(memory["references"]), "patterns": {stage: sum(1 for item in memory["patterns"] if item.get("stage") == stage) for stage in ["observation", "hypothesis", "provisional", "validated", "contradicted", "obsolete"]}}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
