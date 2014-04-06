from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from projects.models import Project, ResponseCodes
from projects.test.test_models import test_project, test_release


class ModelsProject_Latest(TestCase):
    def test_NoReleasesForProject_LatestIsEmpty(self):
        p = test_project()

        self.assertEqual(0, len(p.latest))


    def test_OnlyReleaseIsPending_LatestIsEmpty(self):
        p = test_project()
        r = test_release(project=p)

        self.assertEqual(0, len(p.latest))


    def test_OnlyOneAcceptedReleaseWithNoTag_LatestHasOneRelease(self):
        p = test_project()
        r = test_release(project=p)
        for response in r.responses:
            response.response = ResponseCodes.Accept
            response.save()

        self.assertEqual(1, len(p.latest))
        self.assertEqual(r, p.latest[0]["release"])


    def test_OnlyOneAcceptedReleaseWithTag_LatestHasTwoReleasesOneWithTheTag(self):
        p = test_project()
        r = test_release(project=p)
        r.tags.add("test")
        for response in r.responses:
            response.response = ResponseCodes.Accept
            response.save()

        self.assertEqual(2, len(p.latest))
        self.assertEqual(r, p.latest[0]["release"])
        self.assertEqual(r, p.latest[1]["release"])
        self.assertEqual("test", p.latest[1]["tag"].slug)


    def test_TwoAcceptedReleaseOneWithTag_LatestHasTwoReleasesOneWithTheTag(self):
        p = test_project()
        r1 = test_release(project=p, dateTime=timezone.make_aware(datetime(1970, 1, 1), timezone.get_current_timezone()))
        r1.tags.add("test")
        for response in r1.responses:
            response.response = ResponseCodes.Accept
            response.save()

        r2 = test_release(project=p, number="newnumber", dateTime=timezone.make_aware(datetime(1970, 1, 2), timezone.get_current_timezone()))
        for response in r2.responses:
            response.response = ResponseCodes.Accept
            response.save()


        self.assertEqual(2, len(p.latest))
        self.assertEqual(r2, p.latest[0]["release"])
        self.assertEqual(r1, p.latest[1]["release"])
        self.assertEqual("test", p.latest[1]["tag"].slug)


    def test_TwoAcceptedReleaseOneWithTagOnePendingRelease_LatestHasTwoReleasesOneWithTheTag(self):
        p = test_project()
        r1 = test_release(project=p, dateTime=timezone.make_aware(datetime(1970, 1, 1), timezone.get_current_timezone()))
        r1.tags.add("test")
        for response in r1.responses:
            response.response = ResponseCodes.Accept
            response.save()

        r2 = test_release(project=p, number="newnumber", dateTime=timezone.make_aware(datetime(1970, 1, 2), timezone.get_current_timezone()))
        for response in r2.responses:
            response.response = ResponseCodes.Accept
            response.save()

        test_release(project=p, number="pendingnumber", dateTime=timezone.make_aware(datetime(1970, 1, 3), timezone.get_current_timezone()))

        self.assertEqual(2, len(p.latest))
        self.assertEqual(r2, p.latest[0]["release"])
        self.assertEqual(r1, p.latest[1]["release"])
        self.assertEqual("test", p.latest[1]["tag"].slug)


    def test_TwoAcceptedReleaseOneWithTagOnePendingReleaseWithTheSameTag_LatestHasTwoReleasesOneWithTheTag(self):
        p = test_project()
        r1 = test_release(project=p, dateTime=timezone.make_aware(datetime(1970, 1, 1), timezone.get_current_timezone()))
        r1.tags.add("test")
        for response in r1.responses:
            response.response = ResponseCodes.Accept
            response.save()

        r2 = test_release(project=p, number="newnumber", dateTime=timezone.make_aware(datetime(1970, 1, 2), timezone.get_current_timezone()))
        for response in r2.responses:
            response.response = ResponseCodes.Accept
            response.save()

        test_release(project=p, number="pendingnumber", dateTime=timezone.make_aware(datetime(1970, 1, 3), timezone.get_current_timezone()), tags=["test"])


        self.assertEqual(2, len(p.latest))
        self.assertEqual(r2, p.latest[0]["release"])
        self.assertEqual(r1, p.latest[1]["release"])
        self.assertEqual("test", p.latest[1]["tag"].slug)