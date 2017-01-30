from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase
from .. import views
import json 


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()
        self.client.login(username="bob@example.org", password="password")

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_login_and_redirects_already_logged_in(self):
        # res = self.client.post(email="bob@example.org", password="password")
        payload = {"email":"bob@example.org", "password":"password"}
        res = self.client.post("/accounts/login/", payload, content = "application/json")
        self.assertRedirects(res, "/checks/")

    ### Login with a bad token and check that it redirects
    def test_login_with_bad_token_redirects(self):
        # payload = {"username":"bob@example.org", "token":"password"}
        # res = self.client.post("/accounts/login/", payload, content = "application/json")
        # self.assertRedirects(res, "/checks/")

        r = self.client.post("/accounts/check_token/alice/secret-tokken/")
        self.assertRedirects(r, "/accounts/login/")


    ### Any other tests?
