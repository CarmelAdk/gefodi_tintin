from django.db import models
from django.utils.text import slugify
from app.Entity.CompanyStatus import CompanyStatus
from django.conf import settings  # Importez cette bibliothèque pour référencer le modèle User configuré dans settings.AUTH_USER_MODEL

class Company(models.Model):
    name = models.CharField(max_length=50, null=False)
    acronym = models.CharField(max_length=45)
    siret = models.CharField(max_length=14, null=False, unique=True)
    capital = models.DecimalField(max_digits=14, decimal_places=2)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    fax = models.CharField(max_length=45)
    email = models.EmailField(null=True, blank=True)
    logotype = models.ImageField(null=True, blank=True, upload_to="logotypes")
    naf_ape = models.CharField(max_length=45)
    nb_employees = models.CharField(max_length=12, null=False)
    status = models.ForeignKey(CompanyStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name="companies")
    # Nouveau champ pour représenter le compte  propriétaire de l'entreprise
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_companies')
    slug = models.SlugField(unique=False)
    
    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.name