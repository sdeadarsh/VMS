from django.db import models
from django.utils import timezone
from .config import STATUS_CHOICES
import uuid


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0) #calculated in days
    fulfillment_rate = models.FloatField(default=0.0)


    def save(self, *args, **kwargs):
        if not self.vendor_code:
            self.vendor_code = str(uuid.uuid4().hex)[:10]  # Generate a unique code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField() #calculated in days
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
