from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import CustomAuthenticationForm, UserRegisterForm, ProfileForm
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistrationRequest, CustomUser
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            # Создаем объект RegistrationRequest вместо CustomUser
            user = form.save(commit=False)
            user.save()

            registration_request = RegistrationRequest.objects.create(user=user)

            return redirect('authenticate:register-wait')
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
                        return redirect('management:admin-main')
                    else:
                        return redirect('authenticate:register-wait')
                elif user.is_manager:
                    login(request, user)
                    return redirect('management:main-manager')
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'authenticate/login.html', context)


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.image = request.FILES.get('image')  # сохраняем загруженное изображение в модели пользователя
            user.save()
            return redirect('authenticate:admin-profile')
    else:
        form = ProfileForm(instance=user)
    context = {
        'form': form,
        'admin_profile': True,
    }
    return render(request, 'management/admin/admin-profile.html', context)


@login_required(login_url='authenticate:login')
def request_list(request):
    # получаем все заявки на регистрацию, которые еще не были одобрены или отклонены
    reqs = RegistrationRequest.objects.filter(approved=False, declined=False)

    context = {
        'reqs': reqs,
    }

    return render(request, 'registration/request_list.html', context=context)


@login_required(login_url='authenticate:login')
@user_passes_test(lambda u: u.is_superuser)
def request_list(request):
    all_requests = RegistrationRequest.objects.all()
    for r in all_requests:
        print(r.user)
    context = {'all_requests': all_requests}
    return render(request, 'registration/request_list.html', context)


@login_required(login_url='authenticate:login')
@user_passes_test(lambda u: u.is_superuser)
def approve_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, pk=request_id)
    registration_request.approved = True
    registration_request.save()
    return redirect('authenticate:register-request')


@login_required(login_url='authenticate:login')
@user_passes_test(lambda u: u.is_superuser)
def decline_request(request, request_id):
    registration_request = get_object_or_404(RegistrationRequest, pk=request_id)
    print(registration_request.user, registration_request.declined)
    registration_request.declined = True
    registration_request.save()
    return redirect('authenticate:register-request')


class RegistrationWaitView(TemplateView):
    template_name = 'authenticate/register_wait.html'

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
