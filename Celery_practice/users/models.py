from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Model for create/delete/update users."""
    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        max_length=254
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
