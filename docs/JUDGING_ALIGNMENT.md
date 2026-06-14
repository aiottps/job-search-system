# Judging Alignment

Career Quest Canvas is designed for the Microsoft Agents League Hackathon - Creative Apps track.

## Track Fit: Creative Apps

This project is not a traditional job search tool. It is a creative application that transforms job-search anxiety into an interactive, confidence-building adventure. Inspired by Journey to the West, it turns job opportunities into “mountain gates,” candidate strengths into “magic tools,” uncertainty into quests, and interviews into game-like challenges.

## Required Microsoft IQ Layer

The demo includes a **Foundry IQ-style grounded context layer**.

**Important scope note:**
This demo does not call a live Microsoft cloud service. It uses a local adapter pattern to demonstrate the IQ concept: grounding outputs in resume, job description, and company context, then attaching citations to reduce unsupported claims. The architecture is designed to be plug-and-play with real Microsoft Foundry IQ services in the future.

## Scoring Alignment

### Accuracy & Relevance (20%)

How the project aligns:

* Built specifically for Creative Apps.
* Uses GitHub Copilot-assisted development and documents the collaboration.
* Includes a Microsoft IQ-inspired grounded context layer (local adapter).
* Runs locally as a stable, verified web demo.

Evidence:

* `README.md`
* `docs/SUBMISSION_TEXT.md`
* `docs/COPILOT_USAGE.md`
* `docs/IQ_INTEGRATION.md`

### Reasoning & Multi-step Thinking (20%)

How the project aligns:

* Uses a multi-step career reasoning flow:
  1. Load grounded candidate resume, job description, and company context.
  2. Identify candidate strengths (Magic Tools).
  3. Identify job bright spots (Gate Advantages).
  4. Generate a hero story (Personal Journey).
  5. Convert uncertainty into small quests (Mission Scroll).
  6. Generate interview game challenges (Monster Trial).
  7. Attach citations to all outputs.

Evidence:

* `app/adventure/adventure_service.py`
* `app/iq/grounded_context_service.py`
* `app/iq/citation_builder.py`

### Creativity & Originality (15%)

How the project aligns:

* Reimagines job search as a Journey to the West-inspired adventure.
* Turns stressful career preparation into storytelling, quests, badges, and interview games.
* Focuses on encouragement instead of shame or deficit-only analysis.

Evidence:

* `web/index.html`
* `web/styles.css`
* `docs/DEMO_SCRIPT.md`

### User Experience & Presentation (15%)

How the project aligns:

* One-page FastAPI web demo.
* Native HTML/CSS/JS for zero-dependency reliability.
* Warm, scroll-like visual style for immersive storytelling.
* 60-90 second demo script focused on user impact.
* User can select a job and generate the full adventure in one click.

Evidence:

* `web/index.html`
* `web/app.js`
* `web/styles.css`
* `docs/DEMO_SCRIPT.md`

### Reliability & Safety (20%)

How the project aligns:

* **Pytest final result: 29 passed, 0 failed, 0 errors, 1 warning.**
* Runs without real external AI API (uses local fallback logic).
* Runs without MSSQL (uses local mock repository).
* Runs without external network (demo-friendly).
* Uses fictional demo data only (張小凡).
* Secret scan found only placeholder values in `.env.example`.
* API responses follow consistent success/data/message structure.

Evidence:

* `tests/`
* `.env.example`
* `README.md`
* `docs/SECURITY_CHECKLIST.md`

### Community Vote (10%)

How the project aligns:

* Clear tagline: "Turn job-search anxiety into a confidence-building adventure."
* Memorable concept: anxiety → story, uncertainty → quests, interview → game.
* Easy to explain in a 60-90 second demo.

Evidence:

* `docs/SUBMISSION_TEXT.md`
* `docs/DEMO_SCRIPT.md`

## Final Submission Readiness

**Status:** Hackathon Ready

**Known scope limitation:**
The Microsoft IQ layer is implemented as a local Foundry IQ-style adapter for demo purposes, not as a live Microsoft cloud integration.

**Recommended submission wording:**
“Career Quest Canvas demonstrates a Foundry IQ-style grounded context layer using local demo evidence and citations. The architecture is designed so the local adapter can later be replaced by real Microsoft Foundry IQ or Azure AI services.”
