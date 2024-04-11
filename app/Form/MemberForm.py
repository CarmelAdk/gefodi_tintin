from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from app.Entity.Role import Role

IS_ACTIVE_CHOICES = (
    (True, 'Oui'),
    (False, 'Non'),
)

class MemberForm(forms.ModelForm):
    last_name = forms.CharField(min_length=2, max_length=19, label="Nom", required=True, widget=forms.TextInput(attrs={"class": "form-control", "id": "last_name", "placeholder": "Nom", "pattern": r"([a-zA-ZÀ-ÖØ-öø-ÿ][a-zA-ZÀ-ÖØ-öø-ÿ\-' ]{1,18})"}))
    first_name = forms.CharField(min_length=2, max_length=19, label="Prénom", required=True, widget=forms.TextInput(attrs={"class": "form-control", "id": "first_name", "placeholder": "Prénom", "pattern": r"([a-zA-ZÀ-ÖØ-öø-ÿ][a-zA-ZÀ-ÖØ-öø-ÿ\-' ]{1,18})"}))
    email = forms.EmailField(max_length=50, label="Email", required=True, widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "nom@exemple.com", "pattern": r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,4}"}))
    role = forms.ModelChoiceField(queryset=Role.objects.exclude(name='MANAGER'), empty_label="Choisir un rôle", label="Rôle", required=True, initial=Role.objects.get(name='EDITOR'), widget=forms.Select(attrs={"class": "form-control"}))
    is_active = forms.ChoiceField(label="Actif", required=False, choices=IS_ACTIVE_CHOICES, widget=forms.Select(attrs={"class": "form-control"}))

    class Meta:
        model = get_user_model()
        fields = ("last_name", "first_name", "email", "role", "is_active")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if get_user_model().objects.exclude(id=self.instance.id).filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà associée à un compte. Veuillez utiliser une autre adresse e-mail.")
        return email
