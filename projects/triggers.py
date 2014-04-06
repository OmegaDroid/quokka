from accounts import emails


def post_release_save_create_responses(sender, **kwargs):
    if kwargs["created"]:
        kwargs["instance"].create_responses()

def post_release_save_new_release_auth_emails(sender, **kwargs):
    if kwargs["created"]:
        emails.new_release_auth(kwargs["instance"])

def post_release_save_new_release_team_emails(sender, **kwargs):
    if kwargs["created"]:
        emails.new_release_team(kwargs["instance"])

def post_release_save_reject_pending_releases(sender, **kwargs):
    if kwargs["created"]:
        kwargs["instance"].reject_previous_pending()