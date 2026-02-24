from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


def generate_markdown_report(data: Dict[str, Any], output_dir: Optional[str] = None) -> str:
    """
    Generate a structured markdown report for the resume analysis.

    Args:
        data: A dictionary containing structured analysis results. Expected keys:
            - resume_path: str
            - job_title: Optional[str]
            - match_percentage: float
            - matched_keywords: list[str]
            - missing_keywords: list[str]
            - resume_only_keywords: list[str]
            - suggestions: str
        output_dir: Optional directory where the report should be saved.
            Defaults to a local `reports` folder in the project.

    Returns:
        The absolute path to the generated markdown report.
    """
    output_root = Path(output_dir) if output_dir is not None else Path("reports")
    output_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    report_path = output_root / f"resume_analysis_{timestamp}.md"

    resume_path = data.get("resume_path", "N/A")
    job_title = data.get("job_title") or "Target Role"
    match_percentage = data.get("match_percentage", 0.0)
    matched_keywords = data.get("matched_keywords") or []
    missing_keywords = data.get("missing_keywords") or []
    resume_only_keywords = data.get("resume_only_keywords") or []
    suggestions = data.get("suggestions") or "No suggestions provided."

    report_lines: list[str] = [
        f"# Smart Resume Analyzer Report",
        "",
        f"- **Generated at**: {datetime.now().isoformat(timespec='seconds')}",
        f"- **Resume path**: `{resume_path}`",
        f"- **Target role**: {job_title}",
        f"- **Match percentage**: **{match_percentage:.2f}%**",
        "",
        "## 1. Summary",
        "",
        f"The candidate's resume matches approximately **{match_percentage:.2f}%** of the keywords and concepts "
        "present in the provided job description. The sections below detail overlapping and missing skills, "
        "as well as concrete improvement suggestions.",
        "",
        "## 2. Matched Keywords",
        "",
    ]

    if matched_keywords:
        report_lines.extend([f"- {kw}" for kw in matched_keywords])
    else:
        report_lines.append("_No significant keyword matches detected._")

    report_lines.extend(
        [
            "",
            "## 3. Missing / Low-Frequency Keywords",
            "",
        ]
    )

    if missing_keywords:
        report_lines.extend([f"- {kw}" for kw in missing_keywords])
    else:
        report_lines.append("_No obvious missing keywords detected._")

    report_lines.extend(
        [
            "",
            "## 4. Resume-Only Keywords",
            "",
        ]
    )

    if resume_only_keywords:
        report_lines.extend([f"- {kw}" for kw in resume_only_keywords])
    else:
        report_lines.append("_No extra resume-only keywords identified._")

    report_lines.extend(
        [
            "",
            "## 5. Strategic Recommendations",
            "",
            suggestions,
            "",
        ]
    )

    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    return str(report_path.resolve())

