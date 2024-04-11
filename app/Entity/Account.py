import random
from django.db import models

class Account(models.Model):
    is_active = models.BooleanField(default=True)
    user_subscriber = models.CharField(max_length=12, unique=True)

    def save(self, *args, **kwargs):
        if not self.user_subscriber:
            self.user_subscriber = self.generate_unique_subscriber_number()
        super(Account, self).save(*args, **kwargs)

    def generate_unique_subscriber_number(self):
        length = 12
        # Génère un numéro purement numérique
        while True:
            subscriber_number = ''.join(random.choice('0123456789') for _ in range(length))
            # Vérifie si le numéro est unique
            if not Account.objects.filter(user_subscriber=subscriber_number).exists():
                break
        return subscriber_number

    def __str__(self):
        return f"Compte {self.numero_de_compte}"
