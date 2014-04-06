from django.test import TestCase
from projects.models import Project
from projects.test.test_models import test_project


class ModelsProject_Latest(TestCase):
    def test_NoReleasesForProject_LatestIsEmpty(self):
        p = test_project()

        self.assertEqual(0, len(p.latest))