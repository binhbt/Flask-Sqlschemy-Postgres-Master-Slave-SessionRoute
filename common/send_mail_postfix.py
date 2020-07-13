import smtplib
from socket import gaierror
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
class PostFix(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'mail'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)        
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, subject, body, to):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + to,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            to,
            headers + "\r\n\r\n" + body)

    # def send_mail(self, receiver, title, content):
    #     """Send Email
    #     """
    #     # login
    #     smtp = smtplib.SMTP('mail', 587)
    #     smtp.ehlo('mail')
    #     smtp.login(self.email, self.password)
    #     smtp.set_debuglevel(1)

    #     # construct message
    #     email = MIMEText(content, "plain", 'utf-8')
    #     email["Subject"] = Header(title, 'utf-8')
    #     email["From"] = self.email
    #     email["To"] = receiver
    #     smtp.sendmail(self.email, receiver, email.as_string())
    #     smtp.quit()
    # def sendMessage(self, receiver, subject, message):
    #     msg = MIMEText(message)
    #     msg['From'] = self.email
    #     msg['To'] = receiver
    #     msg['Subject'] = subject
    #     # msg['Date'] = formatdate()
    #     msg['X-Domain'] = "kidssy.com"
    #     msg['X-System'] = "python"

    #     server = smtplib.SMTP('mail')
    #     server.sendmail(self.email, receiver, msg.as_string())