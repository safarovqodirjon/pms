from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Manager, Employee


class CustomUserForm(UserCreationForm):
    is_employee = forms.BooleanField(required=False)
    is_manager = forms.BooleanField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'is_employee', 'is_manager']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['employee_id', 'department']


class ManagerForm(forms.ModelForm):
    class Meta:
        model = Manager
        fields = ['manager_id', 'department']


class RegistrationForm(forms.Form):
    custom_user_form = CustomUserForm()
    employee_form = EmployeeForm()
    manager_form = ManagerForm()

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields.update(self.custom_user_form.fields)
        self.fields.update(self.employee_form.fields)
        self.fields.update(self.manager_form.fields)


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
