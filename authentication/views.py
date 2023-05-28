from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import CustomAuthenticationForm, UserRegisterForm, ProfileForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistrationRequest, CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from management.businesslog.admin import AdminCalculator
from management.businesslog.manager import ManagerCalculation
from management.models import Project, CustomUser
from management.decorators import superuser_required, manager_required


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            registration_request = RegistrationRequest.objects.create(user=user)
            return redirect('authenticate:login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "authenticate/registration.html", context)


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':

        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                if user.is_superuser:
                    login(request, user)

                    return redirect('management:admin-main')
                elif user.is_employee:

                    registration_request = user.registration_request
                    if registration_request and registration_request.approved:
                        login(request, user)
                        return redirect('management:manager-main')
                    else:
                        return redirect('authenticate:register-wait')
                elif user.is_manager:

                    registration_request = user.registration_request
                    if registration_request and registration_request.approved:
                        login(request, user)
                        return redirect('management:manager-main')
                    else:
                        return redirect('authenticate:register-wait')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'authenticate/login.html', context)


@login_required
@superuser_required
def admin_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_image = request.FILES.get('image')
            if new_image:
                # если новое изображение было загружено, сохраняем его в модели пользователя
                user.image = new_image
            user.save()
            return redirect('authenticate:admin-profile')
    else:
        form = ProfileForm(instance=user)

    tasks = ManagerCalculation.count_dryness(request=request)
    assigned_employee = ManagerCalculation.manager_projects(request=request)
    context = {
        'form': form,
        'admin_profile': True,
        'tasks': tasks['tasks'],
    }

    return render(request, 'management/admin/admin-profile.html', context)


@login_required
@manager_required
def manager_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            new_image = request.FILES.get('image')
            if new_image:
                # если новое изображение было загружено, сохраняем его в модели пользователя
                user.image = new_image
            user.save()
            return redirect('authenticate:manager-profile')
    else:
        form = ProfileForm(instance=user)

    tasks = ManagerCalculation.count_dryness(request=request)
    assigned_employee = ManagerCalculation.manager_projects(request=request)
    context = {
        'form': form,
        'manager_profile': True,
        'tasks': tasks['tasks'],
    }

    return render(request, 'management/manager/manager-profile.html', context)


class RegistrationWaitView(TemplateView):
    template_name = 'authenticate/register_wait.html'


def logout_view(request):
    logout(request)
    return redirect('authenticate:login')
