from django.test.utils import override_settings
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddPushoverTestCase(BaseTestCase):
    
    def test_it_adds_channel(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=n&prio=0"
        res = self.client.get("/integrations/add_pushover/?{}".format(params))
        assert res.status_code == 302

        channels = list(Channel.objects.all())
        assert len(channels) == 1
        assert channels[0].value == "a|0"

    @override_settings(PUSHOVER_API_TOKEN=None)
    def test_it_requires_api_token(self):
        self.client.login(username="alice@example.org", password="password")
        res = self.client.get("/integrations/add_pushover/")
        self.assertEqual(res.status_code, 404)

    def test_it_validates_nonce(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        params = "pushover_user_key=a&nonce=INVALID&prio=0"
        res = self.client.get("/integrations/add_pushover/?{}".format(params))
        assert res.status_code == 403

    ### Test that pushover validates priority    
    def test_it_validates_priority(self):
        self.client.login(username="alice@example.org", password="password")

        session = self.client.session
        session["po_nonce"] = "n"
        session.save()

        # Assign the wrong priority parameter
        params = "pushover_user_key=a&nonce=n&prio=123"
        res = self.client.get("/integrations/add_pushover/?{}".format(params))
        assert res.status_code == 400