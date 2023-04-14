from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test

app_name = 'authenticate'

urlpatterns = [
    # Маршрут для регистрации
    path('', views.register, name='register'),
    path('register/', views.register, name='register'),

    # Маршрут для входа в систему
    path('login/', views.login, name='login'),
    path('showreguest/', user_passes_test(lambda u: u.is_superuser)(views.request_list), name='register-request'),
    path('showreguest/<int:request_id>/', user_passes_test(lambda u: u.is_superuser)(views.approve_request),
         name='request-approve'),

    path('showreguest/<int:request_id>/', user_passes_test(lambda u: u.is_superuser)(views.decline_request),
         name='request-decline'),

    path('register/wait/', views.RegistrationWaitView.as_view(), name='register-wait'),
    path('main/employee/', views.MainEmployeeView.as_view(), name='main-employee'),
]
