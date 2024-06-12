from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    type = models.CharField(max_length=500)
    matab = models.CharField(max_length=500)

    def __str__(self):
        return self.username
    