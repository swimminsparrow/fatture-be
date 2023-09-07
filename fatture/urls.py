from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('invoices/', views.InvoiceAPIView.as_view(), name='invoices'),

    path('invoices/invoice_number/<int:pk>/',
         views.InvoiceDetailByInvoiceNumberAPIView.as_view(), name='invoice-detail-invoicenumber'),

    path('invoices/sdi_identifier/<str:sdi_identifier>/', views.InvoiceDetailBySDIAPIView.as_view(),
         name='invoice-detail-sdi'),

    path('invoices/sdi_identifier/<str:sdi_identifier>/status/', views.InvoiceStatusAPIView.as_view(),
         name='invoice-detail-status'),

    path('invoices/xml/invoice_number/<int:pk>/',
         views.InvoiceXMLFileAPIView.as_view(), name='invoice-xml'),

    # NOT IMPLEMENTED
    path('notifications/', views.NotificationListView.as_view(),
         name='notification-list'),
    path('notifications/<int:pk>/',
         views.NotificationDetailView.as_view(), name='notification-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
