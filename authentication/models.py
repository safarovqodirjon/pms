from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    departament = models.CharField(default="Unknown", max_length=255)
    request_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class RegistrationRequest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='registration_request', null=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Запрос на регистрацию'
        verbose_name_plural = 'Запросы на регистрацию'

    def __str__(self):
        return f"request form {self.user.username}"
