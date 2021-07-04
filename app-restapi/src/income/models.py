from django.contrib.auth import get_user_model
from django.db import models

from helpers.models import BaseAppModel

User = get_user_model()


class Income(BaseAppModel):
    SOURCE_OPTIONS = [
        ('SALARY', 'SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLES', 'SIDE-HUSTLES'),
        ('OTHERS', 'OTHERS')
    ]

    source = models.CharField(choices=SOURCE_OPTIONS, max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)

    def __str__(self):
        return str(self.owner) + 's income'
