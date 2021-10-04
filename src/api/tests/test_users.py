import json
from api.utils.test_base import BaseTestCase
from api.models.user import User
import unittest2 as unittest


def create_users():
    User(username="im_gibson", password=User.generate_hash("written1")).create()
    User(username="im_gibson1", password=User.generate_hash("written1")).create()


class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        create_users()

    def test_login_user(self):
        user = {"username": "im_gibson", "password": "written1"}
        response = self.app.post(
            "/api/v1/users/login",
            data=json.dumps(user),
            content_type="application/json",
        )
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue("access_token" in data)

    def test_login_user_wrong_credentials(self):
        user = {"username": "im_gibson", "password": "written11"}
        response = self.app.post(
            "/api/v1/users/login",
            data=json.dumps(user),
            content_type="application/json",
        )
        self.assertEqual(401, response.status_code)


if __name__ == "__main__":
    unittest.main()
