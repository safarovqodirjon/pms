from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .businesslog.admin import AdminCalculator


# Create your views here.
@login_required
def admin_main(request):
    dryness_list = AdminCalculator.count_dryness()

    context = {
        'admin_main': True,
        'employees_count': dryness_list['employees_count'],
        'managers_count': dryness_list['managers_count'],
        'admins_count': dryness_list['admins_count'],
        'project_count': dryness_list['project_count'],
    }
    return render(request, 'management/main_admin.html', context=context)


@login_required
def admin_projects(request):
    context = {
        'admin_projects': True,
    }
    return render(request, 'management/admin/admin-projects.html', context=context)


@login_required
def admin_requests(request):
    context = {
        'admin_request': True,
    }
    return render(request, 'management/admin/admin-requests.html', context=context)


@login_required
def main_employee(request):
    return render(request, 'management/main_employee.html')


@login_required
def main_manager(request):
    return render(request, 'management/main_manager.html')
