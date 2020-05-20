from django.db import models
from CustomUser.models import User

# Create your models here.


class Order(models.Model):
    min_date = models.DateField()
    max_date = models.DateField()
    min_time = models.TimeField()
    max_time = models.TimeField()

    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.min_date) + " - " + str(self.max_date)
