# Generated by Django 4.2.1 on 2023-05-27 21:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("management", "0016_project_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="rating_count",
        ),
        migrations.CreateModel(
            name="ProjectApprovalRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "manager",
                    models.ForeignKey(
                        limit_choices_to={"is_manager": True},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approval_requests",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Менеджер",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approval_requests",
                        to="management.project",
                        verbose_name="Проект",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запрос на одобрение проекта",
                "verbose_name_plural": "Запросы на одобрение проектов",
            },
        ),
    ]
