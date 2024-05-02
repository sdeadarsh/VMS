from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vendor, PurchaseOrder


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


class PurchaseOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_purchase(self):
        response = self.client.post('/api/purchase_order/',
                                    {
                                        "po_number": "12345",
                                        "vendor": 1,
                                        "delivery_date": "2024-05-20T10:00:00",
                                        "items": [
                                            {
                                                "name": "Product 1",
                                                "quantity": 10
                                            },
                                            {
                                                "name": "Product 2",
                                                "quantity": 5
                                            }
                                        ],
                                        "quantity": 15,
                                        "status": "pending",
                                        "issue_date": "2024-05-10T10:00:00",
                                        "acknowledgment_date": None
                                    })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, '12345')

    def test_retrieve_purchase(self):
        purchase_order = PurchaseOrder.objects.create(po_number="12345", vendor=1, delivery_date="2024-05-20T10:00:00",
                                                      quantity=15, status="pending", issue_date="2024-05-10T10:00:00")
        response = self.client.get(f'/api/purchase_order/{purchase_order.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], '12345')
