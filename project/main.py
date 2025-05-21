import os
import smtplib
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email_username = "posu0009@gmail.com"
email_password = "boyupzyjsqynrnis"

app = FastAPI()

templates_dir = os.path.join(os.path.dirname(__file__), "app", "templates")
templates = Jinja2Templates(directory=templates_dir)


# Define email request model
class EmailRequest(BaseModel):
    recipient: str
    subject: str
    body: str
    deviceInfo: Optional[Dict[str, Any]] = None
    ipAddress: Optional[str] = None


def send_email_background(recipient: str, subject: str, body: str):
    """Send email using smtplib in the background"""
    message = MIMEMultipart()
    message["From"] = email_username
    message["To"] = recipient
    message["Subject"] = subject
    
    # Attach HTML body
    message.attach(MIMEText(body, "html"))
    
    # Convert the message to a string
    email_text = message.as_string()
    
    # Connect to SMTP server
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    try:
        s.login(email_username, email_password)
        s.sendmail(email_username, recipient, email_text)
        print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e
    finally:
        s.quit()


@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/sendMail")
async def send_email(email_request: EmailRequest, background_tasks: BackgroundTasks):
    try:
        # Create a modified body that includes device info and IP address
        enhanced_body = email_request.body
        
        # Add device info and IP address to the email body if available
        if email_request.deviceInfo or email_request.ipAddress:
            enhanced_body += "<hr style='margin-top: 20px; border: 1px solid #eee;'>"
            enhanced_body += "<div style='font-size: 12px; color: #666; margin-top: 10px;'>"
            enhanced_body += "<p><strong>Email sent from:</strong></p>"
            
            if email_request.deviceInfo:
                browser = email_request.deviceInfo.get("browser", "Unknown")
                device = email_request.deviceInfo.get("device", "Unknown")
                os = email_request.deviceInfo.get("os", "Unknown")
                enhanced_body += f"<p>Browser: {browser}<br>"
                enhanced_body += f"Device: {device}<br>"
                enhanced_body += f"OS: {os}</p>"
            
            if email_request.ipAddress:
                enhanced_body += f"<p>IP Address: {email_request.ipAddress}</p>"
                
            enhanced_body += "</div>"
        
        # Add the email sending task to background tasks
        background_tasks.add_task(
            send_email_background, 
            email_request.recipient, 
            email_request.subject, 
            enhanced_body
        )
        
        return JSONResponse(content={"message": "Email sent successfully"}, status_code=200)
    except Exception as e:
        return JSONResponse(
            content={"message": f"Failed to send email: {str(e)}"}, 
            status_code=500
        )
