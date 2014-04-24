import os
from django.core.mail import send_mail
from django.template import Template, Context

from quokka.settings import HOSTNAME


SERVER_EMAIL = "no-reply@quokka.com"


def new_release_auth(release):
    with open(os.path.join(os.path.dirname(__file__), "email_templates", "new_release_auth.html")) as f:
        t = Template(f.read())
        send_mail(
            "New " + release.project.name + " release proposed - Awaiting authorisation",
            t.render(Context({"host": HOSTNAME, "response": release})),
            SERVER_EMAIL,
            [auth.email for auth in release.project.authorisers.all()],
            fail_silently=False
        )


def new_release_team(release):
    with open(os.path.join(os.path.dirname(__file__), "email_templates", "new_release_auth.html")) as f:
        t = Template(f.read())
        send_mail(
            "New " + release.project.name + " release proposed",
            t.render(Context({"host": HOSTNAME, "release": release})),
            SERVER_EMAIL,
            [member.email for member in release.project.team.members.all()],
            fail_silently=False
        )