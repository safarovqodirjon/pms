from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test

app_name = 'authenticate'

urlpatterns = [
    # Маршрут для регистрации и входа
    path('', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('register/wait/', views.RegistrationWaitView.as_view(), name='register-wait'),
    path('login/', views.login_view, name='login'),

    # маршрут для администратора по приему заявок
    path('main-admin/show-reguest/', user_passes_test(lambda u: u.is_superuser)(views.request_list),
         name='register-request'),
    path('show-reguest/<int:request_id>/', user_passes_test(lambda u: u.is_superuser)(views.approve_request),
         name='request-approve'),

    path('showreguest/<int:request_id>/', user_passes_test(lambda u: u.is_superuser)(views.decline_request),
         name='request-decline'),

]
