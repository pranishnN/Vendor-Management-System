import json
from django.shortcuts import render
from django.db.models import RestrictedError
import datetime

# rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# project library
from vms_app.serializer import *


def update_vendor_performance(vendor_id:int):
    """ 
    This is the function for updating vendor performance.

    Args:
        vendor_id: used to get vendor queryset

    Return:
        Updating vendor details to PerformanceModel everytime updating 'completed' status in purchase order

    Raise:
        Raise exception error
        
    """
    try:
        tommorrow_date = datetime.date.today() + datetime.timedelta(days=1)
        datetime_now = datetime.datetime.now()

        VENDOR_PO_QS = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        delivery_on_order = VENDOR_PO_QS.filter(delivery_date__date=tommorrow_date).count()
        total_completed_order = VENDOR_PO_QS.filter(status__iexact='completed')
        po_quality_rating = sum(list(total_completed_order.values_list('quality_rating', flat=True)))

        issue_and_acknow_date = VENDOR_PO_QS.values('issue_date', 'acknowledgment_date')
        days_diff_lst = []

        for obj in issue_and_acknow_date:
            issue_date = obj.get('issue_date')
            acknowledgment_date = obj.get('acknowledgment_date')
            if acknowledgment_date and issue_date:
                day_diff = issue_date - acknowledgment_date
                days_diff_lst.append(abs(day_diff.days))

        on_time_delivery_rate = delivery_on_order / total_completed_order.count()
        quality_avg_rating = po_quality_rating / total_completed_order.count()
        avg_response_time = sum(days_diff_lst) / len(days_diff_lst)
        fulfilment_rate = total_completed_order.filter(issue_date__isnull=True).count() / total_completed_order.filter(issue_date__isnull=False).count()

        ven_perf_data = {'vendor_id': vendor_id, 'date': datetime_now, 'on_time_delivery_rate': on_time_delivery_rate,
                        'quality_rating_avg': quality_avg_rating, 'average_response_time': avg_response_time, 'fulfillment_rate': fulfilment_rate}
        default_val = {'vendor_id': vendor_id}

        ven_perf_obj, _created = PerformanceModel.objects.update_or_create(**ven_perf_data, defaults=default_val)
        ven_perf_obj.save()

    except Exception as e:
        print('----------e--', e)
        pass

class VendorAPI(APIView):

    def get(self, request):
        try:
            queryset = VendorModel.objects.all()
            serializer_class = VendorSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer_class = VendorSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class EditVendorAPI(APIView):

    def get_queryset(self, vendor_id):
        """
        Function for getting particular vendor data 

        Args:
            vendor_id: Getting vendor queryset

        Return:
            Return obtained vendor queryset
            
        """
        queryset = VendorModel.objects.filter(id=vendor_id)
        return queryset

    def get(self, request, vendor_id):
        try:
            serializer_class = VendorSerializer(self.get_queryset(vendor_id).first())
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, vendor_id):
        try:
            queryset = self.get_queryset(vendor_id).first()
            serializer_class = VendorSerializer(queryset, data=request.data, partial=True)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        try:
            if self.get_queryset(vendor_id).delete():
                return Response({'message':'Successfully deleted'}, status=status.HTTP_200_OK)
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

        except RestrictedError as r:
            return Response({'error':'This data refered with other instance'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print('---e---', e)
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


# Purchase Order

class PurchaseOrderAPI(APIView):

    def get(self, request):
        try:
            queryset = PurchaseOrder.objects.all()
            serializer_class = PuchaseOrderSerializer(queryset, many=True)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            """
            Here we convert the request data to mutable to update the 
            item value to dumbed value to save in db
            """
            request.data._mutable = True
            request.data['items'] = json.dumps(request.data['items'])
            request.data._mutable = False

            serializer_class = PuchaseOrderSerializer(data=request.data)
            if serializer_class.is_valid():
                serializer_class.save()
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class EditPurchaseOrderAPI(APIView):

    def get_queryset(self, po_id):
        return PurchaseOrder.objects.filter(id=po_id)

    def get(self, request, po_id):
        try:
            serializer_class = PuchaseOrderSerializer(self.get_queryset(po_id).first())
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print('-------e-------', e)
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, po_id):
        try:
            """
            Here we convert the request data to mutable to update the 
            item value to dumbed value to save in db.
            """
            request.data._mutable = True
            request.data['items'] = json.dumps(request.data['items'])
            request.data._mutable = False

            queryset = self.get_queryset(po_id).first()
            serializer_class = PuchaseOrderSerializer(queryset, data=request.data, partial=True)
            if serializer_class.is_valid():
                serializer_class.save()

                # Vendor Performance:
                po_status = serializer_class.data.get('status')
                vendor_id = serializer_class.data.get('vendor')

                if po_status == 'completed':
                    update_vendor_performance(vendor_id=vendor_id)

                return Response(serializer_class.data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, po_id):
        try:
            if self.get_queryset(po_id).delete():
                return Response({'message':'Successfully deleted'}, status=status.HTTP_200_OK)
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        
# Performance History 

class VendorPerformanceAPI(APIView):

    def get(self, request, vendor_id):
        try:
            queryset = PerformanceModel.objects.filter(vendor_id=vendor_id).first()
            serializer_class = VendorPerformanceSerializer(queryset)
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error':'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)