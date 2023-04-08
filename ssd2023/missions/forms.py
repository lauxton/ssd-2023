from django import forms

class LoginForm(forms.Form):
    employee_id = forms.CharField(label='Employee ID', max_length=50)
    password = forms.CharField(label='Password', max_length=100)
