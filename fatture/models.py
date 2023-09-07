from django.db import models
from django.contrib.auth.models import User


class Invoice(models.Model):
    """
    invoice_number (str): Un identificatore univoco per la fattura.
    issue_date (date): La data in cui è stata emessa la fattura.
    due_date (date): La data di scadenza per il pagamento.
    emitter_full_name (str): Il nome completo dell'emittente.
    emitter_email (str): L'indirizzo email dell'emittente.
    destination_full_name (str): Il nome completo del destinatario.
    destination_email (str): L'indirizzo email del destinatario.
    total_amount (decimal): L'importo totale della fattura.
    status (str): Lo stato attuale della fattura.
    emitter_user (ForeignKey to User, opzionale): L'utente che ha emesso la fattura (opzionale).
    destination_user (ForeignKey to User, opzionale): L'utente a cui è stata inviata la fattura (opzionale).
    sdi_identifier (str, unico): Identificativo per il Sistema di Interscambio (SDI).
    xml_file (file, opzionale): Il file XML associato alla fattura (opzionale).
    """

    STATUS_CHOICES = [
        ('Inviata', 'Inviata'),
        ('Ricevuta', 'Ricevuta'),
        ('Pagata', 'Pagata'),
        ('Annullata', 'Annullata'),
        ('Non Pagata', 'Non Pagata'),
    ]
    invoice_number = models.AutoField(primary_key=True)
    issue_date = models.DateField()
    due_date = models.DateField()
    emitter_full_name = models.CharField(max_length=100)
    emitter_email = models.EmailField()
    destination_full_name = models.CharField(max_length=100)
    destination_email = models.EmailField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Inviata')
    emitter_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='emitter_user')
    destination_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='destination_user')
    sdi_identifier = models.CharField(max_length=100, unique=True, null=True)
    xml_file = models.FileField(
        upload_to='xml_invoices/', null=True, blank=True)

    class Meta:
        unique_together = ('invoice_number', 'emitter_user')

    def __str__(self):
        return self.invoice_number


class Notification(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    sdi_identifier = models.CharField(max_length=100)
