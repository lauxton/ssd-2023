import csv
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import Mission

logger = logging.getLogger("ssd2023")


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    missions = Mission.objects.all()

    return render(request, 'index.html', {'missions': missions})


def login_endpoint(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        logger.info(f"User {username} is attempting to log in")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")

    form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_endpoint(request):
    logout(request)

    return render(request, 'logout.html')


def mission_details(request, mission_id):
    mission = Mission.objects.get(pk=mission_id)

    return render(request, 'mission.html', {'mission': mission})
