# Personal Job Search Assistant

A personal job search assistant system designed for candidates.

## Features
- Daily job search on 104 and 1111 (Contract defined, Playwright logic TODO).
- LinkedIn Manual Import (Automated scraping strictly prohibited).
- Candidate-oriented analysis using Gemini.
- MSSQL database for job tracking and company reviews.
- Daily email notifications via GitHub Actions.

## Tech Stack
- Python 3.11+
- Playwright (Web scraping)
- MSSQL (Database)
- Gemini API (Analysis)
- GitHub Actions (Scheduling)

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Install Playwright browsers: `playwright install chromium`
4. Copy `.env.example` to `.env` and fill in your credentials.
5. Initialize the database using `app/db/models.sql`.

## Windows User Notes
If you are using Windows PowerShell, please run the following commands to ensure proper UTF-8 handling and environment configuration:
```powershell
chcp 65001
$env:PYTHONUTF8="1"
```

### Troubleshooting: Windows Python / pip / pytest
If you encounter `CommandNotFound` or if `pip`/`pytest` cannot be found even after installation:
1. **Avoid direct commands:** Always use the `python -m` prefix to ensure you are using the correct Python environment.
   - Use `python -m pip install -r requirements.txt` instead of `pip install`.
   - Use `python -m pytest tests -v` instead of `pytest`.
2. **Check Python Stub:** If your `python` command points to `WindowsApps/python.exe`, it is a Microsoft Store stub. We highly recommend:
   - Installing formal Python from [python.org](https://www.python.org/).
   - Disabling "App execution aliases" for `python.exe` and `python3.exe` in Windows Settings.
3. **Encoding Issues:** If you see garbled characters or mojibake in the terminal, ensure you've run `chcp 65001`.

## Usage & Local Testing

### Configuration
You can customize your job search preferences in `.env`:
- `JOB_KEYWORDS`: Comma-separated list of keywords (e.g. `Data Engineer,Python`).
- `JOB_LOCATIONS`: Comma-separated list of locations (e.g. `桃園市,遠端`).
- `MIN_ANNUAL_SALARY`: Minimum annual salary (e.g. `800000`).

### Run Mock Search
To test the pipeline logic without external dependencies:
```bash
cd job-search-system
python -m app.main --mode mock
```
**Current Implementation Status:**
- `Collector104` and `Collector1111` currently use **Mock Data** to verify the pipeline logic.
- Real-world scraping via **Playwright** is the next development phase.

### Run Tests
To run automated unit tests for normalizers and collector contracts:
```bash
cd job-search-system
python -m pytest tests -v
```

### Collector Contract
All collectors must return a list of dictionaries with the following fields:
- `source`: Platform name (e.g., "104").
- `title`: Job title (Required).
- `company_name`: Hiring company (Required).
- `location`: Location text (Required).
- `salary_text`: Salary description (Required).
- `job_url`: Link to the job (Required, must start with http/https).
- `jd_text`: Full job description (Required).
- `source_job_id`: Platform-specific ID (Optional).

## LinkedIn Policy
LinkedIn automated login or scraping is NOT supported to comply with their terms of service. Users can manually provide job descriptions or URLs for analysis.

## Inclusive Interview Support / 無障礙面試支援
Our system is committed to inclusive and non-discriminatory job search assistance:
- **Gender Neutrality:** Gender identity and preferred names are used only for communication preferences and will never affect job matching, competency scores, or professional recommendations.
- **Accessibility Accommodation:** Support for accessibility needs (e.g., sign language interpreters, live captions, wheelchair access) is treated as essential logistics. These needs are converted into actionable checklists for candidates and are **never** flagged as risks or negative factors.
- **Data-Driven Analysis:** Company analysis, resume optimization, and interview focuses are derived strictly from the Job Description (JD) and verified public sources.
- **Transparency:** If company or job information is insufficient, the system will explicitly output "資料不足" rather than fabricating reviews or market data.

## Company Inclusion Evidence Analysis / 公司包容性來源分析
The system provides preliminary, evidence-based signals regarding workplace inclusion and accessibility:
- **Evidence-Based:** Signals are identified only from provided sources (official reports, news, reviews). No conclusion is generated without a source.
- **Source Transparency:** Each analysis category groups the relevant sources used, allowing candidates to review the underlying evidence for detected signals.
- **No Stereotyping:** Analysis does not produce stereotypical inferences or capability judgements related to gender or accessibility needs.
- **Reliability Awareness:** Information from low-reliability sources (like anonymous forum posts) is explicitly marked to ensure candidate caution.
- **Transparent Limitations:** When data is missing for specific categories, the system explicitly labels them as "資料不足" (Insufficient Data).
- **Practical Guidance:** Generates confirmation questions for candidates to use during interviews to verify inclusion policies directly.

## Deployment
The system is designed to run on GitHub Actions. Ensure all required secrets (DB, Gemini, SMTP) are configured in your repository settings.
