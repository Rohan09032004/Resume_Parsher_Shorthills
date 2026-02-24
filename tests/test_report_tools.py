from pathlib import Path

from smart_resume_agent.tools.report_tools import generate_markdown_report


def test_generate_markdown_report_creates_file(tmp_path: Path) -> None:
    output_dir = tmp_path / "reports_out"
    data = {
        "resume_path": "/path/to/resume.pdf",
        "job_title": "Software Engineer",
        "match_percentage": 80.0,
        "matched_keywords": ["python", "sql"],
        "missing_keywords": ["kubernetes"],
        "resume_only_keywords": ["docker"],
        "suggestions": "Highlight your Kubernetes experience and impact in previous roles.",
    }

    report_path_str = generate_markdown_report(data, output_dir=str(output_dir))
    report_path = Path(report_path_str)

    assert report_path.exists()

    contents = report_path.read_text(encoding="utf-8")
    assert "Smart Resume Analyzer Report" in contents
    assert "Software Engineer" in contents
    assert "80.00%" in contents
    assert "kubernetes" in contents

