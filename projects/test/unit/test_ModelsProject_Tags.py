from django.test import TestCase
from taggit.models import Tag
from projects.test.test_models import test_project, test_release


class ModelsProject_Tags(TestCase):
    def test_NoReleases_TagsIsEmpty(self):
        p = test_project()

        self.assertEqual(0, len(p.tags))

    def test_OneReleasesNoTag_TagsOnlyContainsNone(self):
        p = test_project()
        test_release(project=p)

        self.assertEqual({None}, p.tags)

    def test_OneReleaseWithSingleTag_TagsOnlyContainsTheTag(self):
        p = test_project()
        test_release(project=p, tags=["foo"])

        self.assertEqual({Tag.objects.get(name="foo").id}, p.tags)

    def test_OneReleaseWithMultipleTags_TagsOnlyContainsTheTags(self):
        p = test_project()
        test_release(project=p, tags=["foo", "bar"])

        self.assertEqual({Tag.objects.get(name="foo").id, Tag.objects.get(name="bar").id}, p.tags)

    def test_TwoReleasesWithOverlappingTag_TagsOnlyContainsTheTags(self):
        p = test_project()
        test_release(project=p, tags=["foo", "bar"])
        test_release(number="2", project=p, tags=["bar", "boo"])

        self.assertEqual({Tag.objects.get(name="foo").id, Tag.objects.get(name="bar").id, Tag.objects.get(name="boo").id}, p.tags)

    def test_TwoReleasesOneWithNoTags_TagsOnlyContainsTheTagsAndNonw(self):
        p = test_project()
        test_release(project=p, tags=["foo", "bar"])
        test_release(number="2", project=p)

        self.assertEqual({None, Tag.objects.get(name="foo").id, Tag.objects.get(name="bar").id}, p.tags)
