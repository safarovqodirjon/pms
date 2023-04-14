from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'authenticate'

urlpatterns = [
    # Маршрут для регистрации
    path('register/', views.register, name='register'),

    # Маршрут для входа в систему
    path('login/', views.login, name='login'),

    path('register/wait/', views.RegistrationWaitView.as_view(), name='register-wait'),
    path('main/employee/', views.MainEmployeeView.as_view(), name='main-employee'),
]
