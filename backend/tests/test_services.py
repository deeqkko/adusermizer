from django.test import TestCase
from backend.services import connect

class ConnectionTestCase(TestCase):
    def test_connection_success(self):
        """Connection with correct credentials is successful"""
        conn = connect('192.168.56.10','administrator','kakkah0u5u1!')
        conn.run('')
        self.assertEqual(conn.is_connected, True)
        conn.close()

    def test_connection_not_success(self):
        """Connection with incorrect credentials is not successful"""
        conn = connect('192.168.56.10','administrator','kakka')
        #conn.run('')
        self.assertEqual(conn.is_connected, False)
        conn.close()

class GetUsersTestCase(TestCase):
    def test_get_all_users(self):
        conn = connect('192.168.56.10','administrator','kakkah0u5u1!')
        users = conn.run('powershell documents\getUsers.ps1').stdout