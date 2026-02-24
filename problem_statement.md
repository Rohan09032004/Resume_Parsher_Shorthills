# Problem Statement: Smart Resume Analyzer using Multi-Agent System

## Objective
The goal of this project is to design and implement a functional multi-agent system using Google ADK that analyzes a candidate's resume against a given job description and provides actionable improvement suggestions.

## Background
Job applicants often struggle to tailor their resumes according to specific job descriptions. Many resumes get rejected by Applicant Tracking Systems (ATS) due to missing keywords or poor alignment with job requirements.

## Problem
Build an intelligent agentic system that:

- Extracts text from a resume (PDF/DOCX)
- Analyzes the provided job description
- Uses web search to identify important skills and keywords
- Compares the resume with job requirements
- Generates a structured improvement report

## Expected Outcome
The system should accept:

**Input:**
- Resume file path
- Job description text

**Output:**
- Missing keywords
- Match percentage
- Improvement suggestions
- Generated markdown report

## Agent Architecture
The system will include:

- Root Orchestrator Agent
- Resume Parser Agent
- Job Analyzer Agent
- Keyword Gap Agent
- Report Generator Agent

## Tools to be Used
- Built-in `google_search` tool (mandatory)
- Custom tools:
  - extract_pdf_text(filepath)
  - compare_keywords(resume_text, jd_text)
  - generate_markdown_report(data)

## Success Criteria
- System runs via `adk run` and `adk web`
- Demonstrates multi-agent orchestration
- Uses Gemini stable model
- Produces meaningful resume feedback