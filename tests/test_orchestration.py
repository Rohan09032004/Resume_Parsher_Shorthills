from smart_resume_agent.agent import orchestrate_resume_analysis
from smart_resume_agent.sub_agents import resume_parser


def test_orchestrate_resume_analysis_uses_pipeline(monkeypatch) -> None:
    # Monkeypatch PDF extraction so we don't need a real file.
    def fake_extract_pdf_text(path: str) -> str:
        assert path == "dummy_resume.pdf"
        return "Python SQL Docker"

    monkeypatch.setattr(resume_parser, "extract_pdf_text", fake_extract_pdf_text)

    jd_text = "We are looking for a Software Engineer with strong Python and SQL skills."

    result = orchestrate_resume_analysis("dummy_resume.pdf", jd_text)

    # Basic structural checks
    assert "resume" in result
    assert "job" in result
    assert "keyword_comparison" in result
    assert "report" in result

    comparison = result["keyword_comparison"]
    assert comparison["match_percentage"] > 0
    assert "python" in comparison["matched_keywords"]

