from dataclasses import dataclass
from typing import Any, Dict

from smart_resume_agent.tools.report_tools import generate_markdown_report


@dataclass
class ReportGenerationResult:
    """Represents the outcome of markdown report generation."""

    report_path: str


def report_generator_agent(report_payload: Dict[str, Any]) -> ReportGenerationResult:
    """
    Sub-agent responsible for persisting the final markdown report.

    Args:
        report_payload: A dictionary payload containing all information needed
            to render the final report. See `generate_markdown_report` for the
            expected structure.

    Returns:
        ReportGenerationResult with the saved report path.
    """
    report_path = generate_markdown_report(report_payload)
    return ReportGenerationResult(report_path=report_path)

