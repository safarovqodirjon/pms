from django.urls import path
from . import views

app_name = 'management'

urlpatterns = [
    # Маршрут для основной страниц
    path('admin-main/', views.admin_main, name='admin-main'),
    path('admin-projects/', views.admin_projects, name='admin-projects'),


    path('admin-requests/', views.admin_requests, name='admin-requests'),


    path('main-employee/', views.main_employee, name='main-employee'),
    path('main-manager/', views.main_manager, name='main-manager'),
]
