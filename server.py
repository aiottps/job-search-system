from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import json
from typing import Optional

from app.iq.grounded_context_service import GroundedContextService
from app.iq.citation_builder import CitationBuilder
from app.adventure.adventure_service import AdventureService
from app.adventure.interview_game_service import InterviewGameService

app = FastAPI(title="Career Quest Canvas")

# Initialize Services
iq_service = GroundedContextService(demo_data_dir="demo_data")
adventure_service = AdventureService(iq_service)
interview_game_service = InterviewGameService()

# Request Models
class AdventureRequest(BaseModel):
    job_id: str

# Serve static files
# Ensure the web directory exists
if not os.path.exists("web"):
    os.makedirs("web")

app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/")
async def read_index():
    return FileResponse("web/index.html")

@app.get("/api/health")
async def health_check():
    return {
        "success": True,
        "data": {
            "status": "ok",
            "app": "Career Quest Canvas"
        },
        "message": "取經路已開啟"
    }

@app.get("/api/iq/evidence")
async def get_iq_evidence():
    contexts = iq_service.get_all_contexts()
    builder = CitationBuilder()
    for ctx in contexts:
        builder.add_citation(ctx)
    
    return {
        "success": True,
        "data": {
            "citations": builder.get_citations()
        },
        "message": "Foundry IQ 證據鏈已載入"
    }

@app.get("/api/demo/jobs")
async def get_demo_jobs():
    jobs_path = os.path.join("demo_data", "demo_jobs.json")
    if os.path.exists(jobs_path):
        with open(jobs_path, "r", encoding="utf-8") as f:
            jobs = json.load(f)
            if jobs:
                return {
                    "success": True,
                    "data": jobs,
                    "message": "揭曉各方山門"
                }
    return {
        "success": False,
        "data": None,
        "message": "目前尚無山門開放"
    }

@app.post("/api/adventure/start")
async def start_adventure(req: AdventureRequest):
    try:
        adventure = adventure_service.generate_adventure(req.job_id)
        if adventure["hero_story"]["journey_story"] == "資料不足":
            return {
                "success": False,
                "data": None,
                "message": "資料不足，尚無法生成完整故事"
            }
        return {
            "success": True,
            "data": adventure,
            "message": "取經卷軸已生成"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "message": f"發生意外，修行中斷: {str(e)}"
        }

@app.post("/api/interview/challenge")
async def get_interview_challenge(req: AdventureRequest):
    try:
        challenges = interview_game_service.get_challenges(req.job_id)
        return {
            "success": True,
            "data": challenges,
            "message": "面試關卡已開啟"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "message": f"妖怪太強，關卡暫時封閉: {str(e)}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
