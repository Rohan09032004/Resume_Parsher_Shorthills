from dataclasses import dataclass

from smart_resume_agent.tools.file_tools import extract_pdf_text


@dataclass
class ResumeParseResult:
    """Structured output representing parsed resume text."""

    resume_path: str
    raw_text: str


def resume_parser_agent(resume_path: str) -> ResumeParseResult:
    """
    Sub-agent responsible for parsing and extracting text from a resume file.

    Args:
        resume_path: Path to the resume PDF file.

    Returns:
        ResumeParseResult containing the extracted text.
    """
    text = extract_pdf_text(resume_path)
    return ResumeParseResult(resume_path=resume_path, raw_text=text)

