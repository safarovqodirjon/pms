from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .businesslog.admin import AdminCalculator
from .businesslog.manager import ManagerCalculation
from .models import Project, CustomUser
from .decorators import superuser_required, manager_required
from django.urls import reverse
from .models import ProjectCompletionRequest
from .forms import ProjectCompletionRequestForm, TaskCompletionRequestForm, Task, TaskForm, ProjectForm


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

        'managers_table': employees_table['custom_users_managers'],

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
        'admin_requests': True,
        'role': 'менеджер',
        'blabla': True,

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
        'admin_requests': True,
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
        'admin_requests': True,
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
        'employee_card': True,
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
def manager_manage(request):
    dryness_list = ManagerCalculation.count_dryness(request=request)
    projects = AdminCalculator.project_list()
    employees_table = AdminCalculator.user_list()

    context = {
        'manager_secondary': True,

        'employees_count': dryness_list['employees_count'],
        'managers_count': dryness_list['managers_count'],
        'project_count': dryness_list['project_count'],
        'tasks_count': dryness_list['tasks_count'],

        'projects_table': projects['projects'],
        'managers_table': employees_table['custom_users_managers'],

        'project_card': True,
    }
    return render(request, 'management/manager/manager-secondary.html', context=context)


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
def manager_create_task(request):
    tasks = ManagerCalculation.manager_projects(request=request)
    dryness_list = ManagerCalculation.count_dryness(request=request)
    assigned_employee = ManagerCalculation.manager_projects(request=request)

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


def add_employee_to_project(request, project_id):
    project = Project.objects.get(id=project_id)
    employees = CustomUser.objects.filter(is_employee=True)
    context = {'project': project, 'employees': employees}
    return render(request, 'management/manager/add_employee.html', context)


def assign_employee_to_project(request, project_id, employee_id):
    project = get_object_or_404(Project, id=project_id)
    employee = get_object_or_404(CustomUser, id=employee_id, is_employee=True)
    project.assigned_to.add(employee)
    return redirect('management:manager-main')


# @login_required
# def admin_main(request):
#     dryness_list = AdminCalculator.count_dryness()
#     projects = AdminCalculator.project_list()
#
#     context = {
#         'admin_main': True,
#         'employees_count': dryness_list['employees_count'],
#         'managers_count': dryness_list['managers_count'],
#         'admins_count': dryness_list['admins_count'],
#         'project_count': dryness_list['project_count'],
#
#         'projects_table': projects['projects'],
#     }
#     return render(request, 'management/main_admin.html', context=context)


def error_handler(request, exception):
    if exception.__class__.__name__ == 'ObjectDoesNotExist':
        return redirect('authenticate:login')
    else:
        # Обработка других ошибок
        return redirect('authenticate:register-wait')
