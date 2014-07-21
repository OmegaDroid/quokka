from django.test import TestCase
from projects.test.test_models import test_project, test_release


class ModelsProject_ReleaseWithTag(TestCase):
    def test_NoReleasesForProject_ReturnIsNone(self):
        p = test_project()

        self.assertIsNone(p.release_with_tag("foo"))

    def test_NoReleasesWithTagForProject_ReturnIsNone(self):
        p = test_project()
        r = test_release(project=p, tags=["bar"])

        self.assertIsNone(p.release_with_tag("foo"))

    def test_SingleReleasesWithTagForProject_ReturnIsTheRelease(self):
        p = test_project()
        r = test_release(project=p, tags=["foo"])

        self.assertEqual(r, p.release_with_tag("foo"))

    def test_MultipleReleasesWithTagForProject_ReturnIsTheLatestRelease(self):
        p = test_project()
        r1 = test_release(project=p, tags=["foo"])
        r2 = test_release(number="2", project=p, tags=["foo"])

        self.assertEqual(r2, p.release_with_tag("foo"))
