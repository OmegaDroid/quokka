from django.apps import AppConfig
from django.db.models.signals import post_save

from projects import models
from projects import triggers


class ProjectsConfig(AppConfig):
    name="projects"

    def ready(self):
        #register creation of responses on release being created
        post_save.connect(triggers.post_release_save_create_responses, sender=models.Release)

        #register emailing authorisers on release being created
        post_save.connect(triggers.post_release_new_release_auth_emails, sender=models.Release)

        #register emailing team members on release being created
        post_save.connect(triggers.post_release_new_release_team_emails, sender=models.Release)