import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_simple_email(sender_email, sender_password, recipient_email, subject, body):
    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Create SMTP session
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("Email sent successfully")
    
from email.mime.text import MIMEText

def send_html_email(sender_email, sender_password, recipient_email, subject, html_content):
    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText("This is a fallback plain text", "plain")
    part2 = MIMEText(html_content, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("HTML email sent successfully")
    
    
import os
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage

def send_email_with_attachment(sender_email, sender_password, recipient_email, subject, body, file_path):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Determine the file type and attach accordingly
    file_name = os.path.basename(file_path)
    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        with open(file_path, "rb") as file:
            part = MIMEImage(file.read(), name=file_name)
    else:
        with open(file_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=file_name)
    
    # Add header to make the attachment downloadable
    part['Content-Disposition'] = f'attachment; filename="{file_name}"'
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print(f"Email with attachment {file_name} sent successfully")
    


def send_email_with_multiple_attachments(sender_email, sender_password, recipient_email, subject, body, file_paths):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    for file_path in file_paths:
        file_name = os.path.basename(file_path)
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            with open(file_path, "rb") as file:
                part = MIMEImage(file.read(), name=file_name)
        else:
            with open(file_path, "rb") as file:
                part = MIMEApplication(file.read(), Name=file_name)
        
        part['Content-Disposition'] = f'attachment; filename="{file_name}"'
        message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("Email with multiple attachments sent successfully")

def send_comprehensive_email(sender_email, sender_password, recipient_email, subject, body, html_content=None, attachments=None):
    message = MIMEMultipart("alternative" if html_content else "mixed")
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject

    # Attach plain text and HTML versions
    message.attach(MIMEText(body, "plain"))
    if html_content:
        message.attach(MIMEText(html_content, "html"))

    # Attach files
    if attachments:
        for file_path in attachments:
            file_name = os.path.basename(file_path)
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                with open(file_path, "rb") as file:
                    part = MIMEImage(file.read(), name=file_name)
            else:
                with open(file_path, "rb") as file:
                    part = MIMEApplication(file.read(), Name=file_name)
            
            part['Content-Disposition'] = f'attachment; filename="{file_name}"'
            message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    print("Comprehensive email sent successfully")
    
    
if __name__=="__main__":
    send_comprehensive_email("sender@gmail.com", "password", "recipient@example.com", "Simple Text Email", "This is a simple text email.")
    
    html_content = """
<html>
<body>
    <h1>This is an HTML Email</h1>
    <p>Hello, <strong>World!</strong></p>
</body>
</html>
    """
    send_comprehensive_email("sender@gmail.com", "password", "recipient@example.com", "HTML Email", "This is a fallback text", html_content=html_content)
    
    attachments = ["path/to/document.pdf", "path/to/image.jpg"]
    send_comprehensive_email("sender@gmail.com", "password", "recipient@example.com", "Email with Attachments", "Please find the attachments.", attachments=attachments)
    
    html_content = "<html><body><h1>Email with HTML and Attachments</h1></body></html>"
    attachments = ["static/css/style.css", "path/to/image.jpg"]
    send_comprehensive_email("sender@gmail.com", "password", "recipient@example.com", "HTML Email with Attachments", "This is a fallback text", html_content=html_content, attachments=attachments)