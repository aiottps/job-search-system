import os
from dotenv import load_dotenv

load_dotenv()

def str_to_bool(val: str) -> bool:
    if not val:
        return False
    return val.lower() in ("true", "1", "yes", "on")

class Config:
    # Database
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    
    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # SMTP
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    MAIL_TO = os.getenv("MAIL_TO")
    
    # Feature Flags
    USE_DB = str_to_bool(os.getenv("USE_DB", "false"))
    USE_GEMINI = str_to_bool(os.getenv("USE_GEMINI", "false"))
    SEND_EMAIL = str_to_bool(os.getenv("SEND_EMAIL", "false"))

    # Job Search Preferences
    JOB_KEYWORDS = os.getenv("JOB_KEYWORDS", "Python,Data Engineer").split(",")
    JOB_LOCATIONS = os.getenv("JOB_LOCATIONS", "台北市,遠端").split(",")
    MIN_ANNUAL_SALARY = int(os.getenv("MIN_ANNUAL_SALARY", "700000"))

    # App Settings
    PYTHONUTF8 = os.getenv("PYTHONUTF8", "1") == "1"

    @property
    def user_prefs_text(self):
        """Returns a summarized string of user job preferences."""
        keywords = ", ".join(self.JOB_KEYWORDS)
        locations = ", ".join(self.JOB_LOCATIONS)
        salary = f"{self.MIN_ANNUAL_SALARY / 10000:.0f}萬+"
        return f"關鍵字: {keywords}; 地區: {locations}; 年薪: {salary}"

    @property
    def db_connection_string(self):
        return f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.DB_HOST};DATABASE={self.DB_NAME};UID={self.DB_USER};PWD={self.DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

config = Config()
