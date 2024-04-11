from django.db import models
from django.contrib.auth.models import AbstractUser
from app.Entity.Role import Role
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=70)
    cgu_rgpd = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_user', null=True, blank=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
