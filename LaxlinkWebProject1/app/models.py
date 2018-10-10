"""
Definition of models.
"""

from django.db import models

class Snippet(models.Model):
    name = models.CharField(max_length=100)
    body = models.CharField(max_length=100)

    def __str__(self):
        return self.name
# Create your models here.
