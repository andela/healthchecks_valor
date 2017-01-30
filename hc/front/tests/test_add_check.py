from hc.api.models import Check, Channel
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):
    
    def setUp(self):
        super(AddCheckTestCase, self).setUp()
        self.channel = Channel(user=self.alice, kind="email")
        self.channel.value = "alice@example.org"
        self.channel.save()

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ### Test that team access works
    def test_team_access_works(self):
        url = "/checks/add/"
        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)

        check = Check.objects.get()
        # Bob is assigned all channels that belong to Alice
        self.assertEqual(check.user, self.alice)
