from django.db import models

class CompanyStatus(models.Model):
    status_name = models.CharField(max_length=50, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=False)
    
    class Meta:
        db_table = 'company_status'

    def __str__(self):
        return self.status_name
