from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = ContactMessage
        fields = ["nama", "email", "telepon", "subjek", "pesan"]
        widgets = {
            "nama": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nama lengkap"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "nama@email.com"}),
            "telepon": forms.TextInput(attrs={"class": "form-control", "placeholder": "08xxxxxxxxxx (opsional)"}),
            "subjek": forms.TextInput(attrs={"class": "form-control", "placeholder": "Perihal pesan"}),
            "pesan": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Tulis pesan Anda…"}),
        }

    def clean_pesan(self):
        pesan = self.cleaned_data["pesan"]
        if len(pesan.strip()) < 10:
            raise forms.ValidationError("Pesan minimal 10 karakter.")
        return pesan

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam terdeteksi.")
        return ""