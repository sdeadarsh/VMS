from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor


class VendorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_vendor(self):
        response = self.client.post('/api/vendors/', {'name': 'Test Vendor', 'contact_details': 'test@example.com',
                                                      'address': '123 Test St', 'vendor_code': 'TEST001'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 1)
        self.assertEqual(Vendor.objects.get().name, 'Test Vendor')

    def test_retrieve_vendor(self):
        vendor = Vendor.objects.create(name='Test Vendor', contact_details='test@example.com', address='123 Test St',
                                       vendor_code='TEST001')
        response = self.client.get(f'/api/vendors/{vendor.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Vendor')
