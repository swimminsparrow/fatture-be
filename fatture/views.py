from rest_framework import generics, status, views
from fatture.invoice_form import InvoiceForm
from .models import Invoice, Notification
from .serializers import CreateInvoiceSerializer, InvoiceDetailSerializer, NotificationSerializer, InvoiceSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class InvoiceAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CreateInvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class InvoiceDetailByInvoiceNumberAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceDetailSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDetailBySDIAPIView(views.APIView):
    permission_classes = [IsAuthenticated]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    lookup_field = 'sdi_identifier'

    def get(self, request, sdi_identifier):
        try:
            invoice = self.get_queryset().get(sdi_identifier=sdi_identifier)
            serializer = self.get_serializer(invoice)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)


class InvoiceStatusAPIView(views.APIView):

    def get(self, request, sdi_identifier):
        try:
            invoice = Invoice.objects.get(sdi_identifier=sdi_identifier)
            return Response({"status": invoice.status}, status=status.HTTP_200_OK)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)


class InvoiceXMLFileAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request, pk):
        form = InvoiceForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('xml_file')
            invoice = get_object_or_404(
                Invoice, invoice_number=pk)
            filename = f'invoice_{invoice.invoice_number}_{invoice.emitter_user}.xml'

            if uploaded_file:
                with open('media/invoices/' + filename, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                invoice.xml_file = filename
                invoice.save()
                return Response({"xml_file": filename}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "XML file not provided"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Form Invalid" + str(form.errors)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk):
        invoice = get_object_or_404(
            Invoice, invoice_number=pk)
        if invoice.xml_file:
            xml_file_path = (f'media/invoices/{invoice.xml_file}')
            try:
                with open(xml_file_path, 'rb') as xml_file:
                    print(xml_file_path)

                    xml_data = xml_file.read()

                    response = HttpResponse(content_type='application/xml')
                    response['Content-Disposition'] = f'attachment; filename="{invoice.xml_file}"'
                    response.write(xml_data)
                    return response
            except FileNotFoundError:
                raise Http404
        else:
            return HttpResponse("No XML file associated with this invoice.", status=404)


class NotificationListView(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
