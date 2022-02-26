from django.contrib import admin
from .models import Editor
# Register your models here.
@admin.register(Editor)
class EditorAdmin(admin.ModelAdmin):
    pass

