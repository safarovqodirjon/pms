from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .forms import RegistrationForm, UserLoginForm
from .models import RegistrationRequest, Employee, Manager
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from .models import CustomUser, RegistrationRequest


# ...

@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # создаем нового пользователя
            user = CustomUser(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                username=form.cleaned_data['username'],
                is_employee=form.cleaned_data['is_employee'],
                is_manager=form.cleaned_data['is_manager'],
            )
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()

            # создаем соответствующий профиль (employee или manager)
            if form.cleaned_data['is_employee']:
                profile = Employee(
                    user=user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )
                profile.save()
                user.is_employee = True
            elif form.cleaned_data['is_manager']:
                profile = Manager(
                    user=user,
                    company=form.cleaned_data['company'],
                )
                profile.save()
                user.is_manager = True

            user.save()

            # создаем запись в базе данных с запросом на регистрацию
            registration_request = RegistrationRequest(
                user=user,
                message='Please approve my registration request'
            )
            registration_request.save()
            group, created = Group.objects.get_or_create(name='unapproved')

            # добавляем пользователя в группу 'unapproved'
            group = Group.objects.get(name='unapproved')
            user.groups.add(group)

            return redirect('authenticate:register-wait')

    else:
        form = RegistrationForm()

    return render(request, 'registration/registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        print(request.POST['username'])
        print(request.POST['password'])
        if form.is_valid():
            print('yes')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('authenticate:register-wait')
        else:
            context = {'form': form}
            print(form.error_messages)
            return render(request, 'registration/login.html', context)
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'registration/login.html', context)


@login_required(login_url='authenticate:login')
def request_list(request):
    # получаем все заявки на регистрацию, которые еще не были одобрены или отклонены
    reqs = RegistrationRequest.objects.filter(approved=False, declined=False)

    context = {
        'reqs': reqs,
    }

    return render(request, 'registration/request_list.html', context=context)


@login_required(login_url='authenticate:login')
def request_approve(request, pk):
    registration_request = get_object_or_404(RegistrationRequest, pk=pk)
    user = registration_request.user
    user.is_active = True
    user.groups.remove(Group.objects.get(name='unapproved'))
    user.save()
    registration_request.delete()
    return redirect('authenticate:requests')


@login_required(login_url='authenticate:login')
def request_decline(request, pk):
    registration_request = get_object_or_404(RegistrationRequest, pk=pk)
    user = registration_request.user
    user.delete()
    registration_request.delete()
    return redirect('authenticate:requests')


class RegistrationWaitView(TemplateView):
    template_name = 'registration/register_wait.html'
