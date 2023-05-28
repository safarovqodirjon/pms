from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False, verbose_name='Является сотрудником')
    is_manager = models.BooleanField(default=False, verbose_name='Является менеджером')
    departament = models.CharField(default="Unknown", max_length=255, verbose_name='Отдел')
    request_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата запроса')
    phone = models.CharField(max_length=255, default='Unknown', help_text='+992---', verbose_name='Телефон')
    address = models.CharField(max_length=255, default='Unknown', help_text='address', verbose_name='Адрес')
    image = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True, verbose_name='Изображение')
    rate = models.IntegerField(default=0, verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class RegistrationRequest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='registration_request', null=True,
                                verbose_name='Пользователь')
    message = models.TextField(null=True, blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    approved = models.BooleanField(default=False, verbose_name='Одобрен')
    declined = models.BooleanField(default=False, verbose_name='Отклонен')

    class Meta:
        verbose_name = 'Запрос на регистрацию'
        verbose_name_plural = 'Запросы на регистрацию'

    def __str__(self):
        return f"Запрос от {self.user.username}"
