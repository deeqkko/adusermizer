from rest_framework.test import RequestsClient
from django.test import TestCase

users_url = 'http://localhost:8000/api/users/?format=json'

class UserTestCase(TestCase):

    def test_users_api(self):
        client = RequestsClient()
        response = client.get(users_url)
        print(response)
        assert response.status_code == 200