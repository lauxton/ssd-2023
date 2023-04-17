"""Functions for viewing objects when rendered"""
import logging

from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Mission, MissionReport, Employee
from .forms import MissionForm, GenerateReportForm

logger = logging.getLogger("ssd2023")


@login_required(login_url='/login')
def index(request):
    """View of index page based on access control"""
    content = {
        'can_add_mission': request.user.has_perm("missions.add_mission"),
    }

    # Get the employee object for the current user
    # For the superuser, this will be None
    employee = Employee.objects.filter(user=request.user).first()

    if employee is not None:
        if request.user.groups.filter(name='NASA_Admin_User').exists():
            mission_reports = MissionReport.objects.filter(
                assigned_to=employee)

            content['mission_reports'] = mission_reports

        if request.user.groups.filter(name='ISS_Admin_User').exists():
            missions = Mission.objects.filter(supervisor=employee)
            mission_reports_from_missions = MissionReport.objects.filter(
                mission__in=missions)

            content['missions'] = missions
            content['mission_reports'] = mission_reports_from_missions

    if request.user.is_superuser:
        content['missions'] = Mission.objects.all()
        content['mission_reports'] = MissionReport.objects.all()

    return render(request, 'index.html', content)


def login_endpoint(request):
    """User login endpoint"""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        logger.info(f"User {username} is attempting to log in")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"User {username} has logged in successfully")
            return HttpResponseRedirect("/")

    form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login')
def logout_endpoint(request):
    """User logout endpoint"""
    logout(request)

    return render(request, 'logout.html')


@login_required(login_url='/login')
@permission_required('missions.view_mission', raise_exception=True)
def mission_details(request, mission_id):
    """View mission details"""
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


@login_required(login_url='/login')
@permission_required('missions.add_mission', raise_exception=True)
def mission_create(request):
    """Create mission"""
    if request.method == 'POST':
        mission = Mission()
        form = MissionForm(request.POST, instance=mission)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect("/mission/" + str(mission.pk))

    mission = Mission()
    form = MissionForm(instance=mission)

    return render(request, 'mission-create.html', {'mission': mission, 'form': form})


@login_required(login_url='/login')
@permission_required('missions.change_mission', raise_exception=True)
def mission_update(request, mission_id):
    """Update mission details"""
    if request.method == 'POST':
        mission = Mission.objects.get(pk=mission_id)
        form = MissionForm(request.POST, instance=mission)

        if form.is_valid():
            form.save(commit=True)

            return HttpResponseRedirect("/mission/" + str(mission_id))

    mission = Mission.objects.get(pk=mission_id)
    form = MissionForm(instance=mission)

    return render(request, 'mission-update.html', {'mission': mission, 'form': form})


@login_required(login_url='/login')
@permission_required('missions.delete_mission', raise_exception=True)
def mission_delete(request, mission_id):
    """Delete mission"""
    mission = Mission.objects.get(pk=mission_id)
    mission.delete()

    return HttpResponseRedirect("/")


@login_required(login_url='/login')
@permission_required('missions.add_missionreport', raise_exception=True)
def mission_report_generate(request, mission_id):
    """Generate mission report"""
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


@login_required(login_url='/login')
@permission_required('missions.view_missionreport', raise_exception=True)
def mission_report_details(request, mission_report_id):
    """View mission report details"""
    mission_report = MissionReport.objects.get(pk=mission_report_id)

    return render(request, 'mission-report.html', {'mission_report': mission_report})
