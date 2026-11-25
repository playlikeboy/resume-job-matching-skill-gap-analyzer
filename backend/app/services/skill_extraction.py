from __future__ import annotations

import re
from dataclasses import dataclass

from app.services.taxonomy import SKILLS

NEGATION_PATTERN = re.compile(
    r"\b(?:no\s+(?:prior\s+)?(?:experience|knowledge|background|familiarity)\s+(?:with|in)"
    r"|not\s+familiar\s+with"
    r"|never\s+used"
    r"|haven't\s+used"
    r"|have\s+not\s+used"
    r"|do\s+not\s+know)\s*$",
    re.IGNORECASE,
)


@dataclass
class ExtractedSkill:
    name: str
    category: str
    evidence: str
    alias_found: str
    match_start: int = 0
    match_end: int = 0
    occurrences: int = 1


def _pattern_for(
    term: str,
    *,
    case_sensitive: bool = False,
    excluded_following_words: list[str] | None = None,
) -> re.Pattern[str]:
    escaped = re.escape(term.strip()).replace(r"\ ", r"\s+")
    negative_after = ""
    if excluded_following_words:
        words = "|".join(re.escape(word) for word in excluded_following_words)
        negative_after = rf"(?!\s+(?:{words})\b)"
    flags = 0 if case_sensitive else re.IGNORECASE
    # Avoid accidental matches inside longer words while keeping punctuation-heavy skills usable.
    return re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9]){negative_after}", flags)


def _evidence_for(text: str, match: re.Match[str]) -> str:
    start = max(0, text.rfind("\n", 0, match.start()) + 1)
    end_candidates = [i for i in (text.find("\n", match.end()), text.find(".", match.end())) if i >= 0]
    end = min(end_candidates) + 1 if end_candidates else min(len(text), match.end() + 100)
    line = re.sub(r"\s+", " ", text[start:end]).strip()
    if len(line) > 220:
        left = max(0, match.start() - start - 75)
        line = "…" + line[left:left + 180].strip() + "…"
    return line or text[max(0, match.start() - 40):match.end() + 60].strip()


def _is_negated(text: str, match_start: int) -> bool:
    prefix = text[max(0, match_start - 55):match_start]
    return bool(NEGATION_PATTERN.search(prefix))


def extract_skills(text: str, *, ignore_negated: bool = True) -> dict[str, ExtractedSkill]:
    found: dict[str, ExtractedSkill] = {}
    for canonical, metadata in SKILLS.items():
        aliases = [canonical, *metadata.get("aliases", [])]
        case_sensitive_terms = set(metadata.get("case_sensitive_terms", []))
        excluded_following = metadata.get("excluded_following_words")

        best_match: re.Match[str] | None = None
        best_alias = canonical
        total_occurrences = 0

        for alias in aliases:
            pattern = _pattern_for(
                alias,
                case_sensitive=alias in case_sensitive_terms,
                excluded_following_words=excluded_following if alias.lower() == "express" else None,
            )
            matches = [
                m for m in pattern.finditer(text)
                if not (ignore_negated and _is_negated(text, m.start()))
            ]
            if not matches:
                continue
            total_occurrences += len(matches)
            first_match = matches[0]
            if best_match is None or first_match.start() < best_match.start():
                best_match = first_match
                best_alias = alias

        if best_match is not None:
            found[canonical] = ExtractedSkill(
                name=canonical,
                category=metadata["category"],
                evidence=_evidence_for(text, best_match),
                alias_found=best_alias,
                match_start=best_match.start(),
                match_end=best_match.end(),
                occurrences=total_occurrences,
            )
    return found
