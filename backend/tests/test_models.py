from django.test import TestCase
from backend.models import Domain

class DomainTestCase(TestCase):
    def setUp(self):
        Domain.objects.create(domain="testdom.loc", host_name="dc01",ipv4address='192.168.56.10')

    def test_object_can_be_found(self):
        testdom = Domain.objects.get(domain="testdom.loc")
        self.assertEqual(testdom.domain, 'testdom.loc')