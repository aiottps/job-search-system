# Career Quest Canvas

**Tagline:** Turn job-search anxiety into a confidence-building adventure.

## Introduction

### English
Career Quest Canvas is a creative job-search storytelling app that turns anxiety into story, uncertainty into quests, and interviews into confidence-building games.

### 中文簡介
Career Quest Canvas 是一個求職冒險故事工坊。它把焦慮變成故事，把不確定變成任務，把面試變成遊戲，幫助求職者在每一關中看見自己的優點，累積信心，展現更好的自己。

## Creative Apps Track
This project is submitted to the **Creative Apps** track of the Microsoft Agents League Hackathon. 

It is not a typical job search tool; it's a creative application designed to build candidate confidence through storytelling, quests, and gamified interview preparation. By reframing the stressful job hunt as a "Journey to the West" style adventure, it helps users focus on their strengths and actionable steps.

## GitHub Copilot Collaboration

Career Quest Canvas was developed as a GitHub Copilot-assisted Creative Apps project.

GitHub Copilot was used to support:

* Product ideation and Creative Apps positioning
* Architecture prompting and service planning
* FastAPI web demo structure
* Adventure service design
* Grounded context and citation flow design
* Test case planning
* README, demo script, and submission text refinement

The project documents how GitHub Copilot helped shape the product direction, engineering structure, test coverage, and hackathon-ready documentation.

Final validation result:

* 29 automated tests passed
* 0 failed
* 0 errors
* Local web demo verified at http://127.0.0.1:8000

## Microsoft IQ / Foundry IQ-style Integration
- Career Quest Canvas demonstrates a **Foundry IQ-style grounded context layer**. It does not call a live Microsoft cloud service in this demo.
- Instead, it uses a **local adapter pattern** with fictional demo resume, job, and company context to show how grounded evidence and citations can reduce unsupported claims.
- `GroundedContextService` loads evidence snippets from local sources.
- `CitationBuilder` deduplicates citations and ensures all generated outputs (stories, tools, quests) are grounded in evidence.
- The architecture is designed so the local adapter can later be replaced by real Microsoft Foundry IQ or Azure AI services.

## Hackathon Judging Alignment

Career Quest Canvas aligns with the Creative Apps judging criteria:

* **Accuracy & Relevance**: Built specifically for the Creative Apps track with GitHub Copilot-assisted development and a Microsoft IQ-inspired grounded context layer.
* **Reasoning & Multi-step Thinking**: Uses a multi-step flow from grounded context to strengths, job bright spots, hero story, quests, interview game, and citations.
* **Creativity & Originality**: Reframes job search as a Journey to the West-inspired confidence adventure, turning anxiety into storytelling.
* **User Experience & Presentation**: Provides a warm, scroll-style one-page web demo with a clear 60-90 second presentation script.
* **Reliability & Safety**: Passes 29 automated tests, uses fictional demo data, avoids real secrets, and runs completely offline without Gemini API or network dependencies.


## How to Run
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python server.py
   ```
3. Open in your browser: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## How to Test
Run the automated test suite:
```bash
python -m pytest tests -v
```

## Validation Result
- **29 passed**
- 0 failed
- 0 errors
- 1 warning (Starlette deprecation)
- API endpoints verified
- Web UI verified locally at http://127.0.0.1:8000

## Safety & Reliability
- **Demo data only**: Uses fictional characters (張小凡) and companies.
- **No real PII**: No real personal identifiable information is included.
- **No secrets**: Scanned for secrets; only placeholders in `.env.example` exist.
- **No real Gemini API dependency**: The demo runs offline using local generation logic.
- **No real MSSQL dependency**: Uses a mock repository layer for the demo.
- **No network dependency**: Completely functional in a local environment.
- `.env.example` contains placeholder variable names only, not real credentials.

## Windows PowerShell UTF-8 Notes

If Chinese text appears as mojibake in PowerShell, run:

```powershell
chcp 65001
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()
$env:PYTHONUTF8 = "1"
```

Then test again:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/health | ConvertTo-Json -Depth 10
```

For a more stable JSON display on Windows, use:

```powershell
curl.exe -s http://127.0.0.1:8000/api/health | python -m json.tool
```

---
Developed with GitHub Copilot collaboration for the Microsoft Agents League Hackathon - Creative Apps Track.
