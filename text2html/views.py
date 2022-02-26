from django.shortcuts import render
from .forms import EditorForm
from .models import Editor
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from datetime import datetime


# save the conversion performed by the user
@login_required(login_url='/login/')
def Text2Html(request):
    if request.method == "POST":
        form = EditorForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect("/")

    form = EditorForm()
    return render(request, 'inner-page.html', {'form': form})


def homepage(request):
        part = get_part_of_day(datetime.now().hour)
        return render(request, "homepage.html", context={"part": part})


# Shows all conversions performed by the user
@login_required(login_url='/login/')
def converts(request):
    all_converts = Editor.objects.filter(user=request.user)
    return render(request, 'all.html', {"converts": all_converts})


# get the part of day in each hour
def get_part_of_day(h):
    return (
        "morning"
        if 5 <= h <= 11
        else "afternoon"
        if 12 <= h <= 17
        else "evening"
        if 18 <= h <= 22
        else "night"
    )
