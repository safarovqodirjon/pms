from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from authentication.models import CustomUser


class UserRegisterForm(UserCreationForm):
    is_employee = forms.BooleanField(label='Сотрудник', required=False)
    is_manager = forms.BooleanField(label='Менеджер', required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username',
                  'email', 'is_employee', 'is_manager', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        is_employee = cleaned_data.get("is_employee")
        is_manager = cleaned_data.get("is_manager")
        if is_employee and is_manager:
            raise forms.ValidationError("Выберите только один вариант")
        elif not is_employee and not is_manager:
            raise forms.ValidationError("Выберите хотя бы один вариант")
        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class ProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, label='Изображение')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'departament']
