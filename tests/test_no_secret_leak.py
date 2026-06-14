import pytest
import json
import os
from app.iq.grounded_context_service import GroundedContextService
from app.adventure.adventure_service import AdventureService

def test_no_secrets_in_adventure():
    iq_service = GroundedContextService(demo_data_dir="demo_data")
    adventure_service = AdventureService(iq_service)
    
    res = adventure_service.generate_adventure("demo-data-engineer")
    res_str = json.dumps(res)
    
    secrets = [
        "GEMINI_API_KEY", "DB_PASSWORD", "SMTP_PASSWORD", "SMTP_USER", 
        "API_KEY", "password", "token", "secret"
    ]
    for secret in secrets:
        # Check both uppercase and lowercase
        assert secret.upper() not in res_str
        assert secret.lower() not in res_str

def test_no_secrets_in_demo_data():
    secrets = [
        "GEMINI_API_KEY", "DB_PASSWORD", "SMTP_PASSWORD", "SMTP_USER", 
        "API_KEY", "password", "token", "secret"
    ]
    for root, dirs, files in os.walk("demo_data"):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                for secret in secrets:
                    assert secret.upper() not in content, f"Secret {secret} found in {file_path}"
                    assert secret.lower() not in content, f"Secret {secret} found in {file_path}"
