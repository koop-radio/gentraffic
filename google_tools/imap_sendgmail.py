import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendgmail(subject, body):
    # Email configuration
    sender_email = "prodmmauto@koop.org"
    #receiver_email = "playout@koop.org"
    receiver_email = "sendjunk4me@gmail.com"
    password = "k!!!!^^^^K"  # Replace with your Gmail account password

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, "plain"))

    try:
        # Create a secure SSL/TLS connection
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        
        # Login to the sender's email account
        server.login(sender_email, password)
        
        # Send the email
        server.send_message(message)
        
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending the email:")
        print(str(e))
    finally:
        # Close the SMTP connection
        server.quit()

# Example usage
#subject = input("Enter the email subject: ")
#body = input("Enter the email body: ")
subject = "A test from prodmm@koop.org"
body = "a body"
sendgmail(subject, body)
