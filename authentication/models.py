from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    request_date = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_users',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_users',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username


class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    first_name = models.CharField(max_length=100, default='Unknown')
    last_name = models.CharField(max_length=100, default='Unknown')
    employee_id = models.CharField(max_length=10, default='no')
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Manager(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='manager_profile')
    first_name = models.CharField(max_length=100, default='Unknown')
    last_name = models.CharField(max_length=100, default='Unknown')
    manager_id = models.CharField(max_length=10, default='no')
    department = models.CharField(max_length=100)
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.user.username


class RegistrationRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='registration_request')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # добавляем новое поле
    declined = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
