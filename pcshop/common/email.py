from threading                                              import Thread

from django.conf                                            import settings
from django.core.mail                                       import send_mail


class MakeAppointmentNotificationEmail(Thread):

    def __init__(self, apptment):
        super(MakeAppointmentNotificationEmail, self).__init__()

        self.apptment   = apptment
        self.receiver   = apptment.email1
        self.sender     = settings.EMAIL_SENDER
        self.password   = settings.EMAIL_PASSWORD
        self.subject    = 'Appointment Confirmation'

        Thread.__init__(self)

    def run(self):
        self.send_appointment_notification()

    def send_appointment_notification(self):

        self.name       = self.apptment.fullname
        self.firstname  = self.name.upper()

        self.msg = f"""

            Hi, {self.firstname}.
            Phone Number: +27781114041. 

            Tshibuyi Clinic has sent you appointment confirmation email to you.

            Should you have any question, please contact Tshibuyi Hospital.

            Thanks,
            Tshibuyi Hospital,
            Email: info@tshibuyihospital.com

        """

        send_mail(
            f"{self.subject}",
            f"{self.msg}",
            self.sender,
            [f'{self.receiver}', ],
            fail_silently   = False,
            auth_user       = self.sender,
            auth_password   = self.password
        )

        return