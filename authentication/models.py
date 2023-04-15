from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    departament = models.CharField(default="Unknown", max_length=255)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class RegistrationRequest(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='registration_request', null=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)

    def __str__(self):
        return f"request form {self.user.username}"
