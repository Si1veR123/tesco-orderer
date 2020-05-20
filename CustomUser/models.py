from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    tesco_password = models.CharField(max_length=200)

    class Meta(AbstractUser.Meta):
        pass
