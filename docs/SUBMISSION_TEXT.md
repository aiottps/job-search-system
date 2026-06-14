# Career Quest Canvas Submission Text

## Project Title
Career Quest Canvas

## Tagline
Turn job-search anxiety into a confidence-building adventure.

## Keywords
Creative Apps, GitHub Copilot, Microsoft IQ, Foundry IQ, AI Career Coach, Career Storytelling, Job Search, Interview Game, Confidence Building, Grounded AI, Evidence-Based Recommendations, FastAPI, Adventure UI

## Short Description
Career Quest Canvas is a creative job-search storytelling app that turns anxiety into story, uncertainty into quests, and interviews into confidence-building games. Inspired by Journey to the West, it helps candidates discover their strengths, see the bright side of each opportunity, and generate a grounded, evidence-based career journey.

## Long Description
Career Quest Canvas is a Creative Apps hackathon project that reimagines job search as a confidence-building adventure.

Instead of only showing candidates what they lack, the app helps them discover their strengths, connect those strengths to a target job, turn uncertainty into small quests, and practice interviews as playful challenge stages. Inspired by Journey to the West, each job becomes a “mountain gate,” each skill becomes a “magic tool,” and each interview becomes a confidence-building trial.

The project uses a Foundry IQ-style grounded context layer to connect recommendations with local demo resumes, job descriptions, and company context. Each generated story, quest, and interview challenge is tied to citations, helping reduce unsupported claims while keeping the experience warm, creative, and encouraging.

Built as a FastAPI web demo with native HTML/CSS/JS, Career Quest Canvas runs locally without real external AI API, MSSQL, external network access, or real personal data.

## Microsoft IQ Explanation
Career Quest Canvas demonstrates a Foundry IQ-style grounded context layer. It does not call a live Microsoft cloud service in this demo. Instead, it uses a local adapter pattern with fictional demo resume, job, and company context to show how grounded evidence and citations can reduce unsupported claims. The GroundedContextService turns local sources into evidence snippets, while CitationBuilder deduplicates and attaches citations to generated outputs. The architecture is designed so the local adapter can later be replaced by real Microsoft Foundry IQ or Azure AI services.

## GitHub Copilot Usage

GitHub Copilot was used to help shape the project architecture, generate service and API structures, suggest tests, and improve documentation. The project documents GitHub Copilot-assisted development as part of the Creative Apps submission.

## Safety and Reliability
The demo uses fictional data only. It does not require real external AI API credentials, MSSQL, network access, or personal user data. Tests verify that the core adventure response, APIs, citations, and common secret patterns are handled safely.
