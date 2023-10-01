import os
import smtplib

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.from_email = 'arrayoflilly@gmail.com'
        self.to_email = 'arrayoflilly@gmail.com'
        self.password = os.environ.get("EMAIL_PASSWORD")

    def send_notification_email(self, msg):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.from_email, password=self.password)
            connection.sendmail(from_addr=self.from_email,
                                to_addrs=self.to_email,
                                msg=msg.encode('utf-8'))






