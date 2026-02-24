from dataclasses import dataclass

from smart_resume_agent.tools.analysis_tools import (
    KeywordComparisonResult,
    compare_keywords,
)


@dataclass
class KeywordGapResult:
    """Structured keyword gap analysis between resume and job description."""

    comparison: KeywordComparisonResult


def keyword_gap_agent(resume_text: str, jd_text: str) -> KeywordGapResult:
    """
    Sub-agent that computes the keyword overlap and gap between resume and JD.

    Args:
        resume_text: Parsed resume text.
        jd_text: Job description text.

    Returns:
        KeywordGapResult wrapping KeywordComparisonResult for downstream use.
    """
    comparison = compare_keywords(resume_text=resume_text, jd_text=jd_text)
    return KeywordGapResult(comparison=comparison)

