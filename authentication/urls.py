from django.urls import path
from . import views
from management.views import admin_main, error_handler

app_name = 'authenticate'

urlpatterns = [
    # Маршрут для регистрации и входа

    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('register/wait/', views.RegistrationWaitView.as_view(), name='register-wait'),

    path('main-admin/profile/', views.admin_profile, name='admin-profile'),
    path('main-manager/profile/', views.manager_profile, name='manager-profile'),
    # path('main-manager/profile/', views.employee_profile, name='employee-profile'),

    path('logout/', views.logout_view, name='logout'),

]

handler404 = error_handler
