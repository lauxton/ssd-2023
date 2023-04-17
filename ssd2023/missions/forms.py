from django import forms
from django.forms import Form, ModelForm, TextInput, DateTimeInput, Select

from .models import Mission, Employee


class MissionForm(ModelForm):
    """Form for creating a new mission."""

    class Meta:
        model = Mission
        fields = [
            'name',
            'description',
            'division',
            'supervisor',
            'start_date',
            'end_date',
            'security_clearance',
        ]
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': TextInput(attrs={'class': 'form-control'}),
            'division': Select(attrs={'class': 'form-control'}),
            'supervisor': Select(attrs={'class': 'form-control'}),
            'start_date': DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-MM-dd HH:MM:SS'}),
            'end_date': DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'yyyy-MM-dd HH:MM:SS'}),
            'security_clearance': Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Mission Name',
            'description': 'Mission Description',
            'division': 'Division',
            'supervisor': 'Supervisor',
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'security_clearance': 'Security Clearance',
        }


class GenerateReportForm(Form):
    """Form for generating a new report for an existing mission."""

    assigned_to = forms.ModelChoiceField(
        queryset=Employee.objects.filter(user__groups__name='NASA_Admin_User'),
        required=True,
        widget=Select(attrs={'class': 'form-control'})
    )
    report_summary = forms.CharField(
        required=True,
        widget=TextInput(attrs={'class': 'form-control'})
    )
