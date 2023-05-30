from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .businesslog.admin import AdminCalculator
from .businesslog.manager import ManagerCalculation
from .models import Project, CustomUser
from .decorators import superuser_required, manager_required
from django.urls import reverse
from .models import ProjectCompletionRequest
from .forms import ProjectCompletionRequestForm, TaskCompletionRequestForm, Task, TaskForm, ProjectForm, \
    ProjectCompletionManagerRequestForm


# Create your views here.
@login_required
@superuser_required
def admin_main(request):
    dryness_list = AdminCalculator.count_dryness()
    projects = AdminCalculator.project_list()
    employees_table = AdminCalculator.user_list()
    # bar_emp_man = AdminCalculator.bar_plot_users(model=CustomUser)

    context = {
        'admin_main': True,
        'employees_count': dryness_list['employees_count'],
        'managers_count': dryness_list['managers_count'],
        'admins_count': dryness_list['admins_count'],
        'project_count': dryness_list['project_count'],
        # 'bar_emp_man': bar_emp_man['bar_emp_man'],
        'projects_table': projects['projects'],
        'managers_table': employees_table['custom_users_managers'],

        'project_card': True,
    }
    return render(request, 'management/admin/admin-main.html', context=context)


@login_required
@superuser_required
def admin_projects(request):
    context = {
        'admin_projects': True,
    }
    return render(request, 'management/admin/admin-secondary.html', context=context)


@login_required
@superuser_required
def admin_managers(request):
    dryness_list = AdminCalculator.count_dryness()
    projects = AdminCalculator.project_list()
    employees_table = AdminCalculator.user_list()

    context = {
        'admin_main': True,
        'employees_count': dryness_list['employees_count'],
        'managers_count': dryness_list['managers_count'],
        'admins_count': dryness_list['admins_count'],
        'project_count': dryness_list['project_count'],

        'managers_table': employees_table['custom_users_managers_top'],

        'manager_card': True,
    }
    return render(request, 'management/admin/admin-main.html', context=context)


@login_required
@superuser_required
def admin_manage(request):
    context = {
        'admin_manage': True,
        'role': 'менеджер',
        'lala': True,

    }
    return render(request, 'management/admin/admin-secondary.html', context=context)


@login_required
@superuser_required
def admin_requests(request):
    context = {
        'admin_manage': True,
        'role': 'менеджер',

    }
    return render(request, 'management/admin/admin-requests.html', context=context)


@login_required
@superuser_required
def admin_submit_completion_request(request):
    if request.method == 'POST':
        form = ProjectCompletionRequestForm(request.POST)
        if form.is_valid():
            completion_request = form.save(commit=False)
            completion_request.user = form.cleaned_data['user']
            completion_request.description = form.cleaned_data['description']
            completion_request.save()
            redirect_url = request.META.get('HTTP_REFERER')
            return redirect(redirect_url)

    else:
        form = ProjectCompletionRequestForm()

    context = {
        'admin_manage': True,
        'role': 'менеджер',
        'sub_pro_card': True,
        'form': form,
    }

    return render(request, 'management/admin/admin-requests.html', context=context)


@login_required
@superuser_required
def admin_submit_task_completion_request(request):
    if request.method == 'POST':
        form = TaskCompletionRequestForm(request.POST)
        if form.is_valid():
            completion_request = form.save(commit=False)
            completion_request.user = form.cleaned_data['user']
            completion_request.description = form.cleaned_data['description']
            completion_request.save()
            redirect_url = request.META.get('HTTP_REFERER')
            return redirect(redirect_url)

    else:
        form = TaskCompletionRequestForm()

    context = {
        'admin_manage': True,
        'role': 'менеджер',
        'sub_task_card': True,
        'form': form,
    }

    return render(request, 'management/admin/admin-requests.html', context=context)


@login_required
@superuser_required
def admin_employee(request):
    dryness_list = AdminCalculator.count_dryness()
    projects = AdminCalculator.project_list()
    employees_table = AdminCalculator.user_list()

    context = {
        'admin_main': True,
        'employees_count': dryness_list['employees_count'],
        'managers_count': dryness_list['managers_count'],
        'admins_count': dryness_list['admins_count'],
        'project_count': dryness_list['project_count'],

        'projects_table': projects['projects'],
        'employees_table': employees_table['custom_users'],
        # 'employee_card': True,
    }
    return render(request, 'management/admin/admin-main.html', context=context)


