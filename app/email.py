import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.constants import (
    SMTP_SERVER,
    SMTP_PORT,
    RECIEVER_EMAIL_ADDRESS,
    RECIEVER_EMAIL_PASSWORD,
    SENDER_EMAIL_ADDRESS,
    SENDER_EMAIL_PASSWORD,
    messages
)
from app.get_user_data import content


def email_send( 
            language,
            subject,
            code,
            user,
            role,
            email,
            Type,
            query,
            time):
    server = None

    try:
        receiver_email = RECIEVER_EMAIL_ADDRESS 
       
        if not receiver_email:
            raise ValueError("User email not found")

        subject = subject or "Fixy Test Email"

        body = messages.get(
            language
        ).format(
            code=code,
            user=user,
            role=role,
            email=email,
            Type=Type,
            query=query,
            time=time
        )

        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL_ADDRESS
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(
            MIMEText(body, "html")
        )

        server = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        server.starttls()

        server.login(
            SENDER_EMAIL_ADDRESS,
            SENDER_EMAIL_PASSWORD
        )

        server.send_message(msg)

        print("[✓] Email sent successfully")

        return {
            "success": True,
            "message": "Email sent successfully"
        }

    except Exception as e:
        print("[ERROR]", e)

        return {
            "success": False,
            "message": str(e)
        }

    finally:
        if server:
            server.quit()