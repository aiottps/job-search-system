import json
import os
from typing import List, Dict, Any

class GroundedContextService:
    def __init__(self, demo_data_dir: str = "demo_data"):
        self.demo_data_dir = demo_data_dir
        self._contexts = []
        self._load_demo_data()

    def _load_demo_data(self):
        # Load Candidate Profile
        profile_path = os.path.join(self.demo_data_dir, "candidate_profile.json")
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
                self._add_context("profile-01", "Candidate Profile", "candidate_profile", json.dumps(profile, ensure_ascii=False))

        # Load Resume
        resume_path = os.path.join(self.demo_data_dir, "demo_resume.md")
        if os.path.exists(resume_path):
            with open(resume_path, "r", encoding="utf-8") as f:
                self._add_context("resume-01", "Candidate Resume", "resume", f.read())

        # Load Jobs
        jobs_path = os.path.join(self.demo_data_dir, "demo_jobs.json")
        if os.path.exists(jobs_path):
            with open(jobs_path, "r", encoding="utf-8") as f:
                jobs = json.load(f)
                for job in jobs:
                    self._add_context(f"job-{job['id']}", f"Job: {job['title']}", "job_description", json.dumps(job, ensure_ascii=False))

        # Load Company Context
        company_path = os.path.join(self.demo_data_dir, "demo_company_context.md")
        if os.path.exists(company_path):
            with open(company_path, "r", encoding="utf-8") as f:
                self._add_context("company-ctx-01", "Company Context", "company_context", f.read())

    def _add_context(self, citation_id: str, source_name: str, source_type: str, content: str):
        self._contexts.append({
            "citation_id": citation_id,
            "source_name": source_name,
            "source_type": source_type,
            "content": content
        })

    def get_all_contexts(self) -> List[Dict[str, Any]]:
        return self._contexts

    def get_context_by_type(self, source_type: str) -> List[Dict[str, Any]]:
        return [c for c in self._contexts if c["source_type"] == source_type]

    def get_context_by_id(self, citation_id: str) -> Dict[str, Any]:
        for c in self._contexts:
            if c["citation_id"] == citation_id:
                return c
        return None
