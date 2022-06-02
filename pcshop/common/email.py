from threading import Thread

from django.conf import settings
from django.core.mail import send_mail


class ContactNotificationEmail(Thread):

    def __init__(self, contactform):
        super(ContactNotificationEmail, self).__init__()
        
        self.contactform = contactform
        self.receiver = contactform.email1
        self.sender = settings.EMAIL_SENDER
        self.password = settings.EMAIL_PASSWORD
        self.subject = 'Confirmation Email'

        Thread.__init__(self)

    def run(self):
        self.send_appointment_notification()

    def send_appointment_notification(self):
        self.name = self.contactform.fullname
        self.firstname = self.name.upper()

        self.msg = f"""

Hi, {self.firstname}.
Phone Number: +27 781 114 041. 

Paris Collection send you this email to confirm that  your 
contact form details has been received successfully .

Should you have any question, please contact Paris Collection.

Thanks,
Paris Collection,
Email: info@pariscollection.com

        """

        send_mail(
            f"{self.subject}",
            f"{self.msg}",
            self.sender,
            [f'{self.receiver}', ],
            fail_silently = False,
            auth_user = self.sender,
            auth_password = self.password
        )

        return