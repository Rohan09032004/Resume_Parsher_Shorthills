import math

from smart_resume_agent.tools.analysis_tools import compare_keywords


def test_compare_keywords_basic_overlap() -> None:
    resume_text = "Python SQL Docker"
    jd_text = "Python Go SQL"

    result = compare_keywords(resume_text=resume_text, jd_text=jd_text)

    # JD vocab = {python, go, sql}
    # Matched = {python, sql}
    # Missing = {go}
    # Resume-only = {docker}
    assert sorted(result.matched_keywords) == ["python", "sql"]
    assert result.missing_keywords == ["go"]
    assert result.resume_only_keywords == ["docker"]
    assert math.isclose(result.match_percentage, (2 / 3) * 100, rel_tol=1e-3)

