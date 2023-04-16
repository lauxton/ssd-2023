import logging

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Mission, MissionReport, Employee
from .forms import MissionForm, GenerateReportForm

logger = logging.getLogger("ssd2023")


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/login")

    content = {
        'can_add_mission': request.user.has_perm("missions.add_mission"),
    }

    if request.user.is_superuser or request.user.groups.filter(name='ISS_Admin_User').exists():
        missions = Mission.objects.all()
        content['missions'] = missions

    if request.user.is_superuser or request.user.groups.filter(name='NASA_Admin_User').exists():
        mission_reports = MissionReport.objects.all()
        content['mission_reports'] = mission_reports

    return render(request, 'index.html', content)


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
    mission_reports = mission.missionreport_set.all()
    generate_report_form = GenerateReportForm()

    can_update = request.user.has_perm("missions.change_mission")
    can_delete = request.user.has_perm("missions.delete_mission")
    can_add_report = request.user.has_perm("missions.add_missionreport")

    return render(request, 'mission.html', {
        'can_delete': can_delete,
        'can_update': can_update,
        'can_add_report': can_add_report,
        'mission': mission,
        'reports': mission_reports,
        'generate_report_form': generate_report_form
    })


def mission_create(request):
    if request.method == 'POST':
        mission = Mission()
        form = MissionForm(request.POST, instance=mission)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect("/mission/" + str(mission.pk))

    mission = Mission()
    form = MissionForm(instance=mission)

    return render(request, 'mission-create.html', {'mission': mission, 'form': form})


def mission_update(request, mission_id):
    if request.method == 'POST':
        mission = Mission.objects.get(pk=mission_id)
        form = MissionForm(request.POST, instance=mission)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect("/mission/" + str(mission_id))

    mission = Mission.objects.get(pk=mission_id)
    form = MissionForm(instance=mission)

    return render(request, 'mission-update.html', {'mission': mission, 'form': form})


def mission_delete(mission_id):
    mission = Mission.objects.get(pk=mission_id)
    mission.delete()

    return HttpResponseRedirect("/")


def mission_report_generate(request, mission_id):
    if request.method != 'POST':
        return HttpResponseRedirect("/")

    form = GenerateReportForm(request.POST)

    if not form.is_valid():
        return HttpResponseRedirect("/")

    mission = Mission.objects.get(pk=mission_id)
    mission_reports = mission.missionreport_set.all()
    employee = Employee.objects.get(pk=form.data['assigned_to'])

    if not employee.user.groups.filter(name='NASA_Admin_User').count():
        return HttpResponseRedirect("/")

    mission_report = MissionReport(
        title=f"{mission.name} Report {str(mission_reports.count() + 1)}",
        mission=mission,
        assigned_to=employee,
        publish_date=datetime.now(),
        summary=form.data['report_summary']
    )

    mission_report.save()

    return HttpResponseRedirect("/mission-report/" + str(mission_report.pk))


def mission_report_details(request, mission_report_id):
    mission_report = MissionReport.objects.get(pk=mission_report_id)

    return render(request, 'mission-report.html', {'mission_report': mission_report})
