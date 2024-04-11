from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)
    level = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'role'

    def __str__(self):
        return self.name