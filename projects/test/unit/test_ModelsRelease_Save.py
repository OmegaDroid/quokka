from datetime import datetime
from unittest.mock import MagicMock, patch
from django.test import TestCase
from django.utils import timezone
import accounts
from accounts.test.test_models import test_user
from projects.models import ResponseCodes, DEFAULT_TIME
from projects.test.test_models import test_release, test_project, test_team


class ModelsRelease_Save(TestCase):
    def test_CreateRelease_ResponsesAreCreatedForEachAuthoriser(self):
        u1 = test_user(username="auth1")
        u2 = test_user(username="auth2")
        p = test_project(authorisers=[u1, u2])
        r = test_release(project=p)

        responses = r.pending_responses
        self.assertEqual(2, len(responses))
        self.assertTrue(responses.get(user=u1))
        self.assertTrue(responses.get(user=u2))

    def test_UpdateRelease_NoNewResponsesAreCreated(self):
        u1 = test_user(username="auth1")
        u2 = test_user(username="auth2")
        p = test_project(authorisers=[u1, u2])
        r = test_release(project=p)

        origResponses = [res for res in r.pending_responses]
        r.number = "newnumber"
        r.save()
        newReleases = [res for res in r.pending_responses]

        self.assertEqual(origResponses, newReleases)


    def test_CreateRelease_NewReleaseAuthIsCalled(self):
        with patch("accounts.emails.new_release_auth", MagicMock()):
            u1 = test_user(username="auth1")
            u2 = test_user(username="auth2")
            p = test_project(authorisers=[u1, u2])
            r = test_release(project=p)

            accounts.emails.new_release_auth.assert_called_once_with(r)


    def test_NotRelease_NewReleaseAuthIsNotCalled(self):
        u1 = test_user(username="auth1")
        u2 = test_user(username="auth2")
        p = test_project(authorisers=[u1, u2])
        r = test_release(project=p)

        with patch("accounts.emails.new_release_auth", MagicMock()):
            r.number = "newnumber"
            r.save()

            self.assertFalse(accounts.emails.new_release_auth.called)


    def test_CreateRelease_NewReleaseTeamIsCalled(self):
        with patch("accounts.emails.new_release_team", MagicMock()):
            u1 = test_user(username="member1")
            u2 = test_user(username="member2")
            t = test_team(members=[u1, u2])
            p = test_project(team=t)
            r = test_release(project=p)

            accounts.emails.new_release_team.assert_called_once_with(r)


    def test_UpdateRelease_NewReleaseTeamIsCalled(self):
        u1 = test_user(username="member1")
        u2 = test_user(username="member2")
        t = test_team(members=[u1, u2])
        p = test_project(team=t)
        r = test_release(project=p)

        with patch("accounts.emails.new_release_team", MagicMock()):
            r.number = "newnumber"
            r.save()

            self.assertFalse(accounts.emails.new_release_team.called)


    def test_CreateRelease_PreviousPendingReleasesAreRejected(self):
        p = test_project()
        r = test_release(project=p)
        test_release(project=p, number="2")

        self.assertTrue(r.rejected)


    def test_CreateRelease_PreviousAcceptedReleasesAreUnaffected(self):
        p = test_project()
        r = test_release(project=p)
        for res in r.responses:
            res.response = ResponseCodes.Accept
            res.save()

        test_release(project=p, number="2")

        self.assertTrue(r.accepted)


    def test_CreateRelease_ReleaseTimeIsUpdatedToTheCurrentTime(self):
        r = test_release()

        self.assertNotEqual(DEFAULT_TIME, r.dateTime)
