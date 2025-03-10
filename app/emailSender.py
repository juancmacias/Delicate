from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = FastAPI()

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str

@app.post("/send-email")
async def send_email(email_request: EmailRequest):
    smtp_server = 'smtp.gmail.com'
    from_email = 'devprueba282@gmail.com'
    password = os.getenv('MAIL_PASS')

    try:
        # Create a multipart message
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = email_request.to_email
        message['Subject'] = email_request.subject

        # Attach the body of the message
        message.attach(MIMEText(email_request.body, 'plain'))

        # Establish a secure session with Gmail's outgoing SMTP server
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls()
        server.login(from_email, password)

        # Send email
        server.send_message(message)
        server.quit()

        return {"status": "Email sent successfully"}

    except Exception as e:
        # In a production environment, you'd want to log this error
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

# Optional: Add a health check endpoint
@app.get("/")
async def health_check():
    return {"status": "Email service is running"}