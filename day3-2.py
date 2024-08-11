from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

SMTP_SERVER = "2020csm.r10@svce.edu.in"
SMTP_PORT = 587
SMTP_USER = "dpavan0912@gmail.com"
SMTP_PASSWORD = "Pavan@2002"

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str

def send_email(email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.post("/send-email/")
async def send_email_background(email: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email.email, email.subject, email.body)
    return {"message": "Email sent successfully in the background"}

