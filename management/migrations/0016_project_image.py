# Generated by Django 4.2.1 on 2023-05-27 12:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0015_project_rating_count"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="projects/%Y/%m/%d",
                verbose_name="Изображение",
            ),
        ),
    ]
