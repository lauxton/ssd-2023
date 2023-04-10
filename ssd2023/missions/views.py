import csv
import datetime
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import MissionReport

logger = logging.getLogger("ssd2023")


def index(request):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    reports = MissionReport.objects.all()

    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    # TODO: check if the user is logged in,
    # if they're not redirect to login page,
    # if they are show the index page

    return render(request, 'index.html', {'now': now, 'reports': reports})


def login_endpoint(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        logger.info(f"User {username} is attempting to log in with password {password}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/")

    form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_endpoint(request):
    logout(request)

    return render(request, 'logout.html')


def create_report(request):
    return HttpResponse("Creating a new report")


def export_report(request, report_id):
    report = MissionReport.objects.get(pk=report_id)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="report.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow([report.mission.name, report.title])

    return response
