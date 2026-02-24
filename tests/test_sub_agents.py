from smart_resume_agent.sub_agents.job_analyzer import job_analyzer_agent
from smart_resume_agent.sub_agents.keyword_gap import keyword_gap_agent
from smart_resume_agent.sub_agents.resume_parser import ResumeParseResult, resume_parser_agent


def test_job_analyzer_agent_extracts_title() -> None:
    jd = """Senior Data Engineer

We are looking for a data engineer with experience in Python and SQL."""

    result = job_analyzer_agent(jd)

    assert result.job_title == "Senior Data Engineer"
    assert "data engineer" in result.jd_text.lower()


def test_keyword_gap_agent_wraps_comparison() -> None:
    resume_text = "Python SQL Docker"
    jd_text = "Python Go SQL"

    result = keyword_gap_agent(resume_text=resume_text, jd_text=jd_text)

    comparison = result.comparison
    assert "python" in comparison.matched_keywords
    assert "sql" in comparison.matched_keywords
    assert "go" in comparison.missing_keywords


def test_resume_parser_agent_delegates_to_extract(monkeypatch) -> None:
    def fake_extract(path: str) -> str:
        assert path == "dummy.pdf"
        return "Sample Resume Text"

    monkeypatch.setattr(
        "smart_resume_agent.sub_agents.resume_parser.extract_pdf_text",
        fake_extract,
    )

    result: ResumeParseResult = resume_parser_agent("dummy.pdf")

    assert result.resume_path == "dummy.pdf"
    assert result.raw_text == "Sample Resume Text"

