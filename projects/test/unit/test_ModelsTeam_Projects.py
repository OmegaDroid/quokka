from django.test import TestCase
from accounts.test.test_models import test_user
from projects.test.test_models import test_team, test_project


class ModelsTeam_Projects(TestCase):
    def test_TeamHasNoProjects_ProjectsIsEmpty(self):
        t = test_team()

        self.assertEqual(0, len(t.projects))

    def test_TeamHasOneProject_ProjectsIsOnlyContainsThatItem(self):
        t = test_team()
        p = test_project(team=t)

        self.assertEqual([p], list(t.projects))

    def test_MultipleProjectsTeamHasOneProject_ProjectsIsOnlyContainsThatItem(self):
        t = test_team()
        p = test_project(team=t)

        t2 = test_team(name="foo", leader=test_user(username="foo"))
        test_project(name="foo proj", team=t2)

        self.assertEqual([p], list(t.projects))

    def test_TeamHasMultipleProjects_ProjectsContainsAllProjects(self):
        t = test_team()
        p1 = test_project(team=t)
        p2 = test_project(name="foo proj", team=t)

        self.assertEqual({p1, p2}, set(t.projects))
