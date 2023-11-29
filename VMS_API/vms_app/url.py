from django.urls import path

# project library
from vms_app import views

urlpatterns = [
    path('vendor/', views.VendorAPI.as_view()),
    path('vendor/<int:vendor_id>/', views.EditVendorAPI.as_view()),
    path('purchase_orders/', views.PurchaseOrderAPI.as_view()),
    path('purchase_orders/<int:po_id>/', views.EditPurchaseOrderAPI.as_view()),
    path('vendors/<int:vendor_id>/performance', views.VendorPerformanceAPI.as_view()),

]
