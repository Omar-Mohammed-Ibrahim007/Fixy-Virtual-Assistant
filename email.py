import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .env import EMAIL, EMAIL_API_KEY
from constants import SMTP_SERVER, SMTP_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

# =====================================================
# CREATE MESSAGE
# =====================================================

receiver_email = "receiver@gmail.com" # email from get endpoint in backend

subject = "Fixy Test Email"

body = ""


msg = MIMEMultipart()

msg["From"] = EMAIL_ADDRESS
msg["To"] = receiver_email
msg["Subject"] = subject

msg.attach(
    MIMEText(body, "plain")
)

# =====================================================
# SEND EMAIL
# =====================================================

try:

    server = smtplib.SMTP(
        SMTP_SERVER,
        SMTP_PORT
    )

    server.starttls()

    server.login(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD
    )

    server.send_message(msg)

    print("[✓] Email sent successfully")

except Exception as e:

    print("[ERROR, please try again]", e)

finally:

    server.quit()