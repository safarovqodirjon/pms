from authentication.models import CustomUser, RegistrationRequest
from management.models import Project, Task
from .admin import AdminCalculator


class ManagerCalculator(AdminCalculator):

    @staticmethod
    def project_list(request):
        projects = Project.objects.filter(assigned_to=request.user)
        context = {
            'projects': projects,
        }
        return context

    @staticmethod
    def user_list():
        custom_users = CustomUser.objects.filter(is_superuser=False, is_manager=False).all()
        custom_users_managers = CustomUser.objects.filter(is_superuser=False, is_manager=True).all()
        context = {
            'custom_users': custom_users,
            'custom_users_managers': custom_users_managers,
        }
        return context


class ManagerCalculation:
    @staticmethod
    def manager_projects(request):
        projects = Project.objects.filter(assigned_to=request.user, approved_by_admin=True)
        tasks = Task.objects.filter(project__assigned_to=request.user)
        tasks_conts = tasks.count()
        employees_table = CustomUser.objects.filter(assigned_tasks__in=tasks, is_employee=True).distinct()

        context = {
            'manager_projects': projects,
            'manager_employees': employees_table,

            'task_assigned': tasks,
        }
        # print(context['manager_employees'])
        return context

    @staticmethod
    def count_dryness(request):
        tasks = Task.objects.filter(project__assigned_to=request.user)
        employees = CustomUser.objects.filter(assigned_tasks__in=tasks, is_employee=True)
        employees_count = CustomUser.objects.filter(assigned_tasks__in=tasks, is_employee=True).distinct().count()

        projects = Project.objects.filter(assigned_to=request.user)
        managers_count = CustomUser.objects.filter(registration_request__approved=True, is_manager=True).count()
        projects_count = projects.count()
        tasks_count = tasks.count()

        context = {
            'employees_count': employees_count,
            'managers_count': managers_count,
            'project_count': projects_count,
            'tasks_count': tasks_count,
            'tasks': tasks,
        }

        return context
