from django import forms


class InvoiceForm(forms.Form):
    xml_file = forms.FileField(
        label='XML File',
        required=True,
        widget=forms.FileInput()  # Use the standard FileInput widget for single file upload
    )
