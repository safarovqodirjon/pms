# Generated by Django 4.2.1 on 2023-05-25 14:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0008_project_project_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="rating",
            field=models.IntegerField(default=0, verbose_name="Рейтинг"),
        ),
    ]