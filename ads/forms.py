from django import forms
from ads.models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['email', 'phone_number']