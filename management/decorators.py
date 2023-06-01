from django.http import HttpResponseForbidden
from django.shortcuts import render


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Действия, которые нужно выполнить, если пользователь не является суперпользователем
            return render(request, 'authenticate/403.html')

    return wrapper


def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            # Действия, которые нужно выполнить, если пользователь не является менеджером
            return render(request, 'authenticate/403.html')

    return wrapper
