from django.contrib import admin
from vms_app import models as mdl
# Register your models here.
admin.site.register(mdl.VendorModel)
admin.site.register(mdl.PurchaseOrder)
admin.site.register(mdl.PerformanceModel)
