from django.contrib import admin
from .models import Passcode
# Register your models here.


@admin.register(Passcode)
class PassCodeAdmin(admin.ModelAdmin):
    list_display = ("passcode", "user", "date_created")