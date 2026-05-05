import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from app.config import config
import os

class EmailSender:
    def __init__(self):
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_dir))

    def send_daily_jobs(self, jobs: list):
        if not jobs:
            print("No jobs to send.")
            return

        template = self.jinja_env.get_template('daily_jobs_zh_tw.html')
        content = template.render(jobs=jobs)

        msg = EmailMessage()
        msg['Subject'] = f"【每日職缺推薦】今日共 {len(jobs)} 筆職缺"
        msg['From'] = config.SMTP_USER
        msg['To'] = config.MAIL_TO
        msg.set_content("請查看 HTML 版本郵件。")
        msg.add_alternative(content, subtype='html')

        try:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
                server.starttls()
                server.login(config.SMTP_USER, config.SMTP_PASSWORD)
                server.send_message(msg)
            print(f"Email sent successfully to {config.MAIL_TO}")
        except Exception as e:
            print(f"Failed to send email: {e}")
