from hc.test import BaseTestCase

class Unresolved(BaseTestCase):

    def test_it_works(self):
        url = "/unresolved/"
        self.client.login(username="alice@example.org", password="password")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
