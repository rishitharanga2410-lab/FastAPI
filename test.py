import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Test"
msg["From"] = "test@example.com"
msg["To"] = "you@example.com"
msg.set_content("Hello")

with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as s:
    s.starttls()
    s.login("af1598d2acad12", "e7930a1cfc4bbd")
    s.send_message(msg)