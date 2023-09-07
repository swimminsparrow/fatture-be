
from rest_framework import serializers
from .models import Invoice, Notification


class CreateInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('invoice_number', 'issue_date', 'due_date', 'emitter_full_name', 'emitter_email',
                  'destination_full_name', 'destination_email', 'total_amount', 'status',
                  'emitter_user', 'destination_user', 'sdi_identifier')
        extra_kwargs = {
            'sdi_identifier': {'required': False},
            'invoice_number': {'required': False}
        }


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('issue_date', 'due_date', 'emitter_full_name', 'emitter_email',
                  'destination_full_name', 'destination_email', 'total_amount', 'status',
                  'emitter_user', 'destination_user', 'sdi_identifier')
        extra_kwargs = {
            'issue_date': {'required': False},
            'due_date': {'required': False},
            'emitter_full_name': {'required': False},
            'emitter_email': {'required': False},
            'destination_full_name': {'required': False},
            'destination_email': {'required': False},
            'total_amount': {'required': False},
            'status': {'required': False},
            'emitter_user': {'required': False},
            'destination_user': {'required': False},
            'sdi_identifier': {'required': True}
        }


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
