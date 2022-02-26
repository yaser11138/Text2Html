from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Editor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = RichTextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.body


