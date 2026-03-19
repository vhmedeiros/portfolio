from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name":    forms.TextInput(attrs={"placeholder": "Seu nome"}),
            "email":   forms.EmailInput(attrs={"placeholder": "seu@email.com"}),
            "subject": forms.TextInput(attrs={"placeholder": "Assunto"}),
            "message": forms.Textarea(attrs={"placeholder": "Sua mensagem...", "rows": 5}),
        }
