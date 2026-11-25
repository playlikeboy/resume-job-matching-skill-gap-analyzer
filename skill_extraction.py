from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.taxonomy import SKILLS


@dataclass
class ExtractedSkill:
    name: str
    category: str
    evidence: str
    alias_found: str


def _pattern_for(term: str) -> re.Pattern[str]:
    escaped = re.escape(term.strip()).replace(r"\ ", r"\s+")
    # Avoid accidental matches inside longer words while keeping punctuation-heavy skills usable.
    return re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)


def _evidence_for(text: str, match: re.Match[str]) -> str:
    start = max(0, text.rfind("\n", 0, match.start()) + 1)
    end_candidates = [i for i in (text.find("\n", match.end()), text.find(".", match.end())) if i >= 0]
    end = min(end_candidates) + 1 if end_candidates else min(len(text), match.end() + 100)
    line = re.sub(r"\s+", " ", text[start:end]).strip()
    if len(line) > 220:
        left = max(0, match.start() - start - 75)
        line = "…" + line[left:left + 180].strip() + "…"
    return line or text[max(0, match.start() - 40):match.end() + 60].strip()


def extract_skills(text: str) -> dict[str, ExtractedSkill]:
    found: dict[str, ExtractedSkill] = {}
    for canonical, metadata in SKILLS.items():
        aliases = [canonical, *metadata.get("aliases", [])]
        # Prefer the first alias that yields evidence. Canonical names appear first.
        for alias in aliases:
            match = _pattern_for(alias).search(text)
            if match:
                found[canonical] = ExtractedSkill(
                    name=canonical,
                    category=metadata["category"],
                    evidence=_evidence_for(text, match),
                    alias_found=alias,
                )
                break
    return found
