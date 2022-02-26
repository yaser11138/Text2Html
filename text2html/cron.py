from django.contrib.auth.models import User


def hi():
    User.objects.filter(is_active=False).delete()