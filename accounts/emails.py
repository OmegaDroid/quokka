import os
import smtplib
from email.mime.text import MIMEText
from django.core.mail import send_mail
from django.template import Template, Context

SERVER_EMAIL = "no-reply@badger.com"

def new_release_auth(hostname, response):
    with open(os.path.join(os.path.dirname(__file__), "email_templates", "new_release_auth.html")) as f:
        t = Template(f.read())
        send_mail(
            "New "+response.release.project.name+" release proposed - Awaiting authorisation",
            t.render(Context({"host": hostname, "response": response})),
            SERVER_EMAIL,
            [response.user.email],
            fail_silently=False
        )


def new_release_team(hostname, release):
    with open(os.path.join(os.path.dirname(__file__), "email_templates", "new_release_auth.html")) as f:
        t = Template(f.read())
        send_mail(
            "New "+release.project.name+" release proposed",
            t.render(Context({"host": hostname, "release": release})),
            SERVER_EMAIL,
            [member.email for member in release.project.team.members.all()],
            fail_silently=False
        )