import datetime
from django.shortcuts import render
from .forms import MyUserCreation
from .models import Passcode
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, models, logout, login as dj_login
from django.contrib.auth.decorators import login_required
from djangoProject4 import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
import secrets
import string
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password-reset.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = "/"


# check if the code has expired or not
def is_expired(date_created, user, passcode):
    if datetime.datetime.now() - date_created >= datetime.timedelta(seconds=12720):
        new_passcode = create_password()
        passcode.passcode = new_passcode
        passcode.save()
        sent_email(user.username, user.email, new_passcode)
        return True


# check the user verification
def verification(request, id):
    if request.method == "POST":
        id = force_str(urlsafe_base64_decode(id))
        passcode = request.POST["passcode"]
        user_passcode = Passcode.objects.get(user__id=id)
        user = models.User.objects.get(id=id)
        date_created = user_passcode.date_created.replace(tzinfo=None)
        if is_expired(date_created, user, user_passcode):
            render(request, "validate.html", {"expire": True})
        elif passcode == user_passcode.passcode:
            user.is_active = True
            user.save()
            user_passcode.delete()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, "validate.html", {"error": True})
    else:
        return render(request, "validate.html", {})


# create a user and send email with passcode to user for verification
def signup(request):
    if request.method == "POST":
        user_info = MyUserCreation(request.POST)
        if user_info.is_valid():
            user = user_info.save(commit=False)
            user.is_active = False
            user.save()
            passcode = create_password()
            sent_email(user_info.data["username"], user_info.data["email"], passcode)
            Passcode.objects.create(passcode=passcode, user=user)
            id = urlsafe_base64_encode(force_bytes(user.pk))
            return HttpResponseRedirect(f"/verification/{id}/")
        else:
            return render(request, "signup.html", context={"form": user_info, "errors": user_info.errors})
    sign_up = MyUserCreation()
    return render(request, "signup.html", context={"form": sign_up})


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        auth = authenticate(request, username=username, password=password)
        if auth:
            dj_login(request, auth)
            return HttpResponseRedirect(f"http://{request._get_raw_host()}/")
        else:
            return render(request, "login.html", {"error": True})
    return render(request, "login.html", {})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(f"http://{request._get_raw_host()}/")


# create random password
def create_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    return password


# sent verification email
def sent_email(username, email, passcode):
    subject = 'welcome to T2H world'
    message = f'Hi {username}, thank you for registering in Text To HTML.\n {passcode} \n ' \
              f'this passcode will be expired in tow minutes'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
