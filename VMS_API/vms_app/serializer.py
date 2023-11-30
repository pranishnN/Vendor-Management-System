from rest_framework import serializers

# project libraries
from vms_app.models import *


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorModel
        fields = ['id', 'name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 
                  'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class PuchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 
                   'status', 'quality_rating', 'issue_date', 'acknowledgment_date',]
        
class VendorPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceModel
        fields = ['vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg',
                   'average_response_time', 'fulfillment_rate',]