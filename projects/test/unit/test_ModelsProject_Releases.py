from datetime import timedelta
from django.test import TestCase
from projects.models import DEFAULT_TIME
from projects.test.test_models import test_project, test_release


class ModelsProject_Releases(TestCase):
    def test_ProjectHasNoReleases_ReleasesInEmpty(self):
        p = test_project()

        self.assertEqual(0, len(p.releases))

    def test_ProjectHasSingleRelease_ReleasesOnlyContainsThatRelease(self):
        p = test_project()
        r = test_release(project=p)

        self.assertEqual([r], list(p.releases))

    def test_ProjectHasMultipleReleases_ReleasesContainsAllReleasesInReverseDateOrder(self):
        p = test_project()
        r1 = test_release(project=p)
        r2 = test_release(project=p, dateTime=DEFAULT_TIME + timedelta(1), number="2")

        self.assertEqual([r2, r1], list(p.releases))

    def test_ProjectsHaveMultipleReleases_ReleasesContainsAllReleasesForProjectInReverseDateOrder(self):
        p = test_project()
        r1 = test_release(project=p)
        r2 = test_release(project=p, dateTime=DEFAULT_TIME + timedelta(1), number="2")

        p2 = test_project(name="foo", team=p.team)
        test_release(project=p2)
        test_release(project=p2, dateTime=DEFAULT_TIME + timedelta(1), number="2")

        self.assertEqual([r2, r1], list(p.releases))
