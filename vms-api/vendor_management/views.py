from rest_framework import viewsets
from rest_framework.response import Response
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from rest_framework.decorators import action
import pandas as pd
import numpy as np
from .utils import error_response, success_response
from django.utils import timezone
from django.db.models import Count, Sum, ExpressionWrapper, F, Value, Avg, DurationField, FloatField
from .request import RequestProcess
from .response import ResponseProcess


class VendorViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'patch', 'delete']
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):  # This function is to insert the vendor data
        rs = RequestProcess(request.data)
        rs.has(['name', 'contact_details', 'address'])
        error = rs.has_errors()
        if error:
            res = ResponseProcess({}, message=error)
            return res.errord_response()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):  # This function is to update the vendor data
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):  # This function is to destroy the vendor data
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    def list(self, request, *args, **kwargs):  # This function is list the vendor data
        try:
            df_data = pd.DataFrame(Vendor.objects.all().values())
            df = df_data.replace({np.nan: None})
            if df.empty:
                return error_response("No Data Found")
            final_data = df.to_dict(orient="records")
            return success_response(final_data)
        except Exception as e:
            return error_response('Error in Vendor')

    def retrieve(self, request, *args, **kwargs):
        try:
            df_data = pd.DataFrame(Vendor.objects.filter(id=int(kwargs['pk'])).values())
            df = df_data.replace({np.nan: None})
            if df.empty:
                return error_response("No Data Found")
            final_data = df.to_dict(orient="records")
            return success_response(final_data)
        except Exception as e:
            return error_response('Error in Vendor')

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """
        Retrieve a vendor's performance metrics.

        This endpoint retrieves the calculated performance metrics for a specific vendor.
        It returns data including on_time_delivery_rate, quality_rating_avg,
        average_response_time, and fulfillment_rate.

        Example usage:
        GET /api/vendors/1/performance/

        Response:
        {
            "on_time_delivery_rate": 90.0,
            "quality_rating_avg": 4.5,
            "average_response_time": 2.5,
            "fulfillment_rate": 95.0
        }
        """
        try:
            vendor_df = pd.DataFrame(HistoricalPerformance.objects.filter(vendor=pk).values())
            df = vendor_df.replace({np.nan: None})
            if df.empty:
                return error_response("No Data Found")
            vendor = df.to_dict(orient="records")
            # performance_data = {
            #     'vendor': vendor.id,
            #     'on_time_delivery_rate': vendor.on_time_delivery_rate,
            #     'quality_rating_avg': vendor.quality_rating_avg,
            #     'average_response_time': vendor.average_response_time,
            #     'fulfillment_rate': vendor.fulfillment_rate,
            #     'date': vendor.date
            # }
            return Response(vendor)
        except Exception as e:
            print(str(e))
            return error_response("Error in performances data")


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'get', 'patch', 'delete']
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        rs = RequestProcess(request.data)
        rs.has(['po_number', 'vendor', 'delivery_date', 'items', 'quantity', 'status'])
        error = rs.has_errors()
        if error:
            res = ResponseProcess({}, message=error)
            return res.errord_response()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        rs = RequestProcess(request.data)
        rs.has(['vendor', 'status'])
        error = rs.has_errors()
        if error:
            res = ResponseProcess({}, message=error)
            return res.errord_response()
        historical_performance_payload = {"vendor": int(request.data['vendor'])}
        vendor_payload = {'id': int(request.data['vendor'])}
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        completed_orders = PurchaseOrder.objects.filter(vendor=request.data['vendor'])
        if 'status' in request.data:
            self.update_fulfillment_rate(historical_performance_payload, vendor_payload, completed_orders) # this function is for calculating th average of fulfilment data
        if request.data.get('status', None) == 'completed':
            self.update_on_time_delivery_rate(historical_performance_payload, vendor_payload, completed_orders)  # this function is for calculating th percentage of on time delivery
            self.update_quality_rating_avg(historical_performance_payload, vendor_payload, completed_orders)  # this function is for calculating th average of quality rating
        if 'acknowledgment_date' in request.data:
            self.update_average_response_time(historical_performance_payload, vendor_payload, completed_orders)  # this function is for calculating th average of response time which is stored in days
        self.update_vendor_data(historical_performance_payload, vendor_payload, request.data['vendor']) # this function is used to store the data of Historical vendor and current vendor
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    def list(self, request, *args, **kwargs):
        try:
            df_data = pd.DataFrame(PurchaseOrder.objects.all().values())
            df = df_data.replace({np.nan: None})
            if df.empty:
                return error_response("No Data Found")
            final_data = df.to_dict(orient="records")
            return success_response(final_data)
        except Exception as e:
            return error_response('Error in Purchase Order')

    def retrieve(self, request, *args, **kwargs):
        try:
            df_data = pd.DataFrame(PurchaseOrder.objects.filter(id=int(kwargs['pk'])).values())
            df = df_data.replace({np.nan: None})
            if df.empty:
                return error_response("No Data Found")
            final_data = df.to_dict(orient="records")
            return success_response(final_data)
        except Exception as e:
            return error_response('Error in Purchase Order')

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        if 'acknowledgment_date' in request.data:
            acknowledgment_date = request.data['acknowledgment_date']
            PurchaseOrder.objects.filter(id=pk).update(acknowledgment_date=acknowledgment_date)
            vendor_data = PurchaseOrder.objects.filter(id=pk).values('vendor')
            vendor = vendor_data[0]['vendor']
            completed_orders = PurchaseOrder.objects.filter(vendor=vendor)
            historical_performance_payload = {"vendor": request.data['vendor']}
            vendor_payload = {'id': request.data['vendor']}
            self.update_average_response_time(historical_performance_payload, vendor_payload, completed_orders)
            self.update_vendor_data(historical_performance_payload, vendor_payload, request.data['vendor'])
        return success_response("Successfully Updated")

    def update_on_time_delivery_rate(self, historical_performance_payload, vendor_payload, completed_orders):
        on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = 0.0
        if completed_orders.exists():
            on_time_delivery_rate = round(on_time_orders.count() * 100 / completed_orders.count(), 2)
        vendor_payload['on_time_delivery_rate'] = on_time_delivery_rate
        historical_performance_payload['on_time_delivery_rate'] = on_time_delivery_rate

    def update_quality_rating_avg(self, historical_performance_payload, vendor_payload, completed_orders):
        quality_rating = completed_orders.filter(quality_rating__isnull=False)
        quality_rating_avg = 0.0
        if quality_rating.exists():
            quality_rating_total_sum = quality_rating.aggregate(total_sum=Sum('quality_rating'))['total_sum']
            quality_rating_total_count = quality_rating.count()
            quality_rating_avg = quality_rating_total_sum / quality_rating_total_count
        vendor_payload['quality_rating_avg'] = quality_rating_avg
        historical_performance_payload['quality_rating_avg'] = quality_rating_avg

    def update_average_response_time(self, historical_performance_payload, vendor_payload, completed_orders):
        completed_orders = completed_orders.filter(acknowledgment_date__isnull=False)
        if completed_orders.exists():
            new_response_times = completed_orders.annotate(
                response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField()
                                                )).values()
            response_time_data = new_response_times[0]['response_time'].days
            historical_performance_payload['average_response_time'] = 0
            vendor_payload['average_response_time'] = 0
            if response_time_data > 0:
                historical_performance_payload['average_response_time'] = float(response_time_data)
                vendor_payload['average_response_time'] = float(response_time_data)

    def update_fulfillment_rate(self, historical_performance_payload, vendor_payload, completed_orders):
        total_orders = completed_orders.count()
        fulfilled_orders = completed_orders.filter(status='completed')
        fulfillment_rate = 0.0
        if total_orders > 0:
            fulfillment_rate = float(fulfilled_orders.count() / total_orders)
        historical_performance_payload['fulfillment_rate'] = fulfillment_rate
        vendor_payload['fulfillment_rate'] = fulfillment_rate

    def update_vendor_data(self, historical_performance_payload, vendor_payload, vendor_id):
        Vendor.objects.filter(id=vendor_id).update(**vendor_payload)
        # print(historical_performance_payload)
        hv_ser = HistoricalPerformanceSerializer(data=historical_performance_payload)
        hv_ser.is_valid(raise_exception=True)
        hv_ser.save()
        # serializer = HistoricalPerformanceSerializer..get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # HistoricalPerformance.objects.create(**historical_performance_payload)
