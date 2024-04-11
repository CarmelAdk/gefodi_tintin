from django import forms
from app.models import CompanyStatus

class CompanyStatusForm(forms.ModelForm):
    status_name = forms.CharField(max_length=50, label="Statut", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'status_name', 'placeholder': "Statut"}))
    short_name = forms.CharField(max_length=10, label="Acronyme", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'short_name', 'placeholder': 'Acronyme'}))
    description = forms.CharField(max_length=250, label="Description", required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'description', 'placeholder': 'Description', 'rows': 4}))

    def clean_status_name(self):
        status_name = self.cleaned_data['status_name']
        # Vérifier si un autre enregistrement avec le même statut existe déjà dans la base de données
        if CompanyStatus.objects.filter(status_name=status_name).exists():
            # Si le STATUT existe déjà dans la base de données, vérifier s'il est différent de celui de l'instance actuelle
            if self.instance and self.instance.status_name == status_name:
                # Si le STATUT est identique à celui de l'instance actuelle, laisser passer la validation
                return status_name
            else:
                raise forms.ValidationError("Ce Statut existe déjà.")
        return status_name

    def clean_short_name(self):
        short_name = self.cleaned_data['short_name']
        # Vérifier si un autre enregistrement avec le même Acronyme existe déjà dans la base de données
        if CompanyStatus.objects.filter(short_name=short_name).exists():
            # Si l'Acronyme existe déjà dans la base de données, vérifier s'il est différent de celui de l'instance actuelle
            if self.instance and self.instance.short_name == short_name:
                # Si l'Acronyme est identique à celui de l'instance actuelle, laisser passer la validation
                return short_name
            else:
                raise forms.ValidationError("Cet Acronyme existe déjà.")
        return short_name

    class Meta:
        model = CompanyStatus
        fields = ('status_name', 'short_name', 'description')