"""
Root orchestrator definition for the Smart Resume Analyzer.

This module exposes:
- ``orchestrate_resume_analysis``: a deterministic, multi-step Python pipeline.
- ``root_agent``: an ADK ``Agent`` configured to use ``gemini-2.5-flash`` in
  pure-chat mode (no function calling or tools).

The ADK agent is intentionally tool-less because ``gemini-2.5-flash`` in this
environment does not support function calling. The orchestration pipeline is
still available for direct invocation from Python (for tests or scripts).
"""

from dataclasses import asdict
from typing import Any, Dict

from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search

from smart_resume_agent.sub_agents.job_analyzer import JobAnalysisResult, job_analyzer_agent
from smart_resume_agent.sub_agents.keyword_gap import KeywordGapResult, keyword_gap_agent
from smart_resume_agent.sub_agents.report_generator import (
    ReportGenerationResult,
    report_generator_agent,
)
from smart_resume_agent.sub_agents.resume_parser import ResumeParseResult, resume_parser_agent
from smart_resume_agent.tools.analysis_tools import KeywordComparisonResult, compare_keywords
from smart_resume_agent.tools.file_tools import extract_pdf_text
from smart_resume_agent.tools.report_tools import generate_markdown_report


def orchestrate_resume_analysis(resume_path: str, job_description: str) -> Dict[str, Any]:
    """
    High-level orchestration function used as a tool by the root agent.

    This function demonstrates a **sequential multi-agent pattern**:
    1. Resume Parser sub-agent: extract resume text from PDF.
    2. Job Analyzer sub-agent: normalize job description and infer a job title.
    3. Keyword Gap sub-agent: compute overlap and match percentage.
    4. Report Generator sub-agent: persist a markdown report.

    Args:
        resume_path: Path to the candidate's resume (PDF).
        job_description: Raw job description text.

    Returns:
        A structured dictionary summarizing the full analysis, including
        the path to the generated report.
    """
    # 1. Resume parsing
    resume_result: ResumeParseResult = resume_parser_agent(resume_path)

    # 2. Job analysis (LLM will complement this with google_search as needed)
    job_result: JobAnalysisResult = job_analyzer_agent(job_description)

    # 3. Keyword gap analysis
    gap_result: KeywordGapResult = keyword_gap_agent(
        resume_text=resume_result.raw_text,
        jd_text=job_result.jd_text,
    )

    comparison: KeywordComparisonResult = gap_result.comparison

    # 4. Report generation payload
    report_payload: Dict[str, Any] = {
        "resume_path": resume_result.resume_path,
        "job_title": job_result.job_title,
        "match_percentage": comparison.match_percentage,
        "matched_keywords": comparison.matched_keywords,
        "missing_keywords": comparison.missing_keywords,
        "resume_only_keywords": comparison.resume_only_keywords,
        # The root LLM agent is expected to refine and overwrite this field
        # with richer narrative suggestions, but we provide a safe default.
        "suggestions": (
            "Review the missing keywords and consider weaving the most relevant ones "
            "into your experience, skills, and summary sections where they truthfully "
            "reflect your background."
        ),
    }

    report_result: ReportGenerationResult = report_generator_agent(report_payload)

    return {
        "resume": asdict(resume_result),
        "job": asdict(job_result),
        "keyword_comparison": asdict(comparison),
        "report": asdict(report_result),
    }


__all__ = ["orchestrate_resume_analysis", "root_agent"]


root_agent = Agent(
    model="gemini-2.5-flash",
    name="smart_resume_agent",
    description=(
        "A professional multi-agent system that analyzes a candidate's resume "
        "against a job description, leveraging Google Search for up-to-date "
        "skills and role expectations."
    ),
    instruction=(
        "You are the orchestrator of a multi-agent Smart Resume Analyzer. "
        "Given a resume file path and a job description, you conceptually run a "
        "deterministic pipeline that performs resume parsing, job analysis, keyword "
        "gap analysis, and report generation. You do not invoke tools or function "
        "calling at runtime for this model; instead, reason directly over the "
        "user-provided text and any precomputed analysis artifacts.\n"
        "Use both the structured information provided by the user and your own "
        "reasoning to provide:\n"
        "   - A concise match summary.\n"
        "   - Missing or weakly represented skills and keywords.\n"
        "   - Clear, actionable suggestions to improve the resume.\n"
        "Always:\n"
        "- Explain your reasoning in simple, professional language.\n"
        "- Avoid fabricating experience; suggest only truthful enhancements.\n"
        "- If the resume file cannot be read, ask the user to verify the path."
    ),
    # No tools configured here because `gemini-2.5-flash` in this environment
    # does not support function calling / tool use. The multi-agent pipeline
    # is implemented in pure Python and can be invoked directly from code.
)

