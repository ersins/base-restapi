from django.db import models
from django.utils.translation import gettext_lazy as _

from helpers.models import BaseAppModel


class Book(BaseAppModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.PositiveIntegerField()
    publisher = models.PositiveIntegerField()
    print_length = models.PositiveIntegerField()
    language = models.CharField(max_length=50)
    publication_date = models.DateField()
    isbn_13 = models.CharField(max_length=50)
    isbn_10 = models.CharField(max_length=50)
    translator = models.PositiveIntegerField()
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    dimensions = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Publisher(BaseAppModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Author(BaseAppModel):
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
