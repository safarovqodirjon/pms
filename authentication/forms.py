from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.models import CustomUser


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username',
                  'email', 'is_employee', 'is_manager', 'password1', 'password2']
        widgets = {
            'is_employee': forms.RadioSelect(attrs={'id': 'employee'}),
            'is_manager': forms.RadioSelect(attrs={'id': 'manager'}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['username'].label = 'Username or Email'

# class EmployeeForm(forms.ModelForm):
#     class Meta:
#         model = Employee
#         fields = ['employee_id', 'department']
#
#
# class ManagerForm(forms.ModelForm):
#     class Meta:
#         model = Manager
#         fields = ['manager_id', 'department']
#
#
# class RegistrationForm(forms.Form):
#     custom_user_form = CustomUserForm()
#     employee_form = EmployeeForm()
#     manager_form = ManagerForm()
#
#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#
#         self.fields.update(self.custom_user_form.fields)
#         self.fields.update(self.employee_form.fields)
#         self.fields.update(self.manager_form.fields)
