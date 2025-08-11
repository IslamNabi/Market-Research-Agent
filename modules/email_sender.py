import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASS

class EmailSender:
    def send_email(self, recipient, subject, body, attachment_path):
        try:
            # Create email
            msg = MIMEMultipart()
            msg["From"] = EMAIL_USER
            msg["To"] = recipient
            msg["Subject"] = subject

            # Email body
            msg.attach(MIMEText(body, "plain"))

            # Attach PDF
            with open(attachment_path, "rb") as f:
                pdf_attachment = MIMEApplication(f.read(), _subtype="pdf")
                pdf_attachment.add_header(
                    "Content-Disposition",
                    "attachment",
                    filename=os.path.basename(attachment_path)
                )
                msg.attach(pdf_attachment)

            # Send email
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
                server.login(EMAIL_USER, EMAIL_PASS)
                server.send_message(msg)

            print(f"✅ Email sent to {recipient}")

        except Exception as e:
            print(f"❌ Failed to send email: {e}")
