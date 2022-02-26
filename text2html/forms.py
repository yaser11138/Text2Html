from django import forms
from .models import Editor
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField



class EditorForm(forms.ModelForm):
    class Meta:
        model = Editor
        fields = ("body",)


