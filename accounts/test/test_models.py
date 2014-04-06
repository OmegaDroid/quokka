"""
A set of functions to produce model instances for test.

These allow us to change models and not break tests.
"""
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User


def test_user(username:str="user", first_name:str="", last_name:str="", email:str="", is_staff:bool=True, is_active:bool=True, date_joined: datetime=timezone.now()) -> User:
    """
    Creates, saves and returns a User obj.

    :param username: The username for the user
    :param first_name: The first name of the user
    :param last_name: The last name of the user
    :param email: The email of the user
    :param is_staff: Flag if the user is staff
    :param is_active: Flag if the user is active
    :param date_joined: The date the user joined

    :return: The User object
    """
    u = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_staff=is_staff,
        is_active=is_active,
        date_joined=date_joined
    )

    u.save()
    return u