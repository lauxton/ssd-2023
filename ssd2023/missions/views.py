import csv
import datetime

from django.http import HttpResponse
from django.shortcuts import render

from .forms import LoginForm
from .models import Report


def index(request):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    reports = Report.objects.all()

    return render(request, 'index.html', {'now': now, 'reports': reports})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            employee_id = form.cleaned_data["employee_id"]
            password = form.cleaned_data["password"]

            return HttpResponse(f'Employee ID: {employee_id}, Password: {password}')

    form = LoginForm()

    return render(request, 'login.html', {'form': form})


def create_report(request):
    return HttpResponse("Creating a new report")


def export_report(request, report_id):
    report = Report.objects.get(pk=report_id)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="report.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow([report.mission.name, report.title])

    return response
