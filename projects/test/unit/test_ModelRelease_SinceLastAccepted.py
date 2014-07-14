from django.test import TestCase
from projects.models import ResponseCodes
from projects.test.test_models import test_project, test_release


class ModelRelease_SinceLastAccepted(TestCase):
    def test_OnlyOneRelease_ReturnsThatRelease(self):
        r = test_release()

        self.assertEqual([r], r.since_last_accepted)

    def test_TwoRelease_ReturnsThatBothRelease(self):
        p = test_project()
        r1 = test_release(project=p)
        r2 = test_release(project=p, number="2")

        self.assertEqual([r2, r1], r2.since_last_accepted)

    def test_ThreeReleaseFirstIsAccepted_ReturnsTwoRecentReleases(self):
        p = test_project()
        r1 = test_release(project=p)
        for res in r1.responses:
            res.response = ResponseCodes.Accept
            res.save()

        r2 = test_release(project=p, number="2")
        r3 = test_release(project=p, number="3")

        self.assertEqual([r3, r2], r3.since_last_accepted)

    def test_ManyReleasesSomeAreAcceptedCheckAnAcceptedInTheMiddle_ReturnsUntilThePreviousSaved(self):
        p = test_project()
        r1 = test_release(project=p)
        for res in r1.responses:
            res.response = ResponseCodes.Accept
            res.save()

        r2 = test_release(project=p, number="2")
        r3 = test_release(project=p, number="3")

        r4 = test_release(project=p, number="4")
        for res in r4.responses:
            res.response = ResponseCodes.Accept
            res.save()

        r5 = test_release(project=p, number="5")
        r6 = test_release(project=p, number="6")
        for res in r6.responses:
            res.response = ResponseCodes.Accept
            res.save()

        r7 = test_release(project=p, number="7")

        self.assertEqual([r6, r5], r6.since_last_accepted)
