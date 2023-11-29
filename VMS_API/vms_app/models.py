from django.db import models

# Create your models here.



class VendorModel(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.contact_details})"


class PurchaseOrder(models.Model):
    status = (
        ('pending', 'pending'),
        ('completed', 'completed'),
        ('canceled', 'canceled'),
    )
    po_number = models.CharField(max_length=100)
    vendor = models.ForeignKey('VendorModel',  on_delete=models.RESTRICT, related_name="povendorid")
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=status, default='pending')
    quality_rating = models.FloatField()
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)


class PerformanceModel(models.Model):
    vendor = models.ForeignKey('VendorModel',  on_delete=models.RESTRICT, related_name="perforvendorid")
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()