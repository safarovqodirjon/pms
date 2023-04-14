from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from django.views.generic import TemplateView
# from .forms import RegistrationForm, UserLoginForm
# from .models import RegistrationRequest, Employee, Manager
# from django.views.decorators.http import require_http_methods
# from django.contrib import auth
# from .models import CustomUser, RegistrationRequest

from django.contrib import messages
from django.views.generic import TemplateView
from .forms import CustomAuthenticationForm, UserRegisterForm
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from .models import CustomUser, RegistrationRequest
from django.contrib import auth
from django.shortcuts import render, redirect

from .forms import CustomAuthenticationForm
from .models import RegistrationRequest


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('authenticate:login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "registration/registration.html", context)


def login(request):
    if request.method == 'POST':
        print("--->", request.POST)
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('authenticate:main-employee')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }

    return render(request, 'registration/login.html', context, )


class RegistrationWaitView(TemplateView):
    template_name = 'registration/register_wait.html'


class MainEmployeeView(TemplateView):
    template_name = 'registration/register_employee_view.html'

# @login_required(login_url='authenticate:login')
# def request_list(request):
#     # получаем все заявки на регистрацию, которые еще не были одобрены или отклонены
#     reqs = RegistrationRequest.objects.filter(approved=False, declined=False)
#
#     context = {
#         'reqs': reqs,
#     }
#
#     return render(request, 'registration/request_list.html', context=context)
#
#
# @login_required(login_url='authenticate:login')
# def request_approve(request, pk):
#     registration_request = get_object_or_404(RegistrationRequest, pk=pk)
#     user = registration_request.user
#     user.is_active = True
#     user.groups.remove(Group.objects.get(name='unapproved'))
#     user.save()
#     registration_request.delete()
#     return redirect('authenticate:requests')
#
#
# @login_required(login_url='authenticate:login')
# def request_decline(request, pk):
#     registration_request = get_object_or_404(RegistrationRequest, pk=pk)
#     user = registration_request.user
#     user.delete()
#     registration_request.delete()
#     return redirect('authenticate:requests')
#
#
