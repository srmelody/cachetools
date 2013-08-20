import unittest
import requests


class TestCache(unittest.TestCase):
    root = ""

    def setUp(self):
        self.root = "https://nginx-cache.poc.currdc.net/api"
        pass

    def test403(self):
        r = requests.get(self.root + "/admin",  verify=False, auth=('admin', 'secret'))
        self.assertEquals("Secured resource", r.text)

        r = requests.get(self.root + "/admin", verify=False, auth=('user', 'user'))
        self.assertEquals( 403, r.status_code)


    def testUsers(self):
        r = requests.get(self.root + "/user", verify=False, auth=('admin', 'secret'))

        self.assertEquals("admin", r.text)

        r = requests.get(self.root + "/user", verify=False, auth=('user', 'user'))

        self.assertEquals("user", r.text)

        r = requests.get(self.root + "/user", verify=False, auth=('admin', 'secret'))

        self.assertEquals("admin", r.text)

        r = requests.get(self.root + "/user", verify=False)
        print r.text
        print r.headers
        self.assertEquals(r.text, "No user")

    def testSecure(self):
        r = requests.get(self.root + "/secure", verify=False, auth=('admin', 'secret'))

        self.assertEquals("Secured resource", r.text)

        r = requests.get(self.root + "/secure", verify=False, auth=('user', 'user'))

        self.assertEquals("Secured resource", r.text)

        r2 = requests.get(self.root + "/secure", verify=False, auth=('admin', 'bad'))
        self.assertEquals(r2.status_code, 401)

        r = requests.get(self.root + "/secure", verify=False, auth=('admin', 'secret'))

        self.assertEquals("Secured resource", r.text)


if __name__ == '__main__':
    unittest.main()
