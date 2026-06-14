# Hackathon Tech Stack & Assistance

This project was developed for the Microsoft Agents League Hackathon using a combination of advanced AI tools.

## AI Assistance
1. **GitHub Copilot**: 
   - Initial architecture and prompting were designed for GitHub Copilot.
   - Core adventure services and logical flow were co-authored with Copilot to maintain a consistent creative tone.
2. **Gemini CLI (Auto-Edit Mode)**:
   - Significant implementation, file transformations, and project restructuring were assisted by the Gemini CLI agent.
   - Used for complex file editing and directory management during the transformation from a CLI tool to a Web Demo.

## Implementation Details
- **FastAPI**: Used for the backend server and API endpoints.
- **Native Web**: The frontend was built using native HTML/CSS/JS to ensure zero dependencies and reliable performance.
- **Microsoft IQ Strategy**: The grounded context layer was implemented as a local Foundry IQ-style adapter to ensure evidence-based responses without requiring cloud dependencies for the demo.

## Test Authoring
- Automated tests were generated with AI assistance to ensure high reliability and security, specifically focusing on data grounding and secret prevention.
