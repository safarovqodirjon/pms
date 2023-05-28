from authentication.models import CustomUser, RegistrationRequest
from management.models import Project
# import plotly.express as px
import pandas as pd
# import plotly.graph_objects as go
#
# import plotly.io as pio


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

    # @staticmethod
    # def bar_plot_users(model):
    #     queryset = model.objects.all()
    #     managers_count = queryset.filter(is_manager=True).count()
    #     employees_count = queryset.filter(is_employee=True).count()
    #     admin_count = queryset.filter(is_superuser=True).count()
    #
    #     data = {'Роли': ['Администратор', 'Менеджер', 'Сотрудник'],
    #             'Количество': [admin_count, managers_count, employees_count]}
    #
    #     # Создание столбчатой диаграммы
    #     bar_emp_man = go.Figure(data=[
    #         go.Bar(x=data['Роли'], y=data['Количество'], marker=dict(color=['#FF6384', '#36A2EB', '#FFCE56']))
    #     ])
    #
    #     # Настройка макета и стилей диаграммы
    #     bar_emp_man.update_layout(
    #         title='Соотношения ролей',
    #         xaxis_title='Роли',
    #         yaxis_title='Количество',
    #         plot_bgcolor='#f8f9fa',
    #         paper_bgcolor='#ffffff',
    #         font=dict(family='Arial', size=14),
    #         margin=dict(l=50, r=50, t=50, b=50),
    #         showlegend=False
    #     )
    #
    #     # Преобразование диаграммы в HTML
    #     bar_emp_man_html = pio.to_html(bar_emp_man, full_html=False)
    #
    #     context = {
    #         'bar_emp_man': bar_emp_man_html,
    #     }
    #     return context

    @staticmethod
    def project_list():
        projects = Project.objects.all()
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
