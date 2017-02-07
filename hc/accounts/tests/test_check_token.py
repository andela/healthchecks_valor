from django.contrib.auth.hashers import make_password

import json 

from hc.accounts import views
from hc.test import BaseTestCase

class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
        self.client.login(username="bob@example.org", password="password")

    def test_it_shows_form(self):
        response = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(response, "You are about to log in")

    def test_it_redirects(self):
        response = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(response, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_login_and_redirects_already_logged_in(self):
        payload = {"email":"bob@example.org", "password":"password"}
        response = self.client.post("/accounts/login/", payload, content = "application/json")
        self.assertRedirects(response, "/checks/")

    ### Login with a bad token and check that it redirects
    def test_login_with_bad_token_redirects(self):
        response = self.client.post("/accounts/check_token/alice/secret-tokken/")
        self.assertRedirects(response, "/accounts/login/")


    ### Any other tests?
