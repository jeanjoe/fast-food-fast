from app import app
import json
import unittest
from . import REGISTER_USER, USER_LOGIN, WRONG_USER_LOGIN, REGISTER_USER_RANDOM_EMAIL

BASE_URL = "/api/v1/"

class UserTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_user_register(self):
        response = self.app.post(BASE_URL + 'users/register', json=REGISTER_USER_RANDOM_EMAIL)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "User added successfuly"

    def test_user_register_email_exist(self):
        response = self.app.post(BASE_URL + 'users/register', json=REGISTER_USER)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "This email address is already registered"

    def test_login(self):
        response = self.app.post(BASE_URL + 'users/login', json=USER_LOGIN)
        self.assertEqual(response.status_code, 200)
        assert json.loads(response.data)['message'] == "Login successfully"

    def test_failed_user_login(self):
        response = self.app.post(BASE_URL + 'users/login', json=WRONG_USER_LOGIN)
        self.assertEqual(response.status_code, 401)
        assert json.loads(response.data)['error'] == "Wrong Email or password"
    
    def tearDown(self):
        pass