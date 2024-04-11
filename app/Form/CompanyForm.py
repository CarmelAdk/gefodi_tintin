from django import forms
from app.models import Company, CompanyStatus
from django.core.validators import FileExtensionValidator
from django.template.defaultfilters import filesizeformat
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


NB_EMPLOYES_CHOICES = [
    ('1 - 5', '1 à 5'),
    ('6 - 15', '6 à 15'),
    ('16 - 50', '16 à 50'),
    ('51 - 100', '51 à 100'),
    ('Plus de 100', 'Plus de 100'),
]

class CompanyForm(forms.ModelForm):
    name = forms.CharField(max_length=50, label="Nom de l'entreprise", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': "Nom de l'entreprise", 'readonly': 'readonly', 'style': 'background-color: #f0f0f0;'}))
    acronym = forms.CharField(max_length=45, label="Acronyme", required=False, widget=forms.TextInput(attrs={'class': 'form-control acronym-input', 'id': 'acronym', 'placeholder': 'Acronyme'}))
    siret = forms.CharField(max_length=14, label="SIRET", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'siret', 'placeholder': 'SIRET', 'readonly': 'readonly', 'style': 'background-color: #f0f0f0;'}))
    capital = forms.DecimalField(max_digits=14, decimal_places=2, label="Capital", required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'capital', 'placeholder': 'Capital'}))
    address = forms.CharField(max_length=100, label="Adresse Complete", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Adresse'}))
    phone = forms.CharField(max_length=15, label="Téléphone", required=False, widget=forms.TextInput(attrs={'class': 'form-control phone-input', 'id': 'phone', 'placeholder': 'Téléphone'}))
    fax = forms.CharField(max_length=45, label="Fax", required=False, widget=forms.TextInput(attrs={'class': 'form-control fax-input', 'id': 'fax', 'placeholder': 'Fax'}))
    email = forms.EmailField(max_length=45, label="Email", required=False, widget=forms.EmailInput(attrs={'class': 'form-control email-input', 'id': 'email', 'placeholder': 'Email'}))
    logotype = forms.FileField(label="Logotype", required=False, widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'logotype', 'placeholder': 'Logotype'}),validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])
    naf_ape = forms.CharField(max_length=45, label="Code NAF/APE", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'naf_ape', 'placeholder': 'NAF/APE', 'readonly': 'readonly', 'style': 'background-color: #f0f0f0;'}))
    nb_employees = forms.ChoiceField(label="Nombre d'employés", choices=NB_EMPLOYES_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control', 'id': 'nb_employees', 'placeholder': "Nombre d'employés"}))
    status = forms.ModelChoiceField(queryset=CompanyStatus.objects.all(), label="Statut", required=True, empty_label='', widget=forms.Select(attrs={'class': 'form-control status-input', 'id': 'status', 'placeholder': "Statut de l'entreprise"}))

    def clean_siret(self):
        siret = self.cleaned_data['siret']
        # Vérifier si un autre enregistrement avec le même siret existe déjà dans la base de données
        if Company.objects.filter(siret=siret).exists():
            # Si le SIRET existe déjà dans la base de données, vérifier s'il est différent de celui de l'instance actuelle
            if self.instance and self.instance.siret == siret:
                # Si le SIRET est identique à celui de l'instance actuelle, laisser passer la validation
                return siret
            else:
                raise forms.ValidationError("Ce SIRET existe déjà.")
        # Valider le format du SIRET
        if not siret.isdigit():
            raise forms.ValidationError("Le champ \"SIRET\" doit être composé uniquement de chiffres.")
        if len(siret) != 14:
            raise forms.ValidationError("Le champ \"SIRET\" doit comporter exactement 14 chiffres.")
        return siret

    def clean_capital(self):
        capital = self.cleaned_data['capital']
        if capital is not None:
            capital_str = str(capital)
            if len(capital_str) > 14:
                raise forms.ValidationError([
                    "- Le champ \"Capital\" doit comporter au maximum 12 chiffres.",
                    "- Pour les nombres à virgule, il peut comporter 11 chiffres avant la virgule et au maximum 2 chiffres après la virgule."
                ])
        return capital

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Le champ \"Téléphone\" doit être composé uniquement de chiffres.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError("Veuillez fournir une adresse email valide.")
        return email

    def clean_logotype(self):
        logotype = self.cleaned_data.get('logotype', False)
        if logotype:
            if logotype.size > settings.MAX_LOGO_SIZE:
                max_size = filesizeformat(settings.MAX_LOGO_SIZE)
                raise forms.ValidationError(f"La taille du fichier doit être inférieure à {max_size}.")
        return logotype

    class Meta:
        model = Company
        fields = ('name', 'acronym', 'siret', 'capital', 'address', 'logotype', 'naf_ape', 'nb_employees', 'phone', 'fax', 'email', 'status')