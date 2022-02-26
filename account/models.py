from django.db import models
from django.contrib.auth.models import User


class Passcode(models.Model):
    passcode = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

