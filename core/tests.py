from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Division, Management


@override_settings(STORAGES={
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
})
class ProfileLeadershipChartTests(TestCase):
    def test_profile_renders_leadership_as_hierarchy(self):
        chair = Management.objects.create(nama="Ketua PCM", jabatan="Ketua")
        vice_chair = Management.objects.create(
            nama="Wakil Ketua PCM", jabatan="Wakil Ketua 1"
        )
        member = Management.objects.create(nama="Anggota PCM", jabatan="Anggota")
        division = Division.objects.create(nama="Majelis Pendidikan")
        division_member = Management.objects.create(
            nama="Pengurus Majelis", jabatan="Ketua Majelis", division=division
        )

        response = self.client.get(reverse("core:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["chair"], chair)
        self.assertEqual(response.context["board"], [vice_chair])
        self.assertEqual(response.context["members"], [member])
        self.assertEqual(
            response.context["groups"],
            [{"division": division, "members": [division_member]}],
        )
        self.assertContains(response, "Ketua PCM")
        self.assertContains(response, "Wakil Ketua PCM")
        self.assertContains(response, "Anggota PCM")
        self.assertContains(response, "Majelis Pendidikan")

    def test_empty_active_division_does_not_hide_empty_state(self):
        Division.objects.create(nama="Majelis Tanpa Pengurus")

        response = self.client.get(reverse("core:profile"))

        self.assertContains(response, "Data pengurus sedang disiapkan")

    def test_board_roles_are_ordered_by_position(self):
        Management.objects.create(nama="Ketua PCM", jabatan="Ketua")
        secretary = Management.objects.create(
            nama="Sekretaris", jabatan="Sekretaris"
        )
        vice_chair_two = Management.objects.create(
            nama="Wakil Ketua Dua", jabatan="Wakil Ketua 2", urutan=1
        )
        vice_chair_one = Management.objects.create(
            nama="Wakil Ketua Satu", jabatan="Wakil Ketua 1", urutan=2
        )

        response = self.client.get(reverse("core:profile"))

        self.assertEqual(
            response.context["board"],
            [vice_chair_one, vice_chair_two, secretary],
        )
