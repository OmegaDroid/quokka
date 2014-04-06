"""
A set of functions to produce model instances for test.

These allow us to change models and not break tests.
"""
from datetime import datetime
import os
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files import File
from accounts.test.test_models import test_user

from projects.models import Project, Team, Release


def test_team(leader: User=None, name: str="team", members: list=[], description: str="", img: str=None) -> Team:
    """
    Creates, saves and returns a Team obj.

    :param leader: The leader of the team
    :param name: The name of the team
    :param members: List of members in the team
    :param description: The description of the team
    :param img: Path to the image

    :return: The Team object
    """
    if not leader:
        leader = test_user()

    if not members:
        members = [leader]

    t = Team(
        leader=leader,
        name=name,
        description=description,
    )

    if img:
        t.img.save(
            os.path.basename(img),
            File(open(img))
        )

    t.save()

    for m in members:
        t.members.add(m)

    t.save()
    return t


def test_project(name: str="project", description: str="", team: Team=None, authorisers: list=[], subscribers: list=[], img: str=None) -> Project:
    """
    Creates, saves and returns a Project obj.

    :param name: The name of the project
    :param description: The description of the project
    :param team: The team the project belongs to, if None the test_team is used
    :param authorisers: The list of authorisers, if None the test_team leader is used
    :param subscribers: The list of subscribers
    :param img: Path of the image to load

    :return: The Project object
    """
    if not team:
        team = test_team()

    p = Project(
        name=name,
        description=description,
        team=team
    )

    if img:
        p.img.save(
            os.path.basename(img),
            File(open(img))
        )
    p.save()

    if not authorisers:
        authorisers=[team.leader]

    for a in authorisers:
        p.authorisers.add(a)

    for s in subscribers:
        p.subscribers.add(s)

    p.save()
    return p


def test_release(number: str="1", project:Project=None, notes: str="notes", dateTime: datetime=timezone.now(), url: str="a.b.c", tags=[]) -> Release:
    """
    Creates, saves and returns a Release obj.

    :param number: The release number
    :param project: The Project the release belongs to
    :param notes: The notes for the release
    :param dateTime: The datetime the release was created
    :param url: The url of the downloadable items

    :return: The generated Release object
    """
    if not project:
        project = test_project()

    r = Release(
        number=number,
        project=project,
        notes=notes,
        dateTime=dateTime,
        url=url
    )
    r.save()

    for tag in tags:
        r.tags.add(tag)

    r.save()
    return r