from django.test.utils import override_settings

from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        res = self.client.post(url, form)

        self.assertRedirects(res, "/integrations/")
        assert Channel.objects.count() == 1

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """

        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_{}/".format(frag)
            res = self.client.get(url)
            self.assertContains(res, "Integration Settings", status_code=200)

    ### Test that the team access works
    def test_team_access_works(self):
        self.channel = Channel(user=self.alice, kind="email")
        self.channel.value = "alice@example.org"
        self.channel.save()

        url = "/integrations/{}/checks/".format(self.channel.code)
        # We login as bob since bob has access the code should work.
        self.client.login(username="bob@example.org", password="password")
        res = self.client.get(url)
        self.assertContains(res, "Assign Checks to Channel", status_code=200)

    ### Test that bad kinds don't work
    def test_bad_kinds(self):
        # Tests invalid channels 
        self.client.login(username="alice@example.org", password="password")
        kinds = ("facebook", "whatsapp")
        for frag in kinds:
            url = "/integrations/add_{}/".format(frag)
            res = self.client.get(url)
            assert res.status_code == 404