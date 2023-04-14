from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'authenticate'

urlpatterns = [
    # Маршрут для регистрации
    path('register/', views.register, name='register'),

    # Маршрут для входа в систему
    path('login/', views.login, name='login'),

    # Маршрут для проверки заявок для администратора
    path('requests/', views.request_list, name='requests'),

    # Маршрут для одобрения запроса
    path('requests/approve/<int:pk>/', views.request_approve, name='request-approve'),

    # Маршрут для отклонения запроса
    path('requests/decline/<int:pk>/', views.request_decline, name='request-decline'),

    # Маршрут для выхода из системы
    path('logout/', LogoutView.as_view(), name='logout'),

    # Маршрут для ожидания подтверждения регистрации
    path('register/wait/', views.RegistrationWaitView.as_view(), name='register-wait'),
]
