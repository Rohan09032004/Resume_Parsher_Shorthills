from dataclasses import dataclass
from typing import Optional


@dataclass
class JobAnalysisResult:
    """Summary of a job description and inferred key skills."""

    job_title: Optional[str]
    jd_text: str
    inferred_keywords: list[str]
    market_insights: str


def job_analyzer_agent(job_description: str) -> JobAnalysisResult:
    """
    Lightweight preprocessing for job descriptions before Gemini analysis.

    This sub-agent does not call external services itself; instead, it
    prepares a clean payload for the root LLM agent, which can then
    invoke `google_search` for deeper market research when needed.

    Args:
        job_description: Raw job description text provided by the user.

    Returns:
        JobAnalysisResult with a placeholder structure. The LLM will refine
        `inferred_keywords` and `market_insights` using its reasoning and tools.
    """
    normalized = job_description.strip()

    # Very basic heuristic to guess job title (first line or first sentence).
    job_title: Optional[str] = None
    if normalized:
        first_line = normalized.splitlines()[0]
        job_title = first_line.strip().rstrip(".")

    return JobAnalysisResult(
        job_title=job_title,
        jd_text=normalized,
        inferred_keywords=[],
        market_insights="",
    )

