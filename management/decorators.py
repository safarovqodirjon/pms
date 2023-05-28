from django.http import HttpResponseForbidden


def superuser_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Действия, которые нужно выполнить, если пользователь не является суперпользователем
            return HttpResponseForbidden('Доступ запрещен')

    return wrapper


def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_manager:
            return view_func(request, *args, **kwargs)
        else:
            # Действия, которые нужно выполнить, если пользователь не является менеджером
            return HttpResponseForbidden('Доступ запрещен')

    return wrapper
