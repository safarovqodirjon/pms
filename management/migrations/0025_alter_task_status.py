# Generated by Django 4.2.1 on 2023-05-31 20:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0024_alter_project_options_alter_task_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("todo", "Не начат"),
                    ("inprogress", "В прогрессе"),
                    ("done", "Завершено"),
                ],
                default="todo",
                max_length=20,
                verbose_name="Статус",
            ),
        ),
    ]