# managers views
@login_required
@manager_required
def manager_main(request):
    dryness_list = ManagerCalculation.count_dryness(request=request)
    assigned_manager_pro = ManagerCalculation.manager_projects(request=request)
    employees_table = AdminCalculator.user_list()

    context = {
        'manager_main': True,
        'role': 'менеджер',
        'employees_count': dryness_list['employees_count'],
        'project_count': dryness_list['project_count'],
        'tasks_count': dryness_list['tasks_count'],

        'projects_table': assigned_manager_pro['manager_projects'],
        'managers_table': employees_table['custom_users_managers'],

        'project_card': True,
    }
    return render(request, 'management/manager/manager-main.html', context=context)


@login_required
@manager_required
def manager_employee(request):
    dryness_list = ManagerCalculation.count_dryness(request=request)
    assigned_employee = ManagerCalculation.manager_projects(request=request)
    context = {
        'manager_main': True,
        'role': 'менеджер',
        'employees_count': dryness_list['employees_count'],
        'project_count': dryness_list['project_count'],
        'tasks_count': dryness_list['tasks_count'],

        'employees_table': assigned_employee['manager_employees'],

        'employee_card': True,
    }
    return render(request, 'management/manager/manager-main.html', context=context)


# @login_required
# @manager_required
# def manager_manage(request):
#     dryness_list = ManagerCalculation.count_dryness(request=request)
#     projects = AdminCalculator.project_list()
#     employees_table = AdminCalculator.user_list()
#
#     context = {
#         'manager_secondary': True,
#
#         'employees_count': dryness_list['employees_count'],
#         'managers_count': dryness_list['managers_count'],
#         'project_count': dryness_list['project_count'],
#         'tasks_count': dryness_list['tasks_count'],
#
#         'projects_table': projects['projects'],
#         'managers_table': employees_table['custom_users_managers'],
#
#         'project_card': True,
#     }
#     return render(request, 'management/manager/manager-secondary.html', context=context)


@login_required
@manager_required
def manager_create_task(request):
    dryness_list = ManagerCalculation.count_dryness(request=request)

    if request.method == 'POST':
        form = TaskForm(request.POST, user=request.user)  # Передаем текущего пользователя в форму
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user  # Устанавливаем текущего пользователя как создателя задачи
            form.save()
            return redirect('management:manager-task-list')
    else:
        form = TaskForm(user=request.user)  # Передаем текущего пользователя в форму

    context = {
        'manager_secondary': True,
        'task_create_card': True,
        'project_count': dryness_list['project_count'],
        'employees_count': dryness_list['employees_count'],
        'tasks_count': dryness_list['tasks_count'],

        'form': form,
    }
    return render(request, 'management/manager/manager-secondary.html', context=context)


@login_required
@manager_required
def manager_task_list(request):
    tasks = ManagerCalculation.manager_projects(request=request)
    dryness_list = ManagerCalculation.count_dryness(request=request)
    assigned_employee = ManagerCalculation.manager_projects(request=request)

    context = {
        'manager_main': True,
        'project_count': dryness_list['project_count'],
        'employees_count': dryness_list['employees_count'],
        'tasks_count': dryness_list['tasks_count'],
        'task_card': True,
        'task_list': tasks['task_assigned'],
    }
    return render(request, 'management/manager/manager-main.html', context=context)


@login_required
@manager_required
def manager_delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        print('hello')
        task.delete()
        return redirect('management:manager-task-list')

    context = {
        'manager-main': True,
        'task_create_card': True,
        'task': task,
    }
    return render(request, 'management/manager/manager-main.html', context=context)


@login_required
@manager_required
def manager_update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('management:manager-task-list')
    else:
        form = TaskForm(instance=task, user=request.user)

    context = {
        'manager_secondary': True,
        'task_create_card': True,
        'form': form,
    }
    return render(request, 'management/manager/manager-secondary.html', context=context)


