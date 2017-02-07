import json
from datetime import timedelta as td
from django.utils.timezone import now

from hc.api.models import Check
from hc.test import BaseTestCase
from django.conf import settings
from django.urls import reverse


class ListChecksTestCase(BaseTestCase):

    def setUp(self):
        super(ListChecksTestCase, self).setUp()

        self.now = now().replace(microsecond=0)

        self.a1 = Check(user=self.alice, name="Alice 1")
        self.a1.timeout = td(seconds=3600)
        self.a1.grace = td(seconds=900)
        self.a1.last_ping = self.now
        self.a1.n_pings = 1
        self.a1.status = "new"
        self.a1.save()

        self.a2 = Check(user=self.alice, name="Alice 2")
        self.a2.timeout = td(seconds=86400)
        self.a2.grace = td(seconds=3600)
        self.a2.last_ping = self.now
        self.a2.status = "up"
        self.a2.save()

    def get(self):
        return self.client.get("/api/v1/checks/", HTTP_X_API_KEY="abc")

    def test_it_works(self):
        response = self.get()
        ### Assert the response status code
        self.assertEqual(response.status_code, 200)
        doc = response.json()
        self.assertTrue("checks" in doc)

        checks = {check["name"]: check for check in doc["checks"]}

        ### Assert the expected length of checks
        self.assertEqual(len(checks), 2)
        ### Assert the checks Alice 1 and Alice 2's timeout, grace, ping_url,
        ### status, last_ping, n_pings and pause_url


        alice1 = checks["Alice 1"]
        alice2 = checks["Alice 2"]

        list1 = [
                    alice1["timeout"], alice1["grace"],
                    alice1["ping_url"], alice1["status"],
                    alice1["last_ping"].replace("T"," "),
                    alice1["n_pings"], alice1["pause_url"]
                ]
        list2 = [
                    alice2["timeout"], alice2["grace"],
                    alice2["ping_url"], alice2["status"],
                    alice2["last_ping"].replace("T"," "),
                    alice2["n_pings"], alice2["pause_url"]
                ]
        a1_pause = settings.SITE_ROOT + reverse("hc-api-pause", args = [str(self.a1.code)])
        a2_pause = settings.SITE_ROOT + reverse("hc-api-pause", args = [str(self.a2.code)])

        time_ping = str(self.now).replace("T"," ")

        self.assertListEqual(list1,[3600, 900,
                            settings.PING_ENDPOINT + str(self.a1.code), "new",
                            time_ping, 1, a1_pause
                            ])
        self.assertListEqual(list2,[86400, 3600,
                            settings.PING_ENDPOINT + str(self.a2.code), "up",
                            time_ping, 0, a2_pause
                            ])


    def test_it_shows_only_users_checks(self):
        bobs_check = Check(user=self.bob, name="Bob 1")
        bobs_check.save()

        response = self.get()
        data = response.json()
        self.assertEqual(len(data["checks"]), 2)
        for check in data["checks"]:
            self.assertNotEqual(check["name"], "Bob 1")

    ### Test that it accepts an api_key in the request
    def test_it_accepts_api_key_in_request(self):
        payload = {"api_key":"abc"}
        response =self.client.get("/api/v1/checks/", payload)
        self.assertEqual(response.json()["error"], "wrong api_key")
