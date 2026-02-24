from collections import Counter
from dataclasses import dataclass
from typing import Iterable


@dataclass
class KeywordComparisonResult:
    """Structured result for resume vs job description keyword comparison."""

    matched_keywords: list[str]
    missing_keywords: list[str]
    resume_only_keywords: list[str]
    match_percentage: float


def _normalize_tokens(text: str) -> list[str]:
    """Tokenize and normalize a block of text into lowercase word tokens."""
    separators = {",", ".", ";", ":", "/", "\\", "(", ")", "[", "]", "{", "}", "|", "-", "_", "\n", "\t"}
    normalized = text.lower()
    for sep in separators:
        normalized = normalized.replace(sep, " ")
    tokens = [token for token in normalized.split(" ") if token]
    return tokens


def compare_keywords(resume_text: str, jd_text: str) -> KeywordComparisonResult:
    """
    Compare resume text against a job description and compute keyword overlap.

    This is a lightweight, deterministic analysis that complements the
    Gemini-based reasoning of the agents.

    Args:
        resume_text: Full text extracted from the candidate's resume.
        jd_text: Job description text.

    Returns:
        KeywordComparisonResult: Structured comparison including overlap and match score.
    """
    resume_tokens = _normalize_tokens(resume_text)
    jd_tokens = _normalize_tokens(jd_text)

    resume_counts = Counter(resume_tokens)
    jd_counts = Counter(jd_tokens)

    resume_vocab = set(resume_counts.keys())
    jd_vocab = set(jd_counts.keys())

    matched = sorted(jd_vocab & resume_vocab)
    missing = sorted(jd_vocab - resume_vocab)
    resume_only = sorted(resume_vocab - jd_vocab)

    match_percentage = 0.0
    if jd_vocab:
        match_percentage = round(len(matched) / len(jd_vocab) * 100, 2)

    return KeywordComparisonResult(
        matched_keywords=matched,
        missing_keywords=missing,
        resume_only_keywords=resume_only,
        match_percentage=match_percentage,
    )