@login_required
@manager_required
def manager_create_project(request):
    tasks = ManagerCalculation.manager_projects(request=request)
    dryness_list = ManagerCalculation.count_dryness(request=request)
    assigned_employee = ManagerCalculation.manager_projects(request=request)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            project.assigned_to.set([request.user])
            context = {
                'manager_secondary': True,
                'project_create_card': True,
                'project_requested_name': request.POST['name'],
                'wait_mess': True,
                'project_count': dryness_list['project_count'],
                'employees_count': dryness_list['employees_count'],
                'tasks_count': dryness_list['tasks_count'],
                'form': form,
            }
            return render(request, 'management/manager/manager-secondary.html', context=context)
        else:
            wait_mess = False
            error_message = form.errors.get('__all__')
            print(f'Error: {error_message}')
    else:
        wait_mess = False
        form = ProjectForm(initial={'created_by': CustomUser.objects.filter(is_superuser=True).first()})

    context = {
        'manager_secondary': True,
        'project_create_card': True,
        'wait_mess': wait_mess,
        'project_count': dryness_list['project_count'],
        'employees_count': dryness_list['employees_count'],
        'tasks_count': dryness_list['tasks_count'],
        'form': form,
    }
    return render(request, 'management/manager/manager-secondary.html', context=context)


@login_required
@manager_required
def manger_submit_completion_request_pro(request):
    if request.method == 'POST':
        form = ProjectCompletionManagerRequestForm(request.POST)
        if form.is_valid():
            completion_request = form.save(commit=False)
            completion_request.user = request.user  # Значение текущего пользователя
            completion_request.description = form.cleaned_data['description']
            completion_request.save()
            redirect_url = request.META.get('HTTP_REFERER')
            return redirect(redirect_url)

    else:
        form = ProjectCompletionManagerRequestForm(
            initial={'user': request.user})  # Установка начального значения для поля user

    context = {
        'admin_manage': True,
        'role': 'менеджер',
        'sub_pro_card_manger': True,
        'form': form,
    }

    return render(request, 'management/manager/manager-secondary.html', context=context)


@login_required
def employee_main(request, card):
    current_user = request.user
    projects = Project.objects.filter(assigned_to=current_user)
    tasks = Task.objects.filter(assigned_to=current_user)
    other_users = CustomUser.objects.filter(
        Q(assigned_tasks__in=tasks) & ~Q(id=current_user.id)
    ).distinct()
    projects = Project.objects.filter(tasks__in=tasks)
    managers = CustomUser.objects.filter(created_tasks__in=tasks, is_manager=True).distinct()

    context = {
        'employees': CustomUser.objects.all(),
        'projects': projects,
        'project_count': Project.objects.all().count(),
        'card': card,
        'other_users': other_users,
        'side_dash': True,
        'other_users_count': other_users.count(),
        'task_count': tasks.count(),
        'tasks': tasks,

    }

    return render(request, template_name='management/base/jahongir/main.html', context=context)


@login_required
def employee_requests(request, card):
    current_user = request.user
    projects = Project.objects.filter(assigned_to=current_user)
    tasks = Task.objects.filter(assigned_to=current_user)
    other_users = CustomUser.objects.filter(
        Q(assigned_tasks__in=tasks) & ~Q(id=current_user.id)
    ).distinct()
    projects = Project.objects.filter(tasks__in=tasks)
    managers = CustomUser.objects.filter(created_tasks__in=tasks, is_manager=True).distinct()
    print(other_users.count())

    context = {
        'employees': CustomUser.objects.all(),
        'projects': projects,
        'project_count': Project.objects.all().count(),
        'card': card,
        'other_users': other_users,
        'other_users_count': other_users.count(),
        'tasks': tasks,
        'tasks_count': tasks.count(),
        'side_req': True,
    }

    return render(request, template_name='management/base/jahongir/requtest.html', context=context)


def error_handler(request, exception):
    if exception.__class__.__name__ == 'ObjectDoesNotExist':
        return redirect('authenticate:login')
    else:
        # Обработка других ошибок
        return redirect('authenticate:register-wait')
