from authentication.models import CustomUser, RegistrationRequest
from management.models import Project


class AdminCalculator:
    @staticmethod
    def count_dryness():
        employees_count = CustomUser.objects.filter(registration_request__approved=True, is_employee=True).count()
        managers_count = CustomUser.objects.filter(registration_request__approved=True, is_manager=True).count()
        admins_count = CustomUser.objects.filter(is_superuser=True).count()
        projects_count = Project.objects.count()

        context = {
            'employees_count': employees_count,
            'managers_count': managers_count,
            'admins_count': admins_count,
            'project_count': projects_count,
        }
        for k, v in context.items():
            print(k, v)
        return context
